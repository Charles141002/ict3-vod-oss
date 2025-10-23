# VoD App - Video on Demand

Une application web complète pour le streaming de vidéos avec FastAPI et MinIO.

## 🚀 Fonctionnalités

- **Backend FastAPI** : API REST pour gérer les vidéos
- **Frontend HTML5** : Interface utilisateur moderne et responsive
- **Streaming vidéo** : Lecture directe depuis MinIO
- **Gestion des métadonnées** : Informations sur les fichiers vidéo
- **Interface intuitive** : Design moderne avec statistiques

## 📋 Prérequis

- Python 3.8+
- MinIO en cours d'exécution sur `localhost:9000`
- Bucket `videos` créé dans MinIO

## 🛠️ Installation

### Démarrage avec Docker 🐳

**1. Démarrer l'application :**
```bash
./scripts/docker-start.sh
```

**2. Démarrer ngrok pour l'accès mobile :**
```bash
./scripts/start-ngrok.sh
```

**Services disponibles :**
- **Application VoD** : http://localhost
- **MinIO Console** : http://localhost/minio/ (admin/admin123)
- **MinIO API** : http://localhost:9000
- **ngrok Dashboard** : http://localhost:4040

## 🌐 Utilisation

1. **Accéder à l'application** : http://localhost:8000
2. **API endpoints** :
   - `GET /` : Interface web principale
   - `GET /api/videos` : Liste toutes les vidéos
   - `GET /api/video/{name}` : Stream une vidéo spécifique
   - `GET /api/video/{name}/info` : Métadonnées d'une vidéo

## 📁 Structure du projet

```
ICT3/
├── main.py              # Backend FastAPI
├── requirements.txt     # Dépendances Python
├── create_bucket.py     # Création automatique bucket
├── Dockerfile          # Image Docker application
├── docker-compose.yml  # Orchestration Docker
├── nginx.conf          # Configuration Nginx
├── static/
│   └── index.html      # Frontend HTML5
├── scripts/
│   ├── docker-start.sh # Script démarrage Docker
│   ├── docker-stop.sh  # Script arrêt Docker
│   └── start-ngrok.sh  # Script ngrok pour mobile
├── assets/
│   └── qr_codes/       # QR codes générés (vide)
├── README.md           # Documentation principale
└── SUBMISSION.md       # Rapport de soumission
```

## 🎯 Fonctionnalités détaillées

### Backend (FastAPI)
- Connexion sécurisée à MinIO
- Streaming vidéo optimisé avec headers HTTP appropriés
- Gestion d'erreurs robuste
- API RESTful avec documentation automatique

### Frontend (HTML5)
- Interface responsive et moderne
- Lecteur vidéo HTML5 natif
- Liste des vidéos avec métadonnées
- Statistiques en temps réel
- Gestion d'erreurs utilisateur-friendly

## 🔧 Configuration MinIO

Assurez-vous que MinIO est configuré avec :
- **Endpoint** : `localhost:9000`
- **Access Key** : `admin`
- **Secret Key** : `admin123`
- **Bucket** : `videos` (créé et contenant vos vidéos)

## 📱 Accès Mobile avec QR Codes

**Pour scanner les QR codes avec votre mobile :**

1. **Démarrer ngrok** : `./scripts/start-ngrok.sh`
2. **Accéder aux QR codes** : http://localhost:8000/qr-codes
3. **Scanner avec mobile** : Fonctionne depuis n'importe où !

Les QR codes utilisent automatiquement l'URL ngrok publique pour un accès mobile optimal.

## 🛠️ Scripts utiles

- **`./scripts/docker-start.sh`** : Démarrer l'application complète avec Docker
- **`./scripts/docker-stop.sh`** : Arrêter tous les services Docker
- **`./scripts/start-ngrok.sh`** : Démarrer ngrok pour accès mobile

## 🚀 Prochaines étapes

- [ ] Ajouter l'authentification utilisateur
- [ ] Implémenter le streaming HLS/DASH
- [ ] Ajouter la recherche et filtrage
- [ ] Créer un système de playlists
- [ ] Ajouter les sous-titres
- [ ] Implémenter la compression vidéo automatique
