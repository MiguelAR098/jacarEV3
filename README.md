<p align="center">
  <img src="https://raw.githubusercontent.com/i-barbosa/jacarEV3/main/assets/logo.png" width="150" alt="jacarEV3">
</p>

# jacarEV3 🐊

Lib em português pra controlar o LEGO EV3 via Bluetooth. Sem dependências
externas — só biblioteca padrão do Python.

[![PyPI](https://img.shields.io/pypi/v/jacarev3)](https://pypi.org/project/jacarev3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/i-barbosa/jacarEV3/blob/main/LICENSE)

## Instalação

```bash
pip install jacarev3
```

Ou pra desenvolver localmente:

```bash
git clone https://github.com/i-barbosa/jacarEV3.git
cd jacarEV3
pip install -e . --break-system-packages
```

## Uso rápido

```python
from jacarev3 import RoboEV3

robo = RoboEV3('00:16:53:64:F8:B8')  # MAC do seu EV3

robo.apitar()
robo.led('VERDE')

robo.testar_tudo()  # testa motores A-D e sensores 1-4

robo.fechar()
```

Ou com `with` (fecha a conexão sozinho):

```python
with RoboEV3('00:16:53:64:F8:B8') as robo:
    robo.apitar()
    robo.testar_motores()
```

## Exemplos por funcionalidade

### Som

```python
robo.apitar()                                  # bip padrão
robo.apitar(frequencia=880, duracao_ms=300)    # agudo e curto
robo.apitar(volume=5)                          # mais alto (1-100)
```

### LED

```python
robo.led('VERDE')
robo.led('VERMELHO_PISCA')
robo.led('DESLIGADO')
```

### Motor

```python
# Gira pra frente 1s, velocidade 30%
robo.girar_motor('A', velocidade=30, duracao_ms=1000)

# Gira pra trás (velocidade negativa)
robo.girar_motor('A', velocidade=-30, duracao_ms=1000)

# Solta o motor sem frear (roda livre)
robo.parar_motor('A', frear=False)

# Testa um motor específico
robo.testar_motor('B')

# Testa A, B, C, D de uma vez (pula os vazios com aviso)
robo.testar_motores()
```

### Sensores

```python
# Cada teste espera o valor MUDAR de verdade antes de seguir
# (aproxima algo do ultrassônico, aperta o toque, muda a cor)
robo.testar_ultrassonico(porta=1)
robo.testar_toque(porta=2)
robo.testar_cor(porta=3)

# Testa só alguns tipos, tempo de espera customizado
robo.testar_sensores(tipos=('toque', 'cor'), tempo_limite=10)
```

### Leitura direta (pra loops de controle)

Os `testar_*` são pra conferir se o hardware tá funcionando. Quando você vai
escrever a lógica do robô, usa `ler_sensor()` e `mover_continuo()`:

```python
from jacarev3 import RoboEV3, protocolo as p

with RoboEV3('00:16:53:64:F8:B8') as robo:
    while True:
        distancia = robo.ler_sensor(4, p.MODO_ULTRASSONICO_CM)

        if distancia < 15:
            robo.parar_motor('B')
            robo.parar_motor('C')
            break

        robo.mover_continuo('B', 30)
        robo.mover_continuo('C', 30)
```

Modos de sensor disponíveis: `MODO_TOQUE`, `MODO_ULTRASSONICO_CM`,
`MODO_COR_REFLETIDA`, `MODO_COR_AMBIENTE`, `MODO_COR_COR`.

### Tópicos prontos

`jacarev3.topicos` traz receitas completas de robótica educacional, feitas
pra serem lidas e modificadas em aula — não só chamadas:

```python
from jacarev3 import RoboEV3
from jacarev3.topicos import circuito, desvio

with RoboEV3('00:16:53:64:F8:B8') as robo:
    # Seguir linha preta (bang-bang), 15 segundos
    circuito.seguir_linha(robo, porta_sensor=1, duracao_s=15, verboso=True)

    # Descobrir o limiar claro/escuro do seu tapete
    limiar = circuito.calibrar(robo, porta_sensor=1)

    # Andar reto e desviar de obstáculo
    desvio.desviar_obstaculo(robo, porta_sensor=4, distancia_minima_cm=15)
```

Cada tópico tem um tutorial passo a passo em [docs/](https://github.com/i-barbosa/jacarEV3/tree/main/docs):
[básico](https://github.com/i-barbosa/jacarEV3/blob/main/docs/basico.md) ·
[seguir linha](https://github.com/i-barbosa/jacarEV3/blob/main/docs/circuito.md) ·
[desviar de obstáculo](https://github.com/i-barbosa/jacarEV3/blob/main/docs/desvio.md)

## API completa

### Som e LED
| Método | Descrição |
|---|---|
| `apitar(frequencia=440, duracao_ms=500, volume=1)` | Toca um bip |
| `led(cor)` | `VERDE`, `VERMELHO`, `AMBAR`, `DESLIGADO`, e variantes `_PISCA` / `_PULSA` |

### Motores (portas A-D)
| Método | Descrição |
|---|---|
| `girar_motor(porta, velocidade=30, duracao_ms=1000, frear=True)` | Velocidade de -100 a 100 |
| `mover_continuo(porta, velocidade=30)` | Liga e deixa rodando (não para sozinho) |
| `parar_motor(porta, frear=True)` | Para o motor |
| `testar_motor(porta)` | Testa um motor específico |
| `testar_motores()` | Testa A, B, C, D de uma vez |

### Sensores (portas 1-4)
| Método | Descrição |
|---|---|
| `ler_sensor(porta, modo)` | Leitura direta e imediata, pra loops de controle |
| `testar_ultrassonico(porta, tempo_limite=15)` | Espera a distância mudar |
| `testar_toque(porta, tempo_limite=15)` | Espera pressionado/solto |
| `testar_cor(porta, tempo_limite=15)` | Espera a cor mudar |
| `testar_sensores(tipos=(...), tempo_limite=15)` | Testa os 3 tipos nas 4 portas |
| `testar_tudo(tempo_limite=15)` | Motores + todos os sensores |

### Tópicos (`jacarev3.topicos`)
| Função | Descrição |
|---|---|
| `circuito.seguir_linha(robo, porta_sensor=1, ...)` | Segue linha preta com controle bang-bang |
| `circuito.calibrar(robo, porta_sensor, ...)` | Descobre o limiar claro/escuro do tapete |
| `desvio.desviar_obstaculo(robo, porta_sensor=4, ...)` | Anda reto e desvia com o ultrassônico |

## Troubleshooting

**`OSError` / timeout ao conectar**
Confirma que o EV3 tá pareado nas Configurações Bluetooth do Windows/Linux
e que o Bluetooth dele tá visível/ligado antes de rodar o script.

**`[AVISO] Sem motor (ou erro) na porta X`**
Normal se não tiver motor físico conectado nessa porta — o método pula e
segue pros outros.

**`speed must be in range [1-100]`**
Velocidade tem que ser um valor entre -100 e 100 (direção pelo sinal, não
por valores fora do range).

**`EV3 respondeu com erro pro comando`**
Geralmente é modo/porta errada no sensor (ex: pedir leitura de cor num
sensor de toque). Confere se o sensor físico bate com o tipo do método
chamado.

## Status

v0.2.1 — protocolo validado byte a byte contra a documentação oficial da
LEGO (Communication Developer Kit), ainda em bateria de testes no robô
físico. Veja [CHANGELOG.md](https://github.com/i-barbosa/jacarEV3/blob/main/CHANGELOG.md) pro histórico de versões.

## Contribuindo

Issues e PRs são bem-vindos em
[github.com/i-barbosa/jacarEV3](https://github.com/i-barbosa/jacarEV3).

## Licença

MIT — veja [LICENSE](https://github.com/i-barbosa/jacarEV3/blob/main/LICENSE).
