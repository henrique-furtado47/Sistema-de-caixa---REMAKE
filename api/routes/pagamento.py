"""Rotas para cálculo e processamento de pagamento."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import MensagemOut, PagamentoOut, PagamentoRequest
from api.state import carrinho
from src.services.pagamento import Pagamento

router = APIRouter(prefix="/pagamento", tags=["pagamento"])


@router.post("/calcular", response_model=PagamentoOut)
def calcular_pagamento(body: PagamentoRequest):
    total = carrinho.total
    if carrinho.vazio:
        raise HTTPException(status_code=422, detail="Carrinho está vazio.")

    if body.metodo == "credito":
        if body.parcelas is None:
            raise HTTPException(status_code=422, detail="Informe o número de parcelas.")
        try:
            valor_parcela = Pagamento.calcular_parcela(total, body.parcelas)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))
        total_final = Pagamento.calcular_total_credito(total, body.parcelas)
        return PagamentoOut(
            metodo="credito",
            total_original=total,
            total_final=total_final,
            parcelas=body.parcelas,
            valor_parcela=valor_parcela,
        )

    if body.metodo == "debito":
        return PagamentoOut(
            metodo="debito",
            total_original=total,
            total_final=total,
        )

    # dinheiro
    if body.valor_recebido is None:
        raise HTTPException(status_code=422, detail="Informe o valor recebido.")
    troco = Pagamento.calcular_troco(total, body.valor_recebido)
    if troco is None:
        raise HTTPException(status_code=422, detail="Valor recebido insuficiente.")
    return PagamentoOut(
        metodo="dinheiro",
        total_original=total,
        total_final=total,
        troco=troco,
    )


@router.post("/finalizar", response_model=MensagemOut)
def finalizar_compra(body: PagamentoRequest):
    # Valida o pagamento antes de finalizar
    calcular_pagamento(body)

    erro = carrinho.validar_estoque()
    if erro:
        raise HTTPException(status_code=422, detail=erro)

    try:
        carrinho.finalizar()
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return MensagemOut(mensagem="Compra finalizada com sucesso!")
