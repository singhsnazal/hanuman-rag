from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion.clean_text import clean_text
from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(docs):
    """
    Split documents into smaller chunks for embedding + retrieval.
    Uses RecursiveCharacterTextSplitter (best general splitter).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # clean docs before splitting
    for d in docs:
        d.page_content = clean_text(d.page_content)

    chunks = splitter.split_documents(docs)

    # Add chunk_id for traceability
    for i, c in enumerate(chunks):
        c.metadata["chunk_id"] = i

    return chunks
