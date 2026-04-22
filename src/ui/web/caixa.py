from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.services import Pagamento
from src.ui.web.utils import fmt_moeda

_COLS_GRID = 3


# ── estilos ────────────────────────────────────────────────────────────────────

def _estilos() -> None:
    st.markdown(
        """
        <style>
        /* ── layout ─────────────────────────────────────── */
        [data-testid="stAppViewContainer"] { background: #ecf0ea !important; }
        [data-testid="stHeader"]           { background: transparent !important; }
        .block-container { padding-top: 0 !important; padding-bottom: 2rem !important; max-width: 1400px !important; }

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

        /* ── headings \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        h1, h2, h3, h4 { color: #1a2e1e !important; }

        /* \u2500\u2500 POS header banner \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        .pos-header {
            background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
            padding: 1rem 1.8rem;
            border-radius: 0 0 22px 22px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 6px 24px rgba(27,67,50,0.28);
        }
        .pos-header-title {
            font-size: 1.4rem;
            font-weight: 900;
            color: white;
        }
        .pos-header-stats { display: flex; gap: 2.2rem; }
        .pos-stat { text-align: center; }
        .pos-stat-val {
            font-size: 1.65rem;
            font-weight: 900;
            color: #b7e4c7;
            line-height: 1;
        }
        .pos-stat-lbl {
            font-size: 0.68rem;
            color: rgba(255,255,255,0.6);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-top: 0.2rem;
        }

        /* \u2500\u2500 all buttons base \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        .stButton > button {
            border-radius: 14px !important;
            font-weight: 700 !important;
            transition: border-color 0.12s ease, box-shadow 0.12s ease, transform 0.12s ease !important;
        }

        /* secondary \u2192 white product cards */
        .stButton > button[kind="secondary"] {
            background: white !important;
            border: 1.5px solid #d4e0d0 !important;
            color: #1a2e1e !important;
            padding: 0.8rem 0.7rem !important;
            line-height: 1.65 !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        }
        .stButton > button[kind="secondary"]:hover:not(:disabled) {
            border-color: #2d6a4f !important;
            box-shadow: 0 6px 20px rgba(45,106,79,0.18) !important;
            transform: translateY(-2px) !important;
        }
        .stButton > button[kind="secondary"]:disabled {
            background: #f4f4f4 !important;
            border-color: #e0e0e0 !important;
            color: #aaa !important;
            opacity: 0.6 !important;
            transform: none !important;
        }

        /* primary \u2192 green (cor definida pelo config.toml, apenas forma aqui) */
        .stButton > button[kind="primary"] {
            min-height: 3.2rem !important;
            font-size: 1rem !important;
            letter-spacing: 0.01em !important;
        }

        /* \u2500\u2500 metrics \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        [data-testid="stMetric"] {
            background: white !important;
            border: 1.5px solid #d4e0d0 !important;
            border-radius: 16px !important;
            padding: 0.9rem 1rem !important;
            box-shadow: 0 2px 8px rgba(27,67,50,0.06) !important;
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

        /* \u2500\u2500 widget labels \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        label, [data-testid="stWidgetLabel"] p {
            color: #374a3f !important;
            font-weight: 600 !important;
        }

        /* \u2500\u2500 number input \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        .stNumberInput > div > div > input {
            background: #f5f9f5 !important;
            color: #1a2e1e !important;
            border: 1.5px solid #c4d4c0 !important;
            border-radius: 10px !important;
        }

        /* \u2500\u2500 cart empty placeholder \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        .cart-vazio {
            text-align: center;
            color: #8fa896;
            padding: 3rem 1rem;
            font-size: 1rem;
            line-height: 2.2;
        }

        /* \u2500\u2500 receipt lines \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        .recibo-item {
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px dashed #d4e0d0;
            font-size: 0.9rem;
            color: #374a3f;
        }
        .recibo-total {
            display: flex;
            justify-content: space-between;
            padding: 0.7rem 0 0;
            font-weight: 900;
            font-size: 1.1rem;
            color: #1b4332;
        }

        /* \u2500\u2500 success screen \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        .success-wrap { text-align: center; padding: 1.5rem 0 2rem; }
        .success-icon { font-size: 4.5rem; line-height: 1; }
        .success-title {
            font-size: 2rem;
            font-weight: 900;
            color: #1b4332;
            margin-top: 0.5rem;
        }

        /* \u2500\u2500 dividers & alerts \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */
        hr { border-color: #d4e0d0 !important; }
        [data-testid="stAlert"] { border-radius: 12px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── cabeçalho dinâmico ─────────────────────────────────────────────────────────

def _cabecalho(carrinho) -> None:
    n_itens = carrinho.quantidade_total
    total = fmt_moeda(carrinho.total)
    st.markdown(
        f"""
        <div class="pos-header">
            <span class="pos-header-title">🛒 Caixa</span>
            <div class="pos-header-stats">
                <div class="pos-stat">
                    <div class="pos-stat-val">{n_itens}</div>
                    <div class="pos-stat-lbl">Itens</div>
                </div>
                <div class="pos-stat">
                    <div class="pos-stat-val">{total}</div>
                    <div class="pos-stat-lbl">Total parcial</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── tela 1 — seleção de produtos ──────────────────────────────────────────────

def _tela_selecao() -> None:
    estoque = st.session_state.estoque
    carrinho = st.session_state.carrinho

    col_prod, col_cart = st.columns([3, 2], gap="large")

    with col_prod:
        st.markdown("#### Produtos")
        _grade_produtos(estoque, carrinho)

    with col_cart:
        st.markdown("#### Pedido atual")
        _painel_carrinho(carrinho)


def _grade_produtos(estoque, carrinho) -> None:
    produtos = list(estoque.produtos)
    if not produtos:
        st.info("Nenhum produto cadastrado. Acesse **Estoque** para adicionar.")
        return

    disponiveis = [
        p for p in produtos
        if (p.quantidade - carrinho.quantidade_do_produto(p.codigo)) > 0
    ]
    esgotados = [
        p for p in produtos
        if (p.quantidade - carrinho.quantidade_do_produto(p.codigo)) <= 0
    ]

    _renderizar_grade(disponiveis, carrinho)

    if esgotados:
        with st.expander(f"Esgotados / já no limite ({len(esgotados)})"):
            _renderizar_grade(esgotados, carrinho)


def _renderizar_grade(produtos, carrinho) -> None:
    linhas = [produtos[i : i + _COLS_GRID] for i in range(0, len(produtos), _COLS_GRID)]
    for linha in linhas:
        cols = st.columns(_COLS_GRID)
        for col, produto in zip(cols, linha):
            with col:
                saldo = produto.quantidade - carrinho.quantidade_do_produto(produto.codigo)
                disabled = saldo <= 0
                indicador = f"• {saldo} disp." if not disabled else "• Esgotado"
                rotulo = f"**{produto.nome}**\n\n{fmt_moeda(produto.preco)}\n\n{indicador}"

                if st.button(
                    rotulo,
                    key=f"btn_prod_{produto.codigo}",
                    use_container_width=True,
                    disabled=disabled,
                    help=f"Adicionar '{produto.nome}' ao pedido",
                ):
                    carrinho.adicionar(produto, 1)
                    st.rerun()


def _painel_carrinho(carrinho) -> None:
    if carrinho.vazio:
        st.markdown(
            '<div class="cart-vazio">🛒<br>Selecione os produtos ao lado<br>'
            '<span style="font-size:0.85rem">Clique para adicionar ao pedido</span></div>',
            unsafe_allow_html=True,
        )
        return

    for item in carrinho.itens:
        c_nome, c_ctrl, c_sub, c_del = st.columns([3, 2, 1.8, 0.7])

        c_nome.markdown(f"**{item.produto.nome}**")

        # controles de quantidade
        with c_ctrl:
            b1, b2, b3 = st.columns([1, 1.2, 1])
            if b1.button("−", key=f"dec_{item.produto.codigo}", use_container_width=True):
                carrinho.remover(item.produto.codigo, 1)
                st.rerun()
            b2.markdown(
                f'<p style="text-align:center;font-weight:700;padding-top:7px;margin:0">'
                f"{item.quantidade}</p>",
                unsafe_allow_html=True,
            )
            pode_add = item.produto.quantidade - item.quantidade > 0
            if b3.button(
                "+",
                key=f"inc_{item.produto.codigo}",
                use_container_width=True,
                disabled=not pode_add,
            ):
                carrinho.adicionar(item.produto, 1)
                st.rerun()

        c_sub.markdown(
            f'<p style="text-align:right;font-size:0.9rem;padding-top:7px;margin:0">'
            f"{fmt_moeda(item.subtotal)}</p>",
            unsafe_allow_html=True,
        )

        if c_del.button("×", key=f"del_{item.produto.codigo}", use_container_width=True):
            carrinho.remover(item.produto.codigo, item.quantidade)
            st.rerun()

    st.divider()

    c_total, c_limpar = st.columns([1.4, 1])
    c_total.metric("Total", fmt_moeda(carrinho.total))
    with c_limpar:
        st.write("")
        if st.button("🗑 Limpar tudo", use_container_width=True):
            carrinho.limpar()
            st.rerun()

    st.button(
        "Finalizar compra →",
        use_container_width=True,
        type="primary",
        key="btn_finalizar",
        on_click=_ir_para_pagamento,
    )


def _ir_para_pagamento() -> None:
    st.session_state.caixa_tela = "pagamento"


# ── tela 2 — pagamento ─────────────────────────────────────────────────────────

def _tela_pagamento() -> None:
    carrinho = st.session_state.carrinho

    if carrinho.vazio:
        st.session_state.caixa_tela = "selecao"
        st.rerun()
        return

    total = carrinho.total

    if st.button("← Voltar ao pedido"):
        st.session_state.caixa_tela = "selecao"
        st.rerun()

    st.markdown("---")

    col_resumo, col_form = st.columns([1, 1.6], gap="large")

    with col_resumo:
        st.markdown("**Resumo do pedido**")
        linhas_html = "".join(
            f'<div class="recibo-item">'
            f'<span>{item.produto.nome} × {item.quantidade}</span>'
            f'<span>{fmt_moeda(item.subtotal)}</span>'
            f"</div>"
            for item in carrinho.itens
        )
        st.markdown(
            f'{linhas_html}'
            f'<div class="recibo-total"><span>Total</span><span>{fmt_moeda(total)}</span></div>',
            unsafe_allow_html=True,
        )

    with col_form:
        st.markdown("**Forma de pagamento**")

        metodo = st.radio(
            "Método",
            options=["Crédito", "Débito", "Dinheiro"],
            horizontal=True,
            label_visibility="collapsed",
        )

        pagamento_valido = True
        total_pago = total
        descricao_metodo = metodo

        if metodo == "Crédito":
            parcelas = st.select_slider(
                "Parcelas", options=list(range(1, 13)), value=1
            )
            valor_parcela = Pagamento.calcular_parcela(total, parcelas)
            total_pago = Pagamento.calcular_total_credito(total, parcelas)
            descricao_metodo = f"Crédito {parcelas}×"
            st.info(
                f"**{parcelas}×** de **{fmt_moeda(valor_parcela)}** "
                f"→ total: **{fmt_moeda(total_pago)}**"
            )

        elif metodo == "Débito":
            st.info(f"Pagamento à vista no débito: **{fmt_moeda(total)}**")

        else:
            sugestao = float(int(total) + (0 if total == int(total) else 1))
            valor_recebido = st.number_input(
                "Valor recebido (R$)",
                min_value=0.0,
                step=1.0,
                value=sugestao,
                format="%.2f",
            )
            troco = Pagamento.calcular_troco(total, float(valor_recebido))
            if troco is None:
                st.error("Valor insuficiente para cobrir o total.")
                pagamento_valido = False
            else:
                st.success(f"Troco: **{fmt_moeda(troco)}**")

        erro_estoque = carrinho.validar_estoque()
        if erro_estoque:
            st.error(erro_estoque)
            pagamento_valido = False

        if st.button(
            "Confirmar pagamento",
            use_container_width=True,
            type="primary",
            disabled=not pagamento_valido,
        ):
            _confirmar_pagamento(total_pago, descricao_metodo)


def _confirmar_pagamento(total_pago: float, descricao_metodo: str) -> None:
    carrinho = st.session_state.carrinho
    try:
        itens = carrinho.finalizar()
    except ValueError as exc:
        st.error(str(exc))
        return

    st.session_state.ultima_venda = {
        "horario": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "metodo": descricao_metodo,
        "total": total_pago,
        "itens": [
            {
                "nome": item.produto.nome,
                "quantidade": item.quantidade,
                "subtotal": item.subtotal,
            }
            for item in itens
        ],
    }
    st.session_state.caixa_tela = "concluido"
    st.rerun()


# ── tela 3 — confirmação ───────────────────────────────────────────────────────

def _tela_concluido() -> None:
    venda = st.session_state.ultima_venda
    st.balloons()

    st.markdown(
        '<div class="success-wrap">'
        '<div class="success-icon">✅</div>'
        '<div class="success-title">Venda concluída!</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    if venda:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total pago", fmt_moeda(venda["total"]))
        c2.metric("Método", venda["metodo"])
        c3.metric("Horário", venda["horario"])

        st.divider()
        st.markdown("**Itens desta venda:**")
        for item in venda["itens"]:
            st.write(
                f"• **{item['nome']}** × {item['quantidade']} = {fmt_moeda(item['subtotal'])}"
            )

    st.divider()
    if st.button("Nova venda", use_container_width=True, type="primary"):
        st.session_state.caixa_tela = "selecao"
        st.rerun()


# ── ponto de entrada da página ─────────────────────────────────────────────────

def pagina_caixa() -> None:
    _estilos()
    carrinho = st.session_state.carrinho
    tela = st.session_state.get("caixa_tela", "selecao")

    if tela != "pagamento":
        _cabecalho(carrinho)

    if tela == "selecao":
        _tela_selecao()
    elif tela == "pagamento":
        _tela_pagamento()
    elif tela == "concluido":
        _tela_concluido()
