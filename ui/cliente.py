import streamlit as st
import streamlit_antd_components as sac
import db.models as db
import utils
import math
from config.theme import (
    ICONE_ADICIONAR, 
    ICONE_EDITAR, 
    ICONE_EXCLUIR,
    ICONE_CLIENTES,
    MSG_SUCESSO_ADICIONAR,
    MSG_SUCESSO_ATUALIZAR,
    MSG_SUCESSO_EXCLUIR,
    MSG_CONFIRMAR_EXCLUSAO,
    OPCOES_REGISTROS_POR_PAGINA,
    REGISTROS_POR_PAGINA_DEFAULT
)

@st.dialog("Adicionar Cliente")
def modal_adicionar_cliente():
    """Modal para adicionar novo cliente"""
    with st.form("form_add_cliente"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar", use_container_width=True, type="primary"):
                if not nome.strip():
                    st.error("Informe o nome")
                elif not utils.validar_email(email):
                    st.error("Email inválido")
                else:
                    db.inserir_cliente(nome, email)
                    st.success(MSG_SUCESSO_ADICIONAR.format("Cliente"))
                    st.session_state.pagina_atual_cliente = 1
                    st.session_state.pop('modal_add_cliente', None)
                    st.rerun()
        with col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop('modal_add_cliente', None)
                st.rerun()

@st.dialog("Editar Cliente")
def modal_editar_cliente(cliente_id):
    """Modal para editar cliente existente"""
    cliente = db.obter_cliente(cliente_id)
    
    if cliente:
        with st.form("form_edit_cliente"):
            nome = st.text_input("Nome", value=cliente[1])
            email = st.text_input("Email", value=cliente[2])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Salvar", use_container_width=True, type="primary"):
                    if not nome.strip():
                        st.error("Nome obrigatório")
                    elif not utils.validar_email(email):
                        st.error("Email inválido")
                    else:
                        db.atualizar_cliente(cliente_id, nome, email)
                        st.success(MSG_SUCESSO_ATUALIZAR.format("Cliente"))
                        st.session_state.pop('modal_edit_cliente', None)
                        st.rerun()
            with col2:
                if st.form_submit_button("Cancelar", use_container_width=True):
                    st.session_state.pop('modal_edit_cliente', None)
                    st.rerun()

@st.dialog("Confirmar Exclusão")
def modal_confirmar_exclusao_cliente(cliente_id):
    """Modal de confirmação para excluir cliente"""
    cliente = db.obter_cliente(cliente_id)
    
    if cliente:
        st.warning(MSG_CONFIRMAR_EXCLUSAO.format(f"o cliente **{cliente[1]}**"))
        st.markdown(f"**Email:** {cliente[2]}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sim, excluir", use_container_width=True, type="secondary"):
                db.excluir_cliente(cliente_id)
                st.success(MSG_SUCESSO_EXCLUIR.format("Cliente"))
                st.session_state.pop('modal_confirmar_exclusao_cliente', None)
                st.rerun()
        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.session_state.pop('modal_confirmar_exclusao_cliente', None)
                st.rerun()

def tela_cliente():
    # Inicializar variáveis de sessão
    if 'pagina_atual_cliente' not in st.session_state:
        st.session_state.pagina_atual_cliente = 1
    
    if 'registros_por_pagina_cliente' not in st.session_state:
        st.session_state.registros_por_pagina_cliente = REGISTROS_POR_PAGINA_DEFAULT
    
    # Verificar se deve abrir modal de adicionar
    if 'modal_add_cliente' in st.session_state and st.session_state.modal_add_cliente:
        modal_adicionar_cliente()
    
    # Verificar se deve abrir modal de editar
    if 'modal_edit_cliente' in st.session_state and st.session_state.modal_edit_cliente:
        modal_editar_cliente(st.session_state.cliente_id_editar)
    
    # Verificar se deve abrir modal de confirmação de exclusão
    if 'modal_confirmar_exclusao_cliente' in st.session_state and st.session_state.modal_confirmar_exclusao_cliente:
        modal_confirmar_exclusao_cliente(st.session_state.cliente_id_excluir)
    
    # Título
    sac.divider(label='Gerenciamento de Clientes', icon=ICONE_CLIENTES, align='center', color='blue')
    
    # Barra de controles
    col1, col2, col3, col4 = st.columns([1.2, 3.5, 1, 1])
    
    with col1:
        tipo_busca = st.selectbox(
            "Buscar por",
            ["Nome", "Código"],
            key='tipo_busca_cliente'
        )
        tipo_busca_db = "nome" if tipo_busca == "Nome" else "codigo"
    
    with col2:
        placeholder = "Digite o código..." if tipo_busca == "Código" else "Digite o nome..."
        busca = st.text_input("Digite para buscar", placeholder=placeholder, key='busca_cliente')
        if busca:
            st.session_state.pagina_atual_cliente = 1
    
    with col3:
        registros_por_pagina = st.selectbox(
            "Por página",
            OPCOES_REGISTROS_POR_PAGINA,
            index=OPCOES_REGISTROS_POR_PAGINA.index(st.session_state.registros_por_pagina_cliente),
            key='select_registros_cliente_novo'
        )
        
        if registros_por_pagina != st.session_state.registros_por_pagina_cliente:
            st.session_state.registros_por_pagina_cliente = registros_por_pagina
            st.session_state.pagina_atual_cliente = 1
            st.rerun()
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, type="primary", key="btn_novo_cli"):
            st.session_state.modal_add_cliente = True
            st.rerun()
    
    st.markdown("---")
    
    # Calcular paginação
    total_clientes = db.contar_clientes(busca, tipo_busca_db)
    total_paginas = math.ceil(total_clientes / registros_por_pagina) if total_clientes > 0 else 1
    offset = (st.session_state.pagina_atual_cliente - 1) * registros_por_pagina
    
    # Buscar clientes da página atual
    clientes = db.listar_clientes(busca, tipo_busca_db, registros_por_pagina, offset)
    
    # Informações
    st.markdown(f"**Total:** {total_clientes} clientes | **Página** {st.session_state.pagina_atual_cliente} de {total_paginas}")
    st.markdown("---")
    
    if clientes:
        # Cabeçalho da tabela
        col1, col2, col3, col4 = st.columns([0.7, 3, 3, 1.5])
        with col1:
            st.markdown("**Código**")
        with col2:
            st.markdown("**Nome**")
        with col3:
            st.markdown("**Email**")
        with col4:
            st.markdown("**Ações**")
        
        st.markdown("---")
        
        # Listar clientes
        for cliente in clientes:
            col1, col2, col3, col4 = st.columns([0.7, 3, 3, 1.5])
            with col1:
                st.markdown(f"`#{cliente[0]}`")
            with col2:
                st.write(cliente[1])
            with col3:
                st.write(cliente[2])
            with col4:
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"{ICONE_EDITAR}", key=f"btn_edit_cli_{cliente[0]}", use_container_width=True, help="Editar cliente"):
                        st.session_state.modal_edit_cliente = True
                        st.session_state.cliente_id_editar = cliente[0]
                        st.rerun()
                with col_btn2:
                    if st.button(f"{ICONE_EXCLUIR}", key=f"btn_del_cli_{cliente[0]}", use_container_width=True, type="secondary", help="Excluir cliente"):
                        st.session_state.modal_confirmar_exclusao_cliente = True
                        st.session_state.cliente_id_excluir = cliente[0]
                        st.rerun()
            
            st.divider()
        
        # Paginação
        st.write("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            nova_pagina = sac.pagination(
                total=total_clientes,
                page_size=registros_por_pagina,
                align='center',
                show_total=True,
                jump=True,
                key='pagination_cliente'
            )
            if nova_pagina != st.session_state.pagina_atual_cliente:
                st.session_state.pagina_atual_cliente = nova_pagina
                st.rerun()
    else:
        sac.result(
            label='Nenhum cliente encontrado',
            description=f'Clique em "{ICONE_ADICIONAR} Novo" para adicionar o primeiro cliente.',
            status='empty'
        )
