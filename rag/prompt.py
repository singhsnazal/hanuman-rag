from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.
Answer ONLY from the provided context.
If the context is insufficient, say: "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer in a clear way and include citations like [1], [2].
""")
