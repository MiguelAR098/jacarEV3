"""
jacarev3.conexao
--------------
Transporte de baixo nível: abre um socket Bluetooth clássico (RFCOMM) com o
EV3 e manda/recebe os pacotes crus montados pelo módulo `protocolo`.

Usa só a biblioteca padrão do Python (`socket` com AF_BLUETOOTH), sem
dependência externa — funciona no Windows (10+) e no Linux com BlueZ.
"""

import socket
import itertools


class ConexaoBluetooth:
    """Conexão RFCOMM clássica com o EV3 (a mesma usada pelo app oficial)."""

    CANAL_RFCOMM_PADRAO = 1

    def __init__(self, mac, canal=None, timeout=10):
        self.mac = mac
        self.canal = canal or self.CANAL_RFCOMM_PADRAO
        self._contador = itertools.count(1)
        self.socket = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
        )
        self.socket.settimeout(timeout)
        self.socket.connect((self.mac, self.canal))

    def proximo_contador(self):
        return next(self._contador) & 0xFFFF

    def enviar(self, pacote):
        self.socket.send(pacote)

    def receber(self, tamanho_max=1024):
        return self.socket.recv(tamanho_max)

    def fechar(self):
        try:
            self.socket.close()
        except OSError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.fechar()


# Espaço reservado pra outros transportes (WiFi/USB) no futuro:
#   ConexaoWiFi   -> socket TCP na porta 5555 + handshake de "unlock"
#   ConexaoUSB    -> via pyusb, endpoints bulk do EV3 (vendor/product id
#                    conhecidos: 0x0694 / 0x0005)
