"""
Módulo de Gestão de Usuários - ADMIN ONLY
Requer permissão de administrador
"""
import streamlit as st
import streamlit_antd_components as sac
import styles
from db.auth_models import criar_tabelas_auth
from datetime import datetime
import ui.usuarios as usuarios_ui
from config.empresa import SISTEMA_NOME, SISTEMA_VERSAO
from auth.auth_manager import AuthManager
from auth.decorators import require_auth

# Configuração da página
st.set_page_config(
    page_title=f"Gestão de Usuários - {SISTEMA_NOME}", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="👥"
)

# Verificar autenticação
if not AuthManager.is_authenticated():
    st.warning("⚠️ Você precisa fazer login para acessar esta página")
    st.info("👉 Redirecionando para login...")
    st.switch_page("pages/00_Login.py")
    st.stop()

# Aplicar estilos
styles.aplicar_estilos()

# Criar tabelas
criar_tabelas_auth()

# Sidebar customizado
with st.sidebar:
    st.markdown(f"# 📊 {SISTEMA_NOME}")
    st.markdown(f"**Administração**")
    st.caption(f"Versão {SISTEMA_VERSAO}")
    
    # Informações do usuário
    sac.divider(label='Usuário', icon='person-circle', align='center', color='red')
    st.markdown(f"**👤 {AuthManager.get_user_name()}**")
    st.caption(f"🎭 {AuthManager.get_user_perfil()}")
    
    # Botão de logout
    if st.button("🚪 Sair", use_container_width=True, type="secondary"):
        AuthManager.logout()
        st.switch_page("pages/00_Login.py")
    
    sac.divider(label='Navegação Rápida', icon='compass', align='center', color='red')
    
    # Botões de navegação
    st.markdown("### 🔗 Ir para:")
    
    if st.button("🏠 Dashboard", use_container_width=True, type="secondary"):
        st.switch_page("app.py")
    
    if st.button("👥 Clientes", use_container_width=True, type="secondary"):
        st.switch_page("pages/01_Clientes.py")
    
    if st.button("📦 Produtos", use_container_width=True, type="secondary"):
        st.switch_page("pages/02_Produtos.py")
    
    # Estatísticas
    st.markdown("---")
    st.markdown("### 📊 Sistema")
    
    from db.auth_models import contar_usuarios
    total_usuarios = contar_usuarios("", "nome")
    st.metric("Usuários Cadastrados", total_usuarios)
    
    # Rodapé
    st.markdown("---")
    ano_atual = datetime.now().year
    st.caption(f"© {ano_atual} - Todos os direitos reservados")

# Conteúdo principal - Verificar permissão de administrador
@require_auth
def main():
    if not AuthManager.has_permission('USUARIOS', 'VISUALIZAR'):
        st.error("❌ Acesso Negado")
        st.warning("⚠️ Esta página é restrita a administradores")
        st.info(f"👤 Seu perfil atual: **{AuthManager.get_user_perfil()}**")
        st.info("💡 Apenas usuários com perfil **Administrador** podem acessar a gestão de usuários")
        return
    
    # Registrar acesso no log
    AuthManager.audit_log("ACESSOU_ADMIN", "USUARIOS", "Acessou página de administração de usuários")
    
    # Renderizar tela de usuários
    usuarios_ui.tela_usuarios()

main()
