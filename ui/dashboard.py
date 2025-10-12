"""
Dashboard com estatísticas gerais do sistema
"""
import streamlit as st
import streamlit_antd_components as sac
import db.models as db
from config.empresa import SISTEMA_NOME

def tela_dashboard():
    """Tela de dashboard com métricas e ações rápidas"""
    
    # Título
    sac.divider(label='Dashboard - Visão Geral do Sistema', icon='house-fill', align='center', color='blue')
    
    # Buscar dados
    total_clientes = db.contar_clientes("", "nome")
    total_produtos = db.contar_produtos("", "nome")
    
    # Buscar últimos registros
    ultimos_clientes = db.listar_clientes("", "nome", 5, 0)
    ultimos_produtos = db.listar_produtos("", "nome", 5, 0)
    
    # Calcular valor total de produtos
    todos_produtos = db.listar_produtos("", "nome", 99999, 0)
    valor_total_estoque = sum([float(p[2]) for p in todos_produtos]) if todos_produtos else 0
    
    # Métricas principais
    st.markdown("### 📊 Indicadores Principais")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total de Clientes",
            value=total_clientes,
            delta="Base ativa",
            help="Número total de clientes cadastrados no sistema"
        )
    
    with col2:
        st.metric(
            label="📦 Total de Produtos",
            value=total_produtos,
            delta="Itens cadastrados",
            help="Número total de produtos no catálogo"
        )
    
    with col3:
        st.metric(
            label="💰 Valor do Estoque",
            value=f"R$ {valor_total_estoque:,.2f}",
            delta="Valor total",
            help="Soma do valor de todos os produtos cadastrados"
        )
    
    with col4:
        ticket_medio = valor_total_estoque / total_produtos if total_produtos > 0 else 0
        st.metric(
            label="🎯 Ticket Médio",
            value=f"R$ {ticket_medio:,.2f}",
            delta="Por produto",
            help="Valor médio dos produtos cadastrados"
        )
    
    st.markdown("---")
    
    # Duas colunas para últimos registros
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👥 Últimos Clientes Cadastrados")
        if ultimos_clientes:
            for cliente in ultimos_clientes:
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**{cliente[1]}**")
                        st.caption(f"✉️ {cliente[2]}")
                    with col_b:
                        st.markdown(f"`#{cliente[0]}`")
                    st.divider()
        else:
            st.info("📭 Nenhum cliente cadastrado ainda. Clique em 'Gerenciar Clientes' para começar!")
    
    with col2:
        st.markdown("### 📦 Últimos Produtos Cadastrados")
        if ultimos_produtos:
            for produto in ultimos_produtos:
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**{produto[1]}**")
                        st.caption(f"💵 R$ {produto[2]:,.2f}")
                    with col_b:
                        st.markdown(f"`#{produto[0]}`")
                    st.divider()
        else:
            st.info("📭 Nenhum produto cadastrado ainda. Clique em 'Gerenciar Produtos' para começar!")
    
    # Botões de ação rápida
    st.markdown("---")
    st.markdown("### ⚡ Acesso Rápido aos Módulos")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("👥 Gestão de Clientes", use_container_width=True, type="primary", key="btn_clientes_dash"):
            st.switch_page("pages/01_Clientes.py")
    
    with col2:
        if st.button("📦 Gestão de Produtos", use_container_width=True, type="primary", key="btn_produtos_dash"):
            st.switch_page("pages/02_Produtos.py")
    
    with col3:
        st.button("📊 Relatórios", use_container_width=True, disabled=True, help="Em breve: Central de relatórios")
    
    with col4:
        st.button("⚙️ Configurações", use_container_width=True, disabled=True, help="Em breve: Configurações do sistema")
