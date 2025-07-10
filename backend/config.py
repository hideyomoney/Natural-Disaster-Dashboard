import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
USERNAME = os.getenv("BSKY_USERNAME")
PASSWORD = os.getenv("BSKY_PASSWORD")


#print("[DEBUG] USERNAME:", os.getenv("BSKY_USERNAME"))
#print("[DEBUG] PASSWORD:", os.getenv("BSKY_PASSWORD"))
