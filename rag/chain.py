import time
from langsmith import traceable
from langchain_groq import ChatGroq

from rag.retriever import get_retriever
from rag.prompt import RAG_PROMPT
from rag.citations import format_docs_with_citations
from config import GROQ_API_KEY, LLM_MODEL, FINAL_K
from utils.logger import get_logger

logger = get_logger("rag_chain")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=LLM_MODEL,
    temperature=0.2
)

@traceable(name="hanuman_rag_answer")
def answer_question(question: str, session_id: str):
    start = time.time()
    logger.info(f"USER_QUERY: {question}")

    # ✅ PGVector: retriever uses session_id now
    retriever = get_retriever(session_id)

    # ✅ Retrieval time
    t1 = time.time()
    docs = retriever.invoke(question)
    retrieval_time = time.time() - t1
    logger.info(f"RETRIEVED_DOCS: {len(docs)} in {retrieval_time:.2f}s")

    # ✅ keep only best docs
    docs = docs[:FINAL_K]

    # ✅ contexts for RAGAS evaluation
    contexts = [d.page_content for d in docs]

    # ✅ build context for LLM
    context, sources = format_docs_with_citations(docs)
    logger.info(f"CONTEXT_LENGTH_CHARS: {len(context)}")

    # ✅ LLM time
    t2 = time.time()
    messages = RAG_PROMPT.format_messages(context=context, question=question)
    response = llm.invoke(messages).content
    llm_time = time.time() - t2
    logger.info(f"LLM_LATENCY: {llm_time:.2f}s")

    # ✅ Total time
    total = time.time() - start
    logger.info(f"TOTAL_LATENCY: {total:.2f}s")

    return response, sources, contexts
