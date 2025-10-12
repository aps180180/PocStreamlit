"""
Arquivo de configuração de cores e estilos do sistema
"""

# ==================== CORES DO SISTEMA ====================

# Cores principais
COR_PRIMARY = "#27AE60"  # Verde
COR_SECONDARY = "#E74C3C"  # Vermelho
COR_INFO = "#3498DB"  # Azul
COR_WARNING = "#F39C12"  # Laranja
COR_SUCCESS = "#2ECC71"  # Verde claro
COR_DANGER = "#C0392B"  # Vermelho escuro

# Cores de fundo
COR_FUNDO_DARK = "#1E1E1E"
COR_FUNDO_LIGHT = "#FFFFFF"
COR_FUNDO_CARD = "#2C3E50"

# Cores de texto
COR_TEXTO_PRIMARY = "#2C3E50"
COR_TEXTO_LIGHT = "#ECF0F1"
COR_TEXTO_MUTED = "#95A5A6"

# ==================== ÍCONES ====================

ICONE_ADICIONAR = "➕"
ICONE_EDITAR = "✏️"
ICONE_EXCLUIR = "🗑️"
ICONE_SALVAR = "💾"
ICONE_CANCELAR = "❌"
ICONE_BUSCAR = "🔍"
ICONE_CLIENTES = "people-fill"
ICONE_PRODUTOS = "bag-fill"
ICONE_RELATORIO = "📄"
ICONE_DOWNLOAD = "⬇️"


# ==================== MENSAGENS ====================

MSG_SUCESSO_ADICIONAR = "{} adicionado com sucesso!"
MSG_SUCESSO_ATUALIZAR = "{} atualizado com sucesso!"
MSG_SUCESSO_EXCLUIR = "{} excluído com sucesso!"
MSG_ERRO_CAMPO_OBRIGATORIO = "Por favor, preencha todos os campos obrigatórios."
MSG_CONFIRMAR_EXCLUSAO = "Tem certeza que deseja excluir {}?"

# ==================== CONFIGURAÇÕES DE PAGINAÇÃO ====================

OPCOES_REGISTROS_POR_PAGINA = [10, 25, 50, 100]
REGISTROS_POR_PAGINA_DEFAULT = 10

# ==================== CSS PERSONALIZADO ====================

def get_custom_css():
    """
    Retorna CSS personalizado para a aplicação
    """
    return f"""
    <style>
    /* Cabeçalhos */
    h1, h2, h3, h4 {{
        color: {COR_TEXTO_PRIMARY};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Botões primários */
    div.stButton > button[kind="primary"] {{
        background-color: {COR_PRIMARY};
        color: white;
        border-radius: 8px;
        height: 40px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }}
    
    div.stButton > button[kind="primary"]:hover {{
        background-color: #229954;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }}
    
    /* Botões secundários */
    div.stButton > button[kind="secondary"] {{
        background-color: {COR_SECONDARY};
        color: white;
        border-radius: 8px;
        height: 40px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
    }}
    
    div.stButton > button[kind="secondary"]:hover {{
        background-color: {COR_DANGER};
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }}
    
    /* Botões normais */
    div.stButton > button {{
        background-color: {COR_INFO};
        color: white;
        border-radius: 8px;
        height: 40px;
        font-weight: 600;
        transition: all 0.3s;
    }}
    
    div.stButton > button:hover {{
        background-color: #2980B9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transform: translateY(-1px);
    }}
    
    /* Inputs de texto */
    .stTextInput>div>input {{
        border-radius: 5px;
        border: 1.5px solid #BDC3C7;
        height: 40px;
        padding-left: 12px;
        transition: border-color 0.3s;
    }}
    
    .stTextInput>div>input:focus {{
        border-color: {COR_INFO};
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
    }}
    
    /* Selectbox */
    .stSelectbox>div>div {{
        border-radius: 5px;
        border: 1.5px solid #BDC3C7;
    }}
    
    /* Dividers */
    hr {{
        margin: 1rem 0;
        border-color: #ECF0F1;
    }}
    
    /* Cards */
    [data-testid="column"] {{
        padding: 0.5rem;
    }}
    
    /* Tabelas */
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* Alertas de sucesso */
    .stSuccess {{
        background-color: {COR_SUCCESS};
        color: white;
        border-radius: 5px;
        padding: 1rem;
    }}
    
    /* Alertas de erro */
    .stError {{
        background-color: {COR_SECONDARY};
        color: white;
        border-radius: 5px;
        padding: 1rem;
    }}
    
    /* Alertas de warning */
    .stWarning {{
        background-color: {COR_WARNING};
        color: white;
        border-radius: 5px;
        padding: 1rem;
    }}
    </style>
    """
