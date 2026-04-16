"""Ponto de entrada do Sistema de Caixa."""

from src.ui import SistemaDeCaixa


def main() -> None:
    sistema = SistemaDeCaixa()
    sistema.executar()


if __name__ == "__main__":
    main()
