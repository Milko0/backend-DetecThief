# infraestructura/base_datos/repositorio_postgres.py
import os
from dotenv import load_dotenv
from psycopg2 import pool, errors
from dominio.repositorios.base_repositorio import BaseRepositorio

load_dotenv()

class IncidenteRepositorio(BaseRepositorio):
    def __init__(self):
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )
            print("✅ Conexión a PostgreSQL establecida")
        except errors.OperationalError as e:
            print(f"❌ Error de conexión: {str(e)}")
            raise

    def insertar(self, incidente):
        conn = None
        try:
            conn = self.connection_pool.getconn()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO public.incidentes 
                    (camara_id, tipo_incidente_id, descripcion, fecha_detectado, imagen_referencia)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        incidente.camara_id,
                        incidente.tipo_incidente_id,
                        incidente.descripcion,
                        incidente.fecha_detectado,
                        incidente.imagen_referencia
                    )
                )
                result = cur.fetchone()
                conn.commit()
                return result[0]
        except errors.Error as e:
            if conn:
                conn.rollback()
            print(f"❌ Error en inserción: {str(e)}")
            raise
        finally:
            if conn:
                self.connection_pool.putconn(conn)