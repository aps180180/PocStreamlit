"""
Página de Administração de Usuários - VERSÃO FINAL CORRIGIDA
"""
import streamlit as st
from auth.auth_manager import AuthManager
from utils.menu_builder import MenuBuilder
from utils.custom_css import apply_custom_css
import ui.usuarios as usuarios_ui

# Configuração da página
st.set_page_config(
    page_title="Administração de Usuários",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar CSS customizado
apply_custom_css()

# Verificar autenticação
if not AuthManager.is_authenticated():
    st.error("❌ Você precisa estar autenticado")
    st.switch_page("pages/00_Login.py")

# Verificar permissão (apenas Admin)
if not AuthManager.has_permission('USUARIOS', 'VISUALIZAR'):
    st.error("❌ Sem permissão para acessar esta página")
    st.info(f"Seu perfil: {AuthManager.get_user_perfil()}")
    st.stop()

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
    
    if st.button("🚪 Sair", use_container_width=True, type="secondary", key="btn_logout_usuarios"):
        AuthManager.logout()
        st.switch_page("pages/00_Login.py")

# ========================================
# CONTEÚDO PRINCIPAL
# ========================================
usuarios_ui.tela_usuarios()
