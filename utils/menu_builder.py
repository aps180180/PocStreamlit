"""
Builder do Menu Hierárquico
Constrói menu baseado em permissões do usuário
"""
import streamlit as st
from config.menu_config import get_menu_structure
from auth.auth_manager import AuthManager


class MenuBuilder:
    """Construtor de menu hierárquico"""
    
    @staticmethod
    def build_sidebar_menu():
        """
        Constrói menu lateral hierárquico
        Filtra itens baseado em permissões do usuário
        """
        if not AuthManager.is_authenticated():
            return
        
        menu_structure = get_menu_structure()
        
        st.markdown("### 🧭 Menu")
        
        for item in menu_structure:
            MenuBuilder._render_menu_item(item)
    
    @staticmethod
    def _render_menu_item(item, level=0):
        """
        Renderiza item do menu (recursivo para subitens)
        """
        # Verificar permissão
        if not MenuBuilder._has_permission(item):
            return
        
        # Se tem filhos, renderizar como expander
        if 'children' in item and item['children']:
            # Filtrar filhos com permissão
            visible_children = [
                child for child in item['children']
                if MenuBuilder._has_permission(child)
            ]
            
            # Só mostrar grupo se tiver filhos visíveis
            if not visible_children:
                return
            
            # Renderizar grupo com expander
            with st.expander(f"{item['icon']} **{item['label']}**", expanded=True):
                for child in visible_children:
                    MenuBuilder._render_menu_item(child, level + 1)
        
        else:
            # Item final (folha) - renderizar como botão
            label = f"{item['icon']} {item['label']}"
            
            # Usar chave única para evitar conflitos
            button_key = f"menu_{item['label'].lower().replace(' ', '_')}_{level}"
            
            if st.button(label, use_container_width=True, key=button_key):
                if item.get('page'):
                    st.switch_page(item['page'])
                else:
                    # Dashboard (página principal)
                    st.switch_page("app.py")
    
    @staticmethod
    def _has_permission(item):
        """Verifica se usuário tem permissão para ver o item"""
        # Se não especificou permissão, é público (ou grupo)
        if not item.get('permission_module') or not item.get('permission_action'):
            return True
        
        # Verificar permissão específica
        return AuthManager.has_permission(
            item['permission_module'],
            item['permission_action']
        )
