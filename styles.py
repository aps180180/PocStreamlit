import streamlit as st
from config.theme import get_custom_css

def aplicar_estilos():
    """
    Aplica CSS customizado na página usando configurações do tema
    """
    css_custom = get_custom_css()
    
    css_compacto = """
    <style>
    
    /* ========== FORÇAR SIDEBAR SEMPRE VISÍVEL ========== */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: block !important;
    }
    
    /* ========== OCULTAR MENU E RODAPÉ DO STREAMLIT ========== */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    
    
    /* ========== DESABILITAR LINKS AUTOMÁTICOS ========== */
    a[href^="mailto:"] {
        color: inherit !important;
        text-decoration: none !important;
        pointer-events: none !important;
        cursor: text !important;
    }
    
    /* ========== COLORIR BOTÕES DE AÇÕES - VERSÃO FORÇADA ========== */
    
    /* Todos os botões pequenos na tabela */
    div[data-testid="column"] button[data-testid="baseButton-secondary"] {
        height: 32px !important;
        padding: 0.25rem 0.5rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
        font-weight: 500 !important;
    }
    
    /* Forçar cores por posição - primeiro botão (editar) */
    div[data-testid="column"] > div > div:first-child button {
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%) !important;
        color: white !important;
    }
    
    div[data-testid="column"] > div > div:first-child button:hover {
        background: linear-gradient(135deg, #2980B9 0%, #21618C 100%) !important;
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Forçar cores por posição - segundo botão (excluir) */
    div[data-testid="column"] > div > div:last-child button {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%) !important;
        color: white !important;
    }
    
    div[data-testid="column"] > div > div:last-child button:hover {
        background: linear-gradient(135deg, #C0392B 0%, #A93226 100%) !important;
        box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* ========== COMPACTAR LISTAGENS ========== */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {gap: 0.3rem;}
    hr {margin: 0.3rem 0 !important;}
    div[data-testid="column"] p {margin-bottom: 0.2rem !important; line-height: 1.3 !important;}
    div[data-testid="column"] div[data-testid="stMarkdownContainer"] {padding: 0.2rem 0 !important;}
    div[data-testid="stVerticalBlock"] hr {margin-top: 0.5rem !important; margin-bottom: 0.5rem !important;}
    div[data-testid="column"] {padding: 0.3rem 0.5rem !important;}
    </style>
    """


    
    st.markdown(css_custom + css_compacto, unsafe_allow_html=True)
