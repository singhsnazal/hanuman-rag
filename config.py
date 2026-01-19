import os
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_PATH = os.path.join(BASE_DIR, "data", "raw_docs")
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")  # (old - not used after pgvector)

# ✅ Database (Render Postgres + pgvector)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL missing. Add it to .env file.")

# Embedding model (Ollama local)
EMBEDDING_MODEL = "embeddinggemma:latest"

# LLM (Groq)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.3-70b-versatile"

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

# Retrieval tuning
TOP_K = 10          # fetch these many docs first
FINAL_K = 5         # keep these docs for final context
ENABLE_RERANK = False  # enable later if you want

# Validation
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY missing. Add it to .env file.")

# LangSmith (optional observability)
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "hanuman_god_rag")
