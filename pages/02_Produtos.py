"""
Módulo de Gestão de Produtos - PROTEGIDO
"""
import streamlit as st
import styles
from db.models import criar_tabelas
from db.auth_models import criar_tabelas_auth
import ui.produto as produto_ui
from config.empresa import SISTEMA_NOME
from auth.auth_manager import AuthManager

# Configuração da página
st.set_page_config(
    page_title=f"Gestão de Produtos - {SISTEMA_NOME}", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="📦"
)

# Verificar autenticação
if not AuthManager.is_authenticated():
    st.warning("⚠️ Você precisa fazer login")
    st.switch_page("pages/00_Login.py")
    st.stop()

# Verificar se usuário está ativo
AuthManager.require_active_user()

# Aplicar estilos e criar tabelas
styles.aplicar_estilos()
criar_tabelas()
criar_tabelas_auth()

# Renderizar conteúdo
produto_ui.tela_produto()
