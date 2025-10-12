import streamlit as st
import streamlit_antd_components as sac
import ui.cliente as cliente_ui
import ui.produto as produto_ui
import styles
from db.models import criar_tabelas
from config.theme import ICONE_CLIENTES, ICONE_PRODUTOS

def main():
    st.set_page_config(
        page_title="Sistema CRUD", 
        layout="wide", 
        initial_sidebar_state="expanded",
        page_icon="📊"
    )
    
    styles.aplicar_estilos()
    criar_tabelas()
    
    # Menu lateral com Ant Design
    with st.sidebar:
        sac.divider(label='Sistema CRUD', icon='database-fill-gear', align='center', color='blue')
        
        escolha = sac.menu([
            sac.MenuItem('Clientes', icon=ICONE_CLIENTES),
            sac.MenuItem('Produtos', icon=ICONE_PRODUTOS),
        ], open_all=True, format_func='title', size='md')

    if escolha == 'Clientes':
        cliente_ui.tela_cliente()
    elif escolha == 'Produtos':
        produto_ui.tela_produto()

if __name__ == "__main__":
    main()
