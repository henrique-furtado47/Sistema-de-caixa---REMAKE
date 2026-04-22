from __future__ import annotations

import streamlit as st

from src.services import Carrinho, Estoque


def inicializar_estado() -> None:
    if "estoque" not in st.session_state:
        st.session_state.estoque = Estoque()
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = Carrinho()
    if "caixa_tela" not in st.session_state:
        st.session_state.caixa_tela = "selecao"
    if "ultima_venda" not in st.session_state:
        st.session_state.ultima_venda = None
