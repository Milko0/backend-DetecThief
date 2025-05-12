import requests
import re
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

SUPABASE_URL_ALMACENAMIENTO = os.getenv("SUPABASE_URL_ALMACENAMIENTO")
SUPABASE_KEY= os.getenv("SUPABASE_KEY")

def guardar_imagen_storage(id_camara: int, timestamp: str, image_bytes: bytes):
    bucket_name = "detectchief"

    # 1. Parsear timestamp completo (con hora)
    try:
        dt = datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S")
        fecha_str = dt.strftime("%Y-%m-%d")  # Carpeta por fecha
    except ValueError:
        raise Exception(f"Formato de timestamp inválido: {timestamp}. Debe ser DD/MM/YYYY HH:MM:SS")

    # 2. Limpiar el timestamp para el nombre del archivo
    timestamp_sanitizado = re.sub(r'[^a-zA-Z0-9]', '_', timestamp)

    # 3. Construir nombre del archivo organizado por fecha
    archivo_nombre = f"public/{fecha_str}/camara_{id_camara}_{timestamp_sanitizado}.jpg"

    headers = {
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "image/jpeg",
    }

    upload_url = f"{SUPABASE_URL_ALMACENAMIENTO}/object/{bucket_name}/{archivo_nombre}"

    response = requests.put(upload_url, headers=headers, data=image_bytes)

    if response.status_code == 200:
        return f"{SUPABASE_URL_ALMACENAMIENTO}/{bucket_name}/{archivo_nombre}"
    else:
        raise Exception(f"Error al guardar la imagen: {response.text}")