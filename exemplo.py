"""
Teste completo no robô real. Roda depois de `pip install -e .`
"""

from jacarev3 import RoboEV3

MAC_DO_ROBO = '00:16:53:64:F8:B8'

try:
    with RoboEV3(MAC_DO_ROBO) as robo:
        print("Conectado com sucesso!\n")

        robo.apitar()
        robo.led('VERDE')

        robo.testar_tudo()

        robo.led('DESLIGADO')

except Exception as e:
    print(f"[ERRO] {e}")
