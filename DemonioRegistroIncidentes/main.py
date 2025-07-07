# demonio_registro_incidentes/main.py

import threading
from infraestructura.mensajeria.consumidor_rabbitmq import ConsumidorRabbitMQ
from aplicacion.servicios.validador_incidentes import NotificadorOperador

def iniciar_consumidor():
    consumidor = ConsumidorRabbitMQ()
    consumidor.iniciar()

def iniciar_notificador():
    notificador = NotificadorOperador()
    notificador.ejecutar()

if __name__ == "__main__":
    print("[🔥] Iniciando demonio de registro de incidentes...")

    # Hilo para escuchar RabbitMQ (supervisor)
    hilo_consumidor = threading.Thread(target=iniciar_consumidor, daemon=True)
    hilo_consumidor.start()

    # Hilo para verificar historial y notificar a operadores
    hilo_notificador = threading.Thread(target=iniciar_notificador, daemon=True)
    hilo_notificador.start()

    # Mantener proceso vivo
    hilo_consumidor.join()
    hilo_notificador.join()