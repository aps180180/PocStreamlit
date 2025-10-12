import streamlit as st
from config.theme import get_custom_css

def aplicar_estilos():
    """
    Aplica CSS customizado na página usando configurações do tema
    """
    st.markdown(get_custom_css(), unsafe_allow_html=True)
