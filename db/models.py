"""
Models para CLIENTES e PRODUTOS
Todas as operações de banco de dados para as entidades principais
"""
from db.connection import get_db_cursor, execute_query, get_connection

# ==================== INICIALIZAÇÃO ====================

def criar_tabelas():
    """Cria tabelas de clientes e produtos se não existirem"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Tabela CLIENTES
        cursor.execute("""
            CREATE TABLE CLIENTES (
                ID INTEGER NOT NULL PRIMARY KEY,
                NOME VARCHAR(100) NOT NULL,
                EMAIL VARCHAR(100)
            )
        """)
        print("✅ Tabela CLIENTES criada")
    except:
        pass  # Tabela já existe
    
    try:
        # Tabela PRODUTOS
        cursor.execute("""
            CREATE TABLE PRODUTOS (
                ID INTEGER NOT NULL PRIMARY KEY,
                NOME VARCHAR(100) NOT NULL,
                PRECO DECIMAL(10,2)
            )
        """)
        print("✅ Tabela PRODUTOS criada")
    except:
        pass  # Tabela já existe
    
    try:
        conn.commit()
    except:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# ==================== CLIENTES ====================

def listar_clientes(busca="", tipo_busca="nome", limit=10, offset=0):
    """
    Lista clientes com busca e paginação
    
    Args:
        busca (str): Termo de busca
        tipo_busca (str): 'nome' ou 'codigo'
        limit (int): Quantidade de registros
        offset (int): Offset para paginação
        
    Returns:
        list: Lista de tuplas (ID, NOME, EMAIL)
    """
    if tipo_busca == "nome":
        sql = """
            SELECT ID, NOME, EMAIL FROM CLIENTES 
            WHERE UPPER(NOME) LIKE UPPER(?)
            ORDER BY NOME
            ROWS ? TO ?
        """
        params = (f'%{busca}%', offset + 1, offset + limit)
    else:  # codigo
        sql = """
            SELECT ID, NOME, EMAIL FROM CLIENTES 
            WHERE CAST(ID AS VARCHAR(10)) LIKE ?
            ORDER BY NOME
            ROWS ? TO ?
        """
        params = (f'%{busca}%', offset + 1, offset + limit)
    
    return execute_query(sql, params)

def contar_clientes(busca="", tipo_busca="nome"):
    """
    Conta total de clientes
    
    Args:
        busca (str): Termo de busca
        tipo_busca (str): 'nome' ou 'codigo'
        
    Returns:
        int: Quantidade de clientes
    """
    if tipo_busca == "nome":
        sql = "SELECT COUNT(*) FROM CLIENTES WHERE UPPER(NOME) LIKE UPPER(?)"
    else:
        sql = "SELECT COUNT(*) FROM CLIENTES WHERE CAST(ID AS VARCHAR(10)) LIKE ?"
    
    result = execute_query(sql, (f'%{busca}%',), fetch_one=True)
    return result[0] if result else 0

def obter_cliente(cliente_id):
    """
    Busca cliente por ID
    
    Args:
        cliente_id (int): ID do cliente
        
    Returns:
        tuple: (ID, NOME, EMAIL) ou None
    """
    sql = "SELECT ID, NOME, EMAIL FROM CLIENTES WHERE ID = ?"
    return execute_query(sql, (cliente_id,), fetch_one=True)

def inserir_cliente(nome, email):
    """
    Insere novo cliente
    
    Args:
        nome (str): Nome do cliente
        email (str): Email do cliente
        
    Returns:
        int: ID do cliente criado
    """
    with get_db_cursor(commit=True) as cursor:
        # Gerar próximo ID
        cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM CLIENTES")
        next_id = cursor.fetchone()[0]
        
        # Inserir cliente
        cursor.execute("""
            INSERT INTO CLIENTES (ID, NOME, EMAIL) 
            VALUES (?, ?, ?)
        """, (next_id, nome, email))
        
        return next_id

def atualizar_cliente(cliente_id, nome, email):
    """
    Atualiza cliente existente
    
    Args:
        cliente_id (int): ID do cliente
        nome (str): Novo nome
        email (str): Novo email
    """
    sql = "UPDATE CLIENTES SET NOME = ?, EMAIL = ? WHERE ID = ?"
    execute_query(sql, (nome, email, cliente_id), commit=True)

def excluir_cliente(cliente_id):
    """
    Exclui cliente
    
    Args:
        cliente_id (int): ID do cliente a excluir
    """
    sql = "DELETE FROM CLIENTES WHERE ID = ?"
    execute_query(sql, (cliente_id,), commit=True)

# ==================== PRODUTOS ====================

def listar_produtos(busca="", tipo_busca="nome", limit=10, offset=0):
    """
    Lista produtos com busca e paginação
    
    Args:
        busca (str): Termo de busca
        tipo_busca (str): 'nome' ou 'codigo'
        limit (int): Quantidade de registros
        offset (int): Offset para paginação
        
    Returns:
        list: Lista de tuplas (ID, NOME, PRECO)
    """
    if tipo_busca == "nome":
        sql = """
            SELECT ID, NOME, PRECO FROM PRODUTOS 
            WHERE UPPER(NOME) LIKE UPPER(?)
            ORDER BY NOME
            ROWS ? TO ?
        """
        params = (f'%{busca}%', offset + 1, offset + limit)
    else:  # codigo
        sql = """
            SELECT ID, NOME, PRECO FROM PRODUTOS 
            WHERE CAST(ID AS VARCHAR(10)) LIKE ?
            ORDER BY NOME
            ROWS ? TO ?
        """
        params = (f'%{busca}%', offset + 1, offset + limit)
    
    return execute_query(sql, params)

def contar_produtos(busca="", tipo_busca="nome"):
    """
    Conta total de produtos
    
    Args:
        busca (str): Termo de busca
        tipo_busca (str): 'nome' ou 'codigo'
        
    Returns:
        int: Quantidade de produtos
    """
    if tipo_busca == "nome":
        sql = "SELECT COUNT(*) FROM PRODUTOS WHERE UPPER(NOME) LIKE UPPER(?)"
    else:
        sql = "SELECT COUNT(*) FROM PRODUTOS WHERE CAST(ID AS VARCHAR(10)) LIKE ?"
    
    result = execute_query(sql, (f'%{busca}%',), fetch_one=True)
    return result[0] if result else 0

def obter_produto(produto_id):
    """
    Busca produto por ID
    
    Args:
        produto_id (int): ID do produto
        
    Returns:
        tuple: (ID, NOME, PRECO) ou None
    """
    sql = "SELECT ID, NOME, PRECO FROM PRODUTOS WHERE ID = ?"
    return execute_query(sql, (produto_id,), fetch_one=True)

def inserir_produto(nome, preco):
    """
    Insere novo produto
    
    Args:
        nome (str): Nome do produto
        preco (float): Preço do produto
        
    Returns:
        int: ID do produto criado
    """
    with get_db_cursor(commit=True) as cursor:
        # Gerar próximo ID
        cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM PRODUTOS")
        next_id = cursor.fetchone()[0]
        
        # Inserir produto
        cursor.execute("""
            INSERT INTO PRODUTOS (ID, NOME, PRECO) 
            VALUES (?, ?, ?)
        """, (next_id, nome, preco))
        
        return next_id

def atualizar_produto(produto_id, nome, preco):
    """
    Atualiza produto existente
    
    Args:
        produto_id (int): ID do produto
        nome (str): Novo nome
        preco (float): Novo preço
    """
    sql = "UPDATE PRODUTOS SET NOME = ?, PRECO = ? WHERE ID = ?"
    execute_query(sql, (nome, preco, produto_id), commit=True)

def excluir_produto(produto_id):
    """
    Exclui produto
    
    Args:
        produto_id (int): ID do produto a excluir
    """
    sql = "DELETE FROM PRODUTOS WHERE ID = ?"
    execute_query(sql, (produto_id,), commit=True)

# ==================== CRUD COMPLETO DE USUÁRIOS (ATUALIZADO) ====================

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
    Desativa usuário (SOFT DELETE) ao invés de excluir
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
    
    # SOFT DELETE - Apenas desativar
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
    ATENÇÃO: Exclui também todos os logs de auditoria!
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
                raise ValueError("Não é possível excluir o último administrador do sistema")
        
        # Excluir logs PRIMEIRO
        cursor.execute("DELETE FROM AUDIT_LOG WHERE USUARIO_ID = ?", (usuario_id,))
        
        # Excluir usuário
        cursor.execute("DELETE FROM USUARIOS WHERE ID = ?", (usuario_id,))

def reativar_usuario(usuario_id):
    """
    Reativa usuário desativado
    Remove o sufixo _DELETED_ do login
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("SELECT LOGIN FROM USUARIOS WHERE ID = ?", (usuario_id,))
        result = cursor.fetchone()
        
        if not result:
            raise ValueError("Usuário não encontrado")
        
        login_atual = result[0]
        
        # Remover sufixo _DELETED_
        if "_DELETED_" in login_atual:
            login_original = login_atual.split("_DELETED_")[0]
        else:
            login_original = login_atual
        
        # Reativar
        cursor.execute("""
            UPDATE USUARIOS 
            SET ATIVO = 'S',
                LOGIN = ?
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
