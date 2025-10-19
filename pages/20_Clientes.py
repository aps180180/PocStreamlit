"""
Página de Gestão de Clientes - VERSÃO FINAL CORRIGIDA
"""
import streamlit as st
from auth.auth_manager import AuthManager
from utils.menu_builder import MenuBuilder
from utils.custom_css import apply_custom_css
import ui.cliente as cliente_ui

# Configuração da página
st.set_page_config(
    page_title="Gestão de Clientes",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS customizado
apply_custom_css()

# Verificar autenticação
if not AuthManager.is_authenticated():
    st.error("❌ Você precisa estar autenticado")
    st.switch_page("pages/00_Login.py")

# ========================================
# SIDEBAR COM MENU HIERÁRQUICO
# ========================================
with st.sidebar:
    st.markdown("## 🏢 Sistema ERP")
    st.markdown("---")
    
    # ✅ ÚNICA CHAMADA DO MENU
    MenuBuilder.build_sidebar_menu()
    
    st.markdown("---")
    st.markdown("### 👤 Usuário")
    st.info(f"**{AuthManager.get_user_name()}**")
    st.caption(f"🎭 {AuthManager.get_user_perfil()}")
    
    if st.button("🚪 Sair", use_container_width=True, type="secondary", key="btn_logout_clientes"):
        AuthManager.logout()
        st.switch_page("pages/00_Login.py")

# ========================================
# CONTEÚDO PRINCIPAL
# ========================================
cliente_ui.tela_cliente()
