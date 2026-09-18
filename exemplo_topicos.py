"""
Exemplo de uso dos tópicos (circuito e desvio).
Ajusta as portas de acordo com a montagem do seu robô.
"""

from jacarev3 import RoboEV3
from jacarev3.topicos import circuito, desvio

MAC_DO_ROBO = '00:16:53:64:F8:B8'

with RoboEV3(MAC_DO_ROBO) as robo:

    # --- Tópico: seguir linha ---
    # Calibra automaticamente (pede pra passar no claro e no escuro)
    circuito.seguir_linha(
        robo,
        porta_sensor=1,
        porta_motor_esquerdo='B',
        porta_motor_direito='C',
        velocidade=25,
        duracao_s=15,  # ou None pra rodar até Ctrl+C
    )

    # --- Tópico: desviar de obstáculo ---
    desvio.desviar_obstaculo(
        robo,
        porta_sensor=4,
        porta_motor_esquerdo='B',
        porta_motor_direito='C',
        distancia_minima_cm=15,
        duracao_s=15,
    )
