"""
Modelos de autenticação usando conexão centralizada
"""
from db.connection import get_db_cursor, execute_query, get_connection

def criar_tabelas_auth():
    """Cria tabelas de autenticação"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Tabela de Perfis
        cursor.execute("""
            CREATE TABLE PERFIS (
                ID INTEGER NOT NULL PRIMARY KEY,
                NOME VARCHAR(50) NOT NULL,
                DESCRICAO VARCHAR(200),
                ATIVO CHAR(1) DEFAULT 'S',
                DATA_CADASTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT UQ_PERFIS_NOME UNIQUE (NOME)
            )
        """)
        print("✅ Tabela PERFIS criada")
    except:
        pass
    
    try:
        # Tabela de Usuários
        cursor.execute("""
            CREATE TABLE USUARIOS (
                ID INTEGER NOT NULL PRIMARY KEY,
                LOGIN VARCHAR(50) NOT NULL,
                NOME VARCHAR(100) NOT NULL,
                EMAIL VARCHAR(100),
                SENHA VARCHAR(255) NOT NULL,
                PERFIL_ID INTEGER NOT NULL,
                ATIVO CHAR(1) DEFAULT 'S',
                PRIMEIRO_ACESSO CHAR(1) DEFAULT 'S',
                ULTIMO_LOGIN TIMESTAMP,
                DATA_CADASTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT UQ_USUARIOS_LOGIN UNIQUE (LOGIN),
                CONSTRAINT FK_USUARIOS_PERFIL FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID)
            )
        """)
        print("✅ Tabela USUARIOS criada")
    except:
        pass
    
    try:
        # Tabela de Permissões
        cursor.execute("""
            CREATE TABLE PERMISSOES (
                ID INTEGER NOT NULL PRIMARY KEY,
                MODULO VARCHAR(50) NOT NULL,
                ACAO VARCHAR(50) NOT NULL,
                DESCRICAO VARCHAR(200),
                CONSTRAINT UQ_PERMISSOES_MODULO_ACAO UNIQUE (MODULO, ACAO)
            )
        """)
        print("✅ Tabela PERMISSOES criada")
    except:
        pass
    
    try:
        # Tabela de Perfis x Permissões
        cursor.execute("""
            CREATE TABLE PERFIS_PERMISSOES (
                PERFIL_ID INTEGER NOT NULL,
                PERMISSAO_ID INTEGER NOT NULL,
                PRIMARY KEY (PERFIL_ID, PERMISSAO_ID),
                CONSTRAINT FK_PP_PERFIL FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID),
                CONSTRAINT FK_PP_PERMISSAO FOREIGN KEY (PERMISSAO_ID) REFERENCES PERMISSOES(ID)
            )
        """)
        print("✅ Tabela PERFIS_PERMISSOES criada")
    except:
        pass
    
    try:
        # Tabela de Auditoria
        cursor.execute("""
            CREATE TABLE AUDIT_LOG (
                ID INTEGER NOT NULL PRIMARY KEY,
                USUARIO_ID INTEGER NOT NULL,
                ACAO VARCHAR(100) NOT NULL,
                MODULO VARCHAR(50),
                DETALHES VARCHAR(500),
                IP VARCHAR(50),
                DATA_HORA TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT FK_AUDIT_USUARIO FOREIGN KEY (USUARIO_ID) REFERENCES USUARIOS(ID)
            )
        """)
        print("✅ Tabela AUDIT_LOG criada")
    except:
        pass
    
    try:
        conn.commit()
        inserir_dados_iniciais()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar tabelas de autenticação: {e}")
    finally:
        cursor.close()
        conn.close()

def inserir_dados_iniciais():
    """Insere perfis, permissões e usuário admin padrão"""
    result = execute_query("SELECT COUNT(*) FROM PERFIS", fetch_one=True)
    if result and result[0] > 0:
        print("ℹ️  Dados iniciais de autenticação já existem")
        return
    
    with get_db_cursor(commit=True) as cursor:
        print("📝 Inserindo dados iniciais de autenticação...")
        
        # Inserir Perfis
        cursor.execute("INSERT INTO PERFIS (ID, NOME, DESCRICAO) VALUES (1, 'Administrador', 'Acesso total ao sistema')")
        cursor.execute("INSERT INTO PERFIS (ID, NOME, DESCRICAO) VALUES (2, 'Operador', 'Acesso para criar, editar e visualizar')")
        cursor.execute("INSERT INTO PERFIS (ID, NOME, DESCRICAO) VALUES (3, 'Visualizador', 'Acesso somente leitura')")
        
        # Inserir Permissões
        permissoes = [
            (1, 'CLIENTES', 'VISUALIZAR', 'Ver lista de clientes'),
            (2, 'CLIENTES', 'CRIAR', 'Criar novos clientes'),
            (3, 'CLIENTES', 'EDITAR', 'Editar clientes existentes'),
            (4, 'CLIENTES', 'EXCLUIR', 'Excluir clientes'),
            (5, 'CLIENTES', 'EXPORTAR', 'Exportar relatórios de clientes'),
            (6, 'PRODUTOS', 'VISUALIZAR', 'Ver lista de produtos'),
            (7, 'PRODUTOS', 'CRIAR', 'Criar novos produtos'),
            (8, 'PRODUTOS', 'EDITAR', 'Editar produtos existentes'),
            (9, 'PRODUTOS', 'EXCLUIR', 'Excluir produtos'),
            (10, 'PRODUTOS', 'EXPORTAR', 'Exportar relatórios de produtos'),
            (11, 'USUARIOS', 'VISUALIZAR', 'Ver lista de usuários'),
            (12, 'USUARIOS', 'CRIAR', 'Criar novos usuários'),
            (13, 'USUARIOS', 'EDITAR', 'Editar usuários'),
            (14, 'USUARIOS', 'EXCLUIR', 'Excluir usuários'),
            (15, 'DASHBOARD', 'VISUALIZAR', 'Acessar dashboard'),
        ]
        
        for perm in permissoes:
            cursor.execute("INSERT INTO PERMISSOES (ID, MODULO, ACAO, DESCRICAO) VALUES (?, ?, ?, ?)", perm)
        
        # Administrador tem todas as permissões
        for perm_id in range(1, 16):
            cursor.execute("INSERT INTO PERFIS_PERMISSOES (PERFIL_ID, PERMISSAO_ID) VALUES (1, ?)", (perm_id,))
        
        # Operador
        operador_perms = [1, 2, 3, 5, 6, 7, 8, 10, 15]
        for perm_id in operador_perms:
            cursor.execute("INSERT INTO PERFIS_PERMISSOES (PERFIL_ID, PERMISSAO_ID) VALUES (2, ?)", (perm_id,))
        
        # Visualizador
        visualizador_perms = [1, 5, 6, 10, 15]
        for perm_id in visualizador_perms:
            cursor.execute("INSERT INTO PERFIS_PERMISSOES (PERFIL_ID, PERMISSAO_ID) VALUES (3, ?)", (perm_id,))
        
        # Criar usuário admin
        from auth.password import hash_password
        senha_hash = hash_password("admin123")
        
        cursor.execute("""
            INSERT INTO USUARIOS (ID, LOGIN, NOME, EMAIL, SENHA, PERFIL_ID, ATIVO, PRIMEIRO_ACESSO) 
            VALUES (1, 'admin', 'Administrador', 'admin@sistema.com', ?, 1, 'S', 'N')
        """, (senha_hash,))
        
        print("✅ Dados iniciais inseridos!")
        print("ℹ️  Usuário: admin / Senha: admin123")

# ==================== USUÁRIOS ====================

def listar_usuarios(busca="", tipo_busca="nome", limit=10, offset=0):
    """Lista usuários com busca e paginação"""
    if tipo_busca == "nome":
        sql = """
            SELECT u.ID, u.LOGIN, u.NOME, u.EMAIL, p.NOME, u.ATIVO, u.ULTIMO_LOGIN
            FROM USUARIOS u
            LEFT JOIN PERFIS p ON u.PERFIL_ID = p.ID
            WHERE UPPER(u.NOME) LIKE UPPER(?)
            ORDER BY u.NOME
            ROWS ? TO ?
        """
    else:
        sql = """
            SELECT u.ID, u.LOGIN, u.NOME, u.EMAIL, p.NOME, u.ATIVO, u.ULTIMO_LOGIN
            FROM USUARIOS u
            LEFT JOIN PERFIS p ON u.PERFIL_ID = p.ID
            WHERE UPPER(u.LOGIN) LIKE UPPER(?)
            ORDER BY u.NOME
            ROWS ? TO ?
        """
    
    return execute_query(sql, (f'%{busca}%', offset + 1, offset + limit))

def contar_usuarios(busca="", tipo_busca="nome"):
    """Conta total de usuários"""
    if tipo_busca == "nome":
        sql = "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(NOME) LIKE UPPER(?)"
    else:
        sql = "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(LOGIN) LIKE UPPER(?)"
    
    result = execute_query(sql, (f'%{busca}%',), fetch_one=True)
    return result[0] if result else 0

def obter_usuario(usuario_id):
    """Busca usuário por ID"""
    sql = """
        SELECT u.ID, u.LOGIN, u.NOME, u.EMAIL, u.PERFIL_ID, p.NOME, u.ATIVO
        FROM USUARIOS u
        LEFT JOIN PERFIS p ON u.PERFIL_ID = p.ID
        WHERE u.ID = ?
    """
    return execute_query(sql, (usuario_id,), fetch_one=True)

def obter_usuario_por_login(login):
    """Busca usuário por login"""
    sql = """
        SELECT u.ID, u.LOGIN, u.NOME, u.EMAIL, u.SENHA, u.PERFIL_ID, p.NOME, u.ATIVO
        FROM USUARIOS u
        LEFT JOIN PERFIS p ON u.PERFIL_ID = p.ID
        WHERE UPPER(u.LOGIN) = UPPER(?) AND u.ATIVO = 'S'
    """
    return execute_query(sql, (login,), fetch_one=True)

def atualizar_ultimo_login(usuario_id):
    """Atualiza timestamp do último login"""
    sql = "UPDATE USUARIOS SET ULTIMO_LOGIN = CURRENT_TIMESTAMP WHERE ID = ?"
    execute_query(sql, (usuario_id,), commit=True)

def listar_perfis():
    """Lista todos os perfis ativos"""
    sql = "SELECT ID, NOME, DESCRICAO FROM PERFIS WHERE ATIVO = 'S' ORDER BY NOME"
    return execute_query(sql)

def verificar_permissao(usuario_id, modulo, acao):
    """Verifica se usuário tem permissão específica"""
    sql = """
        SELECT COUNT(*) 
        FROM USUARIOS u
        JOIN PERFIS_PERMISSOES pp ON u.PERFIL_ID = pp.PERFIL_ID
        JOIN PERMISSOES p ON pp.PERMISSAO_ID = p.ID
        WHERE u.ID = ? AND p.MODULO = ? AND p.ACAO = ? AND u.ATIVO = 'S'
    """
    result = execute_query(sql, (usuario_id, modulo, acao), fetch_one=True)
    return result[0] > 0 if result else False

def listar_permissoes_usuario(usuario_id):
    """Lista todas as permissões de um usuário"""
    sql = """
        SELECT p.MODULO, p.ACAO, p.DESCRICAO
        FROM USUARIOS u
        JOIN PERFIS_PERMISSOES pp ON u.PERFIL_ID = pp.PERFIL_ID
        JOIN PERMISSOES p ON pp.PERMISSAO_ID = p.ID
        WHERE u.ID = ? AND u.ATIVO = 'S'
        ORDER BY p.MODULO, p.ACAO
    """
    return execute_query(sql, (usuario_id,))

def registrar_audit_log(usuario_id, acao, modulo=None, detalhes=None, ip=None):
    """Registra ação no log de auditoria"""
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM AUDIT_LOG")
            next_id = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO AUDIT_LOG (ID, USUARIO_ID, ACAO, MODULO, DETALHES, IP)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (next_id, usuario_id, acao, modulo, detalhes, ip))
    except Exception as e:
        print(f"Erro ao registrar audit log: {e}")

def listar_audit_log(limit=50, offset=0):
    """Lista últimos registros de auditoria"""
    sql = """
        SELECT a.ID, u.NOME, a.ACAO, a.MODULO, a.DETALHES, a.IP, a.DATA_HORA
        FROM AUDIT_LOG a
        LEFT JOIN USUARIOS u ON a.USUARIO_ID = u.ID
        ORDER BY a.DATA_HORA DESC
        ROWS ? TO ?
    """
    return execute_query(sql, (offset + 1, offset + limit))

# ==================== CRUD COMPLETO ====================

def inserir_usuario(login, nome, email, senha, perfil_id):
    """Insere novo usuário"""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("SELECT COUNT(*) FROM USUARIOS WHERE UPPER(LOGIN) = UPPER(?)", (login,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Login já está em uso")
        
        if email:
            cursor.execute("SELECT COUNT(*) FROM USUARIOS WHERE UPPER(EMAIL) = UPPER(?)", (email,))
            if cursor.fetchone()[0] > 0:
                raise ValueError("Email já está em uso")
        
        cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM USUARIOS")
        next_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO USUARIOS (ID, LOGIN, NOME, EMAIL, SENHA, PERFIL_ID, ATIVO, PRIMEIRO_ACESSO)
            VALUES (?, ?, ?, ?, ?, ?, 'S', 'S')
        """, (next_id, login, nome, email, senha, perfil_id))
        
        return next_id

def atualizar_usuario(usuario_id, nome, email, perfil_id, ativo):
    """Atualiza dados do usuário"""
    with get_db_cursor(commit=True) as cursor:
        if email:
            cursor.execute(
                "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(EMAIL) = UPPER(?) AND ID != ?",
                (email, usuario_id)
            )
            if cursor.fetchone()[0] > 0:
                raise ValueError("Email já está em uso por outro usuário")
        
        cursor.execute("""
            UPDATE USUARIOS 
            SET NOME = ?, EMAIL = ?, PERFIL_ID = ?, ATIVO = ?
            WHERE ID = ?
        """, (nome, email, perfil_id, ativo, usuario_id))

def alterar_senha_usuario(usuario_id, senha_hash):
    """Altera senha do usuário"""
    sql = """
        UPDATE USUARIOS 
        SET SENHA = ?, PRIMEIRO_ACESSO = 'N'
        WHERE ID = ?
    """
    execute_query(sql, (senha_hash, usuario_id), commit=True)

def excluir_usuario(usuario_id):
    """
    Desativa usuário (SOFT DELETE)
    Mantém integridade referencial com AUDIT_LOG
    """
    with get_db_cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM USUARIOS u
            JOIN PERFIS p ON u.PERFIL_ID = p.ID
            WHERE p.NOME = 'Administrador' AND u.ATIVO = 'S'
        """)
        total_admins = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT p.NOME FROM USUARIOS u
            JOIN PERFIS p ON u.PERFIL_ID = p.ID
            WHERE u.ID = ?
        """, (usuario_id,))
        result = cursor.fetchone()
        
        if result and result[0] == 'Administrador' and total_admins <= 1:
            raise ValueError("Não é possível excluir o último administrador do sistema")
    
    sql = """
        UPDATE USUARIOS 
        SET ATIVO = 'N',
            LOGIN = LOGIN || '_DELETED_' || CAST(ID AS VARCHAR(10))
        WHERE ID = ?
    """
    execute_query(sql, (usuario_id,), commit=True)

def excluir_usuario_permanente(usuario_id):
    """
    Exclui usuário permanentemente (HARD DELETE)
    ATENÇÃO: Exclui também todos os logs!
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM USUARIOS u
            JOIN PERFIS p ON u.PERFIL_ID = p.ID
            WHERE p.NOME = 'Administrador' AND u.ATIVO = 'S'
        """)
        total_admins = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT p.NOME, u.ATIVO FROM USUARIOS u
            JOIN PERFIS p ON u.PERFIL_ID = p.ID
            WHERE u.ID = ?
        """, (usuario_id,))
        result = cursor.fetchone()
        
        if result:
            perfil_nome = result[0]
            is_ativo = result[1] == 'S'
            
            if perfil_nome == 'Administrador' and is_ativo and total_admins <= 1:
                raise ValueError("Não é possível excluir o último administrador")
        
        # Excluir logs PRIMEIRO
        cursor.execute("DELETE FROM AUDIT_LOG WHERE USUARIO_ID = ?", (usuario_id,))
        
        # Excluir usuário
        cursor.execute("DELETE FROM USUARIOS WHERE ID = ?", (usuario_id,))

def reativar_usuario(usuario_id):
    """Reativa usuário desativado"""
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("SELECT LOGIN FROM USUARIOS WHERE ID = ?", (usuario_id,))
        result = cursor.fetchone()
        
        if not result:
            raise ValueError("Usuário não encontrado")
        
        login_atual = result[0]
        
        if "_DELETED_" in login_atual:
            login_original = login_atual.split("_DELETED_")[0]
        else:
            login_original = login_atual
        
        cursor.execute("""
            UPDATE USUARIOS 
            SET ATIVO = 'S', LOGIN = ?
            WHERE ID = ?
        """, (login_original, usuario_id))

def listar_usuarios_inativos(busca="", limit=50):
    """Lista usuários desativados"""
    sql = """
        SELECT u.ID, u.LOGIN, u.NOME, u.EMAIL, p.NOME, u.DATA_CADASTRO
        FROM USUARIOS u
        LEFT JOIN PERFIS p ON u.PERFIL_ID = p.ID
        WHERE u.ATIVO = 'N' AND UPPER(u.NOME) LIKE UPPER(?)
        ORDER BY u.DATA_CADASTRO DESC
        ROWS ? TO ?
    """
    return execute_query(sql, (f'%{busca}%', 1, limit))

def verificar_login_disponivel(login, usuario_id=None):
    """Verifica se login está disponível"""
    if usuario_id:
        sql = "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(LOGIN) = UPPER(?) AND ID != ?"
        result = execute_query(sql, (login, usuario_id), fetch_one=True)
    else:
        sql = "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(LOGIN) = UPPER(?)"
        result = execute_query(sql, (login,), fetch_one=True)
    
    return result[0] == 0 if result else False

def verificar_email_disponivel(email, usuario_id=None):
    """Verifica se email está disponível"""
    if not email:
        return True
    
    if usuario_id:
        sql = "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(EMAIL) = UPPER(?) AND ID != ?"
        result = execute_query(sql, (email, usuario_id), fetch_one=True)
    else:
        sql = "SELECT COUNT(*) FROM USUARIOS WHERE UPPER(EMAIL) = UPPER(?)"
        result = execute_query(sql, (email,), fetch_one=True)
    
    return result[0] == 0 if result else False
