import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL")
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL")
    SUPABASE_DB_USER: str = os.getenv("SUPABASE_DB_USER")
    SUPABASE_DB_PASSWORD: str = os.getenv("SUPABASE_DB_PASSWORD")
    SUPABASE_DB_NAME: str = os.getenv("SUPABASE_DB_NAME")

settings = Settings()