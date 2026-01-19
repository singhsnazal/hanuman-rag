from langchain_postgres import PGVector
from langchain_community.embeddings import OllamaEmbeddings
from config import DATABASE_URL, EMBEDDING_MODEL

COLLECTION_PREFIX = "hanuman_session_"

def get_embeddings():
    return OllamaEmbeddings(model=EMBEDDING_MODEL)

def get_vectorstore(session_id: str):
    """
    One session = one collection in Postgres.
    """
    return PGVector(
        connection=DATABASE_URL,
        embeddings=get_embeddings(),
        collection_name=f"{COLLECTION_PREFIX}{session_id}",
    )
