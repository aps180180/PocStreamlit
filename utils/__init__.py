"""
Pacote de utilitários do sistema
"""
from .validacao import validar_email
from .pdf_generator import gerar_relatorio_clientes_pdf, gerar_relatorio_produtos_pdf

__all__ = [
    'validar_email',
    'gerar_relatorio_clientes_pdf',
    'gerar_relatorio_produtos_pdf'
]