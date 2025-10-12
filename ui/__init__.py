"""
Módulo de interfaces do usuário
"""
from .cliente import tela_cliente
from .produto import tela_produto
from .dashboard import tela_dashboard  # ADICIONAR

__all__ = ['tela_cliente', 'tela_produto', 'tela_dashboard']
