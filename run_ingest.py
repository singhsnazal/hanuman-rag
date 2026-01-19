from ingestion.load_docs import load_documents
from ingestion.chunk_docs import chunk_documents
from ingestion.build_vectorstore import build_vectorstore
from config import DOCS_PATH

docs = load_documents(DOCS_PATH)
chunks = chunk_documents(docs)
build_vectorstore(chunks)

print("✅ Ingestion complete. Chroma DB saved.")
