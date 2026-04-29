"""Rotas para gerenciamento do carrinho de compras."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import (AdicionarItemRequest, CarrinhoOut, ItemCarrinhoOut,
                         MensagemOut, RemoverItemRequest)
from api.state import carrinho, estoque

router = APIRouter(prefix="/carrinho", tags=["carrinho"])


def _carrinho_out() -> CarrinhoOut:
    itens = [
        ItemCarrinhoOut(
            codigo=item.produto.codigo,
            nome=item.produto.nome,
            quantidade=item.quantidade,
            preco_unitario=item.produto.preco,
            subtotal=item.subtotal,
        )
        for item in carrinho.itens
    ]
    return CarrinhoOut(
        itens=itens,
        total=carrinho.total,
        quantidade_total=carrinho.quantidade_total,
        vazio=carrinho.vazio,
    )


@router.get("", response_model=CarrinhoOut)
def ver_carrinho():
    return _carrinho_out()


@router.post("/adicionar", response_model=CarrinhoOut)
def adicionar_item(body: AdicionarItemRequest):
    produto = estoque.buscar_por_codigo(body.codigo)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado no estoque.")

    mensagem = carrinho.adicionar(produto, body.quantidade)
    if "insuficiente" in mensagem.lower():
        raise HTTPException(status_code=422, detail=mensagem)

    return _carrinho_out()


@router.post("/remover", response_model=CarrinhoOut)
def remover_item(body: RemoverItemRequest):
    mensagem = carrinho.remover(body.codigo, body.quantidade)
    if "não encontrado" in mensagem.lower() or "maior" in mensagem.lower():
        raise HTTPException(status_code=422, detail=mensagem)
    return _carrinho_out()


@router.delete("", response_model=MensagemOut)
def limpar_carrinho():
    carrinho.limpar()
    return MensagemOut(mensagem="Carrinho limpo com sucesso!")
