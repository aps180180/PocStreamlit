"""
Model de Produto
Gerencia operações CRUD da tabela PRODUTOS
"""
from db.base import BaseModel
from db.connection import get_db_cursor, execute_query

class Produto(BaseModel):
    TABLE_NAME = "PRODUTOS"
    
    @classmethod
    def criar_tabela(cls):
        """Cria tabela PRODUTOS se não existir"""
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute("""
                    CREATE TABLE PRODUTOS (
                        ID INTEGER NOT NULL PRIMARY KEY,
                        NOME VARCHAR(100) NOT NULL,
                        PRECO DECIMAL(10,2) NOT NULL
                    )
                """)
                print("✅ Tabela PRODUTOS criada")
        except Exception as e:
            print(f"ℹ️ Tabela PRODUTOS já existe ou erro: {e}")
    
    @classmethod
    def criar(cls, nome, preco):
        """Cria novo produto"""
        produto_id = cls._get_next_id()
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO PRODUTOS (ID, NOME, PRECO)
                VALUES (?, ?, ?)
            """, (produto_id, nome, preco))
        
        return produto_id
    
    @classmethod
    def atualizar(cls, produto_id, nome, preco):
        """Atualiza produto existente"""
        sql = """
            UPDATE PRODUTOS 
            SET NOME = ?, PRECO = ?
            WHERE ID = ?
        """
        execute_query(sql, (nome, preco, produto_id), commit=True)
    
    @classmethod
    def buscar(cls, busca="", tipo_busca="nome", limit=10, offset=0):
        """Busca produtos por nome ou código"""
        if tipo_busca == "nome":
            sql = """
                SELECT ID, NOME, PRECO
                FROM PRODUTOS
                WHERE UPPER(NOME) LIKE UPPER(?)
                ORDER BY NOME
                ROWS ? TO ?
            """
            params = (f'%{busca}%', offset + 1, offset + limit)
            return execute_query(sql, params)
        
        else:  # código
            if not busca:
                return cls.find_all(limit, offset)
            
            try:
                id_busca = int(busca)
                result = cls.find_by_id(id_busca)
                return [result] if result else []
            except ValueError:
                return []
    
    @classmethod
    def contar(cls, busca="", tipo_busca="nome"):
        """Conta produtos conforme filtro"""
        if tipo_busca == "nome":
            sql = "SELECT COUNT(*) FROM PRODUTOS WHERE UPPER(NOME) LIKE UPPER(?)"
            params = (f'%{busca}%',)
            result = execute_query(sql, params, fetch_one=True)
            return result[0] if result else 0
        else:
            if not busca:
                return cls.count_all()
            try:
                int(busca)
                return 1 if cls.exists(int(busca)) else 0
            except ValueError:
                return 0
