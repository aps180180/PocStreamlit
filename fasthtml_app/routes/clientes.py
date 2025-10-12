"""
Rotas para gerenciamento de clientes
"""
from fasthtml.common import *
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import db.models as db
from components.layout import base_layout, navbar

app, rt = fast_app()

@rt('/')
def get(busca: str = "", tipo: str = "nome", page: int = 1):
    """Listar clientes com busca e paginação"""
    
    # Configuração
    limit = 10
    offset = (page - 1) * limit
    tipo_db = "nome" if tipo == "nome" else "codigo"
    
    # Buscar dados
    clientes = db.listar_clientes(busca, tipo_db, limit, offset)
    total = db.contar_clientes(busca, tipo_db)
    total_pages = max(1, (total + limit - 1) // limit)
    
    return base_layout(
        navbar(),
        Div(
            # Cabeçalho
            Div(
                H2(
                    I(cls="bi bi-people-fill me-2"),
                    "Gerenciamento de Clientes",
                    cls="mb-4"
                ),
                cls="d-flex justify-content-between align-items-center"
            ),
            
            # Filtros e busca
            Div(
                Form(
                    Div(
                        # Tipo de busca
                        Div(
                            Label("Buscar por:", cls="form-label small text-muted"),
                            Select(
                                Option("Nome", value="nome", selected=(tipo=="nome")),
                                Option("Código", value="codigo", selected=(tipo=="codigo")),
                                name="tipo",
                                id="tipo-busca",
                                cls="form-select form-select-sm",
                                hx_get="/clientes",
                                hx_trigger="change",
                                hx_include="[name='busca']",
                                hx_target="#lista-clientes-wrapper"
                            ),
                            cls="col-md-2"
                        ),
                        
                        # Campo de busca
                        Div(
                            Label("Digite para buscar:", cls="form-label small text-muted"),
                            Input(
                                name="busca",
                                value=busca,
                                placeholder="Digite o nome ou código...",
                                cls="form-control form-control-sm",
                                hx_get="/clientes",
                                hx_trigger="keyup changed delay:500ms",
                                hx_include="[name='tipo']",
                                hx_target="#lista-clientes-wrapper"
                            ),
                            cls="col-md-6"
                        ),
                        
                        # Botão novo (futuro)
                        Div(
                            Label(" ", cls="form-label small d-block"),
                            Button(
                                I(cls="bi bi-plus-circle me-1"),
                                "Novo Cliente",
                                cls="btn btn-primary btn-sm",
                                disabled=True  # Será ativado na Fase 3
                            ),
                            cls="col-md-4 text-end"
                        ),
                        
                        cls="row g-2 align-items-end"
                    ),
                    cls="mb-4"
                ),
                cls="bg-light p-3 rounded shadow-sm"
            ),
            
            # Lista de clientes
            Div(
                id="lista-clientes-wrapper",
                *[clientes_list(clientes, total, page, total_pages, busca, tipo)]
            ),
            
            cls="container mt-4"
        )
    )

def clientes_list(clientes, total, page, total_pages, busca, tipo):
    """Componente de lista de clientes - REUTILIZÁVEL"""
    
    if not clientes:
        return Div(
            Div(
                I(cls="bi bi-inbox fs-1 text-muted mb-3"),
                H4("Nenhum cliente encontrado", cls="text-muted"),
                P("Tente alterar os filtros de busca", cls="text-muted small"),
                cls="text-center py-5"
            ),
            cls="alert alert-light"
        )
    
    return Div(
        # Informações
        Div(
            P(
                Strong(f"Total: {total} cliente{'s' if total != 1 else ''}"),
                Span(" | ", cls="text-muted mx-2"),
                Span(f"Página {page} de {total_pages}", cls="text-muted"),
                cls="mb-3"
            ),
            cls="d-flex justify-content-between align-items-center"
        ),
        
        # Tabela
        Div(
            Table(
                Thead(
                    Tr(
                        Th("Código", style="width: 80px"),
                        Th("Nome"),
                        Th("Email"),
                        Th("Ações", style="width: 100px", cls="text-center"),
                        cls="table-dark"
                    )
                ),
                Tbody(
                    *[cliente_row(c) for c in clientes],
                    id="lista-clientes-tbody"
                ),
                cls="table table-hover table-sm align-middle"
            ),
            cls="table-responsive shadow-sm"
        ),
        
        # Paginação
        paginacao(page, total_pages, busca, tipo) if total_pages > 1 else None
    )

def cliente_row(cliente):
    """Linha individual de cliente"""
    return Tr(
        Td(
            Span(f"#{cliente[0]}", cls="badge bg-secondary"),
        ),
        Td(Strong(cliente[1])),
        Td(
            I(cls="bi bi-envelope-fill text-muted me-1"),
            Span(cliente[2], cls="text-muted small")
        ),
        Td(
            Div(
                # Botões virão na Fase 3
                Span(
                    I(cls="bi bi-tools text-muted"),
                    cls="small text-muted"
                ),
                cls="text-center"
            )
        ),
        id=f"cliente-{cliente[0]}",
        cls="animate-fade-in"
    )

def paginacao(current_page, total_pages, busca, tipo):
    """Componente de paginação"""
    
    def page_item(num):
        is_active = num == current_page
        return Li(
            A(
                str(num),
                href=f"/clientes?page={num}&busca={busca}&tipo={tipo}",
                cls="page-link" + (" active" if is_active else ""),
                hx_get=f"/clientes?page={num}&busca={busca}&tipo={tipo}",
                hx_target="#lista-clientes-wrapper",
                hx_swap="innerHTML"
            ),
            cls="page-item" + (" active" if is_active else "")
        )
    
    # Calcular range de páginas visíveis
    start = max(1, current_page - 2)
    end = min(total_pages, current_page + 2)
    
    pages = []
    
    # Primeira página
    if start > 1:
        pages.append(page_item(1))
        if start > 2:
            pages.append(Li(Span("...", cls="page-link"), cls="page-item disabled"))
    
    # Páginas do meio
    for i in range(start, end + 1):
        pages.append(page_item(i))
    
    # Última página
    if end < total_pages:
        if end < total_pages - 1:
            pages.append(Li(Span("...", cls="page-link"), cls="page-item disabled"))
        pages.append(page_item(total_pages))
    
    return Nav(
        Ul(
            # Anterior
            Li(
                A(
                    I(cls="bi bi-chevron-left"),
                    href=f"/clientes?page={current_page-1}&busca={busca}&tipo={tipo}",
                    cls="page-link" + (" disabled" if current_page == 1 else ""),
                    hx_get=f"/clientes?page={current_page-1}&busca={busca}&tipo={tipo}",
                    hx_target="#lista-clientes-wrapper"
                ),
                cls="page-item" + (" disabled" if current_page == 1 else "")
            ),
            
            # Páginas
            *pages,
            
            # Próxima
            Li(
                A(
                    I(cls="bi bi-chevron-right"),
                    href=f"/clientes?page={current_page+1}&busca={busca}&tipo={tipo}",
                    cls="page-link" + (" disabled" if current_page == total_pages else ""),
                    hx_get=f"/clientes?page={current_page+1}&busca={busca}&tipo={tipo}",
                    hx_target="#lista-clientes-wrapper"
                ),
                cls="page-item" + (" disabled" if current_page == total_pages else "")
            ),
            
            cls="pagination pagination-sm justify-content-center mb-0"
        ),
        cls="mt-3"
    )
