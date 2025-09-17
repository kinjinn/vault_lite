from pydantic import BaseModel
from datetime import datetime
class FileMeta(BaseModel):
    id: str
    original_filename: str
    stored_as: str
    size: int
    upload_at: datetime
    
