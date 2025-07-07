# main.py
from interfaces.consumidor_rabbit import RabbitMQConsumer
from config.settings import settings

if __name__ == "__main__":
    consumidor = RabbitMQConsumer(
        url=settings.RABBITMQ_URL,
        queues=settings.RABBITMQ_QUEUES
    )
    consumidor.start()
