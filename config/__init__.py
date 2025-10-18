"""
Módulo de configurações
Centraliza importações de configurações do sistema
"""
from .empresa import (
    SISTEMA_NOME,
    SISTEMA_VERSAO,
    SISTEMA_SUBTITULO,
    EMPRESA_NOME,
    EMPRESA_CNPJ,
    EMPRESA_ENDERECO,
    EMPRESA_CIDADE,
    EMPRESA_CEP,
    EMPRESA_TELEFONE,
    EMPRESA_EMAIL,
    EMPRESA_SITE,
    BANCO_HOST,
    BANCO_CAMINHO,
    BANCO_USER,
    BANCO_PASSWORD,
    BANCO_CHARSET
)

from .theme import (
    COR_PRIMARIA,          # CORRIGIDO (era COR_PRIMARY)
    COR_SECUNDARIA,        # CORRIGIDO (era COR_SECONDARY)
    COR_SUCESSO,
    COR_PERIGO,
    COR_AVISO,
    COR_INFO,
    COR_FUNDO,
    COR_TEXTO,
    COR_BORDA,
    ICONE_ADICIONAR,
    ICONE_EDITAR,
    ICONE_EXCLUIR,
    ICONE_PDF,
    ICONE_CLIENTES,
    ICONE_PRODUTOS,
    ICONE_USUARIOS
)

__all__ = [
    # Empresa
    'SISTEMA_NOME',
    'SISTEMA_VERSAO',
    'SISTEMA_SUBTITULO',
    'EMPRESA_NOME',
    'EMPRESA_CNPJ',
    'EMPRESA_ENDERECO',
    'EMPRESA_CIDADE',
    'EMPRESA_CEP',
    'EMPRESA_TELEFONE',
    'EMPRESA_EMAIL',
    'EMPRESA_SITE',
    
    # Banco de dados
    'BANCO_HOST',
    'BANCO_CAMINHO',
    'BANCO_USER',
    'BANCO_PASSWORD',
    'BANCO_CHARSET',
    
    # Cores
    'COR_PRIMARIA',
    'COR_SECUNDARIA',
    'COR_SUCESSO',
    'COR_PERIGO',
    'COR_AVISO',
    'COR_INFO',
    'COR_FUNDO',
    'COR_TEXTO',
    'COR_BORDA',
    
    # Ícones
    'ICONE_ADICIONAR',
    'ICONE_EDITAR',
    'ICONE_EXCLUIR',
    'ICONE_PDF',
    'ICONE_CLIENTES',
    'ICONE_PRODUTOS',
    'ICONE_USUARIOS'
]
