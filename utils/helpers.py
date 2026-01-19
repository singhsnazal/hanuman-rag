def safe_str(obj) -> str:
    try:
        return str(obj)
    except Exception:
        return "<unprintable>"
