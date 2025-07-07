import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL")
    RABBITMQ_QUEUES = ["notificacion_supervisor", "notificacion_operador"]
    SUPABASE_DB_URL: str = os.getenv("DB_HOST")
    SUPABASE_DB_USER: str = os.getenv("DB_USER")
    SUPABASE_DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    SUPABASE_DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: int = int(os.getenv("DB_PORT", 6543))
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

    BREVO_API_KEY: str = os.getenv("BREVO_API_KEY")
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER")

settings = Settings()

