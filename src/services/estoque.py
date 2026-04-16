from __future__ import annotations

from src.models import Produto


class Estoque:
    """Gerencia a coleção de produtos disponíveis."""

    def __init__(self) -> None:
        self._produtos: list[Produto] = []

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

    # ── CRUD ───────────────────────────────────────────────

    def cadastrar(self, nome: str, quantidade: int, preco: float) -> Produto:
        produto = Produto(nome, quantidade, preco)
        self._produtos.append(produto)
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
