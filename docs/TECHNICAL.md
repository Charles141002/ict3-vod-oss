# VoD App - Documentation Technique

## Architecture

### Backend (FastAPI)
- **main.py** : Application principale avec tous les endpoints
- **Endpoints** :
  - `GET /` : Interface web principale
  - `GET /api/videos` : Liste des vidéos
  - `GET /api/video/{name}` : Streaming vidéo
  - `POST /api/upload` : Upload de vidéos
  - `GET /qr/{name}` : Génération QR code
  - `GET /qr-codes` : Page QR codes

### Frontend (HTML5)
- **static/index.html** : Interface utilisateur complète
- **Fonctionnalités** :
  - Liste des vidéos avec QR codes intégrés
  - Lecteur vidéo HTML5
  - Upload drag & drop
  - Interface responsive

### Stockage (MinIO)
- **Bucket** : `videos`
- **Format** : URLs signées pour streaming sécurisé
- **Accès** : Via API MinIO Python

## Dépendances

### Backend
- `fastapi` : Framework web
- `uvicorn` : Serveur ASGI
- `minio` : Client MinIO
- `qrcode` : Génération QR codes
- `requests` : Requêtes HTTP

### Frontend
- HTML5 natif
- CSS3 avec animations
- JavaScript ES6+

## Configuration

### Variables d'environnement
Voir `config.env` pour la configuration complète.

### MinIO
- Endpoint : `localhost:9000`
- Credentials : `admin/admin123`
- Bucket : `videos`

## Déploiement

### Local
```bash
python main.py
```

### Avec ngrok
```bash
./scripts/start_ngrok.sh
```

### Redémarrage
```bash
./scripts/restart_server.sh
```

## API Endpoints

### Videos
- `GET /api/videos` : Liste toutes les vidéos
- `GET /api/video/{name}` : Stream une vidéo
- `GET /api/video/{name}/info` : Métadonnées vidéo
- `POST /api/upload` : Upload nouvelle vidéo

### QR Codes
- `GET /qr/{name}` : QR code pour une vidéo
- `GET /qr-codes` : Page avec tous les QR codes

### Utilitaires
- `GET /test/{name}` : Test d'accès vidéo
- `GET /api/test-upload` : Test endpoint upload
