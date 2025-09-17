# VAULT Lite

Vault Lite is a minimal **FastAPI MVP** for file storage:  
    - Upload files (streamed in 1 MB chunks)  
    - Download files with correct MIME type  
    - List uploaded files with both **UUID** (safe storage name) and original filename

This project demonstrates backend fundamentals like file handling, safe storage, and metadata management.  
It’s designed as a learning project / resume piece, not production-ready security.

#quickstart
```bash
#Create Virtual Environment
python -m venv .venv

# 2. Activate it
    # On Git Bash (Windows):
    source .venv/Scripts/activate
    # On PowerShell (Windows):
    .venv\Scripts\Activate.ps1
    # On Linux/macOS:
    source .venv/bin/activate
#Install Dependencies
pip install -r requirements.txt

#Run Server
uvicorn app.main:app --reload
```


The API will be available at:
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc

API Endpoints
POST /upload
    Uploads file
    Returns:
        {
        "id": "uuid",
        "original_name": "resume.pdf",
        "stored_as": "uuid.pdf",
        "size": 233112
        }
GET /list_files
    Lists all uploaded files with UUID + original filename.
GET /file/{stored as}
    Download file by its stored UUID filename

How it works
    Files are stored under data/ directory
    Each file is saved with a UUID to prevent collisions
    A small .json metadatafile is stored alongside each upload
        Has original filenames, uuid filenames, and file size
    mimetypes ensure downloades include the correct Content-Type header


Notes:
    This is an MVP — no authentication or encryption yet.
    In production, you’d want:
        User accounts + JWT authentication
        Database for metadata (instead of JSON files)
        Cloud storage (AWS S3, GCP, Azure Blob)
        Access controls and auditing
        
