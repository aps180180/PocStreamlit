"""
Estilos CSS da aplicação
"""
from fasthtml.common import Style

def get_custom_styles():
    """Retorna tag Style com CSS customizado"""
    return Style("""
        /* ==================== VARIÁVEIS ==================== */
        :root {
            --primary: #3498DB;
            --success: #27AE60;
            --danger: #E74C3C;
            --warning: #F39C12;
            --dark: #2C3E50;
            --light: #ECF0F1;
        }
        
        /* ==================== ANIMAÇÕES ==================== */
        @keyframes fadeIn {
            from { 
                opacity: 0; 
                transform: translateY(10px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.3s ease-in;
        }
        
        .animate-slide-in {
            animation: slideIn 0.4s ease-out;
        }
        
        /* ==================== GERAL ==================== */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-column;
        }
        
        footer {
            margin-top: auto;
        }
        
        /* ==================== NAVBAR ==================== */
        .navbar-brand {
            font-size: 1.3rem;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        
        .nav-link {
            transition: color 0.2s;
        }
        
        .nav-link:hover {
            color: var(--primary) !important;
        }
        
        /* ==================== CARDS ==================== */
        .card {
            transition: all 0.3s ease;
            border: none;
        }
        
        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15) !important;
        }
        
        /* ==================== TABELAS ==================== */
        .table-hover tbody tr {
            transition: all 0.2s;
        }
        
        .table-hover tbody tr:hover {
            background-color: rgba(52, 152, 219, 0.08);
            transform: scale(1.01);
        }
        
        .table thead th {
            border-bottom: 2px solid var(--dark) !important;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }
        
        /* ==================== BADGES ==================== */
        .badge {
            font-weight: 500;
            padding: 0.4em 0.6em;
        }
        
        /* ==================== BOTÕES ==================== */
        .btn {
            transition: all 0.2s;
            font-weight: 500;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, #2980B9 100%);
            border: none;
        }
        
        .btn-success {
            background: linear-gradient(135deg, var(--success) 0%, #229954 100%);
            border: none;
        }
        
        .btn-danger {
            background: linear-gradient(135deg, var(--danger) 0%, #C0392B 100%);
            border: none;
        }
        
        /* ==================== FORMULÁRIOS ==================== */
        .form-control:focus,
        .form-select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
        }
        
        /* ==================== PAGINAÇÃO ==================== */
        .pagination {
            gap: 0.25rem;
        }
        
        .page-link {
            border-radius: 0.375rem !important;
            transition: all 0.2s;
            border: 1px solid #dee2e6;
        }
        
        .page-link:hover {
            background-color: var(--primary);
            color: white;
            border-color: var(--primary);
            transform: scale(1.05);
        }
        
        .page-item.active .page-link {
            background-color: var(--dark);
            border-color: var(--dark);
        }
        
        /* ==================== HTMX LOADING ==================== */
        .htmx-request {
            opacity: 0.6;
            transition: opacity 0.3s;
            pointer-events: none;
        }
        
        .htmx-swapping {
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .htmx-settling {
            opacity: 1;
            transition: opacity 0.3s;
        }
        
        /* ==================== ALERTAS ==================== */
        .alert {
            border-radius: 0.5rem;
            border: none;
        }
        
        /* ==================== RESPONSIVO ==================== */
        @media (max-width: 768px) {
            .table {
                font-size: 0.85rem;
            }
            
            .pagination {
                font-size: 0.85rem;
            }
            
            .card {
                margin-bottom: 1rem;
            }
            
            .btn {
                font-size: 0.9rem;
            }
        }
        
        /* ==================== UTILITÁRIOS ==================== */
        .shadow-sm {
            box-shadow: 0 0.125rem 0.5rem rgba(0,0,0,0.075) !important;
        }
        
        .shadow {
            box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15) !important;
        }
        
        /* ==================== SCROLLBAR CUSTOMIZADO ==================== */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    """)
