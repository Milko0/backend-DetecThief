from fastapi import APIRouter, UploadFile, File, Form
from aplicacion.servicios.procesar_imagen import procesar_imagen

router = APIRouter()

@router.post("/procesar/")
async def procesar(
    id_camara: int = Form(...),
    timestamp: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        resultado = await procesar_imagen(id_camara, timestamp, file)
        return {"prediccion": resultado}
    except Exception as e:
        return {"error": str(e)}