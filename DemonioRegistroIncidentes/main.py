# demonio_registro_incidentes/main.py
from infraestructura.mensajeria.consumidor_rabbitmq import ConsumidorRabbitMQ

if __name__ == "__main__":
    print("🚀 Iniciando demonio de registro de incidentes...")
    consumidor = ConsumidorRabbitMQ()
    consumidor.iniciar()