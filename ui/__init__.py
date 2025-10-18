"""
Módulo UI - Interfaces do usuário
"""
from .cliente import tela_cliente
from .produto import tela_produto
from .dashboard import tela_dashboard
from .usuarios import tela_usuarios

__all__ = [
    'tela_cliente',
    'tela_produto', 
    'tela_dashboard',
    'tela_usuarios'
]
