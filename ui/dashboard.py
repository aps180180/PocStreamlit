"""
Interface do Dashboard
ATUALIZADO: Usando novos models separados
"""
import streamlit as st
import streamlit_antd_components as sac
from db.models import Cliente, Produto
from auth.auth_manager import AuthManager

def tela_dashboard():
    """Dashboard principal"""
    
    if not AuthManager.is_authenticated():
        st.error("❌ Você precisa estar autenticado")
        return
    
    # Título
    st.markdown("# 📊 Dashboard")
    st.markdown(f"Bem-vindo, **{AuthManager.get_user_name()}**!")
    st.markdown(f"🎭 Perfil: **{AuthManager.get_user_perfil()}**")
    
    st.markdown("---")
    
    # Estatísticas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_clientes = Cliente.count_all()
        st.metric("👥 Total de Clientes", total_clientes)
    
    with col2:
        total_produtos = Produto.count_all()
        st.metric("📦 Total de Produtos", total_produtos)
    
    with col3:
        st.metric("👤 Usuário Ativo", AuthManager.get_user_name())
    
    st.markdown("---")
    
    # Últimos clientes
    if AuthManager.has_permission('CLIENTES', 'VISUALIZAR'):
        st.markdown("### 👥 Últimos Clientes Cadastrados")
        
        ultimos_clientes = Cliente.buscar("", "nome", 5, 0)
        
        if ultimos_clientes:
            for cliente in ultimos_clientes:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{cliente[1]}** · {cliente[2] if cliente[2] else 'Sem email'}")
                with col2:
                    st.caption(f"ID: #{cliente[0]}")
                st.divider()
        else:
            st.info("Nenhum cliente cadastrado ainda")
    
    st.markdown("---")
    
    # Últimos produtos
    if AuthManager.has_permission('PRODUTOS', 'VISUALIZAR'):
        st.markdown("### 📦 Últimos Produtos Cadastrados")
        
        ultimos_produtos = Produto.buscar("", "nome", 5, 0)
        
        if ultimos_produtos:
            for produto in ultimos_produtos:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{produto[1]}** · R$ {float(produto[2]):,.2f}")
                with col2:
                    st.caption(f"ID: #{produto[0]}")
                st.divider()
        else:
            st.info("Nenhum produto cadastrado ainda")
