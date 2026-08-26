# ============================================================
# ASISTPQR v2 - ENTORNO DE EJECUCIÓN
# ============================================================

FROM mcr.microsoft.com/playwright/python:v1.62.0-noble


# ------------------------------------------------------------
# 1. EVITAR INTERACCIONES DURANTE INSTALACIÓN
# ------------------------------------------------------------

ENV DEBIAN_FRONTEND=noninteractive


# ------------------------------------------------------------
# 2. DIRECTORIO DE TRABAJO
# ------------------------------------------------------------

WORKDIR /app


# ------------------------------------------------------------
# 3. INSTALAR RCLONE
# ------------------------------------------------------------

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        unzip \
    && curl https://rclone.org/install.sh | bash \
    && rclone version \
    && rm -rf /var/lib/apt/lists/*


# ------------------------------------------------------------
# 4. COPIAR REQUIREMENTS
# ------------------------------------------------------------

COPY requirements.txt .


# ------------------------------------------------------------
# 5. INSTALAR DEPENDENCIAS PYTHON
# ------------------------------------------------------------

RUN pip install --no-cache-dir -r requirements.txt


# ------------------------------------------------------------
# 6. COPIAR TODO EL PROYECTO
# ------------------------------------------------------------

COPY . .


# ------------------------------------------------------------
# 7. CREAR CARPETA DE DESCARGAS
# ------------------------------------------------------------

RUN mkdir -p /app/downloads


# ------------------------------------------------------------
# 8. COMANDO DE EJECUCIÓN
# ------------------------------------------------------------

CMD ["python", "src/robot_pqr.py"]