import pika
import json
import os
import ssl
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

#RABBITMQ_URL=""
RABBITMQ_URL= os.getenv("RABBITMQ_URL")
def obtener_conexion_rabbitmq():
    """Establece conexión segura con RabbitMQ en CloudAMQP usando SSL"""
    try:
        url = RABBITMQ_URL
        if not url:
            raise ValueError("Falta la variable RABBITMQ_URL en .env")
        
        # Crear parámetros con SSL
        params = pika.URLParameters(url)
        params.ssl_options = pika.SSLOptions(ssl.create_default_context())

        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        
        channel.queue_declare(queue='predicciones', durable=True)
        return channel, connection 

    except Exception as e:
        print(f"❌ Error al conectar a RabbitMQ: {str(e)}")
        raise

def publicar_en_rabbitmq(mensaje: dict):
    """Publica un mensaje en RabbitMQ"""
    channel = None
    connection = None
    try:
        channel, connection = obtener_conexion_rabbitmq()
        channel.basic_publish(
            exchange='',
            routing_key='predicciones',
            body=json.dumps(mensaje),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        print("✅ Mensaje publicado correctamente")

    except Exception as e:
        print(f"❌ Error al publicar mensaje: {str(e)}")
        raise

    finally:
        if channel and channel.is_open:
            channel.close()
        if connection and connection.is_open:
            connection.close()