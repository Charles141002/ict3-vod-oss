# VoD Project Submission - ICT3

## 👥 Team Members
- **Charles Pelong** - Full-Stack Developer

## 📋 Project Description

**VoD (Video on Demand) Application** - Modern video streaming platform with Docker and mobile access via QR codes.

# 🎯 Main Features

### ✅ Backend (FastAPI)
- **REST API** : Complete video management
- **Optimized streaming** : Progressive playback with Range headers
- **Drag & drop upload** : Intuitive interface
- **Automatic QR codes** : Simplified mobile access
- **MinIO storage** : S3-compatible

### ✅ Frontend (HTML5)
- **Modern interface** : Responsive design
- **Native HTML5 video player** : Native streaming
- **Intuitive upload** : Drag & drop with validation
- **Integrated QR codes** : Display under each video

### ✅ Infrastructure (Docker)
- **Complete containerization** : MinIO + FastAPI + Nginx
- **Simplified deployment** : Single startup script
- **Mobile access** : ngrok for public QR codes
- **Automatic creation** : MinIO bucket created on startup

## 🛠️ Technologies

- **Backend** : FastAPI, Python 3.11, MinIO
- **Frontend** : HTML5, CSS3, JavaScript
- **Infrastructure** : Docker, Docker Compose, Nginx
- **Mobile** : ngrok, QR codes

## 🚀 Installation and Usage

### Prerequisites
- Docker
- ngrok free account with auth token

### Startup
```bash
# Configure ngrok credentials in .env file
cp env.example .env
# Edit .env and add your NGROK_AUTHTOKEN

# Then start the complete application (including ngrok)
./scripts/docker-start.sh
```

### Available Services
- **VoD Application** : http://localhost
- **MinIO Console** : http://localhost/minio/ (admin/admin123)
- **ngrok Dashboard** : http://localhost:4040
- **Public URL** : Check ngrok dashboard for your unique URL

## 📱 Mobile Access

1. **Start the application** : `./scripts/docker-start.sh` (includes ngrok)
2. **Access QR codes** : http://localhost:8000/qr-codes
3. **Scan with mobile** : Works from anywhere via your ngrok URL
4. **Find your ngrok URL** : Check http://localhost:4040

## 🎓 Technical Learnings

### Development
- **FastAPI** : Modern APIs with automatic documentation
- **MinIO** : Distributed storage and streaming
- **Docker** : Containerization and orchestration
- **QR Codes** : Mobile integration

### Architecture
- **Microservices** : MinIO/App/Nginx separation
- **Streaming** : Optimization for video playback
- **Mobile-first** : QR codes for universal access
- **DevOps** : Automated deployment

## 📊 Results

- ✅ **Functional application** : Streaming, upload, QR codes
- ✅ **Simplified deployment** : One script to start everything
- ✅ **Mobile access** : QR codes with ngrok
- ✅ **Robust architecture** : Docker + health checks
- ✅ **Modern interface** : Responsive and intuitive design

