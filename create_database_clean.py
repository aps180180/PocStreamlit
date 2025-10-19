"""
Script para criar banco de dados do zero - ESTRUTURA LIMPA
Cria tudo corretamente sem tabelas antigas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.connection import get_connection
from auth.password import hash_password

def criar_banco_limpo():
    """Cria banco de dados do zero"""
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("\n" + "="*60)
        print("🏗️  CRIANDO BANCO DE DADOS DO ZERO")
        print("="*60 + "\n")
        
        # ========================================
        # 1. PERFIS
        # ========================================
        print("1️⃣ Criando tabela PERFIS...")
        print("-" * 60)
        
        cursor.execute("""
            CREATE TABLE PERFIS (
                ID INTEGER NOT NULL PRIMARY KEY,
                NOME VARCHAR(50) NOT NULL UNIQUE,
                DESCRICAO VARCHAR(255)
            )
        """)
        conn.commit()
        print("  ✅ Tabela PERFIS criada")
        
        # Inserir perfis
        perfis = [
            (1, 'Visualizador', 'Apenas visualização de dados'),
            (2, 'Operador', 'Visualizar, criar e editar (sem excluir)'),
            (3, 'Administrador', 'Acesso total ao sistema')
        ]
        
        for perfil_id, nome, desc in perfis:
            cursor.execute(
                "INSERT INTO PERFIS (ID, NOME, DESCRICAO) VALUES (?, ?, ?)",
                (perfil_id, nome, desc)
            )
            print(f"  ✅ Perfil {perfil_id}: {nome}")
        
        conn.commit()
        
        # ========================================
        # 2. USUARIOS
        # ========================================
        print("\n2️⃣ Criando tabela USUARIOS...")
        print("-" * 60)
        
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
        conn.commit()
        print("  ✅ Tabela USUARIOS criada")
        
        # Criar admin
        print("\n  👤 Criando usuário Administrador...")
        admin_senha_hash = hash_password("admin123")
        
        cursor.execute("""
            INSERT INTO USUARIOS (ID, NOME, EMAIL, SENHA_HASH, PERFIL_ID, ATIVO)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (1, "Administrador", "admin@sistema.com", admin_senha_hash, 3))
        
        conn.commit()
        print("  ✅ Admin criado")
        print("     📧 Email: admin@sistema.com")
        print("     🔑 Senha: admin123")
        print("     🎭 Perfil: Administrador (ID=3)")
        
        # ========================================
        # 3. PERMISSOES
        # ========================================
        print("\n3️⃣ Criando tabela PERMISSOES...")
        print("-" * 60)
        
        cursor.execute("""
            CREATE TABLE PERMISSOES (
                ID INTEGER NOT NULL PRIMARY KEY,
                PERFIL_ID INTEGER NOT NULL,
                MODULO VARCHAR(50) NOT NULL,
                ACAO VARCHAR(50) NOT NULL,
                FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID)
            )
        """)
        conn.commit()
        print("  ✅ Tabela PERMISSOES criada")
        
        # Inserir permissões
        print("\n  🔐 Inserindo permissões...")
        
        permissoes = []
        perm_id = 1
        
        # VISUALIZADOR (ID=1)
        for modulo, acao in [
            ('CLIENTES', 'VISUALIZAR'), ('CLIENTES', 'EXPORTAR'),
            ('PRODUTOS', 'VISUALIZAR'), ('PRODUTOS', 'EXPORTAR')
        ]:
            permissoes.append((perm_id, 1, modulo, acao))
            perm_id += 1
        
        # OPERADOR (ID=2)
        for modulo, acao in [
            ('CLIENTES', 'VISUALIZAR'), ('CLIENTES', 'CRIAR'), ('CLIENTES', 'EDITAR'), ('CLIENTES', 'EXPORTAR'),
            ('PRODUTOS', 'VISUALIZAR'), ('PRODUTOS', 'CRIAR'), ('PRODUTOS', 'EDITAR'), ('PRODUTOS', 'EXPORTAR')
        ]:
            permissoes.append((perm_id, 2, modulo, acao))
            perm_id += 1
        
        # ADMINISTRADOR (ID=3)
        for modulo, acao in [
            ('CLIENTES', 'VISUALIZAR'), ('CLIENTES', 'CRIAR'), ('CLIENTES', 'EDITAR'), ('CLIENTES', 'EXCLUIR'), ('CLIENTES', 'EXPORTAR'),
            ('PRODUTOS', 'VISUALIZAR'), ('PRODUTOS', 'CRIAR'), ('PRODUTOS', 'EDITAR'), ('PRODUTOS', 'EXCLUIR'), ('PRODUTOS', 'EXPORTAR'),
            ('USUARIOS', 'VISUALIZAR'), ('USUARIOS', 'CRIAR'), ('USUARIOS', 'EDITAR'), ('USUARIOS', 'DESATIVAR'),
            ('CONFIGURACOES', 'EDITAR')
        ]:
            permissoes.append((perm_id, 3, modulo, acao))
            perm_id += 1
        
        for p_id, perfil_id, modulo, acao in permissoes:
            cursor.execute(
                "INSERT INTO PERMISSOES (ID, PERFIL_ID, MODULO, ACAO) VALUES (?, ?, ?, ?)",
                (p_id, perfil_id, modulo, acao)
            )
        
        conn.commit()
        print(f"  ✅ {len(permissoes)} permissões inseridas")
        print("     • Visualizador: 4 permissões")
        print("     • Operador: 8 permissões")
        print("     • Administrador: 15 permissões")
        
        # ========================================
        # 4. LOG_AUDITORIA
        # ========================================
        print("\n4️⃣ Criando tabela LOG_AUDITORIA...")
        print("-" * 60)
        
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
        conn.commit()
        print("  ✅ Tabela LOG_AUDITORIA criada")
        
        # ========================================
        # 5. CLIENTES
        # ========================================
        print("\n5️⃣ Criando tabela CLIENTES...")
        print("-" * 60)
        
        cursor.execute("""
            CREATE TABLE CLIENTES (
                ID INTEGER NOT NULL PRIMARY KEY,
                NOME VARCHAR(100) NOT NULL,
                EMAIL VARCHAR(100),
                TELEFONE1 VARCHAR(20),
                TELEFONE2 VARCHAR(20)
            )
        """)
        conn.commit()
        print("  ✅ Tabela CLIENTES criada")
        
        # Dados de exemplo
        clientes = [
            (1, "João Silva", "joao@email.com", "(11) 98888-7777", "(11) 3333-4444"),
            (2, "Maria Santos", "maria@email.com", "(11) 99999-8888", None),
            (3, "Pedro Oliveira", "pedro@email.com", None, "(11) 2222-3333"),
        ]
        
        for cli_id, nome, email, tel1, tel2 in clientes:
            cursor.execute(
                "INSERT INTO CLIENTES (ID, NOME, EMAIL, TELEFONE1, TELEFONE2) VALUES (?, ?, ?, ?, ?)",
                (cli_id, nome, email, tel1, tel2)
            )
            print(f"  ✅ Cliente: {nome}")
        
        conn.commit()
        
        # ========================================
        # 6. PRODUTOS
        # ========================================
        print("\n6️⃣ Criando tabela PRODUTOS...")
        print("-" * 60)
        
        cursor.execute("""
            CREATE TABLE PRODUTOS (
                ID INTEGER NOT NULL PRIMARY KEY,
                NOME VARCHAR(100) NOT NULL,
                PRECO DECIMAL(10,2) NOT NULL
            )
        """)
        conn.commit()
        print("  ✅ Tabela PRODUTOS criada")
        
        # Dados de exemplo
        produtos = [
            (1, "Notebook Dell Inspiron", 3500.00),
            (2, "Mouse Logitech MX Master", 450.00),
            (3, "Teclado Mecânico Keychron", 650.00),
        ]
        
        for prod_id, nome, preco in produtos:
            cursor.execute(
                "INSERT INTO PRODUTOS (ID, NOME, PRECO) VALUES (?, ?, ?)",
                (prod_id, nome, preco)
            )
            print(f"  ✅ Produto: {nome}")
        
        conn.commit()
        
        # ========================================
        # RESUMO FINAL
        # ========================================
        print("\n" + "="*60)
        print("✅ BANCO DE DADOS CRIADO COM SUCESSO!")
        print("="*60)
        
        print("\n📊 Estrutura criada:")
        print("  ✅ PERFIS (3 perfis)")
        print("  ✅ USUARIOS (1 admin)")
        print("  ✅ PERMISSOES (27 permissões)")
        print("  ✅ LOG_AUDITORIA")
        print("  ✅ CLIENTES (3 exemplos)")
        print("  ✅ PRODUTOS (3 exemplos)")
        
        print("\n🔐 Credenciais de acesso:")
        print("  📧 Email: admin@sistema.com")
        print("  🔑 Senha: admin123")
        print("  🎭 Perfil: Administrador (acesso total)")
        
        print("\n🚀 Execute agora:")
        print("  streamlit run app.py\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def main():
    print("\n" + "="*60)
    print("🏗️  CRIAÇÃO DE BANCO DE DADOS DO ZERO")
    print("="*60)
    print("\n📝 Este script vai criar toda a estrutura limpa")
    print("   com a nova arquitetura de models separados.\n")
    
    resposta = input("Continuar? (digite SIM): ")
    
    if resposta == "SIM":
        print("\n✅ Iniciando criação...\n")
        return 0 if criar_banco_limpo() else 1
    else:
        print("\n❌ Cancelado\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
