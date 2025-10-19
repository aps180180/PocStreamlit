"""
Model de Perfil
Gerencia perfis de usuário (Visualizador, Operador, Admin)
"""
from db.base import BaseModel
from db.connection import get_db_cursor, execute_query

class Perfil(BaseModel):
    TABLE_NAME = "PERFIS"
    
    # Constantes de perfis
    VISUALIZADOR = 1
    OPERADOR = 2
    ADMINISTRADOR = 3
    
    @classmethod
    def criar_tabela(cls):
        """Cria tabela PERFIS e insere perfis padrão"""
        try:
            with get_db_cursor(commit=True) as cursor:
                # Criar tabela
                cursor.execute("""
                    CREATE TABLE PERFIS (
                        ID INTEGER NOT NULL PRIMARY KEY,
                        NOME VARCHAR(50) NOT NULL UNIQUE,
                        DESCRICAO VARCHAR(255)
                    )
                """)
                
                # Inserir perfis padrão
                perfis_padrao = [
                    (cls.VISUALIZADOR, 'Visualizador', 'Apenas visualização de dados'),
                    (cls.OPERADOR, 'Operador', 'Visualizar, criar e editar (sem excluir)'),
                    (cls.ADMINISTRADOR, 'Administrador', 'Acesso total ao sistema')
                ]
                
                for perfil_id, nome, descricao in perfis_padrao:
                    cursor.execute(
                        "INSERT INTO PERFIS (ID, NOME, DESCRICAO) VALUES (?, ?, ?)",
                        (perfil_id, nome, descricao)
                    )
                
                print("✅ Tabela PERFIS criada com perfis padrão")
                
        except Exception as e:
            print(f"ℹ️ Tabela PERFIS já existe ou erro: {e}")
    
    @classmethod
    def listar_todos(cls):
        """Lista todos os perfis"""
        sql = "SELECT ID, NOME, DESCRICAO FROM PERFIS ORDER BY ID"
        return execute_query(sql)
    
    @classmethod
    def obter_nome(cls, perfil_id):
        """Retorna nome do perfil"""
        perfil = cls.find_by_id(perfil_id)
        return perfil[1] if perfil else "Desconhecido"
