"""
Decoradores para proteção de páginas e funções
"""
import streamlit as st
from functools import wraps
from auth.auth_manager import AuthManager

def require_auth(func):
    """
    Decorador que requer autenticação
    Redireciona para login se não autenticado
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not AuthManager.is_authenticated():
            st.warning("⚠️ Você precisa fazer login para acessar esta página")
            st.info("👉 Redirecionando para login...")
            st.switch_page("login.py")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_permission(modulo: str, acao: str, show_message=True):
    """
    Decorador que requer permissão específica
    
    Args:
        modulo (str): Nome do módulo
        acao (str): Nome da ação
        show_message (bool): Mostrar mensagem de erro
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not AuthManager.is_authenticated():
                if show_message:
                    st.error("❌ Você não está autenticado")
                return None
            
            if not AuthManager.has_permission(modulo, acao):
                if show_message:
                    st.error(f"❌ Você não tem permissão para: {modulo} - {acao}")
                    st.info(f"👤 Seu perfil: {AuthManager.get_user_perfil()}")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_permission(modulo: str, acao: str) -> bool:
    """
    Função helper para verificar permissão inline
    
    Uso:
        if check_permission('CLIENTES', 'CRIAR'):
            st.button("Adicionar Cliente")
    """
    return AuthManager.has_permission(modulo, acao)
