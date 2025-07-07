from interfaces.consumidor_rabbit import RabbitMQConsumer
from config.settings import settings

# 🚀 SERVIDOR DE ESTADO PARA RENDER
from threading import Thread
from fastapi import FastAPI
import uvicorn

def iniciar_servidor_estado():
    app = FastAPI()

    @app.get("/estado")
    def estado():
        return {"status": "ok"}

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Iniciar el servidor de estado en segundo plano
    Thread(target=iniciar_servidor_estado, daemon=True).start()

    # Iniciar el consumidor de RabbitMQ
    consumidor = RabbitMQConsumer(
        url=settings.RABBITMQ_URL,
        queues=settings.RABBITMQ_QUEUES
    )
    consumidor.start()
