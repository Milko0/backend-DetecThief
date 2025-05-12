# demonio_registro_incidentes/infraestructura/mensajeria/consumidor_rabbitmq.py
import pika
import json
import os
from dotenv import load_dotenv
from aplicacion.servicios.registrar_incidente import RegistrarIncidenteService

load_dotenv()

class ConsumidorRabbitMQ:
    def __init__(self):
        self.url = os.getenv("RABBITMQ_URL")
        self.queue = os.getenv("RABBITMQ_QUEUE_INCIDENTES", "predicciones")
        self.service = RegistrarIncidenteService()

    def callback(self, ch, method, properties, body):
        try:
            mensaje = json.loads(body)
            print(f"📥 Mensaje recibido: {mensaje}")
            self.service.registrar_incidente(mensaje)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"❌ Error procesando mensaje: {str(e)}")

    def iniciar(self):
        connection = pika.BlockingConnection(pika.URLParameters(self.url))
        channel = connection.channel()
        
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        
        print(f"🔄 Escuchando cola '{self.queue}'...")
        channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=False
        )
        
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        finally:
            if connection.is_open:
                connection.close()