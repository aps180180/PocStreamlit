"""
Gerenciador de autenticação e sessão
VERSÃO CORRIGIDA - Verifica permissões em tempo real
"""
import streamlit as st
from db.auth_models import (
    obter_usuario_por_login,
    atualizar_ultimo_login,
    verificar_permissao,
    listar_permissoes_usuario,
    registrar_audit_log,
    obter_usuario
)
from auth.password import verify_password

class AuthManager:
    """Classe para gerenciar autenticação e autorização"""
    
    @staticmethod
    def login(username: str, password: str) -> tuple[bool, str]:
        """Realiza login do usuário"""
        try:
            usuario = obter_usuario_por_login(username)
            
            if not usuario:
                return False, "Usuário ou senha inválidos"
            
            if usuario[7] != 'S':
                return False, "Usuário inativo. Contate o administrador."
            
            if not verify_password(password, usuario[4]):
                return False, "Usuário ou senha inválidos"
            
            # Criar sessão - APENAS DADOS BÁSICOS
            st.session_state.authenticated = True
            st.session_state.user_id = usuario[0]
            st.session_state.user_login = usuario[1]
            
            atualizar_ultimo_login(usuario[0])
            registrar_audit_log(usuario[0], "LOGIN", "SISTEMA", f"Login realizado: {username}")
            
            return True, "Login realizado com sucesso!"
            
        except Exception as e:
            return False, f"Erro ao realizar login: {str(e)}"
    
    @staticmethod
    def logout():
        """Realiza logout do usuário"""
        if 'user_id' in st.session_state:
            registrar_audit_log(
                st.session_state.user_id,
                "LOGOUT",
                "SISTEMA",
                f"Logout: {st.session_state.user_login}"
            )
        
        # Limpar TODA a sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def is_authenticated() -> bool:
        """Verifica se usuário está autenticado"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_user_id() -> int:
        """Retorna ID do usuário logado"""
        return st.session_state.get('user_id', None)
    
    @staticmethod
    def get_user_login() -> str:
        """Retorna login do usuário"""
        return st.session_state.get('user_login', 'Unknown')
    
    @staticmethod
    def get_user_name() -> str:
        """Retorna nome - BUSCA SEMPRE DO BANCO"""
        if not AuthManager.is_authenticated():
            return 'Usuário'
        
        try:
            user_id = AuthManager.get_user_id()
            usuario = obter_usuario(user_id)
            return usuario[2] if usuario else 'Usuário'
        except:
            return 'Usuário'
    
    @staticmethod
    def get_user_email() -> str:
        """Retorna email - BUSCA SEMPRE DO BANCO"""
        if not AuthManager.is_authenticated():
            return ''
        
        try:
            user_id = AuthManager.get_user_id()
            usuario = obter_usuario(user_id)
            return usuario[3] if (usuario and usuario[3]) else ''
        except:
            return ''
    
    @staticmethod
    def get_user_perfil() -> str:
        """Retorna perfil - BUSCA SEMPRE DO BANCO"""
        if not AuthManager.is_authenticated():
            return 'Sem perfil'
        
        try:
            user_id = AuthManager.get_user_id()
            usuario = obter_usuario(user_id)
            return usuario[5] if usuario else 'Sem perfil'
        except:
            return 'Sem perfil'
    
    @staticmethod
    def get_user_perfil_id() -> int:
        """Retorna ID do perfil - BUSCA SEMPRE DO BANCO"""
        if not AuthManager.is_authenticated():
            return None
        
        try:
            user_id = AuthManager.get_user_id()
            usuario = obter_usuario(user_id)
            return usuario[4] if usuario else None
        except:
            return None
    
    @staticmethod
    def is_user_active() -> bool:
        """Verifica se usuário está ativo - BUSCA SEMPRE DO BANCO"""
        if not AuthManager.is_authenticated():
            return False
        
        try:
            user_id = AuthManager.get_user_id()
            usuario = obter_usuario(user_id)
            return usuario[6] == 'S' if usuario else False
        except:
            return False
    
    @staticmethod
    def has_permission(modulo: str, acao: str) -> bool:
        """
        Verifica permissão - BUSCA SEMPRE DO BANCO EM TEMPO REAL
        CRÍTICO: Não usa cache!
        """
        if not AuthManager.is_authenticated():
            return False
        
        # Verificar se usuário ainda está ativo
        if not AuthManager.is_user_active():
            return False
        
        # BUSCAR PERMISSÃO DIRETO DO BANCO
        user_id = AuthManager.get_user_id()
        return verificar_permissao(user_id, modulo, acao)
    
    @staticmethod
    def get_user_permissions() -> list:
        """Retorna permissões - BUSCA SEMPRE DO BANCO"""
        if not AuthManager.is_authenticated():
            return []
        
        user_id = AuthManager.get_user_id()
        return listar_permissoes_usuario(user_id)
    
    @staticmethod
    def require_active_user():
        """
        Verifica se usuário ainda está ativo
        Se não estiver, faz logout forçado
        """
        if not AuthManager.is_authenticated():
            return
        
        if not AuthManager.is_user_active():
            st.error("❌ Sua conta foi desativada. Entre em contato com o administrador.")
            AuthManager.logout()
            st.switch_page("pages/00_Login.py")
            st.stop()
    
    @staticmethod
    def audit_log(acao: str, modulo: str = None, detalhes: str = None):
        """Registra ação no log de auditoria"""
        if AuthManager.is_authenticated():
            registrar_audit_log(
                AuthManager.get_user_id(),
                acao,
                modulo,
                detalhes
            )
