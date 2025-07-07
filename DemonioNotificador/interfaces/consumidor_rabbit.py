# interfaces/consumidor_rabbit.py

import pika
import json
from config.settings import settings
from aplicacion.notificador import procesar_evento

TELEGRAM_CHAT_IDS = {
    "notificacion_supervisor": "-4785328088",
    "notificacion_operador": "-4610044125"
}

class RabbitMQConsumer:
    def __init__(self, url, queues):
        self.url = url
        self.queues = queues
        self._setup_connection()

    def _setup_connection(self):
        params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        for queue in self.queues:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_consume(queue=queue, on_message_callback=self._callback, auto_ack=True)

    def _callback(self, ch, method, properties, body):
        queue_name = method.routing_key
        try:
            mensaje = json.loads(body.decode("utf-8"))
            print(f"[RabbitMQ] Mensaje en {queue_name}: {mensaje}")

            if queue_name in TELEGRAM_CHAT_IDS:
                rol = "administrador" if "supervisor" in queue_name else "operador"
                procesar_evento(mensaje, rol_destino=rol, chat_id_telegram=TELEGRAM_CHAT_IDS[queue_name])
            else:
                print(f"[RabbitMQ] Cola desconocida: {queue_name}")

        except Exception as e:
            print(f"[RabbitMQ] Error procesando mensaje: {e}")

    def start(self):
        print("[RabbitMQ] Esperando mensajes...")
        self.channel.start_consuming()
