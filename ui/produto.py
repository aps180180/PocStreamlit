import streamlit as st
import streamlit_antd_components as sac
import db.models as db
import math
from config.theme import (
    ICONE_ADICIONAR, 
    ICONE_EDITAR, 
    ICONE_EXCLUIR,
    ICONE_PRODUTOS,
    MSG_SUCESSO_ADICIONAR,
    MSG_SUCESSO_ATUALIZAR,
    MSG_SUCESSO_EXCLUIR,
    MSG_CONFIRMAR_EXCLUSAO,
    OPCOES_REGISTROS_POR_PAGINA,
    REGISTROS_POR_PAGINA_DEFAULT
)

@st.dialog("Adicionar Produto")
def modal_adicionar_produto():
    """Modal para adicionar novo produto"""
    with st.form("form_add_produto"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço", min_value=0.01, format="%.2f")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar", use_container_width=True, type="primary"):
                if not nome.strip():
                    st.error("Informe o nome")
                elif preco <= 0:
                    st.error("Preço inválido")
                else:
                    db.inserir_produto(nome, preco)
                    st.success(MSG_SUCESSO_ADICIONAR.format("Produto"))
                    st.session_state.pagina_atual_produto = 1
                    st.session_state.pop('modal_add_produto', None)
                    st.rerun()
        with col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop('modal_add_produto', None)
                st.rerun()

@st.dialog("Editar Produto")
def modal_editar_produto(produto_id):
    """Modal para editar produto existente"""
    produto = db.obter_produto(produto_id)
    
    if produto:
        with st.form("form_edit_produto"):
            nome = st.text_input("Nome do Produto", value=produto[1])
            preco = st.number_input("Preço", min_value=0.01, value=float(produto[2]), format="%.2f")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Salvar", use_container_width=True, type="primary"):
                    if not nome.strip():
                        st.error("Nome obrigatório")
                    elif preco <= 0:
                        st.error("Preço inválido")
                    else:
                        db.atualizar_produto(produto_id, nome, preco)
                        st.success(MSG_SUCESSO_ATUALIZAR.format("Produto"))
                        st.session_state.pop('modal_edit_produto', None)
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancelar", use_container_width=True):
                    st.session_state.pop('modal_edit_produto', None)
                    st.rerun()

@st.dialog("Confirmar Exclusão")
def modal_confirmar_exclusao_produto(produto_id):
    """Modal de confirmação para excluir produto"""
    produto = db.obter_produto(produto_id)
    
    if produto:
        st.warning(MSG_CONFIRMAR_EXCLUSAO.format(f"o produto **{produto[1]}**"))
        st.markdown(f"**Preço:** R$ {produto[2]:.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim, excluir", use_container_width=True, type="secondary"):
                db.excluir_produto(produto_id)
                st.success(MSG_SUCESSO_EXCLUIR.format("Produto"))
                st.session_state.pop('modal_confirmar_exclusao_produto', None)
                st.rerun()
        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.session_state.pop('modal_confirmar_exclusao_produto', None)
                st.rerun()

def tela_produto():
    # Inicializar variáveis de sessão
    if 'pagina_atual_produto' not in st.session_state:
        st.session_state.pagina_atual_produto = 1
    
    if 'registros_por_pagina_produto' not in st.session_state:
        st.session_state.registros_por_pagina_produto = REGISTROS_POR_PAGINA_DEFAULT
    
    # Verificar se deve abrir modal de adicionar
    if 'modal_add_produto' in st.session_state and st.session_state.modal_add_produto:
        modal_adicionar_produto()
    
    # Verificar se deve abrir modal de editar
    if 'modal_edit_produto' in st.session_state and st.session_state.modal_edit_produto:
        modal_editar_produto(st.session_state.produto_id_editar)
    
    # Verificar se deve abrir modal de confirmação de exclusão
    if 'modal_confirmar_exclusao_produto' in st.session_state and st.session_state.modal_confirmar_exclusao_produto:
        modal_confirmar_exclusao_produto(st.session_state.produto_id_excluir)
    
    # Título
    sac.divider(label='Gerenciamento de Produtos', icon=ICONE_PRODUTOS, align='center', color='green')
    
    # Barra de controles
    col1, col2, col3, col4 = st.columns([1.2, 3.5, 1, 1])
    
    with col1:
        tipo_busca = st.selectbox(
            "Buscar por",
            ["Nome", "Código"],
            key='tipo_busca_produto'
        )
        tipo_busca_db = "nome" if tipo_busca == "Nome" else "codigo"
    
    with col2:
        placeholder = "Digite o código..." if tipo_busca == "Código" else "Digite o nome..."
        busca = st.text_input("Digite para buscar", placeholder=placeholder, key='busca_produto')
        if busca:
            st.session_state.pagina_atual_produto = 1
    
    with col3:
        registros_por_pagina = st.selectbox(
            "Por página",
            OPCOES_REGISTROS_POR_PAGINA,
            index=OPCOES_REGISTROS_POR_PAGINA.index(st.session_state.registros_por_pagina_produto),
            key='select_registros_produto_novo'
        )
        
        if registros_por_pagina != st.session_state.registros_por_pagina_produto:
            st.session_state.registros_por_pagina_produto = registros_por_pagina
            st.session_state.pagina_atual_produto = 1
            st.rerun()
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, type="primary", key="btn_novo_prod"):
            st.session_state.modal_add_produto = True
            st.rerun()
    
    st.markdown("---")
    
    # Calcular paginação
    total_produtos = db.contar_produtos(busca, tipo_busca_db)
    total_paginas = math.ceil(total_produtos / registros_por_pagina) if total_produtos > 0 else 1
    offset = (st.session_state.pagina_atual_produto - 1) * registros_por_pagina
    
    # Buscar produtos da página atual
    produtos = db.listar_produtos(busca, tipo_busca_db, registros_por_pagina, offset)
    
    # Informações
    st.markdown(f"**Total:** {total_produtos} produtos | **Página** {st.session_state.pagina_atual_produto} de {total_paginas}")
    st.markdown("---")
    
    if produtos:
        # Cabeçalho da tabela
        col1, col2, col3, col4 = st.columns([0.7, 4, 2, 1.8])
        with col1:
            st.markdown("**Código**")
        with col2:
            st.markdown("**Nome**")
        with col3:
            st.markdown("**Preço**")
        with col4:
            st.markdown("**Ações**")
        
        st.markdown("---")
        
        # Listar produtos
        for produto in produtos:
            col1, col2, col3, col4 = st.columns([0.7, 4, 2, 1.8])
            with col1:
                st.markdown(f"`#{produto[0]}`")
            with col2:
                st.write(produto[1])
            with col3:
                st.markdown(f"**R$ {produto[2]:.2f}**")
            with col4:
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"{ICONE_EDITAR}", key=f"btn_edit_prod_{produto[0]}", use_container_width=True, help="Editar produto"):
                        st.session_state.modal_edit_produto = True
                        st.session_state.produto_id_editar = produto[0]
                        st.rerun()
                with col_btn2:
                    if st.button(f"{ICONE_EXCLUIR}", key=f"btn_del_prod_{produto[0]}", use_container_width=True, type="secondary", help="Excluir produto"):
                        st.session_state.modal_confirmar_exclusao_produto = True
                        st.session_state.produto_id_excluir = produto[0]
                        st.rerun()
            
            st.divider()
        
        # Paginação
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            nova_pagina = sac.pagination(
                total=total_produtos,
                page_size=registros_por_pagina,
                align='center',
                show_total=True,
                jump=True,
                key='pagination_produto'
            )
            if nova_pagina != st.session_state.pagina_atual_produto:
                st.session_state.pagina_atual_produto = nova_pagina
                st.rerun()
    else:
        sac.result(
            label='Nenhum produto encontrado',
            description=f'Clique em "{ICONE_ADICIONAR} Novo" para adicionar o primeiro produto.',
            status='empty'
        )
