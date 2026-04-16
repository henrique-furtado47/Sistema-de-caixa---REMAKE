from __future__ import annotations

from .produto import Produto


class ItemCarrinho:
    """Representa um item no carrinho (produto + quantidade desejada)."""

    def __init__(self, produto: Produto, quantidade: int) -> None:
        self.produto = produto
        self.quantidade = quantidade

    @property
    def subtotal(self) -> float:
        return self.produto.preco * self.quantidade

    def __repr__(self) -> str:
        return (
            f"ItemCarrinho(produto={self.produto.nome!r}, "
            f"qtd={self.quantidade}, subtotal=R${self.subtotal:.2f})"
        )
