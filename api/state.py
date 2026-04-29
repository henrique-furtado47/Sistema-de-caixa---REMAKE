"""Estado global compartilhado (in-memory) da aplicação."""

from src.services.carrinho import Carrinho
from src.services.estoque import Estoque

estoque = Estoque()
carrinho = Carrinho()
