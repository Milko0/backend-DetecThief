import io
from PIL import Image
from fastapi import UploadFile
import requests
from infraestructura.rmq import publicar_en_rabbitmq
from infraestructura.almacenamiento import guardar_imagen_storage
from infraestructura.supabase import obtener_ngrok_url

# # Cargar el procesador y el modelo de IA
# #processor = AutoImageProcessor.from_pretrained("csr2000/UCF_Crime")
# #model = AutoModelForImageClassification.from_pretrained("csr2000/UCF_Crime")

# # Función para procesar la imagen y enviar la predicción
# async def procesar_imagen(id_camara: int, timestamp: str, file: UploadFile):
#     # Leer la imagen
#     image_bytes = await file.read()
#     img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
#     # Preprocesar la imagen
#     inputs = processor(images=img, return_tensors="pt")

#     # Hacer la predicción
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits
#         pred_idx = logits.argmax(-1).item()
#         pred_label = model.config.id2label[pred_idx]

#     # Solo se publica si la predicción es relevante
#     if pred_label == "ClaseRelevante":  # Cambia "ClaseRelevante" por la clase que te interesa
#         # Guardar la imagen en Supabase Storage
#         image_url = await guardar_imagen_storage(id_camara, timestamp, image_bytes)

#         # Publicar en RabbitMQ
#         mensaje = {
#             "id_camara": id_camara,
#             "timestamp": timestamp,
#             "prediccion": pred_label,
#             "image_url": image_url
#         }
#         await publicar_en_rabbitmq(mensaje)
    
#     return pred_label


async def procesar_imagen(id_camara: int, timestamp: str, file: UploadFile):
    # Leer la imagen
    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Convertir imagen a bytes para enviarla en la solicitud
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    # Obtener la URL de ngrok (asegúrate de que obtener_ngrok_url() devuelve el endpoint correcto)
    ngrok_url =  obtener_ngrok_url()  
    
    try:
        # Hacer la solicitud al endpoint de predicción
        response = requests.post(
            f"{ngrok_url}/predecir",
            files={"file": ("image.jpg", img_byte_arr, "image/jpeg")}
        )
        response.raise_for_status()  # Lanza error si la solicitud falla
        pred_label = response.json().get("prediccion")

        # Filtrar por clases relevantes (ajusta "ClaseRelevante" según tu necesidad)
        if pred_label != "Normal Videos":
            # Guardar imagen en Supabase Storage
            image_url = guardar_imagen_storage(id_camara, timestamp, image_bytes)
            
            # Publicar en RabbitMQ
            mensaje = {
                "id_camara": id_camara,
                "timestamp": timestamp,
                "prediccion": pred_label,
                "image_url": image_url
            }
            publicar_en_rabbitmq(mensaje)
        
        return pred_label

    except Exception as e:
        print(f"Error al llamar al endpoint de predicción: {e}")
        return "Error"