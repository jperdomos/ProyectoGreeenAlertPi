from alert_manager import activar_alerta, limpiar_gpio
from data.log_utils import inicializar_log

try:
    inicializar_log()
    activar_alerta(temperatura=30, humedad=78, duracion=4)
finally:
    limpiar_gpio()

