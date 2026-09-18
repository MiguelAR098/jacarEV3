"""
jacarev3.robo
-----------
RoboEV3 — mesma API de antes (apitar, led, testar_motores, testar_sensores...)
mas agora rodando 100% no protocolo próprio (protocolo.py + conexao.py),
sem depender do pacote `ev3_dc` (GPLv3).

AVISO: primeira versão escrita do zero — os opcodes vêm da documentação
oficial da LEGO, mas ainda não foi validada em bateria extensa no robô
físico. Testa com calma e reporta qualquer comportamento estranho.
"""

import time
import struct

from . import protocolo as p
from .conexao import ConexaoBluetooth

CORES_SENSOR = {
    0: 'nenhuma', 1: 'preto', 2: 'azul', 3: 'verde', 4: 'amarelo',
    5: 'vermelho', 6: 'branco', 7: 'marrom',
}

CODIGOS_LED = {
    'PRETO': p.LED_PRETO, 'DESLIGADO': p.LED_PRETO, 'OFF': p.LED_PRETO,
    'VERDE': p.LED_VERDE,
    'VERMELHO': p.LED_VERMELHO,
    'AMBAR': p.LED_AMBAR, 'LARANJA': p.LED_AMBAR,
    'VERDE_PISCA': p.LED_VERDE_PISCA,
    'VERMELHO_PISCA': p.LED_VERMELHO_PISCA,
    'AMBAR_PISCA': p.LED_AMBAR_PISCA,
    'VERDE_PULSA': p.LED_VERDE_PULSA,
    'VERMELHO_PULSA': p.LED_VERMELHO_PULSA,
    'AMBAR_PULSA': p.LED_AMBAR_PULSA,
}

PORTAS_MOTOR = {'A': p.PORTA_A, 'B': p.PORTA_B, 'C': p.PORTA_C, 'D': p.PORTA_D}
PORTAS_SENSOR = {1: 0, 2: 1, 3: 2, 4: 3}  # porta física -> índice interno (0-based)


class RoboEV3:
    def __init__(self, mac, canal=None, timeout=10):
        self.conexao = ConexaoBluetooth(mac, canal=canal, timeout=timeout)

    def fechar(self):
        self.conexao.fechar()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.fechar()

    # ---------- envio interno ----------

    def _enviar(self, comando, com_resposta=False, bytes_globais=0):
        contador = self.conexao.proximo_contador()
        pacote = comando.montar(contador, com_resposta=com_resposta, bytes_globais=bytes_globais)
        self.conexao.enviar(pacote)
        if com_resposta:
            dados = self.conexao.receber()
            _, ok, payload = p.parse_resposta(dados)
            if not ok:
                raise RuntimeError("EV3 respondeu com erro pro comando")
            return payload
        return None

    # ---------- Som / LED ----------

    def apitar(self, frequencia=440, duracao_ms=500, volume=1):
        cmd = p.Comando().add(
            p.opSOUND, p.SOUND_TONE,
            p.lc_auto(volume), p.lc_auto(frequencia), p.lc_auto(duracao_ms),
        )
        self._enviar(cmd)

    def led(self, cor):
        codigo = CODIGOS_LED.get(cor.upper())
        if codigo is None:
            raise ValueError(f"Cor de LED desconhecida: {cor}. Opções: {list(CODIGOS_LED)}")
        cmd = p.Comando().add(p.opUI_WRITE, p.UI_WRITE_LED, p.lc0(codigo))
        self._enviar(cmd)

    # ---------- Espera por mudança (igual antes) ----------

    @staticmethod
    def espera_mudar(ler_valor, tempo_limite=15, intervalo=0.2, formatar=str, rotulo=""):
        inicial = ler_valor()
        print(f"  Valor inicial{f' ({rotulo})' if rotulo else ''}: {formatar(inicial)}")
        inicio = time.time()
        while time.time() - inicio < tempo_limite:
            atual = ler_valor()
            if atual != inicial:
                print(f"  Mudou! {formatar(inicial)} -> {formatar(atual)}")
                return True
            time.sleep(intervalo)
        print(f"  [TIMEOUT] Nenhuma mudança em {tempo_limite}s.")
        return False

    # ---------- Motores ----------

    def girar_motor(self, porta, velocidade=30, duracao_ms=1000, frear=True):
        """
        Gira o motor por tempo (mais simples e robusto que graus/posição).
        velocidade: -100 a 100 (negativo = sentido contrário)
        """
        bit_porta = PORTAS_MOTOR[porta]
        acao = p.PARAR_BRAKE if frear else p.PARAR_COAST
        cmd = p.Comando().add(
            p.opOUTPUT_TIME_SPEED,
            p.lc0(0),                    # layer 0
            p.lc0(bit_porta),            # porta
            p.lc1(velocidade),           # velocidade
            p.lc0(0),                    # step1 (ramp-up) = 0
            p.lc_auto(duracao_ms),       # step2 (duração em ms)
            p.lc0(0),                    # step3 (ramp-down) = 0
            p.lc0(acao),                 # ação ao parar
        )
        self._enviar(cmd)
        time.sleep(duracao_ms / 1000 + 0.1)

    def parar_motor(self, porta, frear=True):
        bit_porta = PORTAS_MOTOR[porta]
        acao = p.PARAR_BRAKE if frear else p.PARAR_COAST
        cmd = p.Comando().add(p.opOUTPUT_STOP, p.lc0(0), p.lc0(bit_porta), p.lc0(acao))
        self._enviar(cmd)

    def testar_motor(self, porta, velocidade=30, duracao_ms=800):
        print(f"Girando motor {porta} pra frente...")
        self.girar_motor(porta, velocidade=velocidade, duracao_ms=duracao_ms)
        time.sleep(0.2)
        print(f"Girando motor {porta} pra trás...")
        self.girar_motor(porta, velocidade=-velocidade, duracao_ms=duracao_ms)

    def testar_motores(self):
        print("========== TESTANDO MOTORES ==========\n")
        for letra in PORTAS_MOTOR:
            print(f"--- Motor na porta {letra} ---")
            try:
                self.testar_motor(letra)
                print(f"Motor {letra} OK!\n")
            except Exception as e:
                print(f"[AVISO] Sem motor (ou erro) na porta {letra}: {e}\n")

    # ---------- Sensores ----------

    def _ler_sensor(self, indice_porta, modo, n_valores=1):
        cmd = p.Comando().add(
            p.opINPUT_DEVICE, p.INPUT_READY_SI,
            p.lc0(0),                # layer 0
            p.lc0(indice_porta),     # porta (0-3)
            p.lc0(0),                # DO_NOT_CHANGE_TYPE
            p.lc0(modo),             # modo
            p.lc0(n_valores),        # quantidade de valores
            p.gv0(0),                # onde guardar a resposta
        )
        payload = self._enviar(cmd, com_resposta=True, bytes_globais=4 * n_valores)
        if n_valores == 1:
            return struct.unpack_from('<f', payload, 0)[0]
        return struct.unpack_from(f'<{n_valores}f', payload, 0)

    def testar_ultrassonico(self, porta, tempo_limite=15):
        indice = PORTAS_SENSOR[porta]
        self.espera_mudar(
            lambda: round(self._ler_sensor(indice, p.MODO_ULTRASSONICO_CM), 1),
            tempo_limite=tempo_limite,
            formatar=lambda v: f"{v} cm",
        )

    def testar_toque(self, porta, tempo_limite=15):
        indice = PORTAS_SENSOR[porta]
        self.espera_mudar(
            lambda: self._ler_sensor(indice, p.MODO_TOQUE) > 0.5,
            tempo_limite=tempo_limite,
            formatar=lambda v: "pressionado" if v else "solto",
        )

    def testar_cor(self, porta, tempo_limite=15):
        indice = PORTAS_SENSOR[porta]
        self.espera_mudar(
            lambda: int(round(self._ler_sensor(indice, p.MODO_COR_COR))),
            tempo_limite=tempo_limite,
            formatar=lambda v: CORES_SENSOR.get(v, f"desconhecida ({v})"),
        )

    def testar_sensores(self, tipos=('ultrassonico', 'toque', 'cor'), tempo_limite=15):
        metodos = {
            'ultrassonico': ('SENSORES ULTRASSÔNICOS', self.testar_ultrassonico),
            'toque': ('SENSORES DE TOQUE', self.testar_toque),
            'cor': ('SENSORES DE COR', self.testar_cor),
        }
        for tipo in tipos:
            titulo, metodo = metodos[tipo]
            print(f"========== TESTANDO {titulo} ==========\n")
            for numero in PORTAS_SENSOR:
                print(f"--- {tipo} na porta {numero} ---")
                try:
                    metodo(numero, tempo_limite=tempo_limite)
                    print()
                except Exception as e:
                    print(f"[AVISO] Sem sensor (ou erro) na porta {numero}: {e}\n")

    def testar_tudo(self, tempo_limite=15):
        self.testar_motores()
        self.testar_sensores(tempo_limite=tempo_limite)
        print("Teste completo finalizado.")
