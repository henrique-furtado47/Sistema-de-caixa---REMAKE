# 🛒 Sistema de Caixa — Python POO

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://caixasys.streamlit.app/)

Sistema de caixa com gerenciamento de **estoque** e **carrinho de compras**, desenvolvido em Python puro com Programação Orientada a Objetos.

> 🌐 **Demo ao vivo:** [caixasys.streamlit.app](https://caixasys.streamlit.app/)

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
