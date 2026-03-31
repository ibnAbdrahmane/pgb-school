FROM ubuntu:22.04

# Variable de build pour optimiser le cache Docker
ARG BUILDKIT_INLINE_CACHE=1

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=UTC \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3-pip \
    gcc \
    pkg-config \
    libmysqlclient-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    shared-mime-info \
    fonts-liberation \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrader pip
RUN python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Copier les requirements AVANT le code (meilleur cache Docker)
COPY requirements-docker.txt .
RUN python3.11 -m pip install --no-cache-dir -r requirements-docker.txt

# Copier le code applicatif
COPY . .

# Créer les répertoires d'uploads
RUN mkdir -p /app/uploads/photos /app/uploads/bulletins /app/uploads/cartes && \
    chmod -R 755 /app/uploads

# Rendre le script d'entrée exécutable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000

CMD ["/app/entrypoint.sh"]
