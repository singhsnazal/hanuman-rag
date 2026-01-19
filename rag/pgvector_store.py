from langchain_postgres import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import DATABASE_URL

COLLECTION_PREFIX = "hanuman_session_"

def get_embeddings():
    """
    Render-safe embeddings (no Ollama required).
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_vectorstore(session_id: str):
    """
    One session = one collection in Postgres.
    """
    return PGVector(
        connection=DATABASE_URL,
        embeddings=get_embeddings(),
        collection_name=f"{COLLECTION_PREFIX}{session_id}",
    )
