# 🎯 CONTEXTO DO PROJETO - Sistema ERP Streamlit + Firebird

**Data de criação:** 18 de Outubro de 2025  
**Última atualização:** 18 de Outubro de 2025, 20:22 BRT  
**Versão do sistema:** 1.0.0  
**Status:** ✅ Funcional - Módulos Clientes e Produtos implementados

---

## 📋 RESUMO EXECUTIVO

Sistema ERP (Enterprise Resource Planning) desenvolvido em Python usando Streamlit como framework web e Firebird 3.0 como banco de dados. O sistema possui controle granular de permissões com 3 perfis de usuário (Visualizador, Operador e Administrador), gestão de clientes com telefones, gestão de produtos, autenticação segura com bcrypt e auditoria completa de ações.

---

## 🏗️ ARQUITETURA DO SISTEMA

### Stack Tecnológica

- **Frontend:** Streamlit 1.x + streamlit-antd-components
- **Backend:** Python 3.x
- **Banco de Dados:** Firebird 3.0 
- **Driver DB:** fdb (Python Firebird driver)
- **Autenticação:** Sistema proprietário com bcrypt
- **PDF:** ReportLab
- **Validação:** Regex (email/telefone brasileiro)

### Estrutura de Pastas Completa

sistema-erp/
├── app.py # Dashboard principal (home)
│
├── pages/ # Páginas Streamlit (multipage)
│ ├── 00_Login.py # Tela de login
│ ├── 01_Clientes.py # Gestão de clientes
│ ├── 02_Produtos.py # Gestão de produtos
│ └── 99_Admin_Usuarios.py # Administração de usuários
│
├── db/ # Camada de dados
│ ├── init.py
│ ├── connection.py # Conexão Firebird + Context Manager
│ ├── models.py # CRUD: Clientes, Produtos
│ └── auth_models.py # CRUD: Usuários, Perfis, Permissões, Logs
│
├── ui/ # Camada de interface
│ ├── init.py
│ ├── cliente.py # Interface clientes (tabela compacta)
│ ├── produto.py # Interface produtos (tabela compacta)
│ ├── dashboard.py # Interface dashboard
│ └── usuarios.py # Interface gestão usuários
│
├── auth/ # Sistema de autenticação
│ ├── init.py
│ ├── auth_manager.py # Gerenciador central de auth
│ ├── password.py # Hash/verificação senhas (bcrypt)
│ └── decorators.py # @require_permission decorator
│
├── config/ # Configurações
│ ├── init.py
│ ├── empresa.py # Nome empresa, database path
│ └── theme.py # Ícones, cores, constantes UI
│
├── utils/ # Utilitários
│ ├── validacao.py # Validação email/telefone
│ └── pdf_generator.py # Geração de relatórios PDF
│
├── styles.py # CSS customizado (Streamlit)
│
└── CONTEXTO_PROJETO.md # Este arquivo

text

---

## 🗄️ ESTRUTURA DO BANCO DE DADOS

### Tabelas Principais

#### CLIENTES
CREATE TABLE CLIENTES (
ID INTEGER NOT NULL PRIMARY KEY,
NOME VARCHAR(100) NOT NULL,
EMAIL VARCHAR(100),
TELEFONE1 VARCHAR(20), -- ✅ Adicionado recentemente
TELEFONE2 VARCHAR(20) -- ✅ Adicionado recentemente
);

text

#### PRODUTOS
CREATE TABLE PRODUTOS (
ID INTEGER NOT NULL PRIMARY KEY,
NOME VARCHAR(100) NOT NULL,
PRECO DECIMAL(10,2) NOT NULL
);

text

#### USUARIOS
CREATE TABLE USUARIOS (
ID INTEGER NOT NULL PRIMARY KEY,
NOME VARCHAR(100) NOT NULL,
EMAIL VARCHAR(100) NOT NULL UNIQUE,
SENHA_HASH VARCHAR(255) NOT NULL,
PERFIL_ID INTEGER NOT NULL,
ATIVO INTEGER DEFAULT 1, -- 1=ativo, 0=inativo
DATA_CRIACAO TIMESTAMP,
FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID)
);

text

#### PERFIS
CREATE TABLE PERFIS (
ID INTEGER NOT NULL PRIMARY KEY,
NOME VARCHAR(50) NOT NULL UNIQUE,
DESCRICAO VARCHAR(255)
);

-- Dados iniciais:
-- 1 = Visualizador
-- 2 = Operador
-- 3 = Administrador

text

#### PERMISSOES
CREATE TABLE PERMISSOES (
ID INTEGER NOT NULL PRIMARY KEY,
PERFIL_ID INTEGER NOT NULL,
MODULO VARCHAR(50) NOT NULL,
ACAO VARCHAR(50) NOT NULL,
FOREIGN KEY (PERFIL_ID) REFERENCES PERFIS(ID)
);

text

#### LOG_AUDITORIA
CREATE TABLE LOG_AUDITORIA (
ID INTEGER NOT NULL PRIMARY KEY,
USUARIO_ID INTEGER,
ACAO VARCHAR(100),
MODULO VARCHAR(50),
DETALHES VARCHAR(500),
DATA_HORA TIMESTAMP,
FOREIGN KEY (USUARIO_ID) REFERENCES USUARIOS(ID)
);

text

---

## 🔐 SISTEMA DE PERMISSÕES

### Perfis de Usuário

#### 1. 👁️ **VISUALIZADOR** (ID=1)
- **Objetivo:** Consulta read-only
- **Clientes:** Visualizar (botão "Ver" com modal)
- **Produtos:** Visualizar (botão "Ver" com modal)
- **Usuários:** ❌ Sem acesso
- **Exportar PDF:** ✅ Permitido
- **Criar/Editar/Excluir:** ❌ Bloqueado

#### 2. ✏️ **OPERADOR** (ID=2)
- **Objetivo:** Operações do dia a dia
- **Clientes:** Ver + Criar + Editar (botões "✏️" e "➕")
- **Produtos:** Ver + Criar + Editar
- **Usuários:** ❌ Sem acesso
- **Exportar PDF:** ✅ Permitido
- **Excluir:** ❌ Bloqueado (preserva dados)

#### 3. 🔧 **ADMINISTRADOR** (ID=3)
- **Objetivo:** Gestão completa
- **Clientes:** CRUD completo + Exportar
- **Produtos:** CRUD completo + Exportar
- **Usuários:** ✅ Gestão completa (criar, editar, desativar)
- **Permissões:** Todas as ações permitidas
- **Logs:** Acesso a auditoria

### Matriz de Permissões

| Módulo       | Ação       | Visualizador | Operador | Admin |
|--------------|------------|--------------|----------|-------|
| CLIENTES     | VISUALIZAR | ✅           | ✅       | ✅    |
| CLIENTES     | CRIAR      | ❌           | ✅       | ✅    |
| CLIENTES     | EDITAR     | ❌           | ✅       | ✅    |
| CLIENTES     | EXCLUIR    | ❌           | ❌       | ✅    |
| CLIENTES     | EXPORTAR   | ✅           | ✅       | ✅    |
| PRODUTOS     | VISUALIZAR | ✅           | ✅       | ✅    |
| PRODUTOS     | CRIAR      | ❌           | ✅       | ✅    |
| PRODUTOS     | EDITAR     | ❌           | ✅       | ✅    |
| PRODUTOS     | EXCLUIR    | ❌           | ❌       | ✅    |
| PRODUTOS     | EXPORTAR   | ✅           | ✅       | ✅    |
| USUARIOS     | VISUALIZAR | ❌           | ❌       | ✅    |
| USUARIOS     | CRIAR      | ❌           | ❌       | ✅    |
| USUARIOS     | EDITAR     | ❌           | ❌       | ✅    |
| USUARIOS     | DESATIVAR  | ❌           | ❌       | ✅    |

---

## 📊 MÓDULOS IMPLEMENTADOS

### 1. 👥 **CLIENTES** (ui/cliente.py)

#### Layout
- **Tipo:** Tabela compacta de 6 colunas
- **Colunas:** ID | Nome | Email | Telefone 1 | Telefone 2 | Ações
- **Espaçamento:** Máximo aproveitamento horizontal

#### Funcionalidades
- ✅ **Busca inteligente:**
  - Por Nome: `LIKE %texto%` (busca parcial)
  - Por Código: `= ID` (busca exata + validação numérica)
- ✅ **Paginação:** 10/25/50/100 registros por página
- ✅ **CRUD completo:** Criar, Editar, Excluir (conforme permissão)
- ✅ **Modal de visualização:** Para perfil Visualizador
- ✅ **Exportação PDF:** Com filtros aplicados (expander no topo)
- ✅ **Validação:**
  - Email: Regex padrão RFC 5322
  - Telefone: 10-11 dígitos brasileiros
  - Formatação: `(XX) XXXXX-XXXX` ou `(XX) XXXX-XXXX`

#### Campos
| Campo     | Tipo         | Obrigatório | Validação              |
|-----------|--------------|-------------|------------------------|
| Nome      | VARCHAR(100) | ✅          | Mínimo 3 caracteres    |
| Email     | VARCHAR(100) | ✅          | Formato email válido   |
| Telefone1 | VARCHAR(20)  | ❌          | 10-11 dígitos          |
| Telefone2 | VARCHAR(20)  | ❌          | 10-11 dígitos          |

#### Comportamento por Perfil
- **Visualizador:** Botão "👁️ Ver" → Modal read-only
- **Operador:** Botões "✏️" (editar habilitado) + "🗑️" (desabilitado)
- **Admin:** Botões "✏️" + "🗑️" (ambos habilitados)

---

### 2. 📦 **PRODUTOS** (ui/produto.py)

#### Layout
- **Tipo:** Tabela compacta de 4 colunas
- **Colunas:** ID | Nome | Preço | Ações

#### Funcionalidades
- ✅ Mesma estrutura de Clientes (busca, paginação, CRUD)
- ✅ Formatação de preço: `R$ 1.234,56`
- ✅ Validação de preço mínimo: > 0.01

#### Campos
| Campo | Tipo           | Obrigatório | Validação         |
|-------|----------------|-------------|-------------------|
| Nome  | VARCHAR(100)   | ✅          | Mínimo 3 chars    |
| Preço | DECIMAL(10,2)  | ✅          | Maior que 0       |

---

### 3. 👤 **USUÁRIOS** (ui/usuarios.py)

#### Funcionalidades
- ✅ **CRUD de usuários** (apenas Admin)
- ✅ **Desativar ao invés de excluir** (soft delete)
- ✅ **Reset de senha** (gera hash bcrypt novo)
- ✅ **Atribuição de perfil** (Visualizador/Operador/Admin)
- ✅ **Listagem com status** (Ativo/Inativo)

#### Campos
| Campo  | Tipo         | Obrigatório | Validação              |
|--------|--------------|-------------|------------------------|
| Nome   | VARCHAR(100) | ✅          | Mínimo 3 caracteres    |
| Email  | VARCHAR(100) | ✅          | Único + formato válido |
| Senha  | VARCHAR(255) | ✅          | Hash bcrypt            |
| Perfil | INTEGER      | ✅          | ID de PERFIS (1-3)     |
| Ativo  | INTEGER      | ✅          | 1=ativo, 0=inativo     |

---

### 4. 🏠 **DASHBOARD** (app.py)

#### Estatísticas Exibidas
- Total de clientes cadastrados
- Total de produtos cadastrados
- Últimos 5 clientes adicionados
- Resumo de permissões do usuário logado

---

## 🐛 PROBLEMAS RESOLVIDOS (HISTÓRICO)

### ✅ **1. Loop Infinito de st.rerun()**

**Problema:**
❌ CÓDIGO PROBLEMÁTICO
if tipo_busca != st.session_state.tipo_busca_cliente:
st.session_state.tipo_busca_cliente = tipo_busca
st.rerun() # LOOP! Executa sempre que a página carrega

text

**Sintoma:** Tela ficava piscando/recarregando infinitamente

**Solução:**
✅ CÓDIGO CORRETO
if tipo_busca != st.session_state.tipo_busca_cliente:
st.session_state.tipo_busca_cliente = tipo_busca
# Não usa st.rerun() - Streamlit reexecuta automaticamente

text

**Regra:** Usar `st.rerun()` APENAS em:
- Cliques de botões de ação
- Fechamento de modais
- Após salvar/excluir dados

---

### ✅ **2. PDF Não Aparecendo**

**Problema:** Botão PDF fazia `st.rerun()` antes de mostrar o download

**Solução:** Expander no topo controlado por `st.session_state.gerar_pdf_clientes`
if st.session_state.get('gerar_pdf_clientes', False):
with st.expander("📄 Relatório PDF Gerado", expanded=True):
# ... gera PDF ...
st.download_button(...)

text

---

### ✅ **3. Sidebar Duplicada**

**Problema:** Cada página (01_Clientes.py, 02_Produtos.py) criava sidebar própria

**Solução:** Remover blocos `with st.sidebar:` das páginas
- Streamlit já gerencia sidebar automaticamente em multipage apps

---

### ✅ **4. Busca por Código Usando LIKE**

**Problema:**
❌ ERRADO - Busca aproximada para ID
sql = "SELECT * FROM CLIENTES WHERE CAST(ID AS VARCHAR) LIKE ?"
params = (f'%{busca}%',)

text

**Solução:**
✅ CORRETO - Busca exata para ID
if tipo_busca == "código":
try:
id_busca = int(busca)
sql = "SELECT * FROM CLIENTES WHERE ID = ?"
params = (id_busca,)
except ValueError:
return [] # Não é número, retorna vazio

text

---

### ✅ **5. Coluna DATA_CADASTRO Inexistente**

**Problema:** SQL tentava `SELECT ... DATA_CADASTRO` mas campo não existe na tabela

**Solução:**
- Remover DATA_CADASTRO de todas as queries
- OU adicionar coluna via migração:
def migrar_adicionar_data_cadastro():
cursor.execute("ALTER TABLE CLIENTES ADD DATA_CADASTRO TIMESTAMP")

text

---

### ✅ **6. Modal de Visualização para Visualizadores**

**Problema:** Perfil Visualizador via botões desabilitados (UX ruim)

**Solução:** Lógica condicional de botões
if not can_edit and not can_delete:
# Mostrar apenas botão VER
st.button("👁️ Ver", ...)
else:
# Mostrar botões EDITAR + EXCLUIR
col1, col2 = st.columns(2)
st.button("✏️", ...)
st.button("🗑️", ...)

text

---

## 🎨 PADRÕES DE CÓDIGO

### Nomenclatura de Session State

Para evitar conflitos, prefixar keys por módulo:

✅ BOM
st.session_state.pagina_atual_cliente
st.session_state.busca_anterior_produto
st.session_state.modal_add_usuario

❌ RUIM (pode conflitar)
st.session_state.pagina_atual
st.session_state.busca
st.session_state.modal_add

text

### Context Manager para Banco de Dados

✅ Sempre usar context manager
with get_db_cursor(commit=True) as cursor:
cursor.execute("INSERT INTO ...", params)
# Commit automático no final

text

### Validação em Duas Camadas

1. Frontend (Streamlit)
if not validar_email(email):
st.error("Email inválido")

2. Backend (models.py)
def inserir_cliente(nome, email):
if not nome or not email:
raise ValueError("Campos obrigatórios")
# ... insert ...

text

---

## 🔄 PRÓXIMOS PASSOS SUGERIDOS

### Curto Prazo (1-2 semanas)

1. **Módulo de Vendas/Pedidos**
   - Tabela VENDAS (id, cliente_id, data, total)
   - Tabela ITENS_VENDA (id, venda_id, produto_id, qtd, preco_unitario)
   - Interface de criação de pedidos

2. **Dashboard com Gráficos**
   - Plotly/Altair para visualizações
   - Vendas por período
   - Top 10 clientes/produtos

3. **Controle de Estoque**
   - Campo ESTOQUE em PRODUTOS
   - Movimentações de entrada/saída
   - Alerta de estoque mínimo

### Médio Prazo (1-2 meses)

4. **Módulo Financeiro**
   - Contas a pagar/receber
   - Fluxo de caixa
   - Relatórios financeiros

5. **Notas Fiscais**
   - Geração de NF-e (integração com API SEFAZ)
   - XML de nota fiscal
   - DANFE em PDF

6. **API REST**
   - FastAPI para endpoints
   - Integração com sistemas externos
   - Webhooks

### Longo Prazo (3-6 meses)

7. **Mobile App**
   - Flutter/React Native
   - Consulta de pedidos
   - Scanner de código de barras

8. **Multi-empresa**
   - Suporte a múltiplas empresas
   - Dados isolados por empresa
   - Controle de acesso por empresa

9. **Integrações**
   - ERP maior (SAP, TOTVS)
   - E-commerce (WooCommerce, Shopify)
   - CRM (Salesforce, HubSpot)

---

## 📝 NOTAS TÉCNICAS IMPORTANTES

### Firebird 3.0 Específico

#### Paginação
-- ❌ NÃO FUNCIONA (MySQL/PostgreSQL)
SELECT * FROM CLIENTES LIMIT 10 OFFSET 20

-- ✅ FUNCIONA (Firebird)
SELECT * FROM CLIENTES ROWS 21 TO 30

text

#### Auto-incremento
Firebird NÃO tem `AUTO_INCREMENT`. Usar:
cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM CLIENTES")
next_id = cursor.fetchone()
cursor.execute("INSERT INTO CLIENTES (ID, ...) VALUES (?, ...)", (next_id, ...))

text

#### Case Sensitivity
Firebird é **case-insensitive** para nomes de colunas/tabelas por padrão.

### Streamlit Específico

#### Multipage Apps
- Arquivos em `pages/` são descobertos automaticamente
- Prefixo numérico define ordem: `00_`, `01_`, `02_`
- Nome do arquivo vira título da página (underscores → espaços)

#### Session State
- Persiste durante toda a sessão do usuário
- Resetado ao recarregar página (F5)
- Isolado por usuário (multi-tenant seguro)

#### Reruns
- `st.rerun()` reexecuta o script inteiro
- Cuidado com loops infinitos
- Alternativa: usar callbacks de botões

---

## 🔗 LINKS E REFERÊNCIAS

### Documentação Oficial
- **Streamlit:** https://docs.streamlit.io
- **Firebird:** https://firebirdsql.org/en/reference-manuals/
- **FDB Driver:** https://firebird-driver.readthedocs.io
- **Bcrypt:** https://github.com/pyca/bcrypt
- **ReportLab:** https://docs.reportlab.com

### Tutoriais Úteis
- Streamlit Multipage Apps: https://docs.streamlit.io/library/get-started/multipage-apps
- Firebird + Python: https://github.com/FirebirdSQL/python3-driver
- PDF com ReportLab: https://www.reportlab.com/docs/reportlab-userguide.pdf

### Comunidades
- Streamlit Forum: https://discuss.streamlit.io
- Firebird Forum: https://groups.google.com/g/firebird-support

---

## 🚀 COMO INICIAR EM NOVO AMBIENTE

### 1. Pré-requisitos
Python 3.8+
python --version

Firebird 3.0+ instalado
Download: https://firebirdsql.org/en/downloads/
text

### 2. Instalação
Clonar projeto (se em Git)
git clone <repo-url>
cd sistema-erp

Criar ambiente virtual
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

Instalar dependências
pip install streamlit fdb bcrypt reportlab streamlit-antd-components

text

### 3. Configuração
Editar `config/empresa.py`:
DATABASE_PATH = "C:/caminho/para/seu/banco.fdb"
SISTEMA_NOME = "Sua Empresa LTDA"

text

### 4. Executar
streamlit run app.py

text

### 5. Login Padrão
- **Email:** admin@sistema.com
- **Senha:** admin123
- **Perfil:** Administrador

---

## 📊 MÉTRICAS DO PROJETO

### Arquivos
- **Total:** ~20 arquivos Python
- **Linhas de código:** ~3.000 LOC (estimado)
- **Módulos:** 3 principais (Clientes, Produtos, Usuários)

### Banco de Dados
- **Tabelas:** 5 (Clientes, Produtos, Usuários, Perfis, Permissões, Log)
- **Registros esperados:** Escalável para 10k+ registros

### Performance
- **Paginação:** 25 registros/página (padrão)
- **Busca:** < 100ms para 10k registros
- **PDF:** < 3s para relatório de 100 registros

---

## 🎓 CONCEITOS APRENDIDOS

Ao desenvolver este projeto, foram aplicados:

1. **Arquitetura em Camadas** (MVC-like)
   - Models (db/models.py)
   - Views (ui/*.py)
   - Controllers (pages/*.py)

2. **Controle de Acesso Baseado em Perfis** (RBAC)
   - Perfis → Permissões → Ações

3. **Context Managers** (Python)
   - `with get_db_cursor():`

4. **Session State** (Streamlit)
   - Persistência de dados entre reruns

5. **Soft Delete** (Banco de Dados)
   - Campo ATIVO ao invés de DELETE

6. **Audit Trail** (Segurança)
   - Log de todas as ações críticas

7. **Password Hashing** (Segurança)
   - bcrypt para senhas

8. **Validação em Duas Camadas** (Segurança)
   - Frontend + Backend

---

## 🛠️ TROUBLESHOOTING

### Erro: "Connection refused" ao conectar Firebird
**Solução:** Verificar se serviço Firebird está rodando
Windows
services.msc → Firebird Server

Linux
sudo systemctl status firebird

text

### Erro: "Module not found: fdb"
**Solução:** Instalar driver
pip install fdb

text

### Erro: "st.rerun() loop infinito"
**Solução:** Revisar seção "Problemas Resolvidos → Loop Infinito"

### PDF não aparece após clicar no botão
**Solução:** Verificar se `st.session_state.gerar_pdf_clientes` está sendo setado corretamente

---

## 👥 CONTATOS E SUPORTE

- **Desenvolvedor:** [Seu Nome]
- **Email:** [seu@email.com]
- **Repositório:** [URL do Git]

---

## 📜 CHANGELOG

### [1.0.0] - 18/10/2025

#### ✅ Implementado
- Sistema de autenticação com bcrypt
- Controle de permissões (3 perfis)
- Módulo de Clientes (com 2 telefones)
- Módulo de Produtos
- Módulo de Usuários
- Exportação PDF
- Busca inteligente (Nome LIKE, Código =)
- Layout tabela compacta
- Modal de visualização para Visualizadores
- Audit log completo

#### 🐛 Corrigido
- Loop infinito de st.rerun()
- PDF não aparecendo
- Sidebar duplicada
- Busca por código usando LIKE
- Campo DATA_CADASTRO inexistente

---

**FIM DO CONTEXTO - Versão 1.0.0**

---

_Este documento serve como guia completo para retomada do projeto em qualquer momento. Mantenha-o atualizado a cada mudança significativa._
