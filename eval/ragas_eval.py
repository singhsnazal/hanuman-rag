from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, _ContextRelevance
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings

from config import GROQ_API_KEY, EMBEDDING_MODEL
from rag.chain import answer_question

# ✅ Groq as Judge LLM
judge_llm = LangchainLLMWrapper(
    ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )
)

# ✅ Ollama embeddings as Judge embeddings (instead of OpenAIEmbeddings)
judge_embeddings = LangchainEmbeddingsWrapper(
    OllamaEmbeddings(model=EMBEDDING_MODEL)  # embeddinggemma:latest
)

context_relevance = _ContextRelevance()

questions = [
    "What is my full name as written in resume?",
    "Which year did I complete MCA and from which university?",
    "Trick question: What is my date of birth?"
]

data = {"question": [], "answer": [], "contexts": []}

for q in questions:
    answer, sources, contexts = answer_question(q)
    data["question"].append(q)
    data["answer"].append(answer)
    data["contexts"].append(contexts)

dataset = Dataset.from_dict(data)

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_relevance],
    llm=judge_llm,                 # ✅ Groq judge
    embeddings=judge_embeddings     # ✅ Ollama embeddings judge
)

print(result)
