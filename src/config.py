import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# =========================
# API Keys
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TOP_K = 5

# =========================
# LLM Configuration
# =========================
LLM_MODEL = "llama-3.3-70b-versatile"

# =========================
# Embedding Model
# =========================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# =========================
# Text Splitting
# =========================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# =========================
# Vector Database
# =========================
CHROMA_DB_PATH = "chroma_db"