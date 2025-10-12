"""
Configurações da empresa e informações do sistema
"""

# ==================== INFORMAÇÕES DO SISTEMA ====================

SISTEMA_NOME = "Simple ERP"
SISTEMA_NOME_COMPLETO = "Sistema de Cadastro, Relatório, Atualização e Deleção"
SISTEMA_SUBTITULO = "Gestão de Clientes e Produtos"
SISTEMA_VERSAO = "1.0.0"
SISTEMA_DESENVOLVEDOR = "Softlive Soluções em Software"

# ==================== INFORMAÇÕES DA EMPRESA ====================

EMPRESA_NOME = "Sua Empresa Ltda"
EMPRESA_RAZAO_SOCIAL = "Sua Empresa Desenvolvimento de Software Ltda"
EMPRESA_NOME_FANTASIA = "Sua Empresa"

# Endereço
EMPRESA_ENDERECO = "Rua Exemplo, 123"
EMPRESA_BAIRRO = "Centro"
EMPRESA_CIDADE = "São Paulo"
EMPRESA_ESTADO = "SP"
EMPRESA_CEP = "01234-567"
EMPRESA_PAIS = "Brasil"

# Contatos
EMPRESA_TELEFONE = "(11) 3333-4444"
EMPRESA_CELULAR = "(11) 98765-4321"
EMPRESA_EMAIL = "contato@suaempresa.com.br"
EMPRESA_EMAIL_SUPORTE = "suporte@suaempresa.com.br"
EMPRESA_SITE = "www.suaempresa.com.br"

# Dados Fiscais
EMPRESA_CNPJ = "00.000.000/0001-00"
EMPRESA_INSCRICAO_ESTADUAL = "000.000.000.000"
EMPRESA_INSCRICAO_MUNICIPAL = "000000000"

# Redes Sociais (opcional)
EMPRESA_LINKEDIN = "linkedin.com/company/suaempresa"
EMPRESA_INSTAGRAM = "@suaempresa"
EMPRESA_FACEBOOK = "facebook.com/suaempresa"

# ==================== CONFIGURAÇÕES DE RELATÓRIOS PDF ====================

# Metadados dos PDFs
PDF_AUTOR = SISTEMA_NOME
PDF_CRIADOR = f"{SISTEMA_NOME} v{SISTEMA_VERSAO}"
PDF_PRODUTOR = EMPRESA_NOME

# Assuntos dos relatórios
PDF_ASSUNTO_CLIENTES = "Relatório de Clientes"
PDF_ASSUNTO_PRODUTOS = "Relatório de Produtos"

# Configurações de exibição no PDF
PDF_MOSTRAR_LOGO = False  # Se True, tenta carregar logo do arquivo
PDF_LOGO_PATH = "assets/logo.png"  # Caminho para o logo (se existir)
PDF_MOSTRAR_DADOS_EMPRESA = True  # Mostrar dados da empresa no cabeçalho
PDF_MOSTRAR_RODAPE_COMPLETO = True  # Rodapé com todas as informações

# ==================== FUNÇÕES AUXILIARES ====================

def get_endereco_completo():
    """Retorna endereço formatado completo"""
    return f"{EMPRESA_ENDERECO}, {EMPRESA_BAIRRO} - {EMPRESA_CIDADE}/{EMPRESA_ESTADO} - CEP: {EMPRESA_CEP}"

def get_contatos_formatados():
    """Retorna string com todos os contatos"""
    return f"Tel: {EMPRESA_TELEFONE} | Cel: {EMPRESA_CELULAR} | E-mail: {EMPRESA_EMAIL}"

def get_dados_fiscais():
    """Retorna dados fiscais formatados"""
    return f"CNPJ: {EMPRESA_CNPJ} | IE: {EMPRESA_INSCRICAO_ESTADUAL}"

def get_info_sistema():
    """Retorna informações do sistema formatadas"""
    return f"{SISTEMA_NOME} v{SISTEMA_VERSAO} - {SISTEMA_DESENVOLVEDOR}"
