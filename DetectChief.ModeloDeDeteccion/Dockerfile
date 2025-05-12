FROM python:3.10-slim

# Evita prompts y define cache para transformers
ENV DEBIAN_FRONTEND=noninteractive
ENV TRANSFORMERS_CACHE=/tmp/transformers_cache

# Instala dependencias mínimas para compilación y PIL
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    libpng-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala dependencias sin cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Limpia caché de transformers y pip
RUN rm -rf /root/.cache /tmp/transformers_cache

# Puerto por defecto
EXPOSE 8000

# Comando para lanzar FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]