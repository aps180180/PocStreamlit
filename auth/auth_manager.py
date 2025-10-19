"""
Gerenciador de Autenticação
ATUALIZADO: Usando novos models separados
"""
import streamlit as st
from db.models import Usuario, Permissao, LogAuditoria
from auth.password import verify_password

class AuthManager:
    """Gerenciador central de autenticação e permissões"""
    
    @staticmethod
    def login(email, senha):
        """
        Realiza login do usuário
        Retorna: (sucesso: bool, mensagem: str)
        """
        try:
            # Buscar usuário por email
            usuario = Usuario.buscar_por_email(email)
            
            if not usuario:
                return False, "❌ Email ou senha incorretos"
            
            # Verificar se está ativo
            if not usuario[5]:  # ATIVO
                return False, "❌ Usuário inativo. Contate o administrador."
            
            # Verificar senha
            if not verify_password(senha, usuario[3]):  # SENHA_HASH
                return False, "❌ Email ou senha incorretos"
            
            # Login bem-sucedido - salvar na sessão
            st.session_state.user_id = usuario[0]
            st.session_state.user_name = usuario[1]
            st.session_state.user_email = usuario[2]
            st.session_state.user_perfil_id = usuario[4]
            st.session_state.user_perfil_nome = usuario[6]
            st.session_state.authenticated = True
            
            # Registrar no log
            LogAuditoria.registrar(usuario[0], "LOGIN", "SISTEMA", f"Login realizado: {email}")
            
            return True, f"✅ Bem-vindo, {usuario[1]}!"
            
        except Exception as e:
            return False, f"❌ Erro ao fazer login: {str(e)}"
    
    @staticmethod
    def logout():
        """Realiza logout do usuário"""
        try:
            if 'user_id' in st.session_state:
                LogAuditoria.registrar(
                    st.session_state.user_id,
                    "LOGOUT",
                    "SISTEMA",
                    f"Logout: {st.session_state.user_email}"
                )
        except:
            pass
        
        # Limpar sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def is_authenticated():
        """Verifica se usuário está autenticado"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_user_id():
        """Retorna ID do usuário logado"""
        return st.session_state.get('user_id')
    
    @staticmethod
    def get_user_name():
        """Retorna nome do usuário logado"""
        return st.session_state.get('user_name', 'Desconhecido')
    
    @staticmethod
    def get_user_email():
        """Retorna email do usuário logado"""
        return st.session_state.get('user_email', '')
    
    @staticmethod
    def get_user_perfil():
        """Retorna nome do perfil do usuário"""
        return st.session_state.get('user_perfil_nome', 'Desconhecido')
    
    @staticmethod
    def get_user_perfil_id():
        """Retorna ID do perfil do usuário"""
        return st.session_state.get('user_perfil_id')
    
    @staticmethod
    def has_permission(modulo, acao):
        """
        Verifica se usuário tem permissão específica
        Args:
            modulo: Nome do módulo (ex: 'CLIENTES', 'PRODUTOS')
            acao: Ação desejada (ex: 'VISUALIZAR', 'CRIAR', 'EDITAR', 'EXCLUIR')
        """
        if not AuthManager.is_authenticated():
            return False
        
        perfil_id = AuthManager.get_user_perfil_id()
        
        try:
            return Permissao.verificar_permissao(perfil_id, modulo, acao)
        except:
            return False
    
    @staticmethod
    def audit_log(acao, modulo, detalhes=""):
        """
        Registra ação no log de auditoria
        Args:
            acao: Ação realizada (ex: 'CRIAR_CLIENTE')
            modulo: Módulo (ex: 'CLIENTES')
            detalhes: Detalhes adicionais
        """
        if not AuthManager.is_authenticated():
            return
        
        try:
            LogAuditoria.registrar(
                AuthManager.get_user_id(),
                acao,
                modulo,
                detalhes
            )
        except Exception as e:
            print(f"Erro ao registrar log: {e}")
    
    @staticmethod
    def require_auth():
        """Decorator helper - Redireciona para login se não autenticado"""
        if not AuthManager.is_authenticated():
            st.error("❌ Você precisa estar autenticado")
            st.info("Redirecionando para login...")
            st.switch_page("pages/00_Login.py")
            return False
        return True
