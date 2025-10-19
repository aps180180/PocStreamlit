"""
Model de Log de Auditoria
Registra ações dos usuários
"""
from db.base import BaseModel
from db.connection import get_db_cursor, execute_query
from datetime import datetime

class LogAuditoria(BaseModel):
    TABLE_NAME = "LOG_AUDITORIA"
    
    @classmethod
    def criar_tabela(cls):
        """Cria tabela LOG_AUDITORIA"""
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute("""
                    CREATE TABLE LOG_AUDITORIA (
                        ID INTEGER NOT NULL PRIMARY KEY,
                        USUARIO_ID INTEGER,
                        ACAO VARCHAR(100),
                        MODULO VARCHAR(50),
                        DETALHES VARCHAR(500),
                        DATA_HORA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (USUARIO_ID) REFERENCES USUARIOS(ID)
                    )
                """)
                print("✅ Tabela LOG_AUDITORIA criada")
        except Exception as e:
            print(f"ℹ️ Tabela LOG_AUDITORIA já existe ou erro: {e}")
    
    @classmethod
    def registrar(cls, usuario_id, acao, modulo, detalhes=""):
        """Registra ação no log"""
        log_id = cls._get_next_id()
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("""
                INSERT INTO LOG_AUDITORIA (ID, USUARIO_ID, ACAO, MODULO, DETALHES)
                VALUES (?, ?, ?, ?, ?)
            """, (log_id, usuario_id, acao, modulo, detalhes))
        
        return log_id
    
    @classmethod
    def listar_por_usuario(cls, usuario_id, limit=50):
        """Lista logs de um usuário específico"""
        sql = """
            SELECT ID, ACAO, MODULO, DETALHES, DATA_HORA
            FROM LOG_AUDITORIA
            WHERE USUARIO_ID = ?
            ORDER BY DATA_HORA DESC
            ROWS 1 TO ?
        """
        return execute_query(sql, (usuario_id, limit))
    
    @classmethod
    def listar_por_modulo(cls, modulo, limit=50):
        """Lista logs de um módulo específico"""
        sql = """
            SELECT L.ID, L.USUARIO_ID, U.NOME, L.ACAO, L.DETALHES, L.DATA_HORA
            FROM LOG_AUDITORIA L
            LEFT JOIN USUARIOS U ON L.USUARIO_ID = U.ID
            WHERE L.MODULO = ?
            ORDER BY L.DATA_HORA DESC
            ROWS 1 TO ?
        """
        return execute_query(sql, (modulo, limit))
    
    @classmethod
    def listar_recentes(cls, limit=100):
        """Lista logs mais recentes (todos os usuários)"""
        sql = """
            SELECT L.ID, L.USUARIO_ID, U.NOME as USUARIO_NOME, 
                   L.ACAO, L.MODULO, L.DETALHES, L.DATA_HORA
            FROM LOG_AUDITORIA L
            LEFT JOIN USUARIOS U ON L.USUARIO_ID = U.ID
            ORDER BY L.DATA_HORA DESC
            ROWS 1 TO ?
        """
        return execute_query(sql, (limit,))
