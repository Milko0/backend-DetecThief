from fastapi import FastAPI
from interfaces.api import router as api_router

app = FastAPI(title="Servicio de visión por computadora")
app.include_router(api_router, prefix="/api")