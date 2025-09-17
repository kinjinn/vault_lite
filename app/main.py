from typing import Annotated
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os
import uuid, mimetypes, json

app = FastAPI(title="Vault Lite", version="0.1.0")

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/ping")
def ping():
    return {"ok": True, "msg": "pong!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    p = Path(file.filename)
    fid = uuid.uuid4().hex
    dest = DATA_DIR / f"{fid}{p.suffix}"
    
    with dest.open("wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)  # Read in 1 MB chunks
            if not chunk:
                break
            buffer.write(chunk)

    meta = {
        "id": fid,
        "original_name": file.filename,
        "stored_as": dest.name,
        "size": dest.stat().st_size
    }
    (DATA_DIR / f"{fid}.json").write_text(json.dumps(meta), encoding="utf-8")
    return {"saved as": dest.name, "size": meta["size"]}

@app.get("/list_files")
async def list_files():
    items = []
    for meta_file in DATA_DIR.glob("*.json"):
        try: 
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            items.append(data)
        except Exception:
            continue
    return {"files": items}

@app.get("/file/{file_name}")
def get_file(file_name: str):
    file_path = DATA_DIR / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    ctype = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return FileResponse(path=file_path, media_type=ctype, filename=file_name)

