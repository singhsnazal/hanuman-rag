from rag.pgvector_store import get_vectorstore

def build_vectorstore(chunks, session_id: str):
    """
    Stores embeddings in Postgres pgvector (Render DB), per session.
    """
    vs = get_vectorstore(session_id)
    vs.add_documents(chunks)
    return vs
