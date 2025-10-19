"""
Importações centralizadas de todos os models
"""
from db.models.cliente import Cliente
from db.models.produto import Produto
from db.models.usuario import Usuario
from db.models.perfil import Perfil
from db.models.permissao import Permissao
from db.models.log_auditoria import LogAuditoria

__all__ = [
    'Cliente',
    'Produto',
    'Usuario',
    'Perfil',
    'Permissao',
    'LogAuditoria'
]

def criar_todas_tabelas():
    """
    Cria todas as tabelas do sistema
    Ordem importa (foreign keys)
    """
    try:
        # 1. Tabelas independentes
        Cliente.criar_tabela()
        Produto.criar_tabela()
        Perfil.criar_tabela()
        
        # 2. Tabelas com FK
        Usuario.criar_tabela()
        Permissao.criar_tabela()
        LogAuditoria.criar_tabela()
        
        print("✅ Todas as tabelas criadas com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def migrar_tabelas():
    """Executa migrações necessárias"""
    try:
        Cliente.migrar_telefones()
        print("✅ Migrações executadas")
        return True
    except Exception as e:
        print(f"❌ Erro nas migrações: {e}")
        return False
