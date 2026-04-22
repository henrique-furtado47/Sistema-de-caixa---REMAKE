from __future__ import annotations


def fmt_moeda(valor: float) -> str:
    """Formata um float como moeda brasileira: R$ 1.234,56"""
    raw = f"{valor:,.2f}"
    return "R$ " + raw.replace(",", "\u00b7").replace(".", ",").replace("\u00b7", ".")
