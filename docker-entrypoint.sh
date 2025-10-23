#!/bin/bash
set -e

echo "🚀 Démarrage de l'application VoD..."

# Attendre que MinIO soit prêt
echo "⏳ Attente de MinIO..."
until curl -f http://minio:9000/minio/health/live 2>/dev/null; do
    echo "MinIO n'est pas encore prêt, attente..."
    sleep 2
done

echo "✅ MinIO est prêt !"

# Créer le bucket s'il n'existe pas
echo "📁 Vérification du bucket 'videos'..."
python -c "
import minio
import os
from minio.error import S3Error

try:
    client = minio.Minio(
        os.getenv('MINIO_ENDPOINT'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=os.getenv('MINIO_SECURE', 'false').lower() == 'true'
    )
    
    bucket_name = os.getenv('MINIO_BUCKET', 'videos')
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f'✅ Bucket {bucket_name} créé')
    else:
        print(f'✅ Bucket {bucket_name} existe déjà')
        
except Exception as e:
    print(f'❌ Erreur lors de la création du bucket: {e}')
    exit(1)
"

echo "🎬 Démarrage du serveur FastAPI..."

# Exécuter la commande passée en argument
exec "$@"
