"""
Model de Permissão
Gerencia permissões por perfil
"""
from db.base import BaseModel
from db.connection import get_db_cursor, execute_query

class Permissao(BaseModel):
    TABLE_NAME = "PERMISSOES"
    
    @classmethod
    def criar_tabela(cls):
        """Cria tabela PERMISSOES e insere permissões padrão"""
        try:
            with get_db_cursor(commit=True) as cursor:
                # Criar tabela
                cursor.execute("""
                    CREATE TABLE PERMISSOES (
                        ID INTEGER NOT NULL PRIMARY KEY,
                        PERFIL_ID INTEGER NOT NULL,
                        MODULO VARCHAR(50) NOT NULL,
                        ACAO VARCHAR(50) NOT NULL,
                        FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID)
                    )
                """)
                
                # Inserir permissões padrão
                cls._inserir_permissoes_padrao(cursor)
                
                print("✅ Tabela PERMISSOES criada com permissões padrão")
                
        except Exception as e:
            print(f"ℹ️ Tabela PERMISSOES já existe ou erro: {e}")
    
    @classmethod
    def _inserir_permissoes_padrao(cls, cursor):
        """Insere permissões padrão do sistema"""
        
        # Contador de ID
        perm_id = 1
        
        # VISUALIZADOR (ID=1) - Apenas visualizar
        visualizador_perms = [
            ('CLIENTES', 'VISUALIZAR'),
            ('CLIENTES', 'EXPORTAR'),
            ('PRODUTOS', 'VISUALIZAR'),
            ('PRODUTOS', 'EXPORTAR'),
        ]
        
        for modulo, acao in visualizador_perms:
            cursor.execute(
                "INSERT INTO PERMISSOES (ID, PERFIL_ID, MODULO, ACAO) VALUES (?, ?, ?, ?)",
                (perm_id, 1, modulo, acao)
            )
            perm_id += 1
        
        # OPERADOR (ID=2) - Visualizar + Criar + Editar
        operador_perms = [
            ('CLIENTES', 'VISUALIZAR'),
            ('CLIENTES', 'CRIAR'),
            ('CLIENTES', 'EDITAR'),
            ('CLIENTES', 'EXPORTAR'),
            ('PRODUTOS', 'VISUALIZAR'),
            ('PRODUTOS', 'CRIAR'),
            ('PRODUTOS', 'EDITAR'),
            ('PRODUTOS', 'EXPORTAR'),
        ]
        
        for modulo, acao in operador_perms:
            cursor.execute(
                "INSERT INTO PERMISSOES (ID, PERFIL_ID, MODULO, ACAO) VALUES (?, ?, ?, ?)",
                (perm_id, 2, modulo, acao)
            )
            perm_id += 1
        
        # ADMINISTRADOR (ID=3) - Todas as permissões
        admin_perms = [
            ('CLIENTES', 'VISUALIZAR'),
            ('CLIENTES', 'CRIAR'),
            ('CLIENTES', 'EDITAR'),
            ('CLIENTES', 'EXCLUIR'),
            ('CLIENTES', 'EXPORTAR'),
            ('PRODUTOS', 'VISUALIZAR'),
            ('PRODUTOS', 'CRIAR'),
            ('PRODUTOS', 'EDITAR'),
            ('PRODUTOS', 'EXCLUIR'),
            ('PRODUTOS', 'EXPORTAR'),
            ('USUARIOS', 'VISUALIZAR'),
            ('USUARIOS', 'CRIAR'),
            ('USUARIOS', 'EDITAR'),
            ('USUARIOS', 'DESATIVAR'),
            ('CONFIGURACOES', 'EDITAR'),
        ]
        
        for modulo, acao in admin_perms:
            cursor.execute(
                "INSERT INTO PERMISSOES (ID, PERFIL_ID, MODULO, ACAO) VALUES (?, ?, ?, ?)",
                (perm_id, 3, modulo, acao)
            )
            perm_id += 1
    
    @classmethod
    def buscar_por_perfil(cls, perfil_id):
        """Lista todas permissões de um perfil"""
        sql = """
            SELECT ID, MODULO, ACAO
            FROM PERMISSOES
            WHERE PERFIL_ID = ?
            ORDER BY MODULO, ACAO
        """
        return execute_query(sql, (perfil_id,))
    
    @classmethod
    def verificar_permissao(cls, perfil_id, modulo, acao):
        """Verifica se perfil tem permissão específica"""
        sql = """
            SELECT COUNT(*) 
            FROM PERMISSOES 
            WHERE PERFIL_ID = ? AND MODULO = ? AND ACAO = ?
        """
        result = execute_query(sql, (perfil_id, modulo, acao), fetch_one=True)
        return result[0] > 0 if result else False
    
    @classmethod
    def adicionar_permissao(cls, perfil_id, modulo, acao):
        """Adiciona nova permissão a um perfil"""
        perm_id = cls._get_next_id()
        
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO PERMISSOES (ID, PERFIL_ID, MODULO, ACAO) VALUES (?, ?, ?, ?)",
                (perm_id, perfil_id, modulo, acao)
            )
        
        return perm_id
    
    @classmethod
    def remover_permissao(cls, perfil_id, modulo, acao):
        """Remove permissão de um perfil"""
        sql = "DELETE FROM PERMISSOES WHERE PERFIL_ID = ? AND MODULO = ? AND ACAO = ?"
        execute_query(sql, (perfil_id, modulo, acao), commit=True)
