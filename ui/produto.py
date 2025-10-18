"""
Interface de Gestão de Produtos
Com modal de visualização para perfil Visualizador
"""
import streamlit as st
import streamlit_antd_components as sac
import db.models as db
from datetime import datetime
from config.theme import ICONE_ADICIONAR, ICONE_EDITAR, ICONE_EXCLUIR, ICONE_PDF
from utils.pdf_generator import gerar_relatorio_produtos_pdf
from auth.auth_manager import AuthManager
import math

def tela_produto():
    """Tela de gestão de produtos com controle de permissões"""
    
    if not AuthManager.has_permission('PRODUTOS', 'VISUALIZAR'):
        st.error("❌ Você não tem permissão para visualizar produtos")
        st.info(f"👤 Seu perfil atual: **{AuthManager.get_user_perfil()}**")
        return
    
    # Inicialização
    if 'pagina_atual_produto' not in st.session_state:
        st.session_state.pagina_atual_produto = 1
    if 'registros_por_pagina_produto' not in st.session_state:
        st.session_state.registros_por_pagina_produto = 10
    if 'tipo_busca_produto' not in st.session_state:
        st.session_state.tipo_busca_produto = "nome"
    
    sac.divider(label='Gestão de Produtos', icon='box-seam-fill', align='center', color='green')
    
    # Filtros
    st.markdown("##### 🔍 Filtros e Controles")
    col1, col2, col3, col4 = st.columns([1.5, 3.5, 1.2, 1])
    
    with col1:
        st.caption("Buscar por:")
        tipo_busca = sac.segmented(
            items=['Nome', 'Código'],
            label='',
            index=0 if st.session_state.tipo_busca_produto == "nome" else 1,
            align='start',
            size='sm',
            key='seg_tipo_busca_produto',
            readonly=False
        )
        if tipo_busca.lower() != st.session_state.tipo_busca_produto:
            st.session_state.tipo_busca_produto = tipo_busca.lower()
            st.session_state.pagina_atual_produto = 1
        tipo_busca_db = st.session_state.tipo_busca_produto
    
    with col2:
        st.caption("Digite para buscar:")
        placeholder = "Digite o código..." if tipo_busca == "Código" else "Digite o nome..."
        busca = st.text_input("", placeholder=placeholder, key='busca_produto', label_visibility="collapsed")
        if 'busca_anterior_produto' not in st.session_state:
            st.session_state.busca_anterior_produto = ""
        if busca != st.session_state.busca_anterior_produto:
            st.session_state.pagina_atual_produto = 1
            st.session_state.busca_anterior_produto = busca
    
    with col3:
        st.caption("Por página:")
        registros_label = sac.segmented(
            items=['10', '25', '50'],
            label='',
            index=[10, 25, 50].index(st.session_state.registros_por_pagina_produto),
            size='sm',
            key='seg_registros_produto',
            readonly=False
        )
        registros_por_pagina = int(registros_label)
        if registros_por_pagina != st.session_state.registros_por_pagina_produto:
            st.session_state.registros_por_pagina_produto = registros_por_pagina
            st.session_state.pagina_atual_produto = 1
    
    with col4:
        st.caption("Ações:")
        if AuthManager.has_permission('PRODUTOS', 'CRIAR'):
            if st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, type="primary", key="btn_novo_produto"):
                st.session_state.modal_add_produto = True
                st.rerun()
        else:
            st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, disabled=True)
    
    st.markdown("---")
    
    # Paginação
    total_produtos = db.contar_produtos(busca, tipo_busca_db)
    total_paginas = math.ceil(total_produtos / registros_por_pagina) if total_produtos > 0 else 1
    offset = (st.session_state.pagina_atual_produto - 1) * registros_por_pagina
    produtos = db.listar_produtos(busca, tipo_busca_db, registros_por_pagina, offset)
    
    if total_produtos > 0:
        col_info, col_pag = st.columns([1, 2])
        with col_info:
            st.markdown(f"**Total:** {total_produtos} produto(s) | **Página** {st.session_state.pagina_atual_produto} de {total_paginas}")
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
    
    st.markdown("---")
    
    # Ações
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    with col_btn1:
        if AuthManager.has_permission('PRODUTOS', 'EXPORTAR'):
            if st.button(f"{ICONE_PDF} PDF", use_container_width=True, key="btn_pdf_produto"):
                st.session_state.gerar_pdf_produtos = True
                st.rerun()
        else:
            st.button(f"{ICONE_PDF} PDF", disabled=True, use_container_width=True)
    
    st.markdown("---")
    
    # Listagem
    if produtos:
        st.markdown("### 📋 Lista de Produtos")
        
        col1, col2, col3, col4 = st.columns([0.5, 4, 2, 1.5])
        with col1:
            st.markdown("**ID**")
        with col2:
            st.markdown("**Nome**")
        with col3:
            st.markdown("**Preço**")
        with col4:
            st.markdown("**Ações**")
        
        st.markdown("---")
        
        can_edit = AuthManager.has_permission('PRODUTOS', 'EDITAR')
        can_delete = AuthManager.has_permission('PRODUTOS', 'EXCLUIR')
        
        for produto in produtos:
            col1, col2, col3, col4 = st.columns([0.5, 4, 2, 1.5])
            
            with col1:
                st.markdown(f"`#{produto[0]}`")
            with col2:
                st.write(produto[1])
            with col3:
                st.markdown(f"**R$ {float(produto[2]):,.2f}**")
            
            with col4:
                # Se não pode editar NEM excluir, mostrar apenas botão VER
                if not can_edit and not can_delete:
                    if st.button(
                        "👁️ Ver",
                        key=f"btn_view_produto_{produto[0]}",
                        use_container_width=True,
                        help="Ver detalhes do produto"
                    ):
                        st.session_state.visualizar_produto_id = produto[0]
                        st.rerun()
                else:
                    # Botões normais
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button(
                            f"{ICONE_EDITAR}",
                            key=f"btn_edit_produto_{produto[0]}",
                            use_container_width=True,
                            disabled=not can_edit
                        ):
                            st.session_state.editar_produto_id = produto[0]
                            st.rerun()
                    
                    with col_btn2:
                        if st.button(
                            f"{ICONE_EXCLUIR}",
                            key=f"btn_del_produto_{produto[0]}",
                            use_container_width=True,
                            type="secondary",
                            disabled=not can_delete
                        ):
                            st.session_state.excluir_produto_id = produto[0]
                            st.rerun()
            
            st.divider()
    else:
        sac.result(label='Nenhum produto encontrado', description='Ajuste os filtros', status='empty')
    
    # Modais
    if 'modal_add_produto' in st.session_state and st.session_state.modal_add_produto:
        if AuthManager.has_permission('PRODUTOS', 'CRIAR'):
            modal_adicionar_produto()
        st.session_state.modal_add_produto = False
    
    if 'editar_produto_id' in st.session_state:
        if AuthManager.has_permission('PRODUTOS', 'EDITAR'):
            modal_editar_produto(st.session_state.editar_produto_id)
        del st.session_state.editar_produto_id
    
    if 'excluir_produto_id' in st.session_state:
        if AuthManager.has_permission('PRODUTOS', 'EXCLUIR'):
            modal_confirmar_exclusao_produto(st.session_state.excluir_produto_id)
        del st.session_state.excluir_produto_id
    
    # NOVO: Modal de visualização
    if 'visualizar_produto_id' in st.session_state:
        modal_visualizar_produto(st.session_state.visualizar_produto_id)
        del st.session_state.visualizar_produto_id
    
    # PDF
    if 'gerar_pdf_produtos' in st.session_state and st.session_state.gerar_pdf_produtos:
        if AuthManager.has_permission('PRODUTOS', 'EXPORTAR'):
            with st.spinner('📄 Gerando PDF...'):
                todos_produtos = db.listar_produtos(busca, tipo_busca_db, 999999, 0)
                filtros_info = f"Busca: '{busca if busca else 'Todos'}'"
                pdf_buffer = gerar_relatorio_produtos_pdf(todos_produtos, filtros_info)
            
            st.success(f'✅ PDF gerado! {len(todos_produtos)} produto(s)')
            st.download_button(
                label="⬇️ Baixar PDF",
                data=pdf_buffer,
                file_name=f"produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            AuthManager.audit_log("EXPORTAR_PRODUTOS", "PRODUTOS", f"Exportou {len(todos_produtos)} produto(s)")
        st.session_state.pop('gerar_pdf_produtos', None)

# ==================== MODAIS ====================

@st.dialog("👁️ Detalhes do Produto")
def modal_visualizar_produto(produto_id):
    """Modal somente leitura para visualizadores"""
    
    produto = db.obter_produto(produto_id)
    if not produto:
        st.error("❌ Produto não encontrado")
        return
    
    st.markdown("### 📦 Informações do Produto")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**ID:**")
        st.info(f"`#{produto[0]}`")
        
        st.markdown("**Nome:**")
        st.success(f"**{produto[1]}**")
    
    with col2:
        st.markdown("**Preço:**")
        st.success(f"**R$ {float(produto[2]):,.2f}**")
        
        st.markdown("**Status:**")
        st.success("✅ Disponível")
    
    st.markdown("---")
    
    with st.expander("📊 Informações Adicionais", expanded=False):
        st.caption("• Cadastrado em: —")
        st.caption("• Última atualização: —")
        st.caption("• Estoque atual: —")
        st.caption("• Vendas totais: —")
    
    if st.button("✅ Fechar", use_container_width=True, type="primary"):
        st.rerun()

@st.dialog("➕ Adicionar Produto")
def modal_adicionar_produto():
    with st.form("form_add_produto"):
        nome = st.text_input("Nome *", placeholder="Nome do produto", max_chars=100)
        preco = st.number_input("Preço *", min_value=0.01, value=0.01, step=0.01, format="%.2f")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            if not nome:
                st.error("❌ Nome é obrigatório")
            elif len(nome) < 3:
                st.error("❌ Nome muito curto")
            elif preco <= 0:
                st.error("❌ Preço inválido")
            else:
                try:
                    produto_id = db.inserir_produto(nome, preco)
                    AuthManager.audit_log("CRIAR_PRODUTO", "PRODUTOS", f"Criou: {nome} (ID: {produto_id})")
                    st.success(f"✅ Produto **{nome}** criado!")
                    st.balloons()
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("✏️ Editar Produto")
def modal_editar_produto(produto_id):
    produto = db.obter_produto(produto_id)
    if not produto:
        st.error("❌ Produto não encontrado")
        return
    
    with st.form("form_edit_produto"):
        nome = st.text_input("Nome *", value=produto[1], max_chars=100)
        preco = st.number_input("Preço *", min_value=0.01, value=float(produto[2]), step=0.01, format="%.2f")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            if not nome:
                st.error("❌ Nome é obrigatório")
            elif preco <= 0:
                st.error("❌ Preço inválido")
            else:
                try:
                    db.atualizar_produto(produto_id, nome, preco)
                    AuthManager.audit_log("EDITAR_PRODUTO", "PRODUTOS", f"Editou ID: {produto_id}")
                    st.success("✅ Atualizado!")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("⚠️ Confirmar Exclusão")
def modal_confirmar_exclusao_produto(produto_id):
    produto = db.obter_produto(produto_id)
    if not produto:
        st.error("❌ Produto não encontrado")
        return
    
    st.warning("⚠️ Ação irreversível!")
    st.info(f"**ID:** {produto[0]}\n\n**Nome:** {produto[1]}\n\n**Preço:** R$ {float(produto[2]):,.2f}")
    
    confirma = st.text_input("Digite 'EXCLUIR':", placeholder="EXCLUIR", max_chars=10)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Confirmar", use_container_width=True, type="primary", disabled=(confirma != "EXCLUIR")):
            try:
                db.excluir_produto(produto_id)
                AuthManager.audit_log("EXCLUIR_PRODUTO", "PRODUTOS", f"Excluiu: {produto[1]}")
                st.success("✅ Excluído!")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()
