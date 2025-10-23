from fastapi import FastAPI, HTTPException, Request, Depends, UploadFile, File
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from minio import Minio
from minio.error import S3Error
import os
import qrcode
import socket
import requests
from datetime import timedelta
from typing import Optional
import uuid

app = FastAPI(title="VoD App", description="Video-on-Demand Application")

# Configuration MinIO depuis les variables d'environnement
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "admin123")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"
BUCKET = os.getenv("MINIO_BUCKET", "videos")

# Connexion à MinIO
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)

# Servir les fichiers statiques (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_local_ip():
    """Obtenir l'IP locale de la machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_range_header(request: Request) -> Optional[str]:
    """Récupérer le header Range de manière sécurisée"""
    try:
        return request.headers.get('range')
    except:
        return None

def get_ngrok_url() -> Optional[str]:
    """Obtenir l'URL publique ngrok"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            for tunnel in data.get('tunnels', []):
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
        return None
    except:
        return None

# Route principale - servir l'index.html
@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# Lister toutes les vidéos
@app.get("/api/videos")
def list_videos():
    try:
        objects = client.list_objects(BUCKET)
        videos = []
        for obj in objects:
            # Filtrer seulement les fichiers vidéo
            if obj.object_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                videos.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified.isoformat() if obj.last_modified else None
                })
        return videos
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Streamer une vidéo avec streaming par chunks
@app.get("/api/video/{video_name}")
def stream_video(video_name: str, request: Request):
    try:
        # Vérifier que le fichier existe
        try:
            stat = client.stat_object(BUCKET, video_name)
        except S3Error:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Obtenir les headers de range
        range_header = request.headers.get('range')
        
        if range_header:
            # Parser le range header (ex: "bytes=0-1023")
            range_match = range_header.replace('bytes=', '').split('-')
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else stat.size - 1
            
            # S'assurer que end ne dépasse pas la taille du fichier
            end = min(end, stat.size - 1)
            
            # Obtenir la partie spécifique du fichier
            data = client.get_object(BUCKET, video_name, offset=start, length=end - start + 1)
            
            # Headers pour le streaming par chunks
            headers = {
                'Content-Range': f'bytes {start}-{end}/{stat.size}',
                'Accept-Ranges': 'bytes',
                'Content-Length': str(end - start + 1),
                'Content-Type': 'video/mp4',
                'Cache-Control': 'public, max-age=3600',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
                'Access-Control-Allow-Headers': 'Range, Content-Range'
            }
            
            return StreamingResponse(
                data, 
                status_code=206,  # Partial Content
                headers=headers,
                media_type="video/mp4"
            )
        else:
            # Pas de range header, utiliser un streaming plus simple pour ngrok
            def generate_chunks():
                chunk_size = 256 * 1024  # 256KB par chunk (plus petit pour ngrok)
                offset = 0
                
                while offset < stat.size:
                    chunk_length = min(chunk_size, stat.size - offset)
                    try:
                        chunk = client.get_object(BUCKET, video_name, offset=offset, length=chunk_length)
                        chunk_data = chunk.read()
                        yield chunk_data
                        offset += chunk_length
                    except Exception as e:
                        print(f"Erreur lors du streaming: {e}")
                        break
            
            return StreamingResponse(
                generate_chunks(),
                media_type="video/mp4",
                headers={
                    "Accept-Ranges": "bytes",
                    "Content-Type": "video/mp4",
                    "Content-Length": str(stat.size),
                    "Cache-Control": "public, max-age=3600",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
                    "Access-Control-Allow-Headers": "Range, Content-Range",
                    "X-Accel-Buffering": "no"  # Désactiver le buffering pour ngrok
                }
            )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour obtenir les métadonnées d'une vidéo
@app.get("/api/video/{video_name}/info")
def get_video_info(video_name: str):
    try:
        stat = client.stat_object(BUCKET, video_name)
        return {
            "name": video_name,
            "size": stat.size,
            "last_modified": stat.last_modified.isoformat() if stat.last_modified else None,
            "content_type": stat.content_type
        }
    except S3Error:
        raise HTTPException(status_code=404, detail="Video not found")

# Endpoint alternatif avec URL signée MinIO
@app.get("/api/video/{video_name}/url")
def get_video_url(video_name: str):
    try:
        # Vérifier que le fichier existe
        client.stat_object(BUCKET, video_name)
        
        # Générer une URL signée valide pour 1 heure
        url = client.presigned_get_object(
            BUCKET, 
            video_name, 
            expires=timedelta(hours=1)
        )
        return {"url": url}
    except S3Error:
        raise HTTPException(status_code=404, detail="Video not found")

# Générer un QR code pour une vidéo spécifique
@app.get("/qr/{video_name}")
def generate_qr_for_video(video_name: str):
    """Générer un QR code pour une vidéo spécifique"""
    try:
        # Vérifier que le fichier existe
        client.stat_object(BUCKET, video_name)
        
        # Utiliser ngrok si disponible, sinon IP locale
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            video_url = f"{ngrok_url}/api/video/{video_name}"
        else:
            local_ip = get_local_ip()
            video_url = f"http://{local_ip}:8000/api/video/{video_name}"
        
        # Générer le QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(video_url)
        qr.make(fit=True)
        
        # Créer l'image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder temporairement
        qr_path = f"static/qr_{video_name}.png"
        img.save(qr_path)
        
        return FileResponse(qr_path)
    except S3Error:
        raise HTTPException(status_code=404, detail="Video not found")

# Endpoint de test pour voir l'URL générée
@app.get("/test-url/{video_name}")
def test_video_url(video_name: str):
    """Tester l'URL générée pour une vidéo"""
    try:
        # Vérifier que le fichier existe
        client.stat_object(BUCKET, video_name)
        
        # Générer une URL signée MinIO directe
        minio_url = client.presigned_get_object(
            BUCKET, 
            video_name, 
            expires=timedelta(hours=24)
        )
        
        # Remplacer localhost par l'IP locale
        local_ip = get_local_ip()
        minio_url_fixed = minio_url.replace('localhost:9000', f'{local_ip}:9000')
        
        return {
            "original_url": minio_url,
            "fixed_url": minio_url_fixed,
            "local_ip": local_ip,
            "video_name": video_name
        }
    except S3Error:
        raise HTTPException(status_code=404, detail="Video not found")

# Endpoint de test pour diagnostiquer les problèmes
@app.get("/test/{video_name}")
def test_video_access(video_name: str):
    """Tester l'accès à une vidéo pour diagnostiquer les problèmes"""
    try:
        # Vérifier que le fichier existe
        stat = client.stat_object(BUCKET, video_name)
        
        # Tester la récupération d'un petit chunk
        test_chunk = client.get_object(BUCKET, video_name, offset=0, length=1024)
        chunk_data = test_chunk.read()
        
        return {
            "status": "success",
            "video_name": video_name,
            "file_size": stat.size,
            "test_chunk_size": len(chunk_data),
            "ngrok_url": get_ngrok_url(),
            "local_ip": get_local_ip(),
            "message": "MinIO et fichier accessibles"
        }
    except S3Error as e:
        return {
            "status": "error",
            "video_name": video_name,
            "error": str(e),
            "message": "Problème d'accès à MinIO"
        }

# Upload de vidéos
@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Uploader une nouvelle vidéo"""
    try:
        # Vérifier que c'est bien un fichier vidéo
        if not file.content_type or not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="Seuls les fichiers vidéo sont autorisés")
        
        # Générer un nom de fichier unique
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'mp4'
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Upload vers MinIO
        file_data = await file.read()
        
        # Créer un objet BytesIO pour MinIO
        from io import BytesIO
        file_stream = BytesIO(file_data)
        
        client.put_object(
            BUCKET,
            unique_filename,
            file_stream,
            length=len(file_data),
            content_type=file.content_type
        )
        
        return {
            "status": "success",
            "filename": unique_filename,
            "original_name": file.filename,
            "size": len(file_data),
            "message": "Vidéo uploadée avec succès"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

# Endpoint de test pour vérifier que l'upload fonctionne
@app.get("/api/test-upload")
def test_upload_endpoint():
    """Tester que l'endpoint upload est accessible"""
    return {
        "status": "success",
        "message": "Endpoint upload accessible",
        "endpoint": "/api/upload",
        "method": "POST"
    }

# Page avec tous les QR codes
@app.get("/qr-codes")
def list_qr_codes():
    """Page avec tous les QR codes"""
    local_ip = get_local_ip()
    ngrok_url = get_ngrok_url()
    
    try:
        objects = client.list_objects(BUCKET)
        videos = []
        for obj in objects:
            if obj.object_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.webm')):
                videos.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified.isoformat() if obj.last_modified else None
                })
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QR Codes - VoD App</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 15px; 
                padding: 30px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }}
            .header {{ 
                text-align: center; 
                margin-bottom: 30px; 
                color: #4a5568;
            }}
            .instructions {{ 
                background: #f0f8ff; 
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 30px; 
                border-left: 4px solid #667eea;
            }}
            .qr-container {{ 
                margin: 30px 0; 
                text-align: center; 
                padding: 20px;
                background: #f7fafc;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }}
            .qr-container h3 {{ 
                margin-bottom: 15px; 
                color: #2d3748;
            }}
            .qr-container img {{ 
                border: 2px solid #e2e8f0; 
                border-radius: 10px;
                max-width: 200px;
                height: auto;
            }}
            .video-info {{
                margin-top: 10px;
                font-size: 0.9rem;
                color: #718096;
            }}
            .back-link {{
                display: inline-block;
                margin-bottom: 20px;
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
            }}
            .back-link:hover {{
                text-decoration: underline;
            }}
            .refresh-btn {{
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                margin-left: 10px;
            }}
            .refresh-btn:hover {{
                background: #5a67d8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-link">← Retour à l'accueil</a>
            <button onclick="location.reload()" class="refresh-btn">🔄 Actualiser</button>
            
            <div class="header">
                <h1>📱 QR Codes pour Mobile</h1>
                <p>Scannez ces QR codes avec votre téléphone pour accéder aux vidéos</p>
            </div>
            
            <div class="instructions">
                <h3>📋 Instructions :</h3>
                <ol>
                    <li><strong>Scanner :</strong> Utilisez l'appareil photo de votre téléphone pour scanner le QR code</li>
                    <li><strong>Lecture :</strong> La vidéo s'ouvrira directement dans votre navigateur mobile</li>
                    <li><strong>Accès :</strong> Fonctionne depuis n'importe où grâce à ngrok</li>
                </ol>
                <p><strong>🌐 URL publique :</strong> <code>{ngrok_url if ngrok_url else f'{local_ip}:8000'}</code></p>
                <p><strong>⏰ Validité :</strong> Les QR codes sont toujours valides (pas d'expiration)</p>
                <p><strong>📱 Streaming optimisé :</strong> Les QR codes utilisent le streaming FastAPI pour une compatibilité maximale</p>
            </div>
    """
    
    if not videos:
        html_content += """
            <div class="qr-container">
                <h3>📁 Aucune vidéo trouvée</h3>
                <p>Ajoutez des vidéos dans MinIO pour générer des QR codes</p>
            </div>
        """
    else:
        for video in videos:
            # Formater la taille
            size_mb = video['size'] / (1024 * 1024)
            size_str = f"{size_mb:.1f} MB"
            
            html_content += f"""
            <div class="qr-container">
                <h3>🎬 {video['name']}</h3>
                <img src="/qr/{video['name']}" alt="QR Code pour {video['name']}" onerror="this.style.display='none'">
                <div class="video-info">
                    <p><strong>Taille :</strong> {size_str}</p>
                    <p><strong>Modifié :</strong> {video['last_modified'][:19] if video['last_modified'] else 'Inconnu'}</p>
                </div>
            </div>
            """
    
    html_content += """
        </div>
        
        <script>
            // Auto-refresh toutes les 5 minutes pour mettre à jour les QR codes
            setTimeout(() => {
                location.reload();
            }, 300000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
