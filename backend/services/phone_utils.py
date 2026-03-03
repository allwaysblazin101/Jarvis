def normalize_phone(phone: str):
    """
    Strips non-digit characters.
    Prevents +1 / 1 / formatting mismatches.
    """
    if not phone:
        return None

    return "".join(c for c in phone if c.isdigit())
