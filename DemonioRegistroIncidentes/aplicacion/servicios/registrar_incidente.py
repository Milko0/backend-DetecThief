from datetime import datetime
from dominio.entidades.incidente import Incidente
from infraestructura.mensajeria.productor_rabbitmq import ProductorRabbitMQ
from infraestructura.base_datos.repositorio_postgres import IncidenteRepositorio

class RegistrarIncidenteService:
    # Mapeo completo de tipos de incidente (texto -> ID)
    MAPEO_TIPOS_INCIDENTE = {
        "Abuse": 0, "Arrest": 1, "Shooting": 10, "Shoplifting": 11,
        "Stealing": 12, "Vandalism": 13, "Arson": 2, "Assault": 3,
        "Burglary": 4, "Explosion": 5, "Fighting": 6,
        "RoadAccidents": 8, "Robbery": 9
    }

    def __init__(self):
        self.repositorio = IncidenteRepositorio()
        self.productor_notificaciones = ProductorRabbitMQ()

    def registrar_incidente(self, datos: dict):
        # Validar que el tipo de incidente sea válido
        if datos["prediccion"] not in self.MAPEO_TIPOS_INCIDENTE:
            raise ValueError(f"Tipo de incidente no válido: {datos['prediccion']}")

        # Procesar datos
        tipo_incidente_id = self.MAPEO_TIPOS_INCIDENTE[datos["prediccion"]]
        descripcion = self._generar_descripcion(datos)
        fecha = self._parsear_fecha(datos["timestamp"])

        # Crear entidad
        incidente = Incidente(
            camara_id=datos["id_camara"],
            tipo_incidente_id=tipo_incidente_id,
            imagen_referencia=datos["image_url"],
            descripcion=descripcion,
            fecha_detectado=fecha
        )

        # Persistir
        incidente_id = self.repositorio.insertar(incidente)

        # Publicar notificación
        self._publicar_notificacion(incidente_id, datos, tipo_incidente_id, descripcion)

        return incidente_id

    def _publicar_notificacion(self, incidente_id: int, datos_originales: dict, tipo_id: int, descripcion: str):
        mensaje = {
            
            "incidente_id": incidente_id,
            "camara_id": datos_originales["id_camara"],
            "tipo_incidente_id": tipo_id,
            "tipo_incidente": datos_originales["prediccion"],
            "descripcion": descripcion,
            "fecha_deteccion": datos_originales["timestamp"],
            "imagen_url": datos_originales["image_url"]
        }
        self.productor_notificaciones.publicar(mensaje)

    def _generar_descripcion(self, datos: dict) -> str:
        return (
            f"Alerta: {datos['prediccion']} detectado en cámara {datos['id_camara']} "
            f"({datos['timestamp']})"
        )

    def _parsear_fecha(self, fecha_str: str) -> datetime:
        return datetime.strptime(fecha_str, "%d/%m/%Y %H:%M:%S")