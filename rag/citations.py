def format_docs_with_citations(docs):
    """
    Converts docs into a context string with citation markers [1], [2], etc.
    Returns (context_text, sources_list)
    """
    context_parts = []
    sources = []

    for idx, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", "NA")
        sources.append(f"[{idx}] {src} (page {page})")

        context_parts.append(f"[{idx}] {d.page_content}")

    context = "\n\n".join(context_parts)
    return context, sources
