#!/usr/bin/env python3
"""
Script de création automatique du bucket MinIO
Utilisé dans le Dockerfile pour initialiser le bucket 'videos'
"""

import os
import sys
import minio
from minio.error import S3Error

def create_bucket_if_not_exists():
    """Créer le bucket s'il n'existe pas"""
    try:
        # Configuration depuis les variables d'environnement
        # En mode développement, utiliser localhost au lieu de minio
        endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        access_key = os.getenv("MINIO_ACCESS_KEY", "admin")
        secret_key = os.getenv("MINIO_SECRET_KEY", "admin123")
        secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
        bucket_name = os.getenv("MINIO_BUCKET", "videos")
        
        print(f"🔗 Connexion à MinIO: {endpoint}")
        
        # Créer le client MinIO
        client = minio.Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        # Vérifier si le bucket existe
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"✅ Bucket '{bucket_name}' créé avec succès")
        else:
            print(f"✅ Bucket '{bucket_name}' existe déjà")
            
        # Lister les buckets pour vérification
        buckets = client.list_buckets()
        print(f"📋 Buckets disponibles: {[b.name for b in buckets]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du bucket: {e}")
        return False

if __name__ == "__main__":
    success = create_bucket_if_not_exists()
    sys.exit(0 if success else 1)
