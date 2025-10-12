import streamlit as st
from config.theme import get_custom_css

def aplicar_estilos():
    """
    Aplica CSS customizado na página usando configurações do tema
    """
    css_custom = get_custom_css()
    
    # CSS adicional para compactar listagens e ocultar elementos do Streamlit
    css_compacto = """
    <style>
    /* ========== OCULTAR MENU E RODAPÉ DO STREAMLIT ========== */
    
    /* Ocultar menu hamburger */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Ocultar botão de deploy */
    .stDeployButton {
        display: none;
    }
    
    /* Ocultar rodapé "Made with Streamlit" */
    footer {
        visibility: hidden;
    }
    
    /* Ocultar header do Streamlit */
    header {
        visibility: hidden;
    }
    
    /* ========== DESABILITAR LINKS AUTOMÁTICOS ========== */
    
    /* Remover estilo de link dos emails */
    a[href^="mailto:"] {
        color: inherit !important;
        text-decoration: none !important;
        pointer-events: none !important;
        cursor: text !important;
    }
    
    /* ========== COMPACTAR LISTAGENS ========== */
    
    /* Reduzir espaçamento das linhas nas listagens */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        gap: 0.3rem;
    }
    
    /* Reduzir padding dos dividers */
    hr {
        margin: 0.3rem 0 !important;
    }
    
    /* Reduzir altura dos botões na listagem */
    div[data-testid="column"] button {
        padding: 0.25rem 0.5rem !important;
        height: 32px !important;
        font-size: 0.9rem !important;
    }
    
    /* Reduzir espaçamento vertical dos textos */
    div[data-testid="column"] p {
        margin-bottom: 0.2rem !important;
        line-height: 1.3 !important;
    }
    
    /* Compactar markdown nas linhas */
    div[data-testid="column"] div[data-testid="stMarkdownContainer"] {
        padding: 0.2rem 0 !important;
    }
    
    /* Ajustar espaçamento dos dividers na listagem */
    div[data-testid="stVerticalBlock"] hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduzir padding das colunas */
    div[data-testid="column"] {
        padding: 0.3rem 0.5rem !important;
    }
    </style>
    """
    
    st.markdown(css_custom + css_compacto, unsafe_allow_html=True)
