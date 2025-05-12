# infraestructura/mensajeria/productor_rabbitmq.py
import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ProductorRabbitMQ:
    def __init__(self, queue_name="notificacion_supervisor"):  # Parámetro añadido
        self.url = os.getenv("RABBITMQ_URL")
        self.queue_name = queue_name  # Atributo nuevo
        self._setup_connection()

    def _setup_connection(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue=self.queue_name,  # Usamos el atributo
            durable=True
        )

    def publicar(self, mensaje):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,  # Usamos el mismo nombre
                body=json.dumps(mensaje),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Persistente
                )
            )
        except Exception as e:
            print(f"Error al publicar: {str(e)}")
            raise

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_open:
            self.connection.close()