"""
Módulo de Gestão de Produtos
Página para gerenciar o cadastro completo de produtos
"""
import streamlit as st
import streamlit_antd_components as sac
import styles
from db.models import criar_tabelas
from datetime import datetime
import ui.produto as produto_ui
from config.empresa import SISTEMA_NOME, SISTEMA_VERSAO, SISTEMA_SUBTITULO

# Configuração da página
st.set_page_config(
    page_title=f"Gestão de Produtos - {SISTEMA_NOME}", 
    layout="wide", 
    initial_sidebar_state="expanded",
    page_icon="📦"
)

# Aplicar estilos
styles.aplicar_estilos()

# Criar tabelas
criar_tabelas()

# Sidebar customizado
with st.sidebar:
    st.markdown(f"# 📊 {SISTEMA_NOME}")
    st.markdown(f"**Gestão de Produtos**")
    st.caption(f"Versão {SISTEMA_VERSAO}")
    
    sac.divider(label='Navegação Rápida', icon='compass', align='center', color='green')
    
    # Botões de navegação
    st.markdown("### 🔗 Ir para:")
    
    if st.button("🏠 Dashboard", use_container_width=True, type="secondary"):
        st.switch_page("app.py")
    
    if st.button("👥 Clientes", use_container_width=True, type="secondary"):
        st.switch_page("pages/01_Clientes.py")
    
    # Estatísticas do módulo
    st.markdown("---")
    st.markdown("### 📊 Estatísticas")
    
    import db.models as db
    total_produtos = db.contar_produtos("", "nome")
    ultimos_produtos = db.listar_produtos("", "nome", 3, 0)
    
    # Calcular valor total
    todos_produtos = db.listar_produtos("", "nome", 99999, 0)
    valor_total = sum([float(p[2]) for p in todos_produtos]) if todos_produtos else 0
    
    st.metric("Total de Produtos", total_produtos)
    st.metric("Valor Total", f"R$ {valor_total:,.2f}")
    
    if ultimos_produtos:
        st.markdown("**Últimos cadastrados:**")
        for produto in ultimos_produtos:
            st.caption(f"• {produto[1]}")
    
    # Rodapé
    st.markdown("---")
    ano_atual = datetime.now().year
    st.caption(f"© {ano_atual} - Todos os direitos reservados")

# Conteúdo principal
produto_ui.tela_produto()
