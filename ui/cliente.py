"""
Interface de Gestão de Clientes
Com modal de visualização para perfil Visualizador
"""
import streamlit as st
import streamlit_antd_components as sac
import db.models as db
from datetime import datetime
from config.theme import ICONE_ADICIONAR, ICONE_EDITAR, ICONE_EXCLUIR, ICONE_PDF
from utils.pdf_generator import gerar_relatorio_clientes_pdf
from utils.validacao import validar_email
from auth.auth_manager import AuthManager
import math

def tela_cliente():
    """Tela de gestão de clientes com controle de permissões"""
    
    if not AuthManager.has_permission('CLIENTES', 'VISUALIZAR'):
        st.error("❌ Você não tem permissão para visualizar clientes")
        st.info(f"👤 Seu perfil atual: **{AuthManager.get_user_perfil()}**")
        return
    
    # Inicialização
    if 'pagina_atual_cliente' not in st.session_state:
        st.session_state.pagina_atual_cliente = 1
    if 'registros_por_pagina_cliente' not in st.session_state:
        st.session_state.registros_por_pagina_cliente = 10
    if 'tipo_busca_cliente' not in st.session_state:
        st.session_state.tipo_busca_cliente = "nome"
    
    sac.divider(label='Gestão de Clientes', icon='people-fill', align='center', color='blue')
    
    # Filtros
    st.markdown("##### 🔍 Filtros e Controles")
    col1, col2, col3, col4 = st.columns([1.5, 3.5, 1.2, 1])
    
    with col1:
        st.caption("Buscar por:")
        tipo_busca = sac.segmented(
            items=['Nome', 'Código'],
            label='',
            index=0 if st.session_state.tipo_busca_cliente == "nome" else 1,
            align='start',
            size='sm',
            key='seg_tipo_busca_cliente',
            readonly=False
        )
        if tipo_busca.lower() != st.session_state.tipo_busca_cliente:
            st.session_state.tipo_busca_cliente = tipo_busca.lower()
            st.session_state.pagina_atual_cliente = 1
        tipo_busca_db = st.session_state.tipo_busca_cliente
    
    with col2:
        st.caption("Digite para buscar:")
        placeholder = "Digite o código..." if tipo_busca == "Código" else "Digite o nome..."
        busca = st.text_input("", placeholder=placeholder, key='busca_cliente', label_visibility="collapsed")
        if 'busca_anterior_cliente' not in st.session_state:
            st.session_state.busca_anterior_cliente = ""
        if busca != st.session_state.busca_anterior_cliente:
            st.session_state.pagina_atual_cliente = 1
            st.session_state.busca_anterior_cliente = busca
    
    with col3:
        st.caption("Por página:")
        registros_label = sac.segmented(
            items=['10', '25', '50'],
            label='',
            index=[10, 25, 50].index(st.session_state.registros_por_pagina_cliente),
            size='sm',
            key='seg_registros_cliente',
            readonly=False
        )
        registros_por_pagina = int(registros_label)
        if registros_por_pagina != st.session_state.registros_por_pagina_cliente:
            st.session_state.registros_por_pagina_cliente = registros_por_pagina
            st.session_state.pagina_atual_cliente = 1
    
    with col4:
        st.caption("Ações:")
        if AuthManager.has_permission('CLIENTES', 'CRIAR'):
            if st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, type="primary", key="btn_novo_cliente"):
                st.session_state.modal_add_cliente = True
                st.rerun()
        else:
            st.button(f"{ICONE_ADICIONAR} Novo", use_container_width=True, disabled=True)
    
    st.markdown("---")
    
    # Paginação
    total_clientes = db.contar_clientes(busca, tipo_busca_db)
    total_paginas = math.ceil(total_clientes / registros_por_pagina) if total_clientes > 0 else 1
    offset = (st.session_state.pagina_atual_cliente - 1) * registros_por_pagina
    clientes = db.listar_clientes(busca, tipo_busca_db, registros_por_pagina, offset)
    
    if total_clientes > 0:
        col_info, col_pag = st.columns([1, 2])
        with col_info:
            st.markdown(f"**Total:** {total_clientes} cliente(s) | **Página** {st.session_state.pagina_atual_cliente} de {total_paginas}")
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
    
    st.markdown("---")
    
    # Ações
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    with col_btn1:
        if AuthManager.has_permission('CLIENTES', 'EXPORTAR'):
            if st.button(f"{ICONE_PDF} PDF", use_container_width=True, key="btn_pdf_cliente"):
                st.session_state.gerar_pdf_clientes = True
                st.rerun()
        else:
            st.button(f"{ICONE_PDF} PDF", disabled=True, use_container_width=True)
    
    st.markdown("---")
    
    # Listagem
    if clientes:
        st.markdown("### 📋 Lista de Clientes")
        
        col1, col2, col3, col4 = st.columns([0.5, 3, 3, 1.5])
        with col1:
            st.markdown("**ID**")
        with col2:
            st.markdown("**Nome**")
        with col3:
            st.markdown("**Email**")
        with col4:
            st.markdown("**Ações**")
        
        st.markdown("---")
        
        can_edit = AuthManager.has_permission('CLIENTES', 'EDITAR')
        can_delete = AuthManager.has_permission('CLIENTES', 'EXCLUIR')
        
        for cliente in clientes:
            col1, col2, col3, col4 = st.columns([0.5, 3, 3, 1.5])
            
            with col1:
                st.markdown(f"`#{cliente[0]}`")
            with col2:
                st.write(cliente[1])
            with col3:
                st.text(cliente[2] if cliente[2] else "—")
            
            with col4:
                # Se não pode editar NEM excluir, mostrar apenas botão VER
                if not can_edit and not can_delete:
                    if st.button(
                        "👁️ Ver",
                        key=f"btn_view_cliente_{cliente[0]}",
                        use_container_width=True,
                        help="Ver detalhes do cliente"
                    ):
                        st.session_state.visualizar_cliente_id = cliente[0]
                        st.rerun()
                else:
                    # Botões normais
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button(
                            f"{ICONE_EDITAR}",
                            key=f"btn_edit_cliente_{cliente[0]}",
                            use_container_width=True,
                            disabled=not can_edit
                        ):
                            st.session_state.editar_cliente_id = cliente[0]
                            st.rerun()
                    
                    with col_btn2:
                        if st.button(
                            f"{ICONE_EXCLUIR}",
                            key=f"btn_del_cliente_{cliente[0]}",
                            use_container_width=True,
                            type="secondary",
                            disabled=not can_delete
                        ):
                            st.session_state.excluir_cliente_id = cliente[0]
                            st.rerun()
            
            st.divider()
    else:
        sac.result(label='Nenhum cliente encontrado', description='Ajuste os filtros', status='empty')
    
    # Modais
    if 'modal_add_cliente' in st.session_state and st.session_state.modal_add_cliente:
        if AuthManager.has_permission('CLIENTES', 'CRIAR'):
            modal_adicionar_cliente()
        st.session_state.modal_add_cliente = False
    
    if 'editar_cliente_id' in st.session_state:
        if AuthManager.has_permission('CLIENTES', 'EDITAR'):
            modal_editar_cliente(st.session_state.editar_cliente_id)
        del st.session_state.editar_cliente_id
    
    if 'excluir_cliente_id' in st.session_state:
        if AuthManager.has_permission('CLIENTES', 'EXCLUIR'):
            modal_confirmar_exclusao_cliente(st.session_state.excluir_cliente_id)
        del st.session_state.excluir_cliente_id
    
    # NOVO: Modal de visualização
    if 'visualizar_cliente_id' in st.session_state:
        modal_visualizar_cliente(st.session_state.visualizar_cliente_id)
        del st.session_state.visualizar_cliente_id
    
    # PDF
    if 'gerar_pdf_clientes' in st.session_state and st.session_state.gerar_pdf_clientes:
        if AuthManager.has_permission('CLIENTES', 'EXPORTAR'):
            with st.spinner('📄 Gerando PDF...'):
                todos_clientes = db.listar_clientes(busca, tipo_busca_db, 999999, 0)
                filtros_info = f"Busca: '{busca if busca else 'Todos'}'"
                pdf_buffer = gerar_relatorio_clientes_pdf(todos_clientes, filtros_info)
            
            st.success(f'✅ PDF gerado! {len(todos_clientes)} cliente(s)')
            st.download_button(
                label="⬇️ Baixar PDF",
                data=pdf_buffer,
                file_name=f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            AuthManager.audit_log("EXPORTAR_CLIENTES", "CLIENTES", f"Exportou {len(todos_clientes)} cliente(s)")
        st.session_state.pop('gerar_pdf_clientes', None)

# ==================== MODAIS ====================

@st.dialog("👁️ Detalhes do Cliente")
def modal_visualizar_cliente(cliente_id):
    """Modal somente leitura para visualizadores"""
    
    cliente = db.obter_cliente(cliente_id)
    if not cliente:
        st.error("❌ Cliente não encontrado")
        return
    
    st.markdown("### 📋 Informações do Cliente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**ID:**")
        st.info(f"`#{cliente[0]}`")
        
        st.markdown("**Nome:**")
        st.success(f"**{cliente[1]}**")
    
    with col2:
        st.markdown("**Email:**")
        st.info(cliente[2] if cliente[2] else "Não informado")
        
        st.markdown("**Status:**")
        st.success("✅ Ativo")
    
    st.markdown("---")
    
    with st.expander("📊 Informações Adicionais", expanded=False):
        st.caption("• Cadastrado em: —")
        st.caption("• Última atualização: —")
        st.caption("• Total de pedidos: —")
    
    if st.button("✅ Fechar", use_container_width=True, type="primary"):
        st.rerun()

@st.dialog("➕ Adicionar Cliente")
def modal_adicionar_cliente():
    with st.form("form_add_cliente"):
        nome = st.text_input("Nome *", placeholder="Nome completo", max_chars=100)
        email = st.text_input("Email *", placeholder="email@exemplo.com", max_chars=100)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            if not nome or not email:
                st.error("❌ Preencha todos os campos")
            elif len(nome) < 3:
                st.error("❌ Nome muito curto")
            elif not validar_email(email):
                st.error("❌ Email inválido")
            else:
                try:
                    cliente_id = db.inserir_cliente(nome, email)
                    AuthManager.audit_log("CRIAR_CLIENTE", "CLIENTES", f"Criou: {nome} (ID: {cliente_id})")
                    st.success(f"✅ Cliente **{nome}** criado!")
                    st.balloons()
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("✏️ Editar Cliente")
def modal_editar_cliente(cliente_id):
    cliente = db.obter_cliente(cliente_id)
    if not cliente:
        st.error("❌ Cliente não encontrado")
        return
    
    with st.form("form_edit_cliente"):
        nome = st.text_input("Nome *", value=cliente[1], max_chars=100)
        email = st.text_input("Email *", value=cliente[2] or "", max_chars=100)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            if not nome or not email:
                st.error("❌ Preencha todos os campos")
            elif not validar_email(email):
                st.error("❌ Email inválido")
            else:
                try:
                    db.atualizar_cliente(cliente_id, nome, email)
                    AuthManager.audit_log("EDITAR_CLIENTE", "CLIENTES", f"Editou ID: {cliente_id}")
                    st.success("✅ Atualizado!")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("⚠️ Confirmar Exclusão")
def modal_confirmar_exclusao_cliente(cliente_id):
    cliente = db.obter_cliente(cliente_id)
    if not cliente:
        st.error("❌ Cliente não encontrado")
        return
    
    st.warning("⚠️ Ação irreversível!")
    st.info(f"**ID:** {cliente[0]}\n\n**Nome:** {cliente[1]}\n\n**Email:** {cliente[2]}")
    
    confirma = st.text_input("Digite 'EXCLUIR':", placeholder="EXCLUIR", max_chars=10)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Confirmar", use_container_width=True, type="primary", disabled=(confirma != "EXCLUIR")):
            try:
                db.excluir_cliente(cliente_id)
                AuthManager.audit_log("EXCLUIR_CLIENTE", "CLIENTES", f"Excluiu: {cliente[1]}")
                st.success("✅ Excluído!")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()
