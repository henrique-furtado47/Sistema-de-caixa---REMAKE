from __future__ import annotations


class Produto:
    """Representa um produto com nome, quantidade, preço e código."""

    _proximo_codigo: int = 1

    def __init__(
        self, nome: str, quantidade: int, preco: float, codigo: int | None = None
    ) -> None:
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

        if codigo is not None:
            self.codigo = codigo
        else:
            self.codigo = Produto._proximo_codigo
            Produto._proximo_codigo += 1

    def __repr__(self) -> str:
        return (
            f"Produto(nome={self.nome!r}, qtd={self.quantidade}, "
            f"preco=R${self.preco:.2f}, cod={self.codigo})"
        )

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.nome} - R${self.preco:.2f} (qtd: {self.quantidade})"
