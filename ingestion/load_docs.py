from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


def load_documents(folder_path: str):
    """
    Loads all PDFs from a folder and returns LangChain Documents.
    Adds metadata (source filename).
    """
    docs = []
    folder = Path(folder_path)

    for pdf_path in folder.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        loaded = loader.load()

        for d in loaded:
            d.metadata["source"] = pdf_path.name

        docs.extend(loaded)

    return docs


def load_single_pdf(pdf_path: str):
    """
    Loads a single PDF file and returns LangChain Documents.
    Adds metadata (source filename).
    """
    pdf_path = Path(pdf_path)

    loader = PyPDFLoader(str(pdf_path))
    docs = loader.load()

    for d in docs:
        d.metadata["source"] = pdf_path.name

    return docs
