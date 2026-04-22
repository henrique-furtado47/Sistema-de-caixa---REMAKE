from __future__ import annotations

import streamlit as st

from src.ui.web.utils import fmt_moeda


# ── estilos ────────────────────────────────────────────────────────────────────

def _estilos() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] { background: #f4f6f4; }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stSidebarContent"] { background: #1b4332; }
        [data-testid="stSidebarContent"] * { color: #d8f3dc !important; }
        .block-container { padding-top: 1.6rem; padding-bottom: 2rem; }

        [data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #2d6a4f, #1b4332) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 700 !important;
            min-height: 2.8rem !important;
        }
        [data-testid="baseButton-secondary"] {
            background: white !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            border-radius: 12px !important;
            color: #1a1a2e !important;
            min-height: 2.8rem !important;
        }
        [data-testid="stMetric"] {
            background: white;
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        [data-testid="stMetricValue"] {
            color: #1b4332 !important;
            font-weight: 900 !important;
        }
        [data-testid="stDataFrame"] {
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 16px;
            overflow: hidden;
            background: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── ponto de entrada da página ─────────────────────────────────────────────────

def pagina_edicao() -> None:
    _estilos()
    st.markdown("## 📦 Gestão de Estoque")

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

    col_novo, col_editar = st.columns(2, gap="large")

    # ── cadastro ──────────────────────────────────────────
    with col_novo:
        st.markdown("### Novo produto")
        with st.form("form_novo_produto", clear_on_submit=True):
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
                    st.success(f"Produto **{p.nome}** cadastrado (código `{p.codigo}`).")
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
                        st.success("Produto atualizado com sucesso.")
                    except ValueError as exc:
                        st.error(str(exc))

                if remover:
                    if carrinho.contem_produto(codigo):
                        st.error(
                            "Este produto está no pedido ativo. "
                            "Remova-o do carrinho no Caixa antes de excluir."
                        )
                    elif estoque.remover(codigo):
                        st.success("Produto removido.")
                        st.rerun()
                    else:
                        st.error("Produto não encontrado.")
