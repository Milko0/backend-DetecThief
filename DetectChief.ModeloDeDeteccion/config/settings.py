import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RABBITMQ_HOST : str =os.getenv("RABBITMQ_HOST", "localhost")
    SUPABASE_URL : str = os.getenv("SUPABASE_URL", "https://tu-supabase-url.supabase.co")
    SUPABASE_KEY : str =os.getenv("SUPABASE_KEY", "tu-supabase-key")
    SUPABASE_API_KEY : str = os.getenv("SUPABASE_API_KEY", "tu-supabase-api-key")
    SUPABASE_URL_ALMACENAMIENTO : str = os.getenv("SUPABASE_URL_ALMACENAMIENTO", "https://tu-supabase-url.supabase.co/storage/v1")
settings = Settings()