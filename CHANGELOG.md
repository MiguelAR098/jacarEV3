# Changelog

Todas as mudanças notáveis desse projeto são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
versionamento segue [SemVer](https://semver.org/lang/pt-BR/).

## [0.2.1] - 2026-09-17

### Corrigido
- Logo do README agora usa URL absoluta — a página do PyPI não resolve
  caminho relativo, então o logo aparecia quebrado lá. Links pro LICENSE e
  pro CHANGELOG também viraram absolutos pelo mesmo motivo.
- `__version__` estava travado em "0.1.0" enquanto o pacote já era 0.2.0.
  Agora o `pyproject.toml` lê a versão de `jacarev3.__init__` (setuptools
  dynamic), então existe um lugar só pra mudar.

### Adicionado
- README documenta o que entrou na 0.2.0: `ler_sensor()`, `mover_continuo()`
  e o submódulo `jacarev3.topicos`, com link pros tutoriais em `docs/`.
- `jacarev3` re-exporta `protocolo` e `topicos`; `jacarev3.topicos`
  re-exporta `circuito` e `desvio`. Antes `from jacarev3 import protocolo`
  só funcionava por acidente do import machinery.
- Extra de desenvolvimento: `pip install -e ".[dev]"` (pytest, ruff, mypy).
- `MANIFEST.in` põe `docs/`, `assets/` e o CHANGELOG no sdist.
- `.editorconfig`.

## [0.2.0] - 2026-09-17

### Adicionado
- Submódulo `jacarev3.topicos` — receitas prontas de robótica educacional:
  - `topicos.circuito.seguir_linha()` — seguir linha preta (bang-bang) +
    `calibrar()` automática
  - `topicos.desvio.desviar_obstaculo()` — desviar de obstáculo com
    sensor ultrassônico
- `RoboEV3.ler_sensor()` — leitura direta de sensor (pra loops de controle)
- `RoboEV3.mover_continuo()` — motor contínuo sem parar sozinho

## [0.1.0] - 2026-09-17

### Adicionado
- Protocolo "Direct Commands" do EV3 implementado do zero (`protocolo.py`),
  sem dependência de bibliotecas de terceiros — só stdlib do Python.
- Conexão Bluetooth clássica (RFCOMM) via `socket.AF_BLUETOOTH` (`conexao.py`).
- API em português (`RoboEV3`):
  - `apitar()`, `led()`
  - `girar_motor()`, `parar_motor()`, `testar_motor()`, `testar_motores()`
  - `testar_ultrassonico()`, `testar_toque()`, `testar_cor()`,
    `testar_sensores()`, `testar_tudo()`
- Encoding de pacotes validado byte a byte contra os exemplos oficiais do
  "LEGO MINDSTORMS EV3 Communication Developer Kit" (som, sensor, motor).

### Conhecido
- Testado offline (encoding); ainda em validação no robô físico.
- Sem suporte a WiFi/USB ainda (só Bluetooth clássico).
- Movimento de motor é por tempo, não por graus/posição.
