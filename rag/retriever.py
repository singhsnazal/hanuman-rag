from config import TOP_K
from rag.pgvector_store import get_vectorstore

def get_retriever(session_id: str):
    vs = get_vectorstore(session_id)
    return vs.as_retriever(search_kwargs={"k": TOP_K})



