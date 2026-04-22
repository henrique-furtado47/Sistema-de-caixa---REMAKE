from __future__ import annotations

import streamlit as st

from src.ui.web.utils import fmt_moeda

# ── estilos ────────────────────────────────────────────────────────────────────

def _estilos() -> None:
    st.markdown(
        """
        <style>
        /* ── layout ─────────────────────────────────────── */
        [data-testid="stAppViewContainer"] { background: #f0f4f0 !important; }
        [data-testid="stHeader"]           { background: transparent !important; }
        .block-container { padding-top: 1.8rem !important; padding-bottom: 2.5rem !important; }

        /* ── sidebar ────────────────────────────────────── */
        section[data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebarContent"] {
            background: #1b4332 !important;
        }
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] a,
        section[data-testid="stSidebar"] div {
            color: #c8e6cd !important;
        }
        section[data-testid="stSidebar"] svg {
            fill: #c8e6cd !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
            border-radius: 10px !important;
            padding: 0.4rem 0.7rem !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
            background: rgba(255,255,255,0.1) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-selected="true"] {
            background: rgba(255,255,255,0.18) !important;
        }

        /* ── headings ───────────────────────────────────── */
        h1, h2, h3, h4 { color: #1a2e1e !important; }

        /* ── metric cards ───────────────────────────────── */
        [data-testid="stMetric"] {
            background: white !important;
            border: 1.5px solid #d4e0d0 !important;
            border-radius: 18px !important;
            padding: 1.2rem 1.4rem !important;
            box-shadow: 0 4px 18px rgba(27,67,50,0.07) !important;
        }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] * {
            color: #5d7a63 !important;
            font-size: 0.77rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] * {
            color: #1b4332 !important;
            font-weight: 900 !important;
        }

        /* ── form containers (sem caixa pesada) ──────────── */
        [data-testid="stForm"] {
            background: white !important;
            border: 1.5px solid #d4e0d0 !important;
            border-radius: 16px !important;
            padding: 1.2rem 1.2rem 0.6rem !important;
        }

        /* ── input fields ───────────────────────────────── */
        .stTextInput  > div > div > input,
        .stNumberInput > div > div > input {
            background: #f5f9f5 !important;
            color: #1a2e1e !important;
            border: 1.5px solid #c4d4c0 !important;
            border-radius: 10px !important;
        }
        .stTextInput  > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #2d6a4f !important;
            box-shadow: 0 0 0 3px rgba(45,106,79,0.12) !important;
            outline: none !important;
        }

        /* ── widget & form labels ───────────────────────── */
        label,
        [data-testid="stWidgetLabel"] p {
            color: #374a3f !important;
            font-weight: 600 !important;
        }

        /* ── selectbox ──────────────────────────────────── */
        .stSelectbox > div > div {
            background: #f5f9f5 !important;
            border: 1.5px solid #c4d4c0 !important;
            border-radius: 10px !important;
            color: #1a2e1e !important;
        }

        /* ── buttons ────────────────────────────────────── */
        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 12px !important;
            min-height: 2.8rem !important;
            font-weight: 700 !important;
            border: 1.5px solid #d4e0d0 !important;
        }
        .stButton > button[kind="secondary"],
        .stFormSubmitButton > button[kind="secondary"] {
            background: white !important;
            color: #1a2e1e !important;
        }

        /* ── DataFrames ─────────────────────────────────── */
        [data-testid="stDataFrame"] {
            border: 1.5px solid #d4e0d0 !important;
            border-radius: 16px !important;
            overflow: hidden !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        }

        /* ── dividers & alerts ──────────────────────────── */
        hr { border-color: #d4e0d0 !important; margin: 1.5rem 0 !important; }
        [data-testid="stAlert"] { border-radius: 12px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── ponto de entrada da página ─────────────────────────────────────────────────

def pagina_edicao() -> None:
    _estilos()
    st.markdown("## 📦 Gestão de Estoque")

    # exibe e limpa mensagem de feedback de operações anteriores
    flash = st.session_state.pop("estoque_flash", None)
    if flash:
        func = st.success if flash["tipo"] == "ok" else st.error
        func(flash["msg"])

    estoque = st.session_state.estoque
    carrinho = st.session_state.carrinho

    # ── métricas ─────────────────────────────────────────
    total_produtos = len(estoque.produtos)
    total_unidades = sum(p.quantidade for p in estoque.produtos)
    criticos = sum(1 for p in estoque.produtos if p.quantidade <= 3)

    c1, c2, c3 = st.columns(3)
    c1.metric("Produtos cadastrados", total_produtos)
    c2.metric("Unidades em estoque", total_unidades)
    c3.metric(
        "Alertas de estoque baixo",
        criticos,
        delta=f"-{criticos}" if criticos else None,
        delta_color="inverse",
    )

    st.divider()

    # ── tabela do estoque ─────────────────────────────────
    st.markdown("### Produtos em estoque")
    if estoque.vazio:
        st.info("Estoque vazio. Cadastre o primeiro produto abaixo.")
    else:
        dados = estoque.listar()
        # marca linhas com estoque crítico
        for d in dados:
            if int(d["Quantidade"]) <= 3:
                d["Quantidade"] = f"⚠️ {d['Quantidade']}"
        st.dataframe(dados, hide_index=True, use_container_width=True)

    st.divider()

    col_novo, col_editar = st.columns([1, 1], gap="medium")

    # ── cadastro ──────────────────────────────────────────
    with col_novo:
        st.markdown("### Novo produto")
        with st.form("form_novo_produto", clear_on_submit=True, enter_to_submit=False):
            nome = st.text_input("Nome do produto")
            qty = st.number_input("Quantidade inicial", min_value=0, step=1, value=0)
            preco = st.number_input(
                "Preço unitário (R$)", min_value=0.0, step=0.5, format="%.2f", value=0.0
            )
            cadastrar = st.form_submit_button(
                "Cadastrar produto", use_container_width=True, type="primary"
            )
            if cadastrar:
                try:
                    p = estoque.cadastrar(nome, int(qty), float(preco))
                    st.session_state["estoque_flash"] = {
                        "tipo": "ok",
                        "msg": f"Produto **{p.nome}** cadastrado (código `{p.codigo}`).",
                    }
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))

    # ── edição / remoção ──────────────────────────────────
    with col_editar:
        st.markdown("### Editar / Remover")
        if estoque.vazio:
            st.info("Cadastre ao menos um produto para editar.")
        else:
            produtos = list(estoque.produtos)
            codigo = st.selectbox(
                "Selecione o produto",
                options=[p.codigo for p in produtos],
                format_func=lambda c: next(
                    f"[{p.codigo}] {p.nome}" for p in produtos if p.codigo == c
                ),
                key="select_produto_edicao",
            )
            produto = next(p for p in produtos if p.codigo == codigo)

            with st.form("form_edicao_produto", clear_on_submit=False):
                novo_nome = st.text_input(
                    "Nome", value=produto.nome, key=f"nome_{codigo}"
                )
                nova_qty = st.number_input(
                    "Quantidade",
                    min_value=0,
                    step=1,
                    value=int(produto.quantidade),
                    key=f"qty_{codigo}",
                )
                novo_preco = st.number_input(
                    "Preço (R$)",
                    min_value=0.0,
                    step=0.5,
                    format="%.2f",
                    value=float(produto.preco),
                    key=f"preco_{codigo}",
                )

                c_salvar, c_remover = st.columns(2)
                salvar = c_salvar.form_submit_button(
                    "Salvar alterações", use_container_width=True, type="primary"
                )
                remover = c_remover.form_submit_button(
                    "🗑 Remover", use_container_width=True
                )

                if salvar:
                    try:
                        estoque.atualizar(
                            codigo,
                            nome=novo_nome,
                            quantidade=int(nova_qty),
                            preco=float(novo_preco),
                        )
                        st.session_state["estoque_flash"] = {
                            "tipo": "ok",
                            "msg": "Produto atualizado com sucesso.",
                        }
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))

                if remover:
                    if carrinho.contem_produto(codigo):
                        st.error(
                            "Este produto está no pedido ativo. "
                            "Remova-o do carrinho no Caixa antes de excluir."
                        )
                    elif estoque.remover(codigo):
                        st.session_state["estoque_flash"] = {
                            "tipo": "ok",
                            "msg": "Produto removido com sucesso.",
                        }
                        st.rerun()
                    else:
                        st.error("Produto não encontrado.")
