import os
import json
from kombu import Connection, Exchange, Queue
from dotenv import load_dotenv

load_dotenv()

class ProductorRabbitMQ:
    def __init__(self, queue_name="notificacion_supervisor"):
        self.url = os.getenv("RABBITMQ_URL")
        self.queue_name = queue_name
        self.exchange = Exchange('', type='direct')
        self.queue = Queue(name=self.queue_name, exchange=self.exchange, routing_key=self.queue_name)

    def publicar(self, mensaje):
        try:
            with Connection(self.url, heartbeat=60, transport_options={'confirm_publish': True}) as conn:
                producer = conn.Producer(serializer='json')
                producer.publish(
                    mensaje,
                    exchange=self.exchange,
                    routing_key=self.queue_name,
                    declare=[self.queue],
                    retry=True,
                    retry_policy={
                        'interval_start': 0,
                        'interval_step': 2,
                        'interval_max': 10,
                        'max_retries': 3
                    }
                )
                print("✅ Mensaje publicado correctamente con SSL usando kombu")
        except Exception as e:
            print(f"❌ Error al publicar con kombu: {e}")
            raise
