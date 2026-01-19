import re

def clean_text(text: str) -> str:
    """
    Cleans PDF extracted text to improve chunking + embeddings quality.
    """
    text = text.replace("\x00", "")        # remove null chars
    text = re.sub(r"\s+", " ", text)       # collapse multiple spaces/newlines
    return text.strip()

def clean_documents(docs):
    """
    Cleans list of LangChain Document objects.
    """
    for d in docs:
        d.page_content = clean_text(d.page_content)
    return docs
