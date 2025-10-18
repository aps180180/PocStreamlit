"""
Utilitários para criptografia de senhas
Usa PBKDF2 com SHA-256 para segurança
"""
import hashlib
import secrets

def hash_password(password: str) -> str:
    """
    Cria hash seguro da senha usando SHA-256 com salt
    
    Args:
        password (str): Senha em texto plano
        
    Returns:
        str: Hash da senha (salt + hash)
    """
    # Gerar salt aleatório de 16 bytes
    salt = secrets.token_hex(16)
    
    # Gerar hash usando PBKDF2
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # 100.000 iterações
    )
    
    # Retornar salt + hash concatenados
    return salt + pwd_hash.hex()

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica se a senha corresponde ao hash
    
    Args:
        password (str): Senha em texto plano
        hashed (str): Hash armazenado no banco
        
    Returns:
        bool: True se a senha está correta
    """
    if not hashed or len(hashed) < 32:
        return False
    
    # Extrair salt (primeiros 32 caracteres)
    salt = hashed[:32]
    stored_hash = hashed[32:]
    
    # Gerar hash da senha fornecida
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    
    # Comparar hashes
    return pwd_hash.hex() == stored_hash
