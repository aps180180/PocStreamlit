"""
Gerenciador centralizado de conexões com banco de dados Firebird
"""
import fdb
from contextlib import contextmanager
from config.empresa import BANCO_HOST, BANCO_CAMINHO, BANCO_USER, BANCO_PASSWORD

# Pool de configurações (singleton)
_connection_config = {
    'host': BANCO_HOST,
    'database': BANCO_CAMINHO,
    'user': BANCO_USER,
    'password': BANCO_PASSWORD,
    'charset': 'UTF8'
}

def get_connection():
    """
    Retorna uma conexão com o banco de dados
    
    Returns:
        fdb.Connection: Conexão ativa com o banco
        
    Raises:
        ConnectionError: Se não conseguir conectar
    """
    try:
        return fdb.connect(**_connection_config)
    except Exception as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {e}")

@contextmanager
def get_db_connection():
    """
    Context manager para conexão com auto-close
    
    Uso:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CLIENTES")
            results = cursor.fetchall()
            cursor.close()
            
    Garante que a conexão será fechada mesmo em caso de erro
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager para cursor com auto-close e commit opcional
    
    Args:
        commit (bool): Se True, faz commit automaticamente ao final
        
    Uso:
        # SELECT
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM CLIENTES")
            results = cursor.fetchall()
        
        # INSERT/UPDATE/DELETE
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("INSERT INTO CLIENTES (NOME) VALUES (?)", ("João",))
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def execute_query(sql, params=None, fetch_one=False, fetch_all=True, commit=False):
    """
    Executa query de forma simplificada
    
    Args:
        sql (str): Query SQL
        params (tuple): Parâmetros da query
        fetch_one (bool): Retorna apenas um registro
        fetch_all (bool): Retorna todos os registros
        commit (bool): Faz commit após execução
        
    Returns:
        list/tuple/None: Resultado da query
        
    Exemplos:
        # SELECT um registro
        cliente = execute_query("SELECT * FROM CLIENTES WHERE ID = ?", (1,), fetch_one=True)
        
        # SELECT múltiplos registros
        clientes = execute_query("SELECT * FROM CLIENTES")
        
        # INSERT/UPDATE/DELETE
        execute_query("INSERT INTO CLIENTES (NOME) VALUES (?)", ("João",), commit=True)
        
        # COUNT
        total = execute_query("SELECT COUNT(*) FROM CLIENTES", fetch_one=True)[0]
    """
    with get_db_cursor(commit=commit) as cursor:
        cursor.execute(sql, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all and not commit:
            return cursor.fetchall()
        
        return None

def test_connection():
    """
    Testa conexão com o banco de dados
    
    Returns:
        bool: True se conexão bem sucedida, False caso contrário
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM RDB$DATABASE")
            cursor.fetchone()
            cursor.close()
        print("✅ Conexão com banco de dados OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco de dados: {e}")
        return False
