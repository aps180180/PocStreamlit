"""
Interface de Gestão de Clientes - VERSÃO FINAL
Com labels organizados e alinhados
"""
import streamlit as st
from db.models import Cliente
from auth.auth_manager import AuthManager
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def exportar_clientes_pdf(clientes):
    """Exporta lista de clientes para PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    titulo = Paragraph("<b>Relatório de Clientes</b>", styles['Title'])
    elements.append(titulo)
    
    data = [['ID', 'Nome', 'Email', 'Telefone 1', 'Telefone 2']]
    for cliente in clientes:
        data.append([
            str(cliente[0]),
            cliente[1],
            cliente[2] or '-',
            cliente[3] or '-',
            cliente[4] or '-'
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer


def tela_cliente():
    """Renderiza tela de gestão de clientes"""
    
    if not AuthManager.has_permission('CLIENTES', 'VISUALIZAR'):
        st.error("❌ Sem permissão para visualizar clientes")
        return
    
    st.markdown("# 👥 Gestão de Clientes")
    
    # ========================================
    # LINHA 1: LABELS DOS FILTROS
    # ========================================
    col1, col2, col3, col4 = st.columns([1.5, 4, 1, 1])
    
    col1.markdown("**Buscar por**")
    col2.markdown("**Termo de busca**")
    col3.markdown("**Por página**")
    col4.markdown("**Exportar**")
    
    # ========================================
    # LINHA 2: FILTROS + PDF
    # ========================================
    with col1:
        tipo_busca = st.selectbox(
            "tipo", 
            ["Nome"], 
            key="tipo_busca_cli",
            label_visibility="collapsed"
        )
    
    with col2:
        busca = st.text_input(
            "busca", 
            placeholder="🔍 Nome do cliente...", 
            label_visibility="collapsed", 
            key="busca_cli"
        )
    
    with col3:
        registros_por_pagina = st.selectbox(
            "regs", 
            [25, 50, 100], 
            index=0, 
            label_visibility="collapsed", 
            key="reg_cli"
        )
    
    with col4:
        if AuthManager.has_permission('CLIENTES', 'EXPORTAR'):
            try:
                clientes_export = Cliente.buscar("", "nome", 9999, 0)
                if clientes_export:
                    pdf_buffer = exportar_clientes_pdf(clientes_export)
                    st.download_button(
                        label="PDF",
                        data=pdf_buffer,
                        file_name=f"clientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except:
                pass
    
    # ========================================
    # LINHA 3: BOTÃO NOVO CLIENTE
    # ========================================
    if AuthManager.has_permission('CLIENTES', 'CRIAR'):
        if st.button("➕ Novo Cliente", type="primary", use_container_width=False, key="btn_novo_cliente"):
            st.session_state.modal_add_cliente = True
            st.rerun()
    
    st.markdown("---")
    
    # ========================================
    # BUSCAR E LISTAR CLIENTES
    # ========================================
    try:
        clientes = Cliente.buscar(busca if busca else "", "nome", 9999, 0)
        total_clientes = Cliente.contar(busca if busca else "", "nome")
        
        st.caption(f"{total_clientes} cliente(s)")
        
        if clientes:
            # Paginação manual
            if 'pagina_atual_cliente' not in st.session_state:
                st.session_state.pagina_atual_cliente = 1
            
            total_paginas = (total_clientes + registros_por_pagina - 1) // registros_por_pagina
            inicio = (st.session_state.pagina_atual_cliente - 1) * registros_por_pagina
            fim = inicio + registros_por_pagina
            clientes_pagina = clientes[inicio:fim]
            
            # Cabeçalho da tabela
            col1, col2, col3, col4, col5, col6 = st.columns([0.5, 2, 2, 1.5, 1.5, 1])
            col1.markdown("**ID**")
            col2.markdown("**Nome**")
            col3.markdown("**Email**")
            col4.markdown("**Telefone 1**")
            col5.markdown("**Telefone 2**")
            col6.markdown("**Ações**")
            
            st.markdown("---")
            
            # Linhas da tabela
            for cliente in clientes_pagina:
                col1, col2, col3, col4, col5, col6 = st.columns([0.5, 2, 2, 1.5, 1.5, 1])
                
                col1.caption(f"#{cliente[0]}")
                col2.write(cliente[1])
                col3.caption(cliente[2] if cliente[2] else "—")
                col4.caption(cliente[3] if cliente[3] else "—")
                col5.caption(cliente[4] if cliente[4] else "—")
                
                with col6:
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        if AuthManager.has_permission('CLIENTES', 'EDITAR'):
                            if st.button("✏️", key=f"edit_cli_{cliente[0]}", help="Editar"):
                                st.session_state.editar_cliente_id = cliente[0]
                                st.rerun()
                    
                    with c2:
                        if AuthManager.has_permission('CLIENTES', 'EXCLUIR'):
                            if st.button("🗑️", key=f"del_cli_{cliente[0]}", help="Excluir"):
                                st.session_state.excluir_cliente_id = cliente[0]
                                st.rerun()
            
            # Paginação
            if total_paginas > 1:
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.button("⬅️ Anterior", disabled=st.session_state.pagina_atual_cliente == 1):
                        st.session_state.pagina_atual_cliente -= 1
                        st.rerun()
                
                with col2:
                    st.markdown(f"<center>Página {st.session_state.pagina_atual_cliente}/{total_paginas}</center>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("Próxima ➡️", disabled=st.session_state.pagina_atual_cliente == total_paginas):
                        st.session_state.pagina_atual_cliente += 1
                        st.rerun()
        else:
            st.info("📭 Nenhum cliente encontrado")
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar clientes: {e}")
    
    # ========================================
    # MODAIS
    # ========================================
    if st.session_state.get('modal_add_cliente'):
        modal_adicionar_cliente()
        st.session_state.modal_add_cliente = False
    
    if 'editar_cliente_id' in st.session_state:
        modal_editar_cliente(st.session_state.editar_cliente_id)
        del st.session_state.editar_cliente_id
    
    if 'excluir_cliente_id' in st.session_state:
        modal_excluir_cliente(st.session_state.excluir_cliente_id)
        del st.session_state.excluir_cliente_id


@st.dialog("➕ Novo Cliente")
def modal_adicionar_cliente():
    """Modal para adicionar cliente"""
    with st.form("form_add_cliente"):
        nome = st.text_input("Nome *", placeholder="Nome completo")
        email = st.text_input("Email", placeholder="email@exemplo.com")
        
        col1, col2 = st.columns(2)
        with col1:
            telefone1 = st.text_input("Telefone 1", placeholder="(11) 98888-7777")
        with col2:
            telefone2 = st.text_input("Telefone 2", placeholder="(11) 3333-4444")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submitted:
            if nome:
                try:
                    cliente_id = Cliente.criar(nome, email, telefone1, telefone2)
                    st.success(f"✅ Cliente '{nome}' criado! ID: {cliente_id}")
                    AuthManager.audit_log("CRIAR_CLIENTE", "CLIENTES", f"Criou cliente: {nome}")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
            else:
                st.warning("⚠️ Nome é obrigatório!")


@st.dialog("✏️ Editar Cliente")
def modal_editar_cliente(cliente_id):
    """Modal para editar cliente"""
    cliente = Cliente.find_by_id(cliente_id)
    if not cliente:
        st.error("❌ Cliente não encontrado")
        return
    
    with st.form("form_edit_cliente"):
        nome = st.text_input("Nome *", value=cliente[1])
        email = st.text_input("Email", value=cliente[2] or "")
        
        col1, col2 = st.columns(2)
        with col1:
            telefone1 = st.text_input("Telefone 1", value=cliente[3] or "")
        with col2:
            telefone2 = st.text_input("Telefone 2", value=cliente[4] or "")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submitted:
            if nome:
                try:
                    Cliente.atualizar(cliente_id, nome, email, telefone1, telefone2)
                    st.success(f"✅ Cliente '{nome}' atualizado!")
                    AuthManager.audit_log("EDITAR_CLIENTE", "CLIENTES", f"Editou cliente ID: {cliente_id}")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
            else:
                st.warning("⚠️ Nome é obrigatório!")


@st.dialog("⚠️ Excluir Cliente")
def modal_excluir_cliente(cliente_id):
    """Modal para confirmar exclusão"""
    cliente = Cliente.find_by_id(cliente_id)
    if not cliente:
        st.error("❌ Cliente não encontrado")
        return
    
    st.warning(f"⚠️ Tem certeza que deseja excluir o cliente **{cliente[1]}**?")
    st.caption("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Sim, excluir", type="primary", use_container_width=True):
            try:
                Cliente.excluir(cliente_id)
                st.success(f"✅ Cliente '{cliente[1]}' excluído!")
                AuthManager.audit_log("EXCLUIR_CLIENTE", "CLIENTES", f"Excluiu cliente: {cliente[1]}")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()
