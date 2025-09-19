import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # reads .env from project root

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")

supabase: Client = create_client(url, key)