"""
Model de Usuario
Gerencia usuários do sistema
"""
from db.base import BaseModel
from db.connection import get_db_cursor, execute_query
from auth.password import hash_password

class Usuario(BaseModel):
    TABLE_NAME = "USUARIOS"
    
    @classmethod
    def criar_tabela(cls):
        """Cria tabela USUARIOS"""
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute("""
                    CREATE TABLE USUARIOS (
                        ID INTEGER NOT NULL PRIMARY KEY,
                        NOME VARCHAR(100) NOT NULL,
                        EMAIL VARCHAR(100) NOT NULL UNIQUE,
                        SENHA_HASH VARCHAR(255) NOT NULL,
                        PERFIL_ID INTEGER NOT NULL,
                        ATIVO INTEGER DEFAULT 1,
                        DATA_CRIACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID)
                    )
                """)
                print("✅ Tabela USUARIOS criada")
        except Exception as e:
            print(f"ℹ️ Tabela USUARIOS já existe ou erro: {e}")
    
    @classmethod
    def criar(cls, nome, email, senha, perfil_id):
        """Cria novo usuário"""
        usuario_id = cls._get_next_id()
        senha_hash = hash_password(senha)
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO USUARIOS (ID, NOME, EMAIL, SENHA_HASH, PERFIL_ID, ATIVO)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (usuario_id, nome, email, senha_hash, perfil_id))
        
        return usuario_id
    
    @classmethod
    def atualizar(cls, usuario_id, nome, email, perfil_id):
        """Atualiza usuário (sem senha)"""
        sql = """
            UPDATE USUARIOS 
            SET NOME = ?, EMAIL = ?, PERFIL_ID = ?
            WHERE ID = ?
        """
        execute_query(sql, (nome, email, perfil_id, usuario_id), commit=True)
    
    @classmethod
    def atualizar_senha(cls, usuario_id, nova_senha):
        """Atualiza apenas a senha"""
        senha_hash = hash_password(nova_senha)
        sql = "UPDATE USUARIOS SET SENHA_HASH = ? WHERE ID = ?"
        execute_query(sql, (senha_hash, usuario_id), commit=True)
    
    @classmethod
    def desativar(cls, usuario_id):
        """Desativa usuário (soft delete)"""
        sql = "UPDATE USUARIOS SET ATIVO = 0 WHERE ID = ?"
        execute_query(sql, (usuario_id,), commit=True)
    
    @classmethod
    def ativar(cls, usuario_id):
        """Ativa usuário"""
        sql = "UPDATE USUARIOS SET ATIVO = 1 WHERE ID = ?"
        execute_query(sql, (usuario_id,), commit=True)
    
    @classmethod
    def buscar_por_email(cls, email):
        """Busca usuário por email - CORRIGIDO para estrutura legada"""
        sql = """
        SELECT U.ID, U.NOME, U.EMAIL, U.SENHA_HASH, U.PERFIL_ID, 
        U.ATIVO, P.NOME as PERFIL_NOME
        FROM USUARIOS U
        INNER JOIN PERFIS P ON U.PERFIL_ID = P.ID
        WHERE UPPER(U.EMAIL) = UPPER(?)
        """
        return execute_query(sql, (email,), fetch_one=True)
    
    @classmethod
    def listar_todos(cls, apenas_ativos=False):
        """Lista todos usuários"""
        sql = """
            SELECT U.ID, U.NOME, U.EMAIL, U.PERFIL_ID, U.ATIVO, P.NOME as PERFIL_NOME
            FROM USUARIOS U
            INNER JOIN PERFIS P ON U.PERFIL_ID = P.ID
        """
        
        if apenas_ativos:
            sql += " WHERE U.ATIVO = 1"
        
        sql += " ORDER BY U.NOME"
        
        return execute_query(sql)
    
    @classmethod
    def buscar(cls, busca="", limit=10, offset=0):
        """Busca usuários por nome ou email"""
        sql = """
            SELECT U.ID, U.NOME, U.EMAIL, U.PERFIL_ID, U.ATIVO, P.NOME as PERFIL_NOME
            FROM USUARIOS U
            INNER JOIN PERFIS P ON U.PERFIL_ID = P.ID
            WHERE UPPER(U.NOME) LIKE UPPER(?) OR UPPER(U.EMAIL) LIKE UPPER(?)
            ORDER BY U.NOME
            ROWS ? TO ?
        """
        params = (f'%{busca}%', f'%{busca}%', offset + 1, offset + limit)
        return execute_query(sql, params)
    
    @classmethod
    def contar(cls, busca=""):
        """Conta usuários"""
        sql = """
            SELECT COUNT(*) 
            FROM USUARIOS 
            WHERE UPPER(NOME) LIKE UPPER(?) OR UPPER(EMAIL) LIKE UPPER(?)
        """
        result = execute_query(sql, (f'%{busca}%', f'%{busca}%'), fetch_one=True)
        return result[0] if result else 0
