"""
CSS Customizado do Sistema - VERSÃO OTIMIZADA
Esconde menu padrão mas mantém funcionalidade de toggle
"""
import streamlit as st


def apply_custom_css():
    """
    Aplica CSS customizado:
    - Esconde menu de navegação padrão do Streamlit
    - Mantém botão de toggle sempre visível
    - Melhora visual geral
    """
    st.markdown("""
        <style>
            /* ==========================================
               ESCONDER MENU PADRÃO DO STREAMLIT
               ========================================== */
            
            /* Esconder lista de páginas na sidebar */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            
            /* ==========================================
               MELHORIAS VISUAIS
               ========================================== */
            
            /* Sidebar com cor de fundo */
            section[data-testid="stSidebar"] {
                background-color: #f8f9fa;
            }
            
            /* Esconder "Made with Streamlit" */
            footer {
                visibility: hidden;
            }
            
            footer:after {
                content: 'Sistema ERP v2.0';
                visibility: visible;
                display: block;
                position: relative;
                padding: 5px;
                text-align: center;
                color: #888;
                font-size: 12px;
            }
            
            /* Botões do menu com hover */
            .stButton > button {
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background-color: #e0e0e0;
                border-color: #007bff;
                transform: translateX(5px);
            }
            
            /* Expanders com visual melhor */
            .streamlit-expanderHeader {
                font-weight: 600;
                color: #333;
                background-color: #e9ecef;
                border-radius: 5px;
            }
            
            /* Container principal */
            .block-container {
                padding-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)


def apply_login_css():
    """
    CSS específico para tela de login
    """
    st.markdown("""
        <style>
            /* Centralizar conteúdo do login */
            .block-container {
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 70vh;
            }
            
            /* Esconder sidebar no login */
            section[data-testid="stSidebar"] {
                display: none;
            }
            
            /* Esconder botão de toggle no login */
            [data-testid="collapsedControl"] {
                display: none !important;
            }
            
            footer {
                visibility: hidden;
            }
        </style>
    """, unsafe_allow_html=True)
