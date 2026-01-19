from uuid import uuid4
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from rag.chain import answer_question

# ✅ ingestion modules
from ingestion.load_docs import load_single_pdf   # ✅ changed
from ingestion.clean_text import clean_documents
from ingestion.chunk_docs import chunk_documents
from ingestion.build_vectorstore import build_vectorstore


app = FastAPI(title="Hanuman God RAG - Web UI")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "web" / "templates"
STATIC_DIR = BASE_DIR / "web" / "static"

UPLOADS_ROOT = BASE_DIR / "uploads"
UPLOADS_ROOT.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    html_path = TEMPLATES_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


# ✅ 1) Create session id
@app.get("/session")
def create_session():
    session_id = str(uuid4())
    return {"session_id": session_id}


# ✅ 2) Upload pdf into that session
@app.post("/upload")
async def upload_pdf(
    session_id: str = Query(...),
    file: UploadFile = File(...)
):
    if not file.filename.lower().endswith(".pdf"):
        return JSONResponse({"error": "Only PDF files allowed"}, status_code=400)

    # create session folder
    session_upload_dir = UPLOADS_ROOT / session_id
    session_upload_dir.mkdir(parents=True, exist_ok=True)

    save_path = session_upload_dir / file.filename
    contents = await file.read()
    save_path.write_bytes(contents)

    try:
        # ✅ Load ONLY newly uploaded PDF (prevents duplicate indexing)
        docs = load_single_pdf(str(save_path))
        docs = clean_documents(docs)
        chunks = chunk_documents(docs)

        # ✅ store chunks in PGVector (Postgres) by session_id
        build_vectorstore(chunks, session_id=session_id)

        return {
            "message": f"Uploaded & indexed ✅ {file.filename}",
            "filename": file.filename,
            "session_id": session_id,
            "chunks_indexed": len(chunks)
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


class AskRequest(BaseModel):
    session_id: str
    question: str


# ✅ 3) Ask question from PGVector session DB
@app.post("/ask")
def ask(payload: AskRequest):
    q = payload.question
    sid = payload.session_id

    try:
        answer, sources, *_ = answer_question(q, session_id=sid)
        return {"question": q, "answer": answer, "sources": sources}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
from sqlalchemy import create_engine, text
from config import DATABASE_URL

@app.get("/debug_vectors")
def debug_vectors(session_id: str):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    collection = f"hanuman_session_{session_id}"

    with engine.connect() as conn:
        # all collections
        cols = conn.execute(text("SELECT name FROM langchain_pg_collection;")).fetchall()

        # count embeddings inside current collection
        count = conn.execute(text("""
            SELECT COUNT(*) 
            FROM langchain_pg_embedding e
            JOIN langchain_pg_collection c ON e.collection_id = c.uuid
            WHERE c.name = :collection
        """), {"collection": collection}).scalar()

    return {
        "collection": collection,
        "collections_in_db": [c[0] for c in cols],
        "embedding_count": int(count or 0)
    }
    
