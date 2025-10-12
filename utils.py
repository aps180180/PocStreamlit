import re

def validar_email(email: str) -> bool:
    padrão = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrão, email) is not None
