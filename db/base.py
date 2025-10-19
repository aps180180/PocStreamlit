"""
Classe base para todos os models
Fornece métodos CRUD comuns
"""
from db.connection import get_db_cursor, execute_query

class BaseModel:
    """
    Classe base para models com métodos comuns
    Cada model deve herdar desta classe e definir TABLE_NAME
    """
    
    TABLE_NAME = None  # Sobrescrever em cada model
    PRIMARY_KEY = "ID"
    
    @classmethod
    def _get_next_id(cls):
        """Retorna próximo ID disponível (Firebird não tem AUTO_INCREMENT)"""
        if not cls.TABLE_NAME:
            raise ValueError(f"TABLE_NAME não definido para {cls.__name__}")
        
        with get_db_cursor() as cursor:
            cursor.execute(f"SELECT COALESCE(MAX({cls.PRIMARY_KEY}), 0) + 1 FROM {cls.TABLE_NAME}")
            return cursor.fetchone()[0]
    
    @classmethod
    def find_by_id(cls, record_id):
        """Busca registro por ID"""
        if not cls.TABLE_NAME:
            raise ValueError(f"TABLE_NAME não definido para {cls.__name__}")
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE {cls.PRIMARY_KEY} = ?"
        return execute_query(sql, (record_id,), fetch_one=True)
    
    @classmethod
    def find_all(cls, limit=100, offset=0):
        """Lista todos registros com paginação"""
        if not cls.TABLE_NAME:
            raise ValueError(f"TABLE_NAME não definido para {cls.__name__}")
        
        sql = f"""
            SELECT * FROM {cls.TABLE_NAME} 
            ORDER BY {cls.PRIMARY_KEY} 
            ROWS ? TO ?
        """
        return execute_query(sql, (offset + 1, offset + limit))
    
    @classmethod
    def count_all(cls):
        """Conta total de registros"""
        if not cls.TABLE_NAME:
            raise ValueError(f"TABLE_NAME não definido para {cls.__name__}")
        
        sql = f"SELECT COUNT(*) FROM {cls.TABLE_NAME}"
        result = execute_query(sql, fetch_one=True)
        return result[0] if result else 0
    
    @classmethod
    def delete(cls, record_id):
        """Exclui registro por ID"""
        if not cls.TABLE_NAME:
            raise ValueError(f"TABLE_NAME não definido para {cls.__name__}")
        
        sql = f"DELETE FROM {cls.TABLE_NAME} WHERE {cls.PRIMARY_KEY} = ?"
        execute_query(sql, (record_id,), commit=True)
    
    @classmethod
    def exists(cls, record_id):
        """Verifica se registro existe"""
        return cls.find_by_id(record_id) is not None
