"""
Página de Login
"""
import streamlit as st
from auth.auth_manager import AuthManager
from utils.custom_css import apply_login_css

st.set_page_config(
    page_title="Login - Sistema ERP",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"  # ✅ FECHADA no login
)

# CSS específico do login
apply_login_css()

# Verificar se já está logado
if AuthManager.is_authenticated():
    st.switch_page("app.py")

st.markdown("# 🔐 Login")
st.markdown("### Sistema ERP")

with st.form("login_form"):
    email = st.text_input("📧 Email", placeholder="seu@email.com")
    senha = st.text_input("🔑 Senha", type="password", placeholder="Sua senha")
    
    col1, col2 = st.columns(2)
    
    with col1:
        submit = st.form_submit_button("🚀 Entrar", use_container_width=True, type="primary")
    
    with col2:
        st.form_submit_button("❌ Limpar", use_container_width=True)
    
    if submit:
        if email and senha:
            sucesso, mensagem = AuthManager.login(email, senha)
            
            if sucesso:
                st.success(mensagem)
                st.balloons()
                
                import time
                time.sleep(1)
                st.switch_page("app.py")
            else:
                st.error(mensagem)
        else:
            st.warning("⚠️ Preencha email e senha")

st.markdown("---")
st.info("💡 **Credenciais padrão:**\n\n📧 admin@sistema.com\n\n🔑 admin123")
