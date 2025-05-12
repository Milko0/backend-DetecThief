from datetime import datetime
from dataclasses import dataclass

@dataclass
class Incidente:
    camara_id: int
    tipo_incidente_id: str
    imagen_referencia: str
    descripcion: str  # Ahora es obligatorio
    fecha_detectado: datetime = datetime.now()