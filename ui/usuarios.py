"""
Interface de Gestão de Usuários - VERSÃO DEFINITIVA
"""
import streamlit as st
from db.models import Usuario, Perfil
from auth.auth_manager import AuthManager
from auth.password import hash_password


def tela_usuarios():
    """Renderiza tela de gestão de usuários"""
    
    if not AuthManager.has_permission('USUARIOS', 'VISUALIZAR'):
        st.error("❌ Sem permissão para visualizar usuários")
        return
    
    st.markdown("# 👤 Administração de Usuários")
    
    # ========================================
    # LINHA 1: LABELS DOS FILTROS
    # ========================================
    col1, col2, col3 = st.columns([1.5, 5, 1])
    
    col1.markdown("**Buscar por**")
    col2.markdown("**Termo de busca**")
    col3.markdown("**Por página**")
    
    # ========================================
    # LINHA 2: FILTROS
    # ========================================
    with col1:
        tipo_busca = st.selectbox(
            "tipo", 
            ["Nome"], 
            key="tipo_busca_user",
            label_visibility="collapsed"
        )
    
    with col2:
        busca = st.text_input(
            "busca", 
            placeholder="🔍 Nome do usuário...", 
            label_visibility="collapsed", 
            key="busca_user"
        )
    
    with col3:
        registros_por_pagina = st.selectbox(
            "regs", 
            [25, 50, 100], 
            index=0, 
            label_visibility="collapsed", 
            key="reg_user"
        )
    
    # ========================================
    # LINHA 3: BOTÃO NOVO USUÁRIO
    # ========================================
    if AuthManager.has_permission('USUARIOS', 'CRIAR'):
        if st.button("➕ Novo Usuário", type="primary", use_container_width=False, key="btn_novo_usuario"):
            st.session_state.modal_add_usuario = True
            st.rerun()
    
    st.markdown("---")
    
    # ========================================
    # BUSCAR E LISTAR USUÁRIOS
    # ========================================
    try:
        # Usar métodos corretos: buscar(busca, limit, offset) e contar(busca)
        usuarios = Usuario.buscar(busca if busca else "", 9999, 0)
        total_usuarios = Usuario.contar(busca if busca else "")
        
        st.caption(f"{total_usuarios} usuário(s)")
        
        if usuarios:
            # Paginação manual
            if 'pagina_atual_usuario' not in st.session_state:
                st.session_state.pagina_atual_usuario = 1
            
            total_paginas = (total_usuarios + registros_por_pagina - 1) // registros_por_pagina
            inicio = (st.session_state.pagina_atual_usuario - 1) * registros_por_pagina
            fim = inicio + registros_por_pagina
            usuarios_pagina = usuarios[inicio:fim]
            
            # Cabeçalho da tabela
            col1, col2, col3, col4, col5 = st.columns([0.5, 3, 3, 2, 1])
            col1.markdown("**ID**")
            col2.markdown("**Nome**")
            col3.markdown("**Email**")
            col4.markdown("**Perfil**")
            col5.markdown("**Ações**")
            
            st.markdown("---")
            
            # Linhas da tabela
            # Estrutura: ID, NOME, EMAIL, PERFIL_ID, ATIVO, PERFIL_NOME
            for usuario in usuarios_pagina:
                col1, col2, col3, col4, col5 = st.columns([0.5, 3, 3, 2, 1])
                
                col1.caption(f"#{usuario[0]}")  # ID
                col2.write(usuario[1])  # NOME
                col3.caption(usuario[2] if usuario[2] else "—")  # EMAIL
                col4.caption(usuario[5] if len(usuario) > 5 and usuario[5] else "—")  # PERFIL_NOME
                
                with col5:
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        if AuthManager.has_permission('USUARIOS', 'EDITAR'):
                            if st.button("✏️", key=f"edit_user_{usuario[0]}", help="Editar"):
                                st.session_state.editar_usuario_id = usuario[0]
                                st.rerun()
                    
                    with c2:
                        if AuthManager.has_permission('USUARIOS', 'DESATIVAR'):
                            if st.button("🗑️", key=f"del_user_{usuario[0]}", help="Desativar"):
                                st.session_state.desativar_usuario_id = usuario[0]
                                st.rerun()
            
            # Paginação
            if total_paginas > 1:
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.button("⬅️ Anterior", disabled=st.session_state.pagina_atual_usuario == 1, key="pag_ant_user"):
                        st.session_state.pagina_atual_usuario -= 1
                        st.rerun()
                
                with col2:
                    st.markdown(f"<center>Página {st.session_state.pagina_atual_usuario}/{total_paginas}</center>", unsafe_allow_html=True)
                
                with col3:
                    if st.button("Próxima ➡️", disabled=st.session_state.pagina_atual_usuario == total_paginas, key="pag_prox_user"):
                        st.session_state.pagina_atual_usuario += 1
                        st.rerun()
        else:
            st.info("📭 Nenhum usuário encontrado")
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar usuários: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    # ========================================
    # MODAIS
    # ========================================
    if st.session_state.get('modal_add_usuario'):
        modal_adicionar_usuario()
        st.session_state.modal_add_usuario = False
    
    if 'editar_usuario_id' in st.session_state:
        modal_editar_usuario(st.session_state.editar_usuario_id)
        del st.session_state.editar_usuario_id
    
    if 'desativar_usuario_id' in st.session_state:
        modal_desativar_usuario(st.session_state.desativar_usuario_id)
        del st.session_state.desativar_usuario_id


@st.dialog("➕ Novo Usuário")
def modal_adicionar_usuario():
    """Modal para adicionar usuário"""
    # Buscar perfis
    perfis = Perfil.listar_todos()
    perfis_dict = {perfil[1]: perfil[0] for perfil in perfis}
    
    with st.form("form_add_usuario"):
        nome = st.text_input("Nome *", placeholder="Nome completo")
        email = st.text_input("Email *", placeholder="email@exemplo.com")
        senha = st.text_input("Senha *", type="password", placeholder="Mínimo 6 caracteres")
        perfil_nome = st.selectbox("Perfil *", list(perfis_dict.keys()))
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submitted:
            if nome and email and senha:
                if len(senha) < 6:
                    st.warning("⚠️ Senha deve ter no mínimo 6 caracteres!")
                else:
                    try:
                        perfil_id = perfis_dict[perfil_nome]
                        usuario_id = Usuario.criar(nome, email, senha, perfil_id)
                        st.success(f"✅ Usuário '{nome}' criado! ID: {usuario_id}")
                        AuthManager.audit_log("CRIAR_USUARIO", "USUARIOS", f"Criou usuário: {nome}")
                        import time
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios!")


@st.dialog("✏️ Editar Usuário")
def modal_editar_usuario(usuario_id):
    """Modal para editar usuário"""
    usuario = Usuario.find_by_id(usuario_id)
    if not usuario:
        st.error("❌ Usuário não encontrado")
        return
    
    # Buscar perfis
    perfis = Perfil.listar_todos()
    perfis_dict = {perfil[1]: perfil[0] for perfil in perfis}
    
    # Perfil atual
    perfil_atual = Perfil.find_by_id(usuario[4])
    perfil_atual_nome = perfil_atual[1] if perfil_atual else list(perfis_dict.keys())[0]
    
    with st.form("form_edit_usuario"):
        nome = st.text_input("Nome *", value=usuario[1])
        email = st.text_input("Email *", value=usuario[2])
        perfil_nome = st.selectbox("Perfil *", list(perfis_dict.keys()), 
                                   index=list(perfis_dict.keys()).index(perfil_atual_nome) if perfil_atual_nome in perfis_dict else 0)
        
        st.caption("💡 Deixe em branco para manter a senha atual")
        nova_senha = st.text_input("Nova Senha", type="password", placeholder="Deixe vazio para não alterar")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar", type="primary", use_container_width=True)
        with col_btn2:
            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.rerun()
        
        if submitted:
            if nome and email:
                try:
                    perfil_id = perfis_dict[perfil_nome]
                    
                    # Atualizar dados básicos
                    Usuario.atualizar(usuario_id, nome, email, perfil_id)
                    
                    # Atualizar senha se fornecida
                    if nova_senha:
                        if len(nova_senha) < 6:
                            st.warning("⚠️ Senha deve ter no mínimo 6 caracteres!")
                            return
                        Usuario.atualizar_senha(usuario_id, nova_senha)
                    
                    st.success(f"✅ Usuário '{nome}' atualizado!")
                    AuthManager.audit_log("EDITAR_USUARIO", "USUARIOS", f"Editou usuário ID: {usuario_id}")
                    import time
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro: {e}")
            else:
                st.warning("⚠️ Preencha nome e email!")


@st.dialog("⚠️ Desativar Usuário")
def modal_desativar_usuario(usuario_id):
    """Modal para confirmar desativação"""
    usuario = Usuario.find_by_id(usuario_id)
    if not usuario:
        st.error("❌ Usuário não encontrado")
        return
    
    st.warning(f"⚠️ Tem certeza que deseja desativar o usuário **{usuario[1]}**?")
    st.caption("O usuário não poderá mais fazer login no sistema.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Sim, desativar", type="primary", use_container_width=True):
            try:
                Usuario.desativar(usuario_id)
                st.success(f"✅ Usuário '{usuario[1]}' desativado!")
                AuthManager.audit_log("DESATIVAR_USUARIO", "USUARIOS", f"Desativou usuário: {usuario[1]}")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro: {e}")
    
    with col2:
        if st.button("❌ Cancelar", use_container_width=True):
            st.rerun()
