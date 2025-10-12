"""
Sistema CRUD - FastHTML Version
App principal
"""
from fasthtml.common import *
from starlette.staticfiles import StaticFiles
from routes import clientes
from components.layout import base_layout, navbar
import sys
import os

# Adicionar paths para importar módulos compartilhados
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.empresa import SISTEMA_NOME, SISTEMA_VERSAO, SISTEMA_SUBTITULO

# Criar app FastHTML
app, rt = fast_app(
    hdrs=(
        Script(src="https://unpkg.com/htmx.org@1.9.10"),
        Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'),
        Link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css'),
        Style("""
            /* Estilos customizados inline */
            :root {
                --primary: #3498DB;
                --success: #27AE60;
                --danger: #E74C3C;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .animate-fade-in {
                animation: fadeIn 0.3s ease-in;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .table-hover tbody tr:hover {
                background-color: rgba(52, 152, 219, 0.05);
                transition: background-color 0.2s;
            }
            
            .htmx-request {
                opacity: 0.7;
                transition: opacity 0.3s;
            }
            
            .badge {
                font-weight: 500;
            }
            
            .card {
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
            }
            
            .btn {
                transition: all 0.2s;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }
            
            .navbar-brand {
                font-size: 1.3rem;
                letter-spacing: 0.5px;
            }
            
            body {
                min-height: 100vh;
                display: flex;
                flex-column;
            }
            
            footer {
                margin-top: auto;
            }
            
            @media (max-width: 768px) {
                .table {
                    font-size: 0.9rem;
                }
                .pagination {
                    font-size: 0.85rem;
                }
            }
        """),
        Script(src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js')
    ),
    live=True,
    debug=True
)

@rt('/')
def get():
    """Página inicial"""
    return base_layout(
        navbar(),
        Div(
            Div(
                H1(f"🚀 {SISTEMA_NOME}", cls="display-4 mb-3"),
                P(SISTEMA_SUBTITULO, cls="lead text-muted mb-4"),
                P(f"Versão {SISTEMA_VERSAO}", cls="text-muted small"),
                Hr(),
                Div(
                    Div(
                        Div(
                            Div(
                                I(cls="bi bi-people-fill fs-1 text-primary mb-3"),
                                H3("Clientes", cls="card-title"),
                                P("Gerencie sua base de clientes", cls="card-text text-muted"),
                                A("Acessar →", href="/clientes", cls="btn btn-primary"),
                                cls="card-body text-center"
                            ),
                            cls="card shadow-sm h-100"
                        ),
                        cls="col-md-6 mb-4"
                    ),
                    Div(
                        Div(
                            Div(
                                I(cls="bi bi-box-seam-fill fs-1 text-success mb-3"),
                                H3("Produtos", cls="card-title"),
                                P("Controle seu estoque", cls="card-text text-muted"),
                                A("Acessar →", href="/produtos", cls="btn btn-success disabled"),
                                cls="card-body text-center"
                            ),
                            cls="card shadow-sm h-100"
                        ),
                        cls="col-md-6 mb-4"
                    ),
                    cls="row"
                ),
                cls="container mt-5"
            )
        )
    )

# Montar rotas de clientes
app.mount('/clientes', clientes.app)

if __name__ == '__main__':
    print(f"\n{'='*50}")
    print(f"🚀 {SISTEMA_NOME} v{SISTEMA_VERSAO}")
    print(f"{'='*50}")
    print(f"📍 URL: http://localhost:5001")
    print(f"📖 Clientes: http://localhost:5001/clientes")
    print(f"{'='*50}\n")
    serve(port=5001)
