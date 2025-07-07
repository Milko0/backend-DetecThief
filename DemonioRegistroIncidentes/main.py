import threading
from infraestructura.mensajeria.consumidor_rabbitmq import ConsumidorRabbitMQ
from aplicacion.servicios.validador_incidentes import NotificadorOperador

# 🔧 Agregamos FastAPI para exponer puerto y evitar que Render apague el servicio
from fastapi import FastAPI
import uvicorn
from threading import Thread

def iniciar_servidor_estado():
    app = FastAPI()

    @app.get("/estado")
    def estado():
        return {"status": "ok"}

    uvicorn.run(app, host="0.0.0.0", port=8000)

def iniciar_consumidor():
    consumidor = ConsumidorRabbitMQ()
    consumidor.iniciar()

def iniciar_notificador():
    notificador = NotificadorOperador()
    notificador.ejecutar()

if __name__ == "__main__":
    print("[🔥] Iniciando demonio de registro de incidentes...")

    # Iniciar mini servidor HTTP de estado para mantener el puerto abierto
    servidor = Thread(target=iniciar_servidor_estado, daemon=True)
    servidor.start()

    # Hilo para escuchar RabbitMQ (supervisor)
    hilo_consumidor = threading.Thread(target=iniciar_consumidor, daemon=True)
    hilo_consumidor.start()

    # Hilo para verificar historial y notificar a operadores
    hilo_notificador = threading.Thread(target=iniciar_notificador, daemon=True)
    hilo_notificador.start()

    # Mantener proceso vivo
    hilo_consumidor.join()
    hilo_notificador.join()
