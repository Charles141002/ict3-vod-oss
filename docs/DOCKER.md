# Docker - Guide de déploiement

## 🐳 Architecture Docker

L'application VoD utilise Docker Compose pour orchestrer plusieurs services :

- **MinIO** : Stockage des vidéos (port 9000/9001)
- **VoD App** : Application FastAPI (port 8000)
- **Nginx** : Reverse proxy (port 80)

## 🚀 Démarrage rapide

### Prérequis
- Docker
- Docker Compose

### Commandes

```bash
# Démarrer l'application complète
./scripts/docker-start.sh

# Ou manuellement
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
./scripts/docker-stop.sh
# ou
docker-compose down
```

### 🎯 Création automatique du bucket

Le bucket `videos` est **créé automatiquement** au démarrage :

1. **Docker Compose** : Le script `docker-entrypoint.sh` crée le bucket
2. **Mode développement** : Le script `create_bucket.py` gère la création
3. **Vérification** : Le script `test-bucket.sh` teste le fonctionnement

```bash
# Tester la création du bucket
./scripts/test-bucket.sh
```

## 🌐 Accès aux services

- **Application VoD** : http://localhost
- **MinIO Console** : http://localhost/minio/
- **MinIO API** : http://localhost:9000

### Credentials MinIO
- **Username** : admin
- **Password** : admin123

## 📁 Volumes et données

### Volumes persistants
- `minio_data` : Données MinIO (vidéos stockées)
- `./data` : Vidéos d'exemple (monté en lecture seule)
- `./assets` : QR codes générés

### Structure des volumes
```
./data/          → /app/data (lecture seule)
./assets/        → /app/assets
minio_data       → /data (MinIO)
```

## 🔧 Configuration

### Variables d'environnement
```bash
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin123
MINIO_SECURE=false
MINIO_BUCKET=videos
```

### Personnalisation
Modifier `docker-compose.yml` pour :
- Changer les ports
- Modifier les credentials
- Ajouter des volumes
- Configurer le réseau

## 🛠️ Développement

### Build personnalisé
```bash
# Reconstruire l'image
docker-compose build --no-cache

# Redémarrer avec nouvelle image
docker-compose up --build
```

### Debug
```bash
# Accéder au container
docker exec -it vod-app bash

# Voir les logs d'un service
docker-compose logs vod-app
docker-compose logs minio
```

## 📊 Monitoring

### Statut des services
```bash
docker-compose ps
```

### Ressources utilisées
```bash
docker stats
```

### Santé des services
```bash
# MinIO health check
curl http://localhost:9000/minio/health/live

# Application health check
curl http://localhost:8000/api/videos
```

## 🚨 Dépannage

### Problèmes courants

1. **Port déjà utilisé**
   ```bash
   # Changer les ports dans docker-compose.yml
   ports:
     - "8001:8000"  # Au lieu de 8000:8000
   ```

2. **MinIO ne démarre pas**
   ```bash
   # Vérifier les logs
   docker-compose logs minio
   
   # Supprimer les volumes et redémarrer
   docker-compose down -v
   docker-compose up -d
   ```

3. **Application ne trouve pas MinIO**
   ```bash
   # Vérifier la connectivité réseau
   docker exec -it vod-app ping minio
   
   # Vérifier les variables d'environnement
   docker exec -it vod-app env | grep MINIO
   ```

## 🔒 Sécurité

### Production
- Changer les credentials par défaut
- Utiliser HTTPS (MINIO_SECURE=true)
- Configurer un firewall
- Limiter l'accès réseau

### Exemple configuration sécurisée
```yaml
environment:
  MINIO_ROOT_USER: ${MINIO_USER}
  MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
  MINIO_SECURE: "true"
```

## 📈 Performance

### Optimisations
- Augmenter les limites de mémoire Docker
- Utiliser des volumes SSD
- Configurer le cache Nginx
- Optimiser les paramètres MinIO

### Monitoring
```bash
# Ressources par container
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```
