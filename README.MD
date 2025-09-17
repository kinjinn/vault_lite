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
            "id": "c71a7f812a0d4d53a6e1c0e1e5a12345",
            "original_name": "resume.pdf",
            "stored_as": "c71a7f812a0d4d53a6e1c0e1e5a12345.pdf",
            "size": 233112,
            "uploaded_at": "2025-09-16T15:24:00Z"
        }
GET /list_files
    Lists all uploaded files with UUID + original filename.
GET /file/{stored as}
    Download file by its stored UUID filename


How It Works
Files are stored under the data/ directory.
Each file is renamed with a UUID to prevent filename collisions.
A .json metadata file is created alongside each upload.
    Contains id (UUID), original_name, stored_as, size, and uploaded_at.
    Metadata follows the FileMeta Pydantic model for validation and consistency.
Mimetypes ensures downloads include the correct Content-Type header.


Notes:
    This is an MVP — no authentication or encryption yet.
    In production, you’d want:
        User accounts + JWT authentication
        Database for metadata (instead of JSON files)
        Cloud storage (AWS S3, GCP, Azure Blob)
        Access controls and auditing
        
