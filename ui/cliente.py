import streamlit as st
import streamlit_antd_components as sac
import db.models as db
import utils
import math
from config.theme import (
    ICONE_ADICIONAR,
    ICONE_DOWNLOAD, 
    ICONE_EDITAR, 
    ICONE_EXCLUIR,
    ICONE_CLIENTES,
    ICONE_RELATORIO,
    MSG_SUCESSO_ADICIONAR,
    MSG_SUCESSO_ATUALIZAR,
    MSG_SUCESSO_EXCLUIR,
    MSG_CONFIRMAR_EXCLUSAO,
    OPCOES_REGISTROS_POR_PAGINA,
    REGISTROS_POR_PAGINA_DEFAULT
)
from datetime import datetime


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
    
    if 'tipo_busca_cliente' not in st.session_state:
        st.session_state.tipo_busca_cliente = "Nome"
    
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
    
    # Container de controles com labels acima
    st.markdown("##### Filtros e Controles")
    col1, col2, col3, col4 = st.columns([1.5, 3.5, 1.2, 1])
    
    with col1:
        st.caption("Buscar por:")
        tipo_busca = sac.segmented(
            items=['Nome', 'Código'],
            label='',
            index=0 if st.session_state.tipo_busca_cliente == "Nome" else 1,
            align='start',
            size='sm',
            key='seg_tipo_busca_cliente',
            readonly=False
        )
        if tipo_busca != st.session_state.tipo_busca_cliente:
            st.session_state.tipo_busca_cliente = tipo_busca
            st.rerun()
        tipo_busca_db = "nome" if tipo_busca == "Nome" else "codigo"
    
    with col2:
        st.caption("Digite para buscar:")
        placeholder = "Digite o código..." if tipo_busca == "Código" else "Digite o nome..."
        busca = st.text_input("", placeholder=placeholder, key='busca_cliente', label_visibility="collapsed")
        if busca and 'busca_anterior_cliente' in st.session_state and busca != st.session_state.busca_anterior_cliente:
            st.session_state.pagina_atual_cliente = 1
        st.session_state.busca_anterior_cliente = busca
    
    with col3:
        st.caption("Por página:")
        registros_label = sac.segmented(
            items=[str(x) for x in OPCOES_REGISTROS_POR_PAGINA],
            label='',
            index=OPCOES_REGISTROS_POR_PAGINA.index(st.session_state.registros_por_pagina_cliente),
            size='sm',
            key='seg_registros_cliente',
            readonly=False
        )
        registros_por_pagina = int(registros_label)
        
        if registros_por_pagina != st.session_state.registros_por_pagina_cliente:
            st.session_state.registros_por_pagina_cliente = registros_por_pagina
            st.session_state.pagina_atual_cliente = 1
            st.rerun()
    
    with col4:
        st.caption("Ações:")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, type="primary", key="btn_novo_cli"):
                st.session_state.modal_add_cliente = True
                st.rerun()
        with col_btn2:
            if st.button(f"{ICONE_RELATORIO} PDF", use_container_width=True, key="btn_pdf_cli", help="Gerar relatório em PDF"):
                st.session_state.gerar_pdf_clientes = True
                st.rerun()

    # Logo após calcular total_clientes e antes da paginação, adicione:
    if 'gerar_pdf_clientes' in st.session_state and st.session_state.gerar_pdf_clientes:
        from utils.pdf_generator import gerar_relatorio_clientes_pdf
        
        # Buscar TODOS os clientes para o relatório
        todos_clientes = db.listar_clientes(busca, tipo_busca_db, 999999, 0)
        filtros_info = f"Tipo: {tipo_busca}, Busca: '{busca if busca else 'Todos'}'"
        pdf_buffer = gerar_relatorio_clientes_pdf(todos_clientes, filtros_info)
        
        st.download_button(
            label=f"{ICONE_DOWNLOAD} Baixar Relatório de Clientes",
            data=pdf_buffer,
            file_name=f"relatorio_clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
            key="download_pdf_cli"
        )
        st.session_state.pop('gerar_pdf_clientes', None)

        
    
    st.markdown("---")
    
    # Calcular paginação
    total_clientes = db.contar_clientes(busca, tipo_busca_db)
    total_paginas = math.ceil(total_clientes / registros_por_pagina) if total_clientes > 0 else 1
    offset = (st.session_state.pagina_atual_cliente - 1) * registros_por_pagina
    
    # Buscar clientes da página atual
    clientes = db.listar_clientes(busca, tipo_busca_db, registros_por_pagina, offset)
    
    # PAGINAÇÃO NO TOPO
    if total_clientes > 0:
        col_info, col_pag = st.columns([1, 2])
        with col_info:
            st.markdown(f"**Total:** {total_clientes} clientes | **Página** {st.session_state.pagina_atual_cliente} de {total_paginas}")
        with col_pag:
            nova_pagina = sac.pagination(
                total=total_clientes,
                page_size=registros_por_pagina,
                align='end',
                show_total=False,
                jump=True,
                key='pagination_cliente_top'
            )
            if nova_pagina != st.session_state.pagina_atual_cliente:
                st.session_state.pagina_atual_cliente = nova_pagina
                st.rerun()
    
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
    else:
        sac.result(
            label='Nenhum cliente encontrado',
            description=f'Clique em "{ICONE_ADICIONAR} Novo" para adicionar o primeiro cliente.',
            status='empty'
        )
