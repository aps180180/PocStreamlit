"""
Configurações de tema e ícones do sistema
Define cores, ícones e estilos visuais
"""

# ==================== CORES DO TEMA ====================

COR_PRIMARIA = "#3498DB"      # Azul principal
COR_SECUNDARIA = "#2ECC71"    # Verde secundário
COR_SUCESSO = "#27AE60"       # Verde sucesso
COR_PERIGO = "#E74C3C"        # Vermelho perigo
COR_AVISO = "#F39C12"         # Laranja aviso
COR_INFO = "#3498DB"          # Azul informação
COR_FUNDO = "#FFFFFF"         # Branco fundo
COR_TEXTO = "#2C3E50"         # Cinza escuro texto
COR_BORDA = "#BDC3C7"         # Cinza borda

# ==================== ÍCONES DO SISTEMA ====================

# Ícones gerais
ICONE_HOME = "🏠"
ICONE_DASHBOARD = "📊"
ICONE_MENU = "☰"
ICONE_BUSCAR = "🔍"
ICONE_FILTRO = "🎯"

# Ícones de ações
ICONE_ADICIONAR = "➕"
ICONE_EDITAR = "✏️"
ICONE_EXCLUIR = "🗑️"
ICONE_SALVAR = "💾"
ICONE_CANCELAR = "❌"
ICONE_CONFIRMAR = "✅"

# Ícones de exportação
ICONE_PDF = "📄"
ICONE_EXCEL = "📊"
ICONE_CSV = "📋"
ICONE_IMPRIMIR = "🖨️"
ICONE_DOWNLOAD = "⬇️"

# Ícones de navegação
ICONE_ANTERIOR = "◀"
ICONE_PROXIMO = "▶"
ICONE_PRIMEIRA = "⏮"
ICONE_ULTIMA = "⏭"

# Ícones de módulos
ICONE_CLIENTES = "👥"
ICONE_PRODUTOS = "📦"
ICONE_USUARIOS = "👤"
ICONE_RELATORIOS = "📈"
ICONE_CONFIGURACOES = "⚙️"

# Ícones de status
ICONE_ATIVO = "✅"
ICONE_INATIVO = "❌"
ICONE_PENDENTE = "⏳"
ICONE_SUCESSO = "🎉"
ICONE_ERRO = "⚠️"
ICONE_INFO = "ℹ️"

# Ícones de segurança
ICONE_LOGIN = "🔐"
ICONE_LOGOUT = "🚪"
ICONE_SENHA = "🔑"
ICONE_PERFIL = "🎭"
ICONE_PERMISSAO = "🔒"

# ==================== CONFIGURAÇÕES DE TAMANHO ====================

TAMANHO_FONTE_PADRAO = "14px"
TAMANHO_FONTE_TITULO = "24px"
TAMANHO_FONTE_SUBTITULO = "18px"
TAMANHO_FONTE_PEQUENA = "12px"

# ==================== CONFIGURAÇÕES DE ESPAÇAMENTO ====================

ESPACAMENTO_PEQUENO = "0.5rem"
ESPACAMENTO_MEDIO = "1rem"
ESPACAMENTO_GRANDE = "2rem"

# ==================== CONFIGURAÇÕES DE BORDA ====================

BORDA_RAIO_PEQUENO = "3px"
BORDA_RAIO_MEDIO = "5px"
BORDA_RAIO_GRANDE = "10px"

# ==================== TEMAS PRÉ-DEFINIDOS ====================

TEMA_CLARO = {
    "primaryColor": COR_PRIMARIA,
    "backgroundColor": "#FFFFFF",
    "secondaryBackgroundColor": "#F0F2F6",
    "textColor": COR_TEXTO,
    "font": "sans serif"
}

TEMA_ESCURO = {
    "primaryColor": COR_PRIMARIA,
    "backgroundColor": "#1E1E1E",
    "secondaryBackgroundColor": "#262730",
    "textColor": "#FFFFFF",
    "font": "sans serif"
}

# ==================== MAPEAMENTO DE CORES POR STATUS ====================

CORES_STATUS = {
    "ativo": COR_SUCESSO,
    "inativo": COR_PERIGO,
    "pendente": COR_AVISO,
    "concluido": COR_SUCESSO,
    "cancelado": COR_PERIGO,
    "processando": COR_INFO
}

# ==================== MAPEAMENTO DE ÍCONES POR AÇÃO ====================

ICONES_ACOES = {
    "criar": ICONE_ADICIONAR,
    "editar": ICONE_EDITAR,
    "excluir": ICONE_EXCLUIR,
    "visualizar": "👁️",
    "exportar": ICONE_PDF,
    "imprimir": ICONE_IMPRIMIR,
    "download": ICONE_DOWNLOAD
}

# ==================== FUNÇÕES AUXILIARES ====================

def get_icone_por_acao(acao: str) -> str:
    """
    Retorna o ícone correspondente à ação
    
    Args:
        acao (str): Nome da ação
        
    Returns:
        str: Ícone correspondente
    """
    return ICONES_ACOES.get(acao.lower(), "📌")

def get_cor_por_status(status: str) -> str:
    """
    Retorna a cor correspondente ao status
    
    Args:
        status (str): Nome do status
        
    Returns:
        str: Código hexadecimal da cor
    """
    return CORES_STATUS.get(status.lower(), COR_INFO)
