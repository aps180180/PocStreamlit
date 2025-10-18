"""
Página de Login do Sistema
"""
import streamlit as st
import streamlit_antd_components as sac
from auth.auth_manager import AuthManager
from config.empresa import SISTEMA_NOME, SISTEMA_VERSAO, SISTEMA_SUBTITULO
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title=f"Login - {SISTEMA_NOME}",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para página de login
st.markdown("""
<style>
    /* Ocultar menu e header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ocultar sidebar na página de login */
    [data-testid="stSidebar"] {display: none;}
    
    /* Centralizar conteúdo */
    .block-container {
        padding-top: 2rem;
        max-width: 500px;
    }
</style>
""", unsafe_allow_html=True)

# Verificar se já está autenticado
if AuthManager.is_authenticated():
    st.success("✅ Você já está logado!")
    st.info("👉 Redirecionando para o dashboard...")
    st.switch_page("app.py")
    st.stop()

# Container principal
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Logo/Título
    st.markdown(f"<h1 style='text-align: center;'>🔐</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{SISTEMA_NOME}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #666;'>{SISTEMA_SUBTITULO}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #999; font-size: 0.8rem;'>v{SISTEMA_VERSAO}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Formulário de login
    with st.form("login_form"):
        st.markdown("#### 🔑 Acesso ao Sistema")
        
        username = st.text_input(
            "Usuário",
            placeholder="Digite seu usuário",
            help="Use 'admin' para primeiro acesso"
        )
        
        password = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite sua senha",
            help="Use 'admin123' para primeiro acesso"
        )
        
        remember = st.checkbox("Lembrar-me neste dispositivo", value=False)
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            submit = st.form_submit_button(
                "🚀 Entrar",
                use_container_width=True,
                type="primary"
            )
        
        with col_btn2:
            if st.form_submit_button(
                "❌ Limpar",
                use_container_width=True
            ):
                st.rerun()
    
    # Processar login
    if submit:
        if not username or not password:
            st.error("❌ Preencha usuário e senha")
        else:
            with st.spinner("🔄 Autenticando..."):
                success, message = AuthManager.login(username, password)
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                    st.info("👉 Redirecionando para o dashboard...")
                    st.switch_page("app.py")
                else:
                    st.error(f"❌ {message}")
    
    st.markdown("---")
    
    # Informações adicionais
    with st.expander("ℹ️ Primeiro Acesso"):
        st.markdown("""
        **Credenciais padrão:**
        - **Usuário:** admin
        - **Senha:** admin123
        
        ⚠️ **Importante:** Altere a senha após o primeiro acesso!
        """)
    
    with st.expander("🆘 Esqueci minha senha"):
        st.info("Entre em contato com o administrador do sistema")
    
    # Rodapé
    st.markdown("---")
    ano_atual = datetime.now().year
    st.markdown(
        f"<p style='text-align: center; color: #999; font-size: 0.8rem;'>© {ano_atual} {SISTEMA_NOME} - Todos os direitos reservados</p>",
        unsafe_allow_html=True
    )
