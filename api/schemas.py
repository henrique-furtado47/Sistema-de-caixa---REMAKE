"""Schemas Pydantic para os endpoints da API."""

from __future__ import annotations

from pydantic import BaseModel, Field


# ── Produto ────────────────────────────────────────────────────────────────────

class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    quantidade: int = Field(..., ge=0)
    preco: float = Field(..., ge=0)


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1)
    quantidade: int | None = Field(None, ge=0)
    preco: float | None = Field(None, ge=0)


class ProdutoOut(BaseModel):
    codigo: int
    nome: str
    quantidade: int
    preco: float

    model_config = {"from_attributes": True}


# ── Carrinho ───────────────────────────────────────────────────────────────────

class AdicionarItemRequest(BaseModel):
    codigo: int
    quantidade: int = Field(..., ge=1)


class RemoverItemRequest(BaseModel):
    codigo: int
    quantidade: int = Field(..., ge=1)


class ItemCarrinhoOut(BaseModel):
    codigo: int
    nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float


class CarrinhoOut(BaseModel):
    itens: list[ItemCarrinhoOut]
    total: float
    quantidade_total: int
    vazio: bool


# ── Pagamento ──────────────────────────────────────────────────────────────────

class PagamentoRequest(BaseModel):
    metodo: str = Field(..., pattern="^(credito|debito|dinheiro)$")
    parcelas: int | None = Field(None, ge=1)
    valor_recebido: float | None = Field(None, ge=0)


class PagamentoOut(BaseModel):
    metodo: str
    total_original: float
    total_final: float
    parcelas: int | None = None
    valor_parcela: float | None = None
    troco: float | None = None


# ── Genérico ───────────────────────────────────────────────────────────────────

class MensagemOut(BaseModel):
    mensagem: str
    sucesso: bool = True
