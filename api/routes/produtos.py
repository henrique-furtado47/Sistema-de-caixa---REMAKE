"""Rotas para gerenciamento de produtos (estoque)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import MensagemOut, ProdutoCreate, ProdutoOut, ProdutoUpdate
from api.state import estoque

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("", response_model=list[ProdutoOut])
def listar_produtos():
    return [
        ProdutoOut(
            codigo=p.codigo,
            nome=p.nome,
            quantidade=p.quantidade,
            preco=p.preco,
        )
        for p in estoque.produtos
    ]


@router.get("/{codigo}", response_model=ProdutoOut)
def buscar_produto(codigo: int):
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return ProdutoOut(
        codigo=produto.codigo,
        nome=produto.nome,
        quantidade=produto.quantidade,
        preco=produto.preco,
    )


@router.post("", response_model=ProdutoOut, status_code=201)
def cadastrar_produto(body: ProdutoCreate):
    try:
        produto = estoque.cadastrar(body.nome, body.quantidade, body.preco)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return ProdutoOut(
        codigo=produto.codigo,
        nome=produto.nome,
        quantidade=produto.quantidade,
        preco=produto.preco,
    )


@router.put("/{codigo}", response_model=ProdutoOut)
def atualizar_produto(codigo: int, body: ProdutoUpdate):
    try:
        produto = estoque.atualizar(
            codigo,
            nome=body.nome,
            quantidade=body.quantidade,
            preco=body.preco,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return ProdutoOut(
        codigo=produto.codigo,
        nome=produto.nome,
        quantidade=produto.quantidade,
        preco=produto.preco,
    )


@router.delete("/{codigo}", response_model=MensagemOut)
def remover_produto(codigo: int):
    from api.state import carrinho

    if carrinho.contem_produto(codigo):
        raise HTTPException(
            status_code=409,
            detail="Remova o produto do carrinho antes de excluí-lo do estoque.",
        )

    if not estoque.remover(codigo):
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return MensagemOut(mensagem="Produto removido com sucesso!")
