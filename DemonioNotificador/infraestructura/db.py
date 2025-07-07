# infraestructura/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from config.settings import settings


def get_db_connection():
    return psycopg2.connect(
            host=settings.SUPABASE_DB_URL,
            port=settings.DB_PORT,
            dbname=settings.SUPABASE_DB_NAME,
            user=settings.SUPABASE_DB_USER,
            password=settings.SUPABASE_DB_PASSWORD
    )


from psycopg2.extras import RealDictCursor

def obtener_contactos_por_rol(rol: str) -> list[dict]:
    query = """
    SELECT id, email AS correo, nickname AS nombre
    FROM usuarios
    WHERE rol = %s AND estado_sistema = 'activo' AND estado_notificaciones = 'activo'
    """

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (rol,))
            contactos = cursor.fetchall()
        conn.close()
        return contactos
    except Exception as e:
        print(f"[DB] Error al obtener contactos: {e}")
        return []
