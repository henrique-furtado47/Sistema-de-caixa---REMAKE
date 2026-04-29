# 🛒 Sistema de Caixa — FastAPI + Vue

Sistema de caixa com gerenciamento de **estoque** e **carrinho de compras**, desenvolvido com **FastAPI** (backend REST) e **Vue 3 + Vite** (frontend).

## 📁 Estrutura do Projeto

```
Sistema-de-caixa---REMAKE/
├── api/                       # FastAPI REST backend
│   ├── main.py                # App FastAPI + CORS
│   ├── schemas.py             # Schemas Pydantic
│   ├── state.py               # Estado in-memory (estoque + carrinho)
│   └── routes/
│       ├── produtos.py        # CRUD de produtos
│       ├── carrinho.py        # Gerenciamento do carrinho
│       └── pagamento.py       # Calcular e finalizar pagamento
├── frontend/                  # Vue 3 + Vite frontend
│   └── src/
│       ├── api/index.js       # Cliente axios
│       ├── router/index.js    # Vue Router
│       ├── views/
│       │   ├── CaixaView.vue  # Página POS (grid de produtos + carrinho)
│       │   └── EstoqueView.vue# Página de estoque (tabela CRUD)
│       └── components/
│           ├── ProdutoCard.vue
│           └── CarrinhoSidebar.vue
├── main.py                    # Interface de terminal
├── src/
│   ├── models/                # Produto, ItemCarrinho
│   └── services/             # Estoque, Carrinho, Pagamento
└── requirements.txt
```

## ▶️ Como executar

### Backend (FastAPI)

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

API disponível em `http://localhost:8000`  
Docs interativos: `http://localhost:8000/docs`

### Frontend (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

Site disponível em `http://localhost:5173`

### Interface de terminal (legado)

```bash
python main.py
```

> **Requisito:** Python 3.10+ | Node.js 18+

## 🌐 Endpoints da API

| Método | Rota                       | Descrição           |
| ------ | -------------------------- | ------------------- |
| GET    | `/api/produtos`            | Listar produtos     |
| POST   | `/api/produtos`            | Cadastrar produto   |
| PUT    | `/api/produtos/{codigo}`   | Atualizar produto   |
| DELETE | `/api/produtos/{codigo}`   | Remover produto     |
| GET    | `/api/carrinho`            | Ver carrinho        |
| POST   | `/api/carrinho/adicionar`  | Adicionar item      |
| POST   | `/api/carrinho/remover`    | Remover item        |
| DELETE | `/api/carrinho`            | Limpar carrinho     |
| POST   | `/api/pagamento/calcular`  | Prévia de pagamento |
| POST   | `/api/pagamento/finalizar` | Finalizar compra    |

## 🧩 Funcionalidades

- **Caixa (POS):** grid de produtos, busca, adicionar ao carrinho, pagamento (crédito/débito/dinheiro) com cálculo de parcelas e troco
- **Estoque:** cadastrar, editar e remover produtos
- **Pagamento crédito:** juros automáticos acima de 6x

## 🏗️ Arquitetura

| Camada          | Responsabilidade                                       |
| --------------- | ------------------------------------------------------ |
| `src/models/`   | Classes de dados (`Produto`, `ItemCarrinho`)           |
| `src/services/` | Lógica de negócio (`Estoque`, `Carrinho`, `Pagamento`) |
| `api/`          | FastAPI: schemas, rotas REST, estado in-memory         |
| `frontend/`     | Vue 3 SPA: views, componentes, cliente axios           |

## 👤 Autor

**Henrique Furtado** — [@henrique-furtado47](https://github.com/henrique-furtado47)

## 📁 Estrutura do Projeto

```
Sistema-de-caixa---REMAKE/
├── streamlit_app.py           # Ponto de entrada da interface web
├── main.py                    # Ponto de entrada
├── README.md
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── produto.py         # Classe Produto
│   │   └── item_carrinho.py   # Classe ItemCarrinho
│   ├── services/
│   │   ├── __init__.py
│   │   ├── estoque.py         # CRUD de produtos
│   │   ├── carrinho.py        # Gerenciamento do carrinho
│   │   └── pagamento.py       # Lógica de pagamento
│   └── ui/
│       ├── __init__.py
│       ├── menu.py            # Interface de terminal (menus)
│       └── web/
│           ├── __init__.py
│           ├── state.py       # Estado da sessão Streamlit
│           ├── utils.py       # Utilitários (formatação)
│           ├── caixa.py       # Página Caixa (POS)
│           └── edicao.py      # Página Estoque (CRUD)
└── Sistema_de_caixa_v2.ipynb  # Versão antiga (Jupyter Notebook)
```

## ▶️ Como executar

### Deploy online

Acesse diretamente em **[caixasys.streamlit.app](https://caixasys.streamlit.app/)** — sem instalar nada.

### Localmente

Antes de rodar, instale as dependências:

```bash
pip install -r requirements.txt
```

#### Interface web

```bash
streamlit run streamlit_app.py
```

#### Interface de terminal

```bash
python main.py
```

> **Requisito:** Python 3.10+ (usa `type | None` syntax).

## 🧩 Funcionalidades

### Estoque

- Cadastrar produto (código auto-incrementado)
- Listar produtos em tabela formatada
- Remover produto por código
- Atualizar nome, quantidade ou preço
- Localizar por nome ou código

### Carrinho

- Adicionar produto (validando estoque)
- Listar itens com subtotais e total
- Remover quantidade parcial ou total
- Limpar carrinho
- Finalizar compra (desconta do estoque)

### Pagamento

- **Crédito** — parcelamento com juros acima de 6x
- **Débito** — à vista
- **Dinheiro** — calcula troco

### Interface web (Streamlit)

- Painel com métricas de operação e alerta de baixo estoque
- Cadastro, edição e remoção de produtos na mesma tela
- Carrinho com inclusão, ajuste parcial e limpeza rápida
- Fechamento da venda com crédito, débito ou dinheiro
- Resumo da última venda concluída na sessão

## 🏗️ Arquitetura

| Camada      | Responsabilidade                                       |
| ----------- | ------------------------------------------------------ |
| `models/`   | Classes de dados (`Produto`, `ItemCarrinho`)           |
| `services/` | Lógica de negócio (`Estoque`, `Carrinho`, `Pagamento`) |
| `ui/`       | Interface com o usuário (`SistemaDeCaixa`, menus)      |

## 👤 Autor

**Henrique Furtado** — [@henrique-furtado47](https://github.com/henrique-furtado47)
