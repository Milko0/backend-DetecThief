# infraestructura/email_sender.py
import requests
from config.settings import settings


def enviar_email(destinatario: str, asunto: str, cuerpo_html: str) -> bool:
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {"name": "Sistema de Alertas", "email": settings.EMAIL_SENDER},
        "to": [{"email": destinatario}],
        "subject": asunto,
        "htmlContent": cuerpo_html
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print(f"[Email] Enviado a {destinatario}")
            return True
        else:
            print(f"[Email] Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[Email] Excepción: {e}")
        return False
