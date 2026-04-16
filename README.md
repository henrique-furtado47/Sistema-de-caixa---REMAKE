# 🛒 Sistema de Caixa — Python POO

Sistema de caixa com gerenciamento de **estoque** e **carrinho de compras**, desenvolvido em Python puro com Programação Orientada a Objetos.

## 📁 Estrutura do Projeto

```
Sistema-de-caixa---REMAKE/
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
│       └── menu.py            # Interface de terminal (menus)
└── Sistema_de_caixa_v2.ipynb  # Versão antiga (Jupyter Notebook)
```

## ▶️ Como executar

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

## 🏗️ Arquitetura

| Camada      | Responsabilidade                                       |
| ----------- | ------------------------------------------------------ |
| `models/`   | Classes de dados (`Produto`, `ItemCarrinho`)           |
| `services/` | Lógica de negócio (`Estoque`, `Carrinho`, `Pagamento`) |
| `ui/`       | Interface com o usuário (`SistemaDeCaixa`, menus)      |

## 👤 Autor

**Henrique Furtado** — [@henrique-furtado47](https://github.com/henrique-furtado47)
