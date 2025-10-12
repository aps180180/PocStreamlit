import streamlit as st
import streamlit_antd_components as sac
import ui.cliente as cliente_ui
import ui.produto as produto_ui
import styles
from db.models import criar_tabelas
from datetime import datetime
from config.empresa import (
    SISTEMA_NOME,
    SISTEMA_VERSAO,
    SISTEMA_SUBTITULO
)
from config.theme import ICONE_CLIENTES, ICONE_PRODUTOS

def main():
    st.set_page_config(
        page_title=f"{SISTEMA_NOME} v{SISTEMA_VERSAO}", 
        layout="wide", 
        initial_sidebar_state="expanded",
        page_icon="📊"
    )
    
    styles.aplicar_estilos()
    criar_tabelas()
    
    # Menu lateral com informações do sistema
    with st.sidebar:
        # Título do sistema
        st.markdown(f"# {SISTEMA_NOME}")
        st.markdown(f"**{SISTEMA_SUBTITULO}**")
        st.caption(f"Versão {SISTEMA_VERSAO}")
        
        sac.divider(label='Menu Principal', icon='list', align='center', color='blue')
        
        # Menu de navegação
        escolha = sac.menu([
            sac.MenuItem('Clientes', icon=ICONE_CLIENTES),
            sac.MenuItem('Produtos', icon=ICONE_PRODUTOS),
        ], open_all=True, format_func='title', size='md')
        
        # Rodapé do menu com ano dinâmico
        st.markdown("---")
        ano_atual = datetime.now().year
        st.caption(f"© {ano_atual} - Todos os direitos reservados")

    # Renderizar tela selecionada
    if escolha == 'Clientes':
        cliente_ui.tela_cliente()
    elif escolha == 'Produtos':
        produto_ui.tela_produto()

if __name__ == "__main__":
    main()
