"""
Configuração do Menu Hierárquico
Sistema escalável e baseado em permissões
"""

# Estrutura hierárquica do menu
# Cada item pode ter: label, icon, page (arquivo), permission_module, permission_action, children
MENU_STRUCTURE = [
    {
        "label": "Dashboard",
        "icon": "📊",
        "page": None,  # None = página principal (app.py)
        "permission_module": None,
        "permission_action": None
    },
    {
        "label": "Cadastros",
        "icon": "📋",
        "permission_module": None,
        "permission_action": None,
        "children": [
            {
                "label": "Clientes",
                "icon": "👥",
                "page": "pages/20_Clientes.py",
                "permission_module": "CLIENTES",
                "permission_action": "VISUALIZAR"
            },
            {
                "label": "Produtos",
                "icon": "📦",
                "page": "pages/21_Produtos.py",
                "permission_module": "PRODUTOS",
                "permission_action": "VISUALIZAR"
            },
            # Espaço para expandir:
            # {
            #     "label": "Fornecedores",
            #     "icon": "🏭",
            #     "page": "pages/22_Fornecedores.py",
            #     "permission_module": "FORNECEDORES",
            #     "permission_action": "VISUALIZAR"
            # },
        ]
    },
    {
        "label": "Movimentação",
        "icon": "💰",
        "permission_module": None,
        "permission_action": None,
        "children": [
            # Preparado para expansão:
            # {
            #     "label": "Vendas",
            #     "icon": "💵",
            #     "page": "pages/30_Vendas.py",
            #     "permission_module": "VENDAS",
            #     "permission_action": "VISUALIZAR"
            # },
            # {
            #     "label": "Compras",
            #     "icon": "🛒",
            #     "page": "pages/31_Compras.py",
            #     "permission_module": "COMPRAS",
            #     "permission_action": "VISUALIZAR"
            # },
        ]
    },
    {
        "label": "Relatórios",
        "icon": "📈",
        "permission_module": None,
        "permission_action": None,
        "children": [
            # Preparado para expansão:
            # {
            #     "label": "Vendas por Período",
            #     "icon": "📊",
            #     "page": "pages/40_Relatorio_Vendas.py",
            #     "permission_module": "RELATORIOS",
            #     "permission_action": "VISUALIZAR"
            # },
        ]
    },
    {
        "label": "Configurações",
        "icon": "⚙️",
        "permission_module": None,
        "permission_action": None,
        "children": [
            {
                "label": "Usuários",
                "icon": "👤",
                "page": "pages/99_Usuarios.py",
                "permission_module": "USUARIOS",
                "permission_action": "VISUALIZAR"
            },
            # Preparado para expansão:
            # {
            #     "label": "Parâmetros",
            #     "icon": "🔧",
            #     "page": "pages/98_Parametros.py",
            #     "permission_module": "CONFIGURACOES",
            #     "permission_action": "EDITAR"
            # },
        ]
    }
]


def get_menu_structure():
    """Retorna estrutura do menu"""
    return MENU_STRUCTURE


def get_flat_menu_items():
    """
    Retorna lista plana de todos os itens do menu (sem hierarquia)
    Útil para busca e indexação
    """
    items = []
    
    def extract_items(menu_list, parent_label=""):
        for item in menu_list:
            item_copy = item.copy()
            item_copy['parent'] = parent_label
            items.append(item_copy)
            
            if 'children' in item and item['children']:
                extract_items(item['children'], item['label'])
    
    extract_items(MENU_STRUCTURE)
    return items
