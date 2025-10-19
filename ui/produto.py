"""
Interface de Gestão de Produtos - VERSÃO FINAL
Com labels organizados e botão ajustado
"""
import streamlit as st
from db.models import Produto
from auth.auth_manager import AuthManager
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def exportar_produtos_pdf(produtos):
    """Exporta lista de produtos para PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    titulo = Paragraph("<b>Relatório de Produtos</b>", styles['Title'])
    elements.append(titulo)
    
    data = [['ID', 'Nome', 'Preço']]
    for produto in produtos:
        data.append([
            str(produto[0]),
            produto[1],
            f"R$ {float(produto[2]):,.2f}"
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


def tela_produto():
    """Renderiza tela de gestão de produtos"""
    
    if not AuthManager.has_permission('PRODUTOS', 'VISUALIZAR'):
        st.error("❌ Sem permissão para visualizar produtos")
        return
    
    st.markdown("# 📦 Gestão de Produtos")
    
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
            key="tipo_busca_prod",
            label_visibility="collapsed"
        )
    
    with col2:
        busca = st.text_input(
            "busca", 
            placeholder="🔍 Nome do produto...", 
            label_visibility="collapsed", 
            key="busca_prod"
        )
    
    with col3:
        registros_por_pagina = st.selectbox(
            "regs", 
            [25, 50, 100], 
            index=0, 
            label_visibility="collapsed", 
            key="reg_prod"
        )
    
    with col4:
        if AuthManager.has_permission('PRODUTOS', 'EXPORTAR'):
            try:
                produtos_export = Produto.buscar("", "nome", 9999, 0)
                if produtos_export:
                    pdf_buffer = exportar_produtos_pdf(produtos_export)
                    st.download_button(
                        label="PDF",
                        data=pdf_buffer,
                        file_name=f"produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except:
                pass
    
    # ========================================
    # LINHA 3: BOTÃO NOVO PRODUTO
    # ========================================
    if AuthManager.has_permission('PRODUTOS', 'CRIAR'):
        if st.button("➕ Novo Produto", type="primary", use_container_width=False, key="btn_novo_produto"):
            st.session_state.modal_add_produto = True
            st.rerun()
    
    st.markdown("---")
    
    # ========================================
    # BUSCAR E LISTAR PRODUTOS
    # ========================================
    try:
        produtos = Produto.buscar(busca if busca else "", "nome", 9999, 0)
        total_produtos = Produto.contar(busca if busca else "", "nome")
        
        st.caption(f"{total_produtos} produto(s)")
        
        if produtos:
            # Paginação manual
            if 'pagina_atual_produto' not in st.session_state:
                st.session_state.pagina_atual_produto = 1
            
            total_paginas = (total_produtos + registros_por_pagina - 1) // registros_por_pagina
            inicio = (st.session_state.pagina_atual_produto - 1) * registros_por_pagina
            fim = inicio + registros_por_pagina
            produtos_pagina = produtos[inicio:fim]
            
            # Cabeçalho da tabela
            col1, col2, col3, col4 = st.columns([0.5, 4, 2, 1])
            col1.markdown("**ID**")
            col2.markdown("**Nome**")
            col3.markdown("**Preço**")
            col4.markdown("**Ações**")
            
            st.markdown("---")
            
            # Linhas da tabela
            for produto in produtos_pagina:
                col1, col2, col3, col4 = st.columns([0.5, 4, 2, 1])
                
                col1.caption(f"#{produto[0]}")
                col2.write(produto[1])
                col3.markdown(f"**R$ {float(produto[2]):,.2f}**")
                
                with col4:
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        if AuthManager.has_permission('PRODUTOS', 'EDITAR'):
                            if st.button("✏️", key=f"edit_prod_{produto[0]}", help="Editar"):
                                st.session_state.editar_produto_id = produto[0]
                                st.rerun()
                    
                    with c2:
                        if AuthManager.has_permission('PRODUTOS', 'EXCLUIR'):
                            if st.button("🗑️", key=f"del_prod_{produto[0]}", help="Excluir"):
                                st.session_state.excluir_produto_id = produto[0]
                                st.rerun()
            
            # Paginação
            if total_paginas > 1:
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.button("⬅️ Anterior", disabled=st.session_state.pagina_atual_produto == 1, key="pag_ant_prod"):
                        st.session_state.pagina_atual_produto -= 1
                        st.rerun()
                
                with col2:
                    st.markdown(f"<center>Página {st.session_state.pagina_atual_produto}/{total_paginas}</center>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("Próxima ➡️", disabled=st.session_state.pagina_atual_produto == total_paginas, key="pag_prox_prod"):
                        st.session_state.pagina_atual_produto += 1
                        st.rerun()
        else:
            st.info("📭 Nenhum produto encontrado")
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar produtos: {e}")
    
    # ========================================
    # MODAIS
    # ========================================
    if st.session_state.get('modal_add_produto'):
        modal_adicionar_produto()
        st.session_state.modal_add_produto = False
    
    if 'editar_produto_id' in st.session_state:
        modal_editar_produto(st.session_state.editar_produto_id)
        del st.session_state.editar_produto_id
    
    if 'excluir_produto_id' in st.session_state:
        modal_excluir_produto(st.session_state.excluir_produto_id)
        del st.session_state.excluir_produto_id


@st.dialog("➕ Novo Produto")
def modal_adicionar_produto():
    """Modal para adicionar produto"""
    with st.form("form_add_produto"):
        nome = st.text_input("Nome *", placeholder="Ex: Notebook Dell")
        preco = st.number_input("Preço (R$) *", min_value=0.0, step=0.01, format="%.2f")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submitted:
            if nome and preco > 0:
                try:
                    produto_id = Produto.criar(nome, preco)
                    st.success(f"✅ Produto '{nome}' criado! ID: {produto_id}")
                    AuthManager.audit_log("CRIAR_PRODUTO", "PRODUTOS", f"Criou produto: {nome}")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
            else:
                st.warning("⚠️ Preencha nome e preço!")


@st.dialog("✏️ Editar Produto")
def modal_editar_produto(produto_id):
    """Modal para editar produto"""
    produto = Produto.find_by_id(produto_id)
    if not produto:
        st.error("❌ Produto não encontrado")
        return
    
    with st.form("form_edit_produto"):
        nome = st.text_input("Nome *", value=produto[1])
        preco = st.number_input("Preço (R$) *", min_value=0.0, value=float(produto[2]), step=0.01, format="%.2f")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submitted:
            if nome and preco > 0:
                try:
                    Produto.atualizar(produto_id, nome, preco)
                    st.success(f"✅ Produto '{nome}' atualizado!")
                    AuthManager.audit_log("EDITAR_PRODUTO", "PRODUTOS", f"Editou produto ID: {produto_id}")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
            else:
                st.warning("⚠️ Preencha nome e preço!")


@st.dialog("⚠️ Excluir Produto")
def modal_excluir_produto(produto_id):
    """Modal para confirmar exclusão"""
    produto = Produto.find_by_id(produto_id)
    if not produto:
        st.error("❌ Produto não encontrado")
        return
    
    st.warning(f"⚠️ Tem certeza que deseja excluir o produto **{produto[1]}**?")
    st.caption("Esta ação não pode ser desfeita.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Sim, excluir", type="primary", use_container_width=True):
            try:
                Produto.excluir(produto_id)
                st.success(f"✅ Produto '{produto[1]}' excluído!")
                AuthManager.audit_log("EXCLUIR_PRODUTO", "PRODUTOS", f"Excluiu produto: {produto[1]}")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()
