from __future__ import annotations

from src.models import ItemCarrinho, Produto


class Carrinho:
    """Gerencia os itens selecionados para compra."""

    def __init__(self) -> None:
        self._itens: list[ItemCarrinho] = []

    # ── busca ──────────────────────────────────────────────

    def _buscar_item(self, codigo: int) -> ItemCarrinho | None:
        for item in self._itens:
            if item.produto.codigo == codigo:
                return item
        return None

    # ── propriedades ───────────────────────────────────────

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self._itens)

    @property
    def vazio(self) -> bool:
        return len(self._itens) == 0

    # ── ações ──────────────────────────────────────────────

    def adicionar(self, produto: Produto, quantidade: int) -> str:
        """Adiciona produto ao carrinho. Retorna mensagem de status."""
        if quantidade > produto.quantidade:
            return "Quantidade insuficiente no estoque!"

        item_existente = self._buscar_item(produto.codigo)
        if item_existente:
            item_existente.quantidade += quantidade
        else:
            self._itens.append(ItemCarrinho(produto, quantidade))
        return "Produto adicionado ao carrinho!"

    def remover(self, codigo: int, quantidade: int) -> str:
        item = self._buscar_item(codigo)
        if item is None:
            return "Produto não encontrado no carrinho."

        if quantidade > item.quantidade:
            return "Quantidade maior do que a presente no carrinho!"
        elif quantidade == item.quantidade:
            self._itens.remove(item)
            return "Produto removido do carrinho!"
        else:
            item.quantidade -= quantidade
            return "Quantidade atualizada no carrinho!"

    def limpar(self) -> None:
        self._itens.clear()

    def listar(self) -> list[dict]:
        return [
            {
                "Código": i.produto.codigo,
                "Nome": i.produto.nome,
                "Qtd": i.quantidade,
                "Preço Unit. (R$)": f"{i.produto.preco:.2f}",
                "Subtotal (R$)": f"{i.subtotal:.2f}",
            }
            for i in self._itens
        ]

    def finalizar(self) -> list[ItemCarrinho]:
        """Retorna os itens, desconta do estoque e esvazia o carrinho."""
        itens = list(self._itens)
        for item in itens:
            item.produto.quantidade -= item.quantidade
        self._itens.clear()
        return itens
