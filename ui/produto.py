import streamlit as st
import streamlit_antd_components as sac
import db.models as db
import math
from datetime import datetime
from config.theme import (
    ICONE_ADICIONAR, 
    ICONE_EDITAR, 
    ICONE_EXCLUIR,
    ICONE_PRODUTOS,
    ICONE_RELATORIO,
    ICONE_DOWNLOAD,
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
    
    if 'tipo_busca_produto' not in st.session_state:
        st.session_state.tipo_busca_produto = "Nome"
    
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
    
    # Container de controles com labels acima
    st.markdown("##### Filtros e Controles")
    col1, col2, col3, col4 = st.columns([1.5, 3.5, 1.2, 1])
    
    with col1:
        st.caption("Buscar por:")
        tipo_busca = sac.segmented(
            items=['Nome', 'Código'],
            label='',
            index=0 if st.session_state.tipo_busca_produto == "Nome" else 1,
            align='start',
            size='sm',
            key='seg_tipo_busca_produto',
            readonly=False
        )
        if tipo_busca != st.session_state.tipo_busca_produto:
            st.session_state.tipo_busca_produto = tipo_busca
            st.rerun()
        tipo_busca_db = "nome" if tipo_busca == "Nome" else "codigo"
    
    with col2:
        st.caption("Digite para buscar:")
        placeholder = "Digite o código..." if tipo_busca == "Código" else "Digite o nome..."
        busca = st.text_input("", placeholder=placeholder, key='busca_produto', label_visibility="collapsed")
        if busca and 'busca_anterior_produto' in st.session_state and busca != st.session_state.busca_anterior_produto:
            st.session_state.pagina_atual_produto = 1
        st.session_state.busca_anterior_produto = busca
    
    with col3:
        st.caption("Por página:")
        registros_label = sac.segmented(
            items=[str(x) for x in OPCOES_REGISTROS_POR_PAGINA],
            label='',
            index=OPCOES_REGISTROS_POR_PAGINA.index(st.session_state.registros_por_pagina_produto),
            size='sm',
            key='seg_registros_produto',
            readonly=False
        )
        registros_por_pagina = int(registros_label)
        
        if registros_por_pagina != st.session_state.registros_por_pagina_produto:
            st.session_state.registros_por_pagina_produto = registros_por_pagina
            st.session_state.pagina_atual_produto = 1
            st.rerun()
    
    with col4:
        st.caption("Ações:")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, type="primary", key="btn_novo_prod"):
                st.session_state.modal_add_produto = True
                st.rerun()
        with col_btn2:
            if st.button(f"{ICONE_RELATORIO} PDF", use_container_width=True, key="btn_pdf_prod", help="Gerar relatório em PDF"):
                st.session_state.gerar_pdf_produtos = True
                st.rerun()
    
    st.markdown("---")
    
    # Calcular paginação
    total_produtos = db.contar_produtos(busca, tipo_busca_db)
    total_paginas = math.ceil(total_produtos / registros_por_pagina) if total_produtos > 0 else 1
    offset = (st.session_state.pagina_atual_produto - 1) * registros_por_pagina
    
    # Buscar produtos da página atual
    produtos = db.listar_produtos(busca, tipo_busca_db, registros_por_pagina, offset)
    
    # Verificar se deve gerar PDF
    if 'gerar_pdf_produtos' in st.session_state and st.session_state.gerar_pdf_produtos:
        from utils.pdf_generator import gerar_relatorio_produtos_pdf
        
        # Buscar TODOS os produtos para o relatório
        todos_produtos = db.listar_produtos(busca, tipo_busca_db, 999999, 0)
        filtros_info = f"Tipo: {tipo_busca}, Busca: '{busca if busca else 'Todos'}'"
        pdf_buffer = gerar_relatorio_produtos_pdf(todos_produtos, filtros_info)
        
        st.download_button(
            label=f"{ICONE_DOWNLOAD} Baixar Relatório de Produtos",
            data=pdf_buffer,
            file_name=f"relatorio_produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
            key="download_pdf_prod"
        )
        st.session_state.pop('gerar_pdf_produtos', None)
    
    # PAGINAÇÃO NO TOPO
    if total_produtos > 0:
        col_info, col_pag = st.columns([1, 2])
        with col_info:
            st.markdown(f"**Total:** {total_produtos} produtos | **Página** {st.session_state.pagina_atual_produto} de {total_paginas}")
        with col_pag:
            nova_pagina = sac.pagination(
                total=total_produtos,
                page_size=registros_por_pagina,
                align='end',
                show_total=False,
                jump=True,
                key='pagination_produto_top'
            )
            if nova_pagina != st.session_state.pagina_atual_produto:
                st.session_state.pagina_atual_produto = nova_pagina
                st.rerun()
    
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
    else:
        sac.result(
            label='Nenhum produto encontrado',
            description=f'Clique em "{ICONE_ADICIONAR} Novo" para adicionar o primeiro produto.',
            status='empty'
        )
