# infraestructura/telegram_sender.py
import requests
from config.settings import settings


def enviar_mensaje_telegram(chat_id: str, mensaje: str) -> bool:
    """
    Envía un mensaje de texto a un chat o grupo de Telegram.
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensaje,
        "parse_mode": "HTML"  
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[Telegram] Enviado a chat_id {chat_id}")
            return True
        else:
            print(f"[Telegram] Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[Telegram] Excepción: {e}")
        return False
