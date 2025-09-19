from typing import Annotated
from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from fastapi.responses import FileResponse
from pathlib import Path
import uuid, mimetypes, json, os

from app.models import FileMeta
from supabase_client import create_client

import datetime

app = FastAPI(title="Vault Lite", version="0.1.0")

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

#Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
if not supabase_url or not supabase_key:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables")
sb = create_client(supabase_url, supabase_key)

@app.get("/ping")
def ping():
    return {"ok": True, "msg": "pong!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    p = Path(file.filename)
    fid = uuid.uuid4().hex
    stored_name = f"{fid}{p.suffix}"
    dest = DATA_DIR / f"{fid}{p.suffix}"
    
    with dest.open("wb") as buffer:
        while True:
            chunk = await file.read(1024 * 1024)  # Read in 1 MB chunks
            if not chunk:
                break
            buffer.write(chunk)
    insert = {
        "original_name": file.filename,
        "stored_as": stored_name,
        "size": dest.stat().st_size,
        "content_type": file.content_type
    }
    res = sb.table("files").insert(insert).execute()
    if getattr(res, "error", None):
        try: dest.unlink(missing_ok=True)
        except Exception: pass
        raise HTTPException(status_code=500, detail="Failed to save file metadata")
    row = res.data[0] if res.data else {}
    upload_at = row.get("upload_at")
    if upload_at is None:
        upload_at = datetime.datetime.utcnow()

    meta = FileMeta(
        id=fid,
        original_name=file.filename,
        stored_as=dest.name,
        size=dest.stat().st_size,
        upload_at=upload_at
    )
    (DATA_DIR / f"{fid}.json").write_text(meta.json())
    return meta

@app.get("/list_files", response_model=list[FileMeta])
async def list_files():
    items: list[FileMeta] = []
    for meta_file in DATA_DIR.glob("*.json"):
        try:
            items.append(FileMeta.parse_file(meta_file))
        except Exception:
            continue
    items.sort(key=lambda x: x.upload_at, reverse=True)
    return items

@app.get("/file/{file_name}")
def get_file(file_name: str):
    file_path = DATA_DIR / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    ctype = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    return FileResponse(path=file_path, media_type=ctype, filename=file_name)


@app.delete("/file/{file_name}")
def delete_file(fid: str):
    meta_path = DATA_DIR / f"{fid}.json"
    if not meta_path.exists():
        raise HTTPException(status_code=404, detail="File metadata not found")
    meta = FileMeta.parse_file(meta_path)
    file_path = DATA_DIR / meta.stored_as
    file_path.unlink(missing_ok=True)
    meta_path.unlink(missing_ok=True)

    return Response(status_code=204)
