"""Ponto de entrada da API REST (FastAPI)."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.carrinho import router as carrinho_router
from api.routes.pagamento import router as pagamento_router
from api.routes.produtos import router as produtos_router

app = FastAPI(
    title="Sistema de Caixa API",
    description="API REST para o Sistema de Caixa",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(produtos_router, prefix="/api")
app.include_router(carrinho_router, prefix="/api")
app.include_router(pagamento_router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}
