# aplicacion/notificador.py
from html import escape
from infraestructura.db import obtener_contactos_por_rol
from infraestructura.telegram_sender import enviar_mensaje_telegram
from infraestructura.email_sender import enviar_email

def procesar_evento(mensaje: dict, rol_destino: str, chat_id_telegram: str):
    print(f"[Procesador] Procesando mensaje para rol '{rol_destino}'")

    # Campos flexibles
    camara_id = escape(str(mensaje.get("camara_id", "N/A")))
    tipo_incidente = escape(mensaje.get("tipo_incidente", f"ID {mensaje.get('tipo_incidente_id', 'N/A')}"))
    descripcion = escape(mensaje.get("descripcion", "Sin descripción"))
    fecha = escape(mensaje.get("fecha_deteccion", "Fecha no disponible"))
    imagen_url = mensaje.get("imagen_url") or mensaje.get("imagen_referencia")

    texto = f"""🚨 <b>Incidente Detectado</b>
<b>Cámara:</b> {camara_id}
<b>Tipo:</b> {tipo_incidente}
<b>Descripción:</b> {descripcion}
<b>Fecha:</b> {fecha}
"""

    if imagen_url:
        texto += f"\n📷 <a href='{escape(imagen_url)}'>Ver imagen</a>"

    cuerpo_html = texto.replace("\n", "<br>")
    asunto = f"🚨 Alerta: {tipo_incidente} en cámara {camara_id}"

    contactos = obtener_contactos_por_rol(rol_destino)
    print(f"[Procesador] {len(contactos)} contactos '{rol_destino}' encontrados")

    for contacto in contactos:
        correo = contacto.get("correo")
        print(f"[Procesador] Notificando a {correo}")
        if correo:
            enviar_email(destinatario=correo, asunto=asunto, cuerpo_html=cuerpo_html)

    if chat_id_telegram:
        enviar_mensaje_telegram(chat_id_telegram, texto)
