import requests
from dotenv import load_dotenv
import os

#SUPABASE_URL = "https://yvqpmfzdpzdrtczkcupv.supabase.co"  # Ejemplo real
#SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2cXBtZnpkcHpkcnRjemtjdXB2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxNjA5NjgsImV4cCI6MjA2MTczNjk2OH0.tlzDQwqOKYqQTCxKDb_mHn-tfizkBE7RnAnG_7z0l_o"  # Clave API (anon/public o service role)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY= os.getenv("SUPABASE_API_KEY")

def obtener_ngrok_url():
    url = f"{SUPABASE_URL}/rest/v1/ngrok_urls?select=endpoint"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["endpoint"]
        else:
            raise Exception("No se encontró la URL de ngrok en Supabase")
    else:
        raise Exception(f"Error al obtener la URL de ngrok: {response.text}")