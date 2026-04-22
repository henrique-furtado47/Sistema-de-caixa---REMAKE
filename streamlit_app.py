from __future__ import annotations

import streamlit as st

from src.ui.web.caixa import pagina_caixa
from src.ui.web.edicao import pagina_edicao
from src.ui.web.state import inicializar_estado

st.set_page_config(
    page_title="Sistema de Caixa",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

inicializar_estado()

pg = st.navigation(
    [
        st.Page(pagina_caixa, title="Caixa", icon="🛒", default=True),
        st.Page(pagina_edicao, title="Estoque", icon="📦"),
    ],
)
pg.run()
