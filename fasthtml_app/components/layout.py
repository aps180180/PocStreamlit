"""
Componentes de layout base
"""
from fasthtml.common import *
from .styles import get_custom_styles  # ADICIONAR
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config.empresa import SISTEMA_NOME, SISTEMA_VERSAO
from datetime import datetime

def navbar():
    """Barra de navegação principal"""
    return Nav(
        Div(
            A(
                SISTEMA_NOME,
                href="/",
                cls="navbar-brand fw-bold"
            ),
            Button(
                Span(cls="navbar-toggler-icon"),
                cls="navbar-toggler",
                type="button",
                **{
                    'data-bs-toggle': 'collapse',
                    'data-bs-target': '#navbarNav'
                }
            ),
            Div(
                Ul(
                    Li(
                        A("Dashboard", href="/", cls="nav-link"),
                        cls="nav-item"
                    ),
                    Li(
                        A(
                            I(cls="bi bi-people-fill me-1"),
                            "Clientes",
                            href="/clientes",
                            cls="nav-link"
                        ),
                        cls="nav-item"
                    ),
                    Li(
                        A(
                            I(cls="bi bi-box-seam-fill me-1"),
                            "Produtos",
                            href="/produtos",
                            cls="nav-link disabled"
                        ),
                        cls="nav-item"
                    ),
                    cls="navbar-nav me-auto"
                ),
                Span(
                    f"v{SISTEMA_VERSAO}",
                    cls="navbar-text text-muted small"
                ),
                cls="collapse navbar-collapse",
                id="navbarNav"
            ),
            cls="container-fluid"
        ),
        cls="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4"
    )

def base_layout(*content):
    """Layout base da aplicação"""
    ano_atual = datetime.now().year
    
    return Html(
        Head(
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Title(f"{SISTEMA_NOME} - FastHTML"),
            Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'),
            Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css'),
            get_custom_styles(),  # ADICIONAR CSS CUSTOMIZADO
            Script(src="https://unpkg.com/htmx.org@1.9.10"),
            Script(src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js')
        ),
        Body(
            *content,
            Footer(
                Div(
                    Hr(cls="mt-5"),
                    P(
                        f"© {ano_atual} {SISTEMA_NOME} - Desenvolvido com FastHTML + Python",
                        cls="text-center text-muted small"
                    ),
                    cls="container"
                ),
                cls="mt-auto py-3"
            ),
            cls="d-flex flex-column min-vh-100"
        )
    )
