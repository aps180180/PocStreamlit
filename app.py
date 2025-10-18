"""
Sistema CRUD - Aplicação Principal
Verifica autenticação e redireciona para login se necessário
"""
import streamlit as st
import streamlit_antd_components as sac
import ui.dashboard as dashboard_ui
import styles
from db.models import criar_tabelas
from db.auth_models import criar_tabelas_auth
from auth.auth_manager import AuthManager
from datetime import datetime
from config.empresa import (
    SISTEMA_NOME,
    SISTEMA_VERSAO,
    SISTEMA_SUBTITULO
)

# Configuração da página
st.set_page_config(
    page_title=f"{SISTEMA_NOME} - Dashboard", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="📊",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': f"**{SISTEMA_NOME}** v{SISTEMA_VERSAO}\n\n{SISTEMA_SUBTITULO}"
    }
)

# VERIFICAR SE ESTÁ AUTENTICADO - Se não, redirecionar para login
if not AuthManager.is_authenticated():
    st.switch_page("pages/00_Login.py")
    st.stop()
# ADICIONAR ESTA VERIFICAÇÃO
AuthManager.require_active_user()
# Aplicar estilos
styles.aplicar_estilos()

# Criar tabelas do banco
criar_tabelas()
criar_tabelas_auth()

# Sidebar customizado
with st.sidebar:
    st.markdown(f"# 📊 {SISTEMA_NOME}")
    st.markdown(f"**{SISTEMA_SUBTITULO}**")
    st.caption(f"Versão {SISTEMA_VERSAO}")
    
    sac.divider(label='Usuário', icon='person-circle', align='center', color='blue')
    
    # Informações do usuário
    st.markdown(f"**👤 {AuthManager.get_user_name()}**")
    st.caption(f"🎭 Perfil: {AuthManager.get_user_perfil()}")
    st.caption(f"📧 {st.session_state.get('user_email', 'N/A')}")
    
    # Botão de logout
    if st.button("🚪 Sair do Sistema", use_container_width=True, type="secondary"):
        AuthManager.logout()
        st.success("✅ Logout realizado com sucesso!")
        st.switch_page("pages/00_Login.py")
    
    sac.divider(label='Sistema', icon='gear-fill', align='center', color='blue')
    
    # Informação
    st.info("👈 Use o menu de páginas para navegar entre os módulos do sistema")
    
    # Estatísticas rápidas (se tiver permissão)
    if AuthManager.has_permission('DASHBOARD', 'VISUALIZAR'):
        st.markdown("### 📈 Status")
        import db.models as db
        total_clientes = db.contar_clientes("", "nome")
        total_produtos = db.contar_produtos("", "nome")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Clientes", total_clientes)
        with col2:
            st.metric("Produtos", total_produtos)
    
    # Rodapé
    st.markdown("---")
    ano_atual = datetime.now().year
    st.caption(f"© {ano_atual} - Todos os direitos reservados")

# Conteúdo principal - Dashboard
dashboard_ui.tela_dashboard()
