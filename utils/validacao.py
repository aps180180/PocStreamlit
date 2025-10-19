import re

def validar_email(email):
    """Valida formato de email"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_telefone(telefone):
    """
    Valida e formata telefone brasileiro
    Aceita: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    """
    if not telefone:
        return True  # Telefone é opcional
    
    # Remover caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    
    # Telefone deve ter 10 ou 11 dígitos
    if len(numeros) not in [10, 11]:
        return False
    
    return True

def formatar_telefone(telefone):
    """
    Formata telefone brasileiro
    (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    """
    if not telefone:
        return ""
    
    # Remover caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    
    return telefone
