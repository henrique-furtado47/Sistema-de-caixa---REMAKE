from __future__ import annotations

import os

from src.services import Carrinho, Estoque, Pagamento


def limpar_tela() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def exibir_tabela(dados: list[dict], titulo: str = "") -> None:
    """Exibe uma lista de dicts como tabela formatada no terminal."""
    if not dados:
        print("Nenhum dado para exibir.")
        return

    if titulo:
        print(f"\n{'─' * 60}")
        print(f"  {titulo}")
        print(f"{'─' * 60}")

    colunas = list(dados[0].keys())
    larguras = {col: max(len(str(col)), *(len(str(d[col])) for d in dados)) for col in colunas}

    header = " | ".join(col.ljust(larguras[col]) for col in colunas)
    print(header)
    print("-+-".join("-" * larguras[col] for col in colunas))

    for linha in dados:
        print(" | ".join(str(linha[col]).ljust(larguras[col]) for col in colunas))
    print()


class SistemaDeCaixa:
    """Orquestra estoque, carrinho e pagamento via terminal."""

    def __init__(self) -> None:
        self.estoque = Estoque()
        self.carrinho = Carrinho()

    # ── menus ──────────────────────────────────────────────

    def _menu_estoque(self) -> None:
        opcoes = {
            1: self._cadastrar_produto,
            2: self._listar_estoque,
            3: self._remover_produto,
            4: self._atualizar_produto,
            5: self._localizar_produto,
        }
        print("\n--- Estoque ---")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Remover produto")
        print("4 - Atualizar produto")
        print("5 - Localizar produto")
        print("0 - Voltar")

        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            return

        acao = opcoes.get(opcao)
        if acao:
            acao()
        elif opcao != 0:
            print("Opção inválida!")

    def _menu_carrinho(self) -> None:
        print("\n--- Carrinho ---")
        print("1 - Adicionar produto")
        print("2 - Listar produtos")
        print("3 - Limpar carrinho")
        print("4 - Remover produto")
        print("5 - Finalizar compra")
        print("0 - Voltar")

        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Digite um número válido!")
            return

        acoes = {
            1: self._adicionar_ao_carrinho,
            2: self._listar_carrinho,
            3: self._limpar_carrinho,
            4: self._remover_do_carrinho,
            5: self._finalizar_compra,
        }
        acao = acoes.get(opcao)
        if acao:
            acao()
        elif opcao == 0:
            limpar_tela()
        else:
            print("Opção inválida!")

    # ── ações do estoque ───────────────────────────────────

    def _cadastrar_produto(self) -> None:
        nome = input("Nome do produto: ")
        try:
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
        except ValueError:
            print("Valores inválidos!")
            return
        produto = self.estoque.cadastrar(nome, quantidade, preco)
        print(f"✔ Produto '{produto.nome}' cadastrado com código {produto.codigo}.")

    def _listar_estoque(self) -> None:
        limpar_tela()
        dados = self.estoque.listar()
        exibir_tabela(dados, "ESTOQUE")

    def _remover_produto(self) -> None:
        try:
            codigo = int(input("Código do produto: "))
        except ValueError:
            print("Código inválido!")
            return
        if self.estoque.remover(codigo):
            print("✔ Produto removido com sucesso!")
        else:
            print("✘ Produto não encontrado.")

    def _atualizar_produto(self) -> None:
        try:
            codigo = int(input("Código do produto: "))
        except ValueError:
            print("Código inválido!")
            return

        produto = self.estoque.buscar_por_codigo(codigo)
        if produto is None:
            print("✘ Produto não encontrado.")
            return

        print("1 - Nome  |  2 - Quantidade  |  3 - Preço  |  0 - Cancelar")
        try:
            opcao = int(input("O que atualizar? "))
        except ValueError:
            print("Opção inválida!")
            return

        if opcao == 1:
            produto.nome = input("Novo nome: ")
        elif opcao == 2:
            produto.quantidade = int(input("Nova quantidade: "))
        elif opcao == 3:
            produto.preco = float(input("Novo preço: "))
        elif opcao == 0:
            return
        else:
            print("Opção inválida!")
            return
        print("✔ Produto atualizado!")

    def _localizar_produto(self) -> None:
        print("1 - Por nome  |  2 - Por código")
        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Opção inválida!")
            return

        produto = None
        if opcao == 1:
            nome = input("Nome: ")
            produto = self.estoque.buscar_por_nome(nome)
        elif opcao == 2:
            codigo = int(input("Código: "))
            produto = self.estoque.buscar_por_codigo(codigo)
        else:
            print("Opção inválida!")
            return

        if produto:
            print(f"✔ Encontrado: {produto}")
        else:
            print("✘ Produto não encontrado.")

    # ── ações do carrinho ──────────────────────────────────

    def _adicionar_ao_carrinho(self) -> None:
        try:
            codigo = int(input("Código do produto: "))
        except ValueError:
            print("Código inválido!")
            return

        produto = self.estoque.buscar_por_codigo(codigo)
        if produto is None:
            print("✘ Produto não encontrado no estoque!")
            return

        try:
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("Quantidade inválida!")
            return

        msg = self.carrinho.adicionar(produto, quantidade)
        print(msg)

    def _listar_carrinho(self) -> None:
        limpar_tela()
        dados = self.carrinho.listar()
        exibir_tabela(dados, "CARRINHO")
        if not self.carrinho.vazio:
            print(f"  TOTAL: R${self.carrinho.total:.2f}\n")

    def _limpar_carrinho(self) -> None:
        opcao = input("Tem certeza? (s/n): ").strip().lower()
        if opcao == "s":
            self.carrinho.limpar()
            limpar_tela()
            print("✔ Carrinho limpo!")
        else:
            print("Operação cancelada.")

    def _remover_do_carrinho(self) -> None:
        try:
            codigo = int(input("Código do produto: "))
            quantidade = int(input("Quantidade a remover: "))
        except ValueError:
            print("Valores inválidos!")
            return
        msg = self.carrinho.remover(codigo, quantidade)
        print(msg)

    def _finalizar_compra(self) -> None:
        if self.carrinho.vazio:
            print("Carrinho está vazio!")
            return

        total = self.carrinho.total
        limpar_tela()
        print(f"\n  Total da compra: R${total:.2f}\n")
        self._processar_pagamento(total)
        self.carrinho.finalizar()
        print("\n✔ Compra finalizada com sucesso!")

    def _processar_pagamento(self, total: float) -> None:
        print("Método de pagamento:")
        print("1 - Crédito  |  2 - Débito  |  3 - Dinheiro")

        try:
            opcao = int(input("Opção: "))
        except ValueError:
            print("Opção inválida!")
            return

        if opcao == 1:
            parcelas = int(input("Número de parcelas: "))
            valor = Pagamento.calcular_parcela(total, parcelas)
            print(f"{parcelas}x de R${valor:.2f}")
        elif opcao == 2:
            print(f"Total no débito: R${total:.2f}")
        elif opcao == 3:
            dinheiro = float(input("Valor recebido: "))
            troco = Pagamento.calcular_troco(total, dinheiro)
            if troco is None:
                print("✘ Valor insuficiente!")
                return
            print(f"Troco: R${troco:.2f}")
        else:
            print("Opção inválida!")
            return

        print("✔ Pagamento realizado com sucesso!")

    # ── loop principal ─────────────────────────────────────

    def executar(self) -> None:
        while True:
            print("\n╔══════════════════════════╗")
            print("║   SISTEMA DE CAIXA       ║")
            print("╠══════════════════════════╣")
            print("║  1 - Acessar estoque     ║")
            print("║  2 - Acessar carrinho    ║")
            print("║  0 - Sair                ║")
            print("╚══════════════════════════╝")

            try:
                opcao = int(input("Opção: "))
            except ValueError:
                print("Digite um número válido!")
                continue

            if opcao == 1:
                self._menu_estoque()
            elif opcao == 2:
                self._menu_carrinho()
            elif opcao == 0:
                limpar_tela()
                print("FIM DO PROGRAMA")
                break
            else:
                print("Opção inválida!")
