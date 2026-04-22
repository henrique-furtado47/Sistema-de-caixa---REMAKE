from __future__ import annotations

from datetime import datetime
from html import escape

import streamlit as st

from src.models import ItemCarrinho, Produto
from src.services import Carrinho, Estoque, Pagamento

MENSAGENS_SUCESSO_CARRINHO = {
    "Produto adicionado ao carrinho!",
    "Produto removido do carrinho!",
    "Quantidade atualizada no carrinho!",
}


def formatar_moeda(valor: float) -> str:
    valor_formatado = f"{valor:,.2f}"
    return f"R$ {valor_formatado}".replace(",", "#").replace(".", ",").replace("#", ".")


def aplicar_estilos() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg-start: #f6edda;
            --bg-end: #d7e5d8;
            --ink: #163126;
            --muted: #5f6d66;
            --card: rgba(255, 255, 255, 0.78);
            --line: rgba(22, 49, 38, 0.12);
            --accent: #1f6b46;
            --accent-strong: #12482f;
            --highlight: #d9892b;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at top left, rgba(217, 137, 43, 0.28), transparent 24%),
                radial-gradient(circle at 85% 15%, rgba(31, 107, 70, 0.16), transparent 18%),
                linear-gradient(135deg, var(--bg-start) 0%, #eef3e5 46%, var(--bg-end) 100%);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.8rem;
            padding-bottom: 2.2rem;
        }

        html, body, [class*="css"] {
            color: var(--ink);
            font-family: "Aptos", "Segoe UI Variable", "Trebuchet MS", sans-serif;
        }

        h1, h2, h3 {
            color: var(--ink);
            font-family: "Rockwell", "Georgia", serif;
            letter-spacing: -0.02em;
        }

        .hero-panel {
            padding: 1.7rem 1.8rem;
            border: 1px solid var(--line);
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.92) 0%, rgba(249, 246, 236, 0.88) 100%);
            box-shadow: 0 24px 60px rgba(22, 49, 38, 0.08);
            margin-bottom: 1rem;
        }

        .hero-eyebrow {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .hero-title {
            font-size: clamp(2rem, 4vw, 3.4rem);
            line-height: 0.95;
            margin: 0;
            max-width: 12ch;
        }

        .hero-copy {
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.6;
            margin: 0.95rem 0 0;
            max-width: 62ch;
        }

        .spotlight-card {
            min-height: 210px;
            padding: 1.35rem 1.4rem;
            border: 1px solid var(--line);
            border-radius: 24px;
            background: var(--card);
            box-shadow: 0 16px 40px rgba(22, 49, 38, 0.06);
        }

        .spotlight-label {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .spotlight-title {
            font-size: 1.7rem;
            line-height: 1.1;
            margin-bottom: 0.55rem;
        }

        .spotlight-copy {
            color: var(--muted);
            line-height: 1.55;
            margin: 0;
        }

        .receipt-list {
            color: var(--muted);
            line-height: 1.55;
            margin-top: 0.9rem;
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.74);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 1rem 1.1rem;
            box-shadow: 0 16px 30px rgba(22, 49, 38, 0.04);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--accent-strong);
            font-family: "Rockwell", "Georgia", serif;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.65);
            border: 1px solid var(--line);
            padding: 0.5rem 1rem;
            color: var(--muted);
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-strong);
            color: #fff;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 16px;
            border: 0;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
            color: #fff;
            font-weight: 700;
            min-height: 2.8rem;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            filter: brightness(1.04);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 22px;
            overflow: hidden;
        }

        div[data-testid="stMarkdownContainer"] p {
            color: inherit;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-top: 1rem;
            }

            .hero-panel {
                padding: 1.3rem;
            }

            .spotlight-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inicializar_estado() -> tuple[Estoque, Carrinho]:
    if "estoque" not in st.session_state:
        st.session_state["estoque"] = Estoque()
    if "carrinho" not in st.session_state:
        st.session_state["carrinho"] = Carrinho()
    if "ultima_venda" not in st.session_state:
        st.session_state["ultima_venda"] = None
    return st.session_state["estoque"], st.session_state["carrinho"]


def selecionar_produto(produtos: tuple[Produto, ...], codigo: int) -> Produto:
    for produto in produtos:
        if produto.codigo == codigo:
            return produto
    raise ValueError("Produto selecionado não está disponível.")


def rotulo_produto(produto: Produto) -> str:
    return (
        f"[{produto.codigo}] {produto.nome} | "
        f"{produto.quantidade} un. | {formatar_moeda(produto.preco)}"
    )


def mostrar_feedback_carrinho(mensagem: str) -> None:
    if mensagem in MENSAGENS_SUCESSO_CARRINHO:
        st.success(mensagem)
        return
    st.error(mensagem)


def registrar_ultima_venda(
    itens: list[ItemCarrinho],
    metodo: str,
    total_pago: float,
) -> None:
    resumo_itens = [f"{item.produto.nome} x{item.quantidade}" for item in itens]
    st.session_state["ultima_venda"] = {
        "horario": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "metodo": metodo,
        "total": total_pago,
        "itens": resumo_itens,
    }


def renderizar_topo(estoque: Estoque, carrinho: Carrinho) -> None:
    st.markdown(
        """
        <section class="hero-panel">
            <div class="hero-eyebrow">Frente de caixa em tempo real</div>
            <h1 class="hero-title">Estoque, carrinho e pagamento no mesmo painel.</h1>
            <p class="hero-copy">
                Organize a operação do caixa com um fluxo único: cadastre produtos,
                reserve itens no carrinho e conclua a venda sem sair da tela.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    total_produtos = len(estoque.produtos)
    total_unidades = sum(produto.quantidade for produto in estoque.produtos)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Produtos", total_produtos)
    col2.metric("Unidades em estoque", total_unidades)
    col3.metric("Itens no carrinho", carrinho.quantidade_total)
    col4.metric("Venda em aberto", formatar_moeda(carrinho.total))


def renderizar_painel(estoque: Estoque, carrinho: Carrinho) -> None:
    produtos_baixo_estoque = [produto for produto in estoque.produtos if produto.quantidade <= 3]
    ultima_venda = st.session_state["ultima_venda"]
    col1, col2 = st.columns((1.2, 1))

    col1.markdown(
        f"""
        <section class="spotlight-card">
            <div class="spotlight-label">Ritmo da operação</div>
            <div class="spotlight-title">{len(produtos_baixo_estoque)} alerta(s) de reposição</div>
            <p class="spotlight-copy">
                A sessão mantém {len(estoque.produtos)} produto(s) ativo(s),
                {carrinho.quantidade_total} item(ns) reservado(s) no carrinho e
                um total parcial de {escape(formatar_moeda(carrinho.total))}.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if ultima_venda is None:
        col2.markdown(
            """
            <section class="spotlight-card">
                <div class="spotlight-label">Última venda</div>
                <div class="spotlight-title">Ainda sem fechamento</div>
                <p class="spotlight-copy">
                    Assim que uma compra for concluída, o resumo da operação aparece aqui.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )
    else:
        itens_venda = ultima_venda["itens"]
        if len(itens_venda) > 3:
            itens_venda = itens_venda[:3] + [f"+{len(ultima_venda['itens']) - 3} item(ns)"]
        resumo_venda = "<br>".join(escape(item) for item in itens_venda)
        col2.markdown(
            f"""
            <section class="spotlight-card">
                <div class="spotlight-label">Última venda</div>
                <div class="spotlight-title">{escape(formatar_moeda(ultima_venda['total']))}</div>
                <p class="spotlight-copy">
                    {escape(ultima_venda['metodo'])} • {escape(ultima_venda['horario'])}
                </p>
                <div class="receipt-list">{resumo_venda}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Estoque pedindo atenção")
    if not produtos_baixo_estoque:
        st.success("Nenhum produto em nível crítico no momento.")
        return

    st.dataframe(
        [
            {
                "Código": produto.codigo,
                "Nome": produto.nome,
                "Quantidade": produto.quantidade,
                "Preço (R$)": f"{produto.preco:.2f}",
            }
            for produto in produtos_baixo_estoque
        ],
        hide_index=True,
        use_container_width=True,
    )


def renderizar_estoque(estoque: Estoque, carrinho: Carrinho) -> None:
    st.subheader("Cadastro e manutenção do estoque")
    st.caption("Os dados permanecem ativos enquanto a sessão Streamlit estiver aberta.")
    col1, col2 = st.columns((1, 1))

    with col1:
        with st.form("form_cadastrar_produto", clear_on_submit=True):
            st.markdown("#### Novo produto")
            nome = st.text_input("Nome do produto")
            quantidade = st.number_input("Quantidade inicial", min_value=0, step=1)
            preco = st.number_input("Preço unitário", min_value=0.0, step=0.5, format="%.2f")
            cadastrar = st.form_submit_button("Cadastrar produto", use_container_width=True)
            if cadastrar:
                try:
                    produto = estoque.cadastrar(nome, int(quantidade), float(preco))
                except ValueError as exc:
                    st.error(str(exc))
                else:
                    st.success(f"Produto '{produto.nome}' cadastrado com código {produto.codigo}.")

    with col2:
        if estoque.vazio:
            st.info("Cadastre ao menos um produto para liberar edição e remoção.")
        else:
            codigos = [produto.codigo for produto in estoque.produtos]
            codigo_edicao = st.selectbox(
                "Produto para editar",
                options=codigos,
                format_func=lambda codigo: rotulo_produto(selecionar_produto(estoque.produtos, codigo)),
                key="selecionar_produto_edicao",
            )
            produto_edicao = selecionar_produto(estoque.produtos, codigo_edicao)

            with st.form("form_editar_produto"):
                st.markdown("#### Editar produto")
                novo_nome = st.text_input(
                    "Nome atualizado",
                    value=produto_edicao.nome,
                    key=f"nome_produto_{codigo_edicao}",
                )
                nova_quantidade = st.number_input(
                    "Quantidade atualizada",
                    min_value=0,
                    step=1,
                    value=int(produto_edicao.quantidade),
                    key=f"quantidade_produto_{codigo_edicao}",
                )
                novo_preco = st.number_input(
                    "Preço atualizado",
                    min_value=0.0,
                    step=0.5,
                    format="%.2f",
                    value=float(produto_edicao.preco),
                    key=f"preco_produto_{codigo_edicao}",
                )
                salvar = st.form_submit_button("Salvar alterações", use_container_width=True)
                if salvar:
                    try:
                        estoque.atualizar(
                            codigo_edicao,
                            nome=novo_nome,
                            quantidade=int(nova_quantidade),
                            preco=float(novo_preco),
                        )
                    except ValueError as exc:
                        st.error(str(exc))
                    else:
                        st.success("Produto atualizado com sucesso.")

            with st.form("form_remover_produto"):
                remover = st.form_submit_button("Remover produto selecionado", use_container_width=True)
                if remover:
                    if carrinho.contem_produto(codigo_edicao):
                        st.error("Remova o item do carrinho antes de excluir do estoque.")
                    elif estoque.remover(codigo_edicao):
                        st.success("Produto removido com sucesso.")
                    else:
                        st.error("Produto não encontrado.")

    st.markdown("#### Produtos cadastrados")
    if estoque.vazio:
        st.info("O estoque ainda está vazio.")
        return

    st.dataframe(estoque.listar(), hide_index=True, use_container_width=True)


def renderizar_carrinho(estoque: Estoque, carrinho: Carrinho) -> None:
    st.subheader("Montagem do carrinho")
    produtos_disponiveis = [produto for produto in estoque.produtos if produto.quantidade > 0]

    col1, col2 = st.columns((1, 1))
    with col1:
        if not produtos_disponiveis:
            st.info("Cadastre produtos com quantidade disponível para começar uma venda.")
        else:
            codigos = [produto.codigo for produto in produtos_disponiveis]
            codigo_produto = st.selectbox(
                "Produto para adicionar",
                options=codigos,
                format_func=lambda codigo: rotulo_produto(selecionar_produto(tuple(produtos_disponiveis), codigo)),
                key="produto_carrinho",
            )
            produto = selecionar_produto(tuple(produtos_disponiveis), codigo_produto)
            saldo_disponivel = produto.quantidade - carrinho.quantidade_do_produto(produto.codigo)
            st.caption(f"Disponível para nova reserva agora: {max(saldo_disponivel, 0)} unidade(s).")

            with st.form("form_adicionar_carrinho"):
                quantidade = st.number_input(
                    "Quantidade",
                    min_value=1,
                    step=1,
                    value=1,
                )
                adicionar = st.form_submit_button(
                    "Adicionar ao carrinho",
                    use_container_width=True,
                    disabled=saldo_disponivel <= 0,
                )
                if adicionar:
                    mensagem = carrinho.adicionar(produto, int(quantidade))
                    mostrar_feedback_carrinho(mensagem)

    with col2:
        st.markdown("#### Resumo do carrinho")
        if carrinho.vazio:
            st.info("Nenhum item reservado ainda.")
        else:
            st.dataframe(carrinho.listar(), hide_index=True, use_container_width=True)
            st.metric("Total parcial", formatar_moeda(carrinho.total))

    if carrinho.vazio:
        return

    st.markdown("#### Ajustes rápidos")
    codigos_carrinho = [item.produto.codigo for item in carrinho.itens]
    codigo_item = st.selectbox(
        "Item para remover",
        options=codigos_carrinho,
        format_func=lambda codigo: rotulo_produto(selecionar_produto(estoque.produtos, codigo)),
        key="item_remocao_carrinho",
    )
    item = next(item for item in carrinho.itens if item.produto.codigo == codigo_item)
    col3, col4 = st.columns((1, 1))
    with col3:
        with st.form("form_remover_item_carrinho"):
            quantidade_remocao = st.number_input(
                "Quantidade a remover",
                min_value=1,
                max_value=int(item.quantidade),
                step=1,
                value=1,
            )
            remover = st.form_submit_button("Remover do carrinho", use_container_width=True)
            if remover:
                mensagem = carrinho.remover(codigo_item, int(quantidade_remocao))
                mostrar_feedback_carrinho(mensagem)

    with col4:
        st.markdown("### ")
        if st.button("Limpar carrinho", use_container_width=True):
            carrinho.limpar()
            st.success("Carrinho limpo com sucesso.")


def renderizar_pagamento(carrinho: Carrinho) -> None:
    st.subheader("Fechamento da venda")
    if carrinho.vazio:
        st.info("Adicione itens ao carrinho para liberar o pagamento.")
        return

    st.dataframe(carrinho.listar(), hide_index=True, use_container_width=True)
    total = carrinho.total
    st.metric("Total da compra", formatar_moeda(total))

    metodo = st.radio(
        "Forma de pagamento",
        options=("Crédito", "Débito", "Dinheiro"),
        horizontal=True,
    )

    pagamento_valido = True
    descricao_metodo = metodo
    total_pago = total

    if metodo == "Crédito":
        parcelas = st.slider("Parcelas", min_value=1, max_value=12, value=1)
        valor_parcela = Pagamento.calcular_parcela(total, parcelas)
        total_pago = Pagamento.calcular_total_credito(total, parcelas)
        descricao_metodo = f"Crédito em {parcelas}x"
        st.info(
            f"{parcelas}x de {formatar_moeda(valor_parcela)} | "
            f"Total final: {formatar_moeda(total_pago)}"
        )
    elif metodo == "Débito":
        st.info(f"Pagamento à vista no débito: {formatar_moeda(total)}")
    else:
        valor_recebido = st.number_input(
            "Valor recebido",
            min_value=0.0,
            step=1.0,
            value=float(total),
            format="%.2f",
        )
        troco = Pagamento.calcular_troco(total, float(valor_recebido))
        if troco is None:
            pagamento_valido = False
            st.warning("O valor recebido é menor que o total da compra.")
        else:
            st.info(f"Troco: {formatar_moeda(troco)}")

    erro_estoque = carrinho.validar_estoque()
    if erro_estoque is not None:
        pagamento_valido = False
        st.error(erro_estoque)

    if st.button("Finalizar compra", use_container_width=True, disabled=not pagamento_valido):
        try:
            itens_finalizados = carrinho.finalizar()
        except ValueError as exc:
            st.error(str(exc))
        else:
            registrar_ultima_venda(itens_finalizados, descricao_metodo, total_pago)
            st.success(
                f"Venda concluída com sucesso. Total processado: {formatar_moeda(total_pago)}."
            )


def renderizar_interface_web() -> None:
    st.set_page_config(
        page_title="Sistema de Caixa",
        page_icon="\U0001F6D2",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    aplicar_estilos()
    estoque, carrinho = inicializar_estado()

    with st.sidebar:
        st.markdown("## Caixa ao vivo")
        st.write("Use as abas para cadastrar produtos, reservar itens e fechar a venda.")
        st.write(f"Produtos ativos: {len(estoque.produtos)}")
        st.write(f"Itens reservados: {carrinho.quantidade_total}")
        st.write(f"Venda em aberto: {formatar_moeda(carrinho.total)}")

    renderizar_topo(estoque, carrinho)
    aba_painel, aba_estoque, aba_carrinho, aba_pagamento = st.tabs(
        ["Painel", "Estoque", "Carrinho", "Pagamento"]
    )

    with aba_painel:
        renderizar_painel(estoque, carrinho)

    with aba_estoque:
        renderizar_estoque(estoque, carrinho)

    with aba_carrinho:
        renderizar_carrinho(estoque, carrinho)

    with aba_pagamento:
        renderizar_pagamento(carrinho)