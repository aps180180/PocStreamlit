"""
Estilos customizados para o sistema
"""
import streamlit as st
from config.theme import (
    COR_PRIMARIA, COR_SECUNDARIA, COR_SUCESSO, COR_PERIGO,
    COR_AVISO, COR_INFO, COR_FUNDO, COR_TEXTO, COR_BORDA
)

def get_custom_css():
    """
    Retorna o CSS customizado baseado no tema
    """
    return f"""
    <style>
    /* ========== VARIÁVEIS CSS ========== */
    :root {{
        --cor-primaria: {COR_PRIMARIA};
        --cor-secundaria: {COR_SECUNDARIA};
        --cor-sucesso: {COR_SUCESSO};
        --cor-perigo: {COR_PERIGO};
        --cor-aviso: {COR_AVISO};
        --cor-info: {COR_INFO};
        --cor-fundo: {COR_FUNDO};
        --cor-texto: {COR_TEXTO};
        --cor-borda: {COR_BORDA};
    }}
    
    /* ========== GERAL ========== */
    .main {{
        background-color: var(--cor-fundo);
    }}
    
    /* ========== OCULTAR ELEMENTOS PADRÃO ========== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Ocultar mensagem "Press Enter to submit form" */
    div[data-testid="InputInstructions"] {{
        display: none !important;
    }}
    
    /* ========== BOTÕES ========== */
    .stButton > button {{
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* ========== INPUTS ========== */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {{
        border-radius: 5px;
    }}
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {{
        border-color: var(--cor-primaria);
        box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    }}
    
    /* ========== DIVIDERS ========== */
    hr {{
        margin: 1rem 0;
        border-color: var(--cor-borda);
    }}
    
    /* ========== TABELAS ========== */
    .dataframe {{
        font-size: 0.9rem;
    }}
    
    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {{
        background-color: #f8f9fa;
    }}
    
    /* ========== MÉTRICAS ========== */
    div[data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: bold;
    }}
    
    /* ========== MODAIS ========== */
    div[data-testid="stModal"] {{
        max-width: 800px;
    }}
    
    /* ========== ALERTAS ========== */
    .stAlert {{
        border-radius: 5px;
    }}
    
    /* ========== ANIMAÇÕES ========== */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .main > div {{
        animation: fadeIn 0.5s ease-in;
    }}
    
    /* ========== RESPONSIVO ========== */
    @media (max-width: 768px) {{
        .stButton > button {{
            font-size: 0.9rem;
            padding: 0.5rem 1rem;
        }}
    }}
    </style>
    """

def aplicar_estilos():
    """
    Aplica CSS customizado na página
    """
    css = get_custom_css()
    st.markdown(css, unsafe_allow_html=True)
