<p align="center">
  <img src="assets/logo.png" width="150" alt="jacarEV3">
</p>

# jacarEV3 🐊

Lib em português pra controlar o LEGO EV3 via Bluetooth. Sem dependências
externas — só biblioteca padrão do Python.

[![PyPI](https://img.shields.io/pypi/v/jacarev3)](https://pypi.org/project/jacarev3/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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
| `parar_motor(porta, frear=True)` | Para o motor |
| `testar_motor(porta)` | Testa um motor específico |
| `testar_motores()` | Testa A, B, C, D de uma vez |

### Sensores (portas 1-4)
| Método | Descrição |
|---|---|
| `testar_ultrassonico(porta, tempo_limite=15)` | Espera a distância mudar |
| `testar_toque(porta, tempo_limite=15)` | Espera pressionado/solto |
| `testar_cor(porta, tempo_limite=15)` | Espera a cor mudar |
| `testar_sensores(tipos=(...), tempo_limite=15)` | Testa os 3 tipos nas 4 portas |
| `testar_tudo(tempo_limite=15)` | Motores + todos os sensores |

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

v0.1.0 — protocolo validado byte a byte contra a documentação oficial da
LEGO (Communication Developer Kit), ainda em bateria de testes no robô
físico. Veja [CHANGELOG.md](CHANGELOG.md) pro histórico de versões.

## Contribuindo

Issues e PRs são bem-vindos em
[github.com/i-barbosa/jacarEV3](https://github.com/i-barbosa/jacarEV3).

## Licença

MIT — veja [LICENSE](LICENSE).
