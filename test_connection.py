"""
Script para testar a conexão e inicializar o banco de dados
"""
import sys
from db.connection import test_connection
from db.models import criar_tabelas
from db.auth_models import criar_tabelas_auth

def main():
    print("="*60)
    print("SISTEMA CRUD - TESTE DE CONEXÃO E INICIALIZAÇÃO")
    print("="*60)
    print()
    
    # Passo 1: Testar conexão
    print("📡 Passo 1: Testando conexão com banco de dados...")
    if not test_connection():
        print()
        print("❌ FALHA: Não foi possível conectar ao banco de dados")
        print()
        print("Verifique:")
        print("  1. Firebird está rodando?")
        print("  2. Arquivo .fdb existe no caminho especificado?")
        print("  3. Credenciais corretas no config/empresa.py ou .env?")
        print("  4. Porta 3050 está aberta?")
        print()
        sys.exit(1)
    
    print()
    
    # Passo 2: Criar tabelas principais
    print("📦 Passo 2: Criando tabelas principais (Clientes, Produtos)...")
    try:
        criar_tabelas()
        print("✅ Tabelas principais criadas/verificadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas principais: {e}")
        sys.exit(1)
    
    print()
    
    # Passo 3: Criar tabelas de autenticação
    print("🔐 Passo 3: Criando tabelas de autenticação (Usuários, Perfis, Permissões)...")
    try:
        criar_tabelas_auth()
        print("✅ Tabelas de autenticação criadas/verificadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas de autenticação: {e}")
        sys.exit(1)
    
    print()
    print("="*60)
    print("✅ SETUP COMPLETO!")
    print("="*60)
    print()
    print("🎉 Banco de dados inicializado com sucesso!")
    print()
    print("📝 Credenciais padrão:")
    print("   Usuário: admin")
    #print("   Senha: admin123")
    print()
    print("⚠️  IMPORTANTE: Altere a senha após o primeiro acesso!")
    print()
    print("🚀 Para iniciar o sistema, execute:")
    print("   streamlit run login.py")
    print()
    print("="*60)

if __name__ == "__main__":
    main()
