"""
Interface de Gestão de Usuários - CRUD Completo
Inclui: Criar, Editar, Excluir e Alterar Senha
"""
import streamlit as st
from db.auth_models import (
    listar_usuarios,
    contar_usuarios,
    listar_perfis,
    obter_usuario,
    inserir_usuario,
    atualizar_usuario,
    excluir_usuario,
    excluir_usuario_permanente,  # ADICIONAR
    alterar_senha_usuario,
    verificar_login_disponivel,
    verificar_email_disponivel,
    execute_query  # ADICIONAR
)

from auth.auth_manager import AuthManager
from auth.password import hash_password, verify_password
from utils.validacao import validar_email
import math
import re

# ==================== MODAIS ====================

@st.dialog("➕ Adicionar Novo Usuário")
def modal_adicionar_usuario():
    """Modal para adicionar novo usuário"""
    
    st.markdown("Preencha os dados do novo usuário:")
    
    with st.form("form_adicionar_usuario", clear_on_submit=False):
        perfis = listar_perfis()
        perfis_dict = {f"{p[1]}": p[0] for p in perfis}
        
        col1, col2 = st.columns(2)
        
        with col1:
            login = st.text_input("Login *", placeholder="usuario123", max_chars=50)
            nome = st.text_input("Nome Completo *", placeholder="João da Silva", max_chars=100)
            senha = st.text_input("Senha *", type="password", placeholder="Mínimo 6 caracteres", max_chars=50)
        
        with col2:
            email = st.text_input("Email", placeholder="usuario@empresa.com", max_chars=100)
            perfil_nome = st.selectbox("Perfil *", options=list(perfis_dict.keys()))
            senha_confirma = st.text_input("Confirmar Senha *", type="password", max_chars=50)
        
        st.caption("* Campos obrigatórios")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            erros = []
            
            if not login or not nome or not senha or not senha_confirma:
                erros.append("❌ Preencha todos os campos obrigatórios")
            if login and len(login) < 3:
                erros.append("❌ Login deve ter pelo menos 3 caracteres")
            if login and not re.match(r'^[a-zA-Z0-9_]+$', login):
                erros.append("❌ Login: apenas letras, números e underscore")
            if senha and len(senha) < 6:
                erros.append("❌ Senha deve ter pelo menos 6 caracteres")
            if senha != senha_confirma:
                erros.append("❌ As senhas não conferem")
            if email and not validar_email(email):
                erros.append("❌ Email inválido")
            if login and not verificar_login_disponivel(login):
                erros.append("❌ Login já está em uso")
            if email and not verificar_email_disponivel(email):
                erros.append("❌ Email já está em uso")
            
            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                try:
                    senha_hash = hash_password(senha)
                    perfil_id = perfis_dict[perfil_nome]
                    usuario_id = inserir_usuario(login, nome, email, senha_hash, perfil_id)
                    
                    AuthManager.audit_log("CRIAR_USUARIO", "USUARIOS", f"Criou: {login} (ID: {usuario_id})")
                    
                    st.success(f"✅ Usuário **{login}** criado com sucesso!")
                    st.balloons()
                    
                    import time
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("✏️ Editar Usuário")
def modal_editar_usuario(usuario_id):
    """Modal para editar usuário"""
    
    usuario = obter_usuario(usuario_id)
    if not usuario:
        st.error("❌ Usuário não encontrado")
        return
    
    st.markdown(f"Editando: **{usuario[2]}** (`{usuario[1]}`)")
    
    with st.form("form_editar_usuario"):
        perfis = listar_perfis()
        perfis_dict = {f"{p[1]}": p[0] for p in perfis}
        perfil_atual = usuario[5]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Login", value=usuario[1], disabled=True)
            nome = st.text_input("Nome *", value=usuario[2], max_chars=100)
        
        with col2:
            email = st.text_input("Email", value=usuario[3] or "", max_chars=100)
            perfil_nome = st.selectbox(
                "Perfil *",
                options=list(perfis_dict.keys()),
                index=list(perfis_dict.keys()).index(perfil_atual) if perfil_atual in perfis_dict.keys() else 0
            )
        
        ativo = st.checkbox("✅ Usuário Ativo", value=(usuario[6] == 'S'))
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            erros = []
            if not nome:
                erros.append("❌ Nome é obrigatório")
            if email and not validar_email(email):
                erros.append("❌ Email inválido")
            if email and not verificar_email_disponivel(email, usuario_id):
                erros.append("❌ Email em uso")
            
            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                try:
                    perfil_id = perfis_dict[perfil_nome]
                    ativo_char = 'S' if ativo else 'N'
                    atualizar_usuario(usuario_id, nome, email, perfil_id, ativo_char)
                    
                    AuthManager.audit_log("EDITAR_USUARIO", "USUARIOS", f"Editou ID: {usuario_id}")
                    st.success("✅ Atualizado!")
                    
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("🔐 Alterar Senha")
def modal_alterar_senha(usuario_id):
    """Modal para alterar senha"""
    
    usuario = obter_usuario(usuario_id)
    if not usuario:
        st.error("❌ Usuário não encontrado")
        return
    
    is_self = usuario_id == AuthManager.get_user_id()
    st.markdown(f"Senha de: **{usuario[2]}** (`{usuario[1]}`)")
    
    with st.form("form_alterar_senha", clear_on_submit=True):
        if is_self:
            senha_atual = st.text_input("Senha Atual *", type="password")
        
        nova_senha = st.text_input("Nova Senha *", type="password", placeholder="Mínimo 6 caracteres")
        confirma_senha = st.text_input("Confirmar *", type="password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit = st.form_submit_button("🔑 Alterar", use_container_width=True, type="primary")
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submit:
            erros = []
            if is_self and not senha_atual:
                erros.append("❌ Digite senha atual")
            if not nova_senha or not confirma_senha:
                erros.append("❌ Preencha todos os campos")
            if len(nova_senha) < 6:
                erros.append("❌ Mínimo 6 caracteres")
            if nova_senha != confirma_senha:
                erros.append("❌ Senhas não conferem")
            
            if is_self and senha_atual:
                from db.auth_models import obter_usuario_por_login
                user_data = obter_usuario_por_login(st.session_state.user_login)
                if user_data and not verify_password(senha_atual, user_data[4]):
                    erros.append("❌ Senha atual incorreta")
            
            if erros:
                for erro in erros:
                    st.error(erro)
            else:
                try:
                    senha_hash = hash_password(nova_senha)
                    alterar_senha_usuario(usuario_id, senha_hash)
                    AuthManager.audit_log("ALTERAR_SENHA", "USUARIOS", f"ID: {usuario_id}")
                    st.success("✅ Senha alterada!")
                    
                    if is_self:
                        st.info("🔄 Você será desconectado")
                        import time
                        time.sleep(2)
                        AuthManager.logout()
                        st.switch_page("pages/00_Login.py")
                    else:
                        import time
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

@st.dialog("⚠️ Confirmar Exclusão")
def modal_confirmar_exclusao(usuario_id):
    """Modal de confirmação de exclusão com opções"""
    
    usuario = obter_usuario(usuario_id)
    if not usuario:
        st.error("❌ Usuário não encontrado")
        return
    
    st.warning("⚠️ Escolha o tipo de exclusão:")
    st.markdown(f"**Usuário:** {usuario[2]} (`{usuario[1]}`)")
    st.markdown(f"**Perfil:** {usuario[5]}")
    
    # Verificar se tem logs
    result = execute_query(
        "SELECT COUNT(*) FROM AUDIT_LOG WHERE USUARIO_ID = ?",
        (usuario_id,),
        fetch_one=True
    )
    total_logs = result[0] if result else 0
    
    if total_logs > 0:
        st.info(f"ℹ️ Este usuário possui **{total_logs} registro(s)** no log de auditoria")
    
    st.markdown("---")
    
    # Escolher tipo de exclusão
    tipo_exclusao = st.radio(
        "Tipo de exclusão:",
        options=[
            "🔒 Desativar usuário (Recomendado)",
            "🗑️ Excluir permanentemente (inclui logs)"
        ],
        index=0,
        help="Desativar mantém o histórico de auditoria"
    )
    
    st.markdown("---")
    
    if "Desativar" in tipo_exclusao:
        st.warning("O usuário será **DESATIVADO** mas não excluído do banco.")
        st.caption("✓ Login será bloqueado")
        st.caption("✓ Histórico de ações será mantido")
        st.caption("✓ Pode ser reativado depois")
        
        palavra_confirmacao = "DESATIVAR"
    else:
        st.error("⚠️ ATENÇÃO: Exclusão permanente!")
        st.caption(f"✗ Usuário será removido do banco")
        st.caption(f"✗ {total_logs} registro(s) de auditoria serão perdidos")
        st.caption(f"✗ Esta ação NÃO pode ser desfeita")
        
        palavra_confirmacao = "EXCLUIR"
    
    confirma = st.text_input(
        f"Digite '{palavra_confirmacao}' para confirmar:",
        placeholder=palavra_confirmacao,
        max_chars=10
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            f"✓ Confirmar {palavra_confirmacao.title()}",
            use_container_width=True,
            type="primary",
            disabled=(confirma != palavra_confirmacao)
        ):
            try:
                if "Desativar" in tipo_exclusao:
                    # Soft delete
                    excluir_usuario(usuario_id)
                    
                    AuthManager.audit_log(
                        "DESATIVAR_USUARIO",
                        "USUARIOS",
                        f"Desativou usuário: {usuario[1]} (ID: {usuario_id})"
                    )
                    
                    st.success(f"✅ Usuário **{usuario[1]}** desativado com sucesso!")
                else:
                    # Hard delete
                    excluir_usuario_permanente(usuario_id)
                    
                    AuthManager.audit_log(
                        "EXCLUIR_USUARIO_PERMANENTE",
                        "USUARIOS",
                        f"Excluiu permanentemente: {usuario[1]} (ID: {usuario_id})"
                    )
                    
                    st.success(f"✅ Usuário **{usuario[1]}** excluído permanentemente!")
                
                import time
                time.sleep(1.5)
                st.rerun()
                
            except ValueError as e:
                st.error(f"❌ {e}")
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()

# ==================== TELA PRINCIPAL ====================

def tela_usuarios():
    """Tela principal com CRUD completo"""
    
    if 'pagina_atual_usuario' not in st.session_state:
        st.session_state.pagina_atual_usuario = 1
    if 'registros_por_pagina_usuario' not in st.session_state:
        st.session_state.registros_por_pagina_usuario = 10
    if 'tipo_busca_usuario' not in st.session_state:
        st.session_state.tipo_busca_usuario = "nome"
    
    st.markdown("## 👥 Gestão de Usuários")
    st.markdown("---")
    
    # Filtros
    col1, col2, col3, col4 = st.columns([2, 4, 2, 2])
    
    with col1:
        tipo_busca = st.radio("Buscar por:", ["Nome", "Login"], horizontal=True, key='radio_tipo')
        tipo_busca_db = tipo_busca.lower()
        if tipo_busca_db != st.session_state.tipo_busca_usuario:
            st.session_state.tipo_busca_usuario = tipo_busca_db
            st.session_state.pagina_atual_usuario = 1
    
    with col2:
        busca = st.text_input("Buscar:", placeholder=f"Digite o {tipo_busca.lower()}...", key='input_busca')
        if busca and 'busca_anterior' in st.session_state and busca != st.session_state.busca_anterior:
            st.session_state.pagina_atual_usuario = 1
        st.session_state.busca_anterior = busca
    
    with col3:
        registros = st.selectbox("Por página:", [10, 25, 50], key='select_reg')
        if registros != st.session_state.registros_por_pagina_usuario:
            st.session_state.registros_por_pagina_usuario = registros
            st.session_state.pagina_atual_usuario = 1
    
    with col4:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        if AuthManager.has_permission('USUARIOS', 'CRIAR'):
            if st.button("➕ Novo", use_container_width=True, type="primary"):
                modal_adicionar_usuario()
        else:
            st.button("➕ Novo", disabled=True, use_container_width=True)
    
    st.markdown("---")
    
    # Paginação
    total = contar_usuarios(busca, tipo_busca_db)
    total_pag = math.ceil(total / registros) if total > 0 else 1
    offset = (st.session_state.pagina_atual_usuario - 1) * registros
    
    try:
        usuarios = listar_usuarios(busca, tipo_busca_db, registros, offset)
    except Exception as e:
        st.error(f"❌ Erro: {e}")
        usuarios = []
    
    if total > 0:
        col_info, col_pag = st.columns([2, 3])
        with col_info:
            st.markdown(f"**{offset+1}-{min(offset+registros, total)} de {total}** | Pág. {st.session_state.pagina_atual_usuario}/{total_pag}")
        with col_pag:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1:
                if st.button("◀ Ant.", disabled=(st.session_state.pagina_atual_usuario==1)):
                    st.session_state.pagina_atual_usuario -= 1
                    st.rerun()
            with c2:
                st.markdown(f"<div style='text-align:center;padding-top:8px;'>Pág {st.session_state.pagina_atual_usuario}</div>", unsafe_allow_html=True)
            with c3:
                if st.button("Prox. ▶", disabled=(st.session_state.pagina_atual_usuario==total_pag)):
                    st.session_state.pagina_atual_usuario += 1
                    st.rerun()
    
    st.markdown("---")
    
    # Listagem
    if usuarios:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 1.2, 2.5, 2.5, 1.5, 1, 2])
        with col1:
            st.markdown("**ID**")
        with col2:
            st.markdown("**Login**")
        with col3:
            st.markdown("**Nome**")
        with col4:
            st.markdown("**Email**")
        with col5:
            st.markdown("**Perfil**")
        with col6:
            st.markdown("**Status**")
        with col7:
            st.markdown("**Ações**")
        
        st.markdown("---")
        
        for u in usuarios:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 1.2, 2.5, 2.5, 1.5, 1, 2])
            with col1:
                st.markdown(f"`#{u[0]}`")
            with col2:
                st.write(u[1])
            with col3:
                st.write(u[2])
            with col4:
                st.text(u[3] or "—")
            with col5:
                p = u[4] if len(u) > 4 else "N/A"
                if p == 'Administrador':
                    st.markdown("🔴 **Admin**")
                elif p == 'Operador':
                    st.markdown("🟡 **Oper.**")
                else:
                    st.markdown("🔵 **Vis.**")
            with col6:
                st.markdown("✅" if (u[5] if len(u)>5 else 'N')=='S' else "❌")
            with col7:
                can_edit = AuthManager.has_permission('USUARIOS', 'EDITAR')
                can_del = AuthManager.has_permission('USUARIOS', 'EXCLUIR')
                is_self = u[0] == AuthManager.get_user_id()
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("✏️", key=f"e{u[0]}", disabled=not can_edit, help="Editar"):
                        modal_editar_usuario(u[0])
                with c2:
                    if st.button("🔑", key=f"p{u[0]}", disabled=not(is_self or can_edit), help="Senha"):
                        modal_alterar_senha(u[0])
                with c3:
                    if st.button("🗑️", key=f"d{u[0]}", type="secondary", disabled=not can_del or is_self, help="Excluir"):
                        modal_confirmar_exclusao(u[0])
            
            st.divider()
    else:
        st.info("📭 Nenhum usuário encontrado")
    
    # Footer
    st.markdown("---")
    if st.button("🔐 Alterar Minha Senha", use_container_width=False):
        modal_alterar_senha(AuthManager.get_user_id())
