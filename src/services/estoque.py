from __future__ import annotations

from src.models import Produto


class Estoque:
    """Gerencia a coleção de produtos disponíveis."""

    def __init__(self) -> None:
        self._produtos: list[Produto] = []

    @staticmethod
    def _validar_nome(nome: str) -> str:
        nome_normalizado = nome.strip()
        if not nome_normalizado:
            raise ValueError("O nome do produto não pode ficar vazio.")
        return nome_normalizado

    @staticmethod
    def _validar_quantidade(quantidade: int) -> int:
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        return quantidade

    @staticmethod
    def _validar_preco(preco: float) -> float:
        if preco < 0:
            raise ValueError("O preço não pode ser negativo.")
        return preco

    # ── busca ──────────────────────────────────────────────

    def buscar_por_codigo(self, codigo: int) -> Produto | None:
        for p in self._produtos:
            if p.codigo == codigo:
                return p
        return None

    def buscar_por_nome(self, nome: str) -> Produto | None:
        for p in self._produtos:
            if p.nome.lower() == nome.lower():
                return p
        return None

    @property
    def produtos(self) -> tuple[Produto, ...]:
        return tuple(self._produtos)

    # ── CRUD ───────────────────────────────────────────────

    def cadastrar(self, nome: str, quantidade: int, preco: float) -> Produto:
        produto = Produto(
            self._validar_nome(nome),
            self._validar_quantidade(quantidade),
            self._validar_preco(preco),
        )
        self._produtos.append(produto)
        return produto

    def atualizar(
        self,
        codigo: int,
        *,
        nome: str | None = None,
        quantidade: int | None = None,
        preco: float | None = None,
    ) -> Produto | None:
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            return None

        if nome is not None:
            produto.nome = self._validar_nome(nome)
        if quantidade is not None:
            produto.quantidade = self._validar_quantidade(quantidade)
        if preco is not None:
            produto.preco = self._validar_preco(preco)

        return produto

    def remover(self, codigo: int) -> bool:
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            return False
        self._produtos.remove(produto)
        return True

    def listar(self) -> list[dict]:
        """Retorna uma lista de dicts para exibição tabular."""
        return [
            {
                "Código": p.codigo,
                "Nome": p.nome,
                "Quantidade": p.quantidade,
                "Preço (R$)": f"{p.preco:.2f}",
            }
            for p in self._produtos
        ]

    @property
    def vazio(self) -> bool:
        return len(self._produtos) == 0
