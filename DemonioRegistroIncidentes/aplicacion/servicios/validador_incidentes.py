import time
from infraestructura.mensajeria.productor_rabbitmq import ProductorRabbitMQ
from infraestructura.base_datos.repositorio_postgres import IncidenteRepositorio

INTERVALO_SEGUNDOS = 20  # puedes ajustar esto según necesidad

class NotificadorOperador:
    def __init__(self):
        self.repo = IncidenteRepositorio()
        self.productor = ProductorRabbitMQ(queue_name="notificacion_operador")

    def ejecutar(self):
        print("[🟢] Iniciando notificador de operadores...")
        while True:
            try:
                incidentes = self.repo.obtener_historial_activos()

                if not incidentes:
                    print("[🔍] No hay incidentes activos para operadores.")
                
                for incidente in incidentes:
                    print(f"[📤] Publicando a operadores: ID {incidente['id']} | {incidente['descripcion']}")
                    self.productor.publicar(incidente)
                    self.repo.marcar_historial_confirmado(incidente['id'])

            except Exception as e:
                print(f"[❌] Error en notificador operador: {e}")
            
            time.sleep(INTERVALO_SEGUNDOS)