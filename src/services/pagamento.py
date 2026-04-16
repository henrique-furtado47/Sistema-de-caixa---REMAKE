from __future__ import annotations


class Pagamento:
    """Calcula valores de pagamento (à vista, parcelado, troco)."""

    PARCELAS_SEM_JUROS = 6

    @staticmethod
    def calcular_parcela(total: float, parcelas: int) -> float:
        """Retorna o valor de cada parcela (com juros se > 6x)."""
        if parcelas <= Pagamento.PARCELAS_SEM_JUROS:
            return total / parcelas
        juros = parcelas / 150
        return total * (1 + juros) / parcelas

    @staticmethod
    def calcular_troco(total: float, valor_recebido: float) -> float | None:
        """Retorna o troco ou None se o valor for insuficiente."""
        if valor_recebido < total:
            return None
        return valor_recebido - total
