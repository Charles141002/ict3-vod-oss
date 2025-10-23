# Dockerfile pour l'application VoD
# Utilisation d'une image Python alternative en cas de problème Docker Hub
FROM python:3.11-alpine

# Métadonnées
LABEL maintainer="Charles Pelong"
LABEL description="VoD Application with FastAPI and MinIO"
LABEL version="1.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MINIO_ENDPOINT=minio:9000
ENV MINIO_ACCESS_KEY=admin
ENV MINIO_SECRET_KEY=admin123
ENV MINIO_SECURE=false
ENV MINIO_BUCKET=videos

# Créer le répertoire de travail
WORKDIR /app

# Installer les dépendances système (Alpine Linux)
RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY main.py .
COPY create_bucket.py .
COPY static/ ./static/

# Créer les répertoires nécessaires
RUN mkdir -p /app/data /app/assets/qr_codes

# Exposer le port
EXPOSE 8000

# Script de démarrage avec création automatique du bucket
RUN echo '#!/bin/sh' > /app/docker-entrypoint.sh && \
    echo 'set -e' >> /app/docker-entrypoint.sh && \
    echo '' >> /app/docker-entrypoint.sh && \
    echo 'echo "🚀 Démarrage de l'\''application VoD..."' >> /app/docker-entrypoint.sh && \
    echo '' >> /app/docker-entrypoint.sh && \
    echo '# Attendre que MinIO soit prêt' >> /app/docker-entrypoint.sh && \
    echo 'echo "⏳ Attente de MinIO..."' >> /app/docker-entrypoint.sh && \
    echo 'until curl -f http://minio:9000/minio/health/live 2>/dev/null; do' >> /app/docker-entrypoint.sh && \
    echo '  echo "MinIO n'\''est pas encore prêt, attente..."' >> /app/docker-entrypoint.sh && \
    echo '  sleep 2' >> /app/docker-entrypoint.sh && \
    echo 'done' >> /app/docker-entrypoint.sh && \
    echo '' >> /app/docker-entrypoint.sh && \
    echo 'echo "✅ MinIO est prêt !"' >> /app/docker-entrypoint.sh && \
    echo '' >> /app/docker-entrypoint.sh && \
    echo '# Créer le bucket s'\''il n'\''existe pas' >> /app/docker-entrypoint.sh && \
    echo 'echo "📁 Création du bucket videos..."' >> /app/docker-entrypoint.sh && \
    echo 'python3 create_bucket.py' >> /app/docker-entrypoint.sh && \
    echo '' >> /app/docker-entrypoint.sh && \
    echo 'echo "🎬 Démarrage du serveur FastAPI..."' >> /app/docker-entrypoint.sh && \
    echo '' >> /app/docker-entrypoint.sh && \
    echo '# Exécuter la commande passée en argument' >> /app/docker-entrypoint.sh && \
    echo 'exec "$@"' >> /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

# Point d'entrée
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Commande par défaut
CMD ["python", "main.py"]
