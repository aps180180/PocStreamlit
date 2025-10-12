"""
Módulo de Gestão de Clientes
Página para gerenciar o cadastro completo de clientes
"""
import streamlit as st
import streamlit_antd_components as sac
import styles
from db.models import criar_tabelas
from datetime import datetime
import ui.cliente as cliente_ui
from config.empresa import SISTEMA_NOME, SISTEMA_VERSAO, SISTEMA_SUBTITULO

# Configuração da página
st.set_page_config(
    page_title=f"Gestão de Clientes - {SISTEMA_NOME}", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="👥"
)

# Aplicar estilos
styles.aplicar_estilos()

# Criar tabelas
criar_tabelas()

# Sidebar customizado
with st.sidebar:
    st.markdown(f"# 📊 {SISTEMA_NOME}")
    st.markdown(f"**Gestão de Clientes**")
    st.caption(f"Versão {SISTEMA_VERSAO}")
    
    sac.divider(label='Navegação Rápida', icon='compass', align='center', color='blue')
    
    # Botões de navegação
    st.markdown("### 🔗 Ir para:")
    
    if st.button("🏠 Dashboard", use_container_width=True, type="secondary"):
        st.switch_page("app.py")
    
    if st.button("📦 Produtos", use_container_width=True, type="secondary"):
        st.switch_page("pages/02_Produtos.py")
    
    # Estatísticas do módulo
    st.markdown("---")
    st.markdown("### 📊 Estatísticas")
    
    import db.models as db
    total_clientes = db.contar_clientes("", "nome")
    ultimos_clientes = db.listar_clientes("", "nome", 3, 0)
    
    st.metric("Total de Clientes", total_clientes)
    
    if ultimos_clientes:
        st.markdown("**Últimos cadastrados:**")
        for cliente in ultimos_clientes:
            st.caption(f"• {cliente[1]}")
    
    # Rodapé
    st.markdown("---")
    ano_atual = datetime.now().year
    st.caption(f"© {ano_atual} - Todos os direitos reservados")

# Conteúdo principal
cliente_ui.tela_cliente()
