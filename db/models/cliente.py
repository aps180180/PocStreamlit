"""
Model de Cliente
Gerencia operações CRUD da tabela CLIENTES
"""
from db.base import BaseModel
from db.connection import get_db_cursor, execute_query

class Cliente(BaseModel):
    TABLE_NAME = "CLIENTES"
    
    @classmethod
    def criar_tabela(cls):
        """Cria tabela CLIENTES se não existir"""
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute("""
                    CREATE TABLE CLIENTES (
                        ID INTEGER NOT NULL PRIMARY KEY,
                        NOME VARCHAR(100) NOT NULL,
                        EMAIL VARCHAR(100),
                        TELEFONE1 VARCHAR(20),
                        TELEFONE2 VARCHAR(20)
                    )
                """)
                print("✅ Tabela CLIENTES criada")
        except Exception as e:
            print(f"ℹ️ Tabela CLIENTES já existe ou erro: {e}")
    
    @classmethod
    def migrar_telefones(cls):
        """Adiciona campos de telefone se não existirem"""
        with get_db_cursor(commit=True) as cursor:
            try:
                cursor.execute("ALTER TABLE CLIENTES ADD TELEFONE1 VARCHAR(20)")
                print("✅ Campo TELEFONE1 adicionado")
            except:
                pass
            
            try:
                cursor.execute("ALTER TABLE CLIENTES ADD TELEFONE2 VARCHAR(20)")
                print("✅ Campo TELEFONE2 adicionado")
            except:
                pass
    
    @classmethod
    def criar(cls, nome, email, telefone1=None, telefone2=None):
        """Cria novo cliente"""
        cliente_id = cls._get_next_id()
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO CLIENTES (ID, NOME, EMAIL, TELEFONE1, TELEFONE2)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente_id, nome, email, telefone1, telefone2))
        
        return cliente_id
    
    @classmethod
    def atualizar(cls, cliente_id, nome, email, telefone1=None, telefone2=None):
        """Atualiza cliente existente"""
        sql = """
            UPDATE CLIENTES 
            SET NOME = ?, EMAIL = ?, TELEFONE1 = ?, TELEFONE2 = ?
            WHERE ID = ?
        """
        execute_query(sql, (nome, email, telefone1, telefone2, cliente_id), commit=True)
    
    @classmethod
    def buscar(cls, busca="", tipo_busca="nome", limit=10, offset=0):
        """
        Busca clientes por nome ou código
        
        Args:
            busca: Termo de busca
            tipo_busca: "nome" ou "codigo"
            limit: Registros por página
            offset: Ponto de início
        """
        if tipo_busca == "nome":
            sql = """
                SELECT ID, NOME, EMAIL, TELEFONE1, TELEFONE2
                FROM CLIENTES
                WHERE UPPER(NOME) LIKE UPPER(?)
                ORDER BY NOME
                ROWS ? TO ?
            """
            params = (f'%{busca}%', offset + 1, offset + limit)
            return execute_query(sql, params)
        
        else:  # busca por código
            if not busca:
                # Se busca vazia, retorna todos
                return cls.find_all(limit, offset)
            
            try:
                # Validar se é número
                id_busca = int(busca)
                result = cls.find_by_id(id_busca)
                return [result] if result else []
            except ValueError:
                # Não é número, retorna vazio
                return []
    
    @classmethod
    def contar(cls, busca="", tipo_busca="nome"):
        """Conta clientes conforme filtro"""
        if tipo_busca == "nome":
            sql = "SELECT COUNT(*) FROM CLIENTES WHERE UPPER(NOME) LIKE UPPER(?)"
            params = (f'%{busca}%',)
            result = execute_query(sql, params, fetch_one=True)
            return result[0] if result else 0
        
        else:  # código
            if not busca:
                return cls.count_all()
            
            try:
                int(busca)
                return 1 if cls.exists(int(busca)) else 0
            except ValueError:
                return 0
