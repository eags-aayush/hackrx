import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

VECTOR_INDEX_PATH = "vector_store/faiss_index/index"

UPLOAD_DIR = "data/uploads"
CHUNK_DIR = "data/processed"
