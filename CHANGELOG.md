# Changelog

Todas as mudanças notáveis desse projeto são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
versionamento segue [SemVer](https://semver.org/lang/pt-BR/).

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
