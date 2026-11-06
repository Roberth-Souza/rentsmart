"""Saída do orçamento: resumo no terminal e projeção de 12 meses em CSV."""

import csv
from decimal import Decimal
from pathlib import Path

from orcamento import Orcamento

# Larguras das colunas do resumo no terminal
LARGURA_TEXTO = 30
LARGURA_VALOR = 13
LARGURA_TOTAL = LARGURA_TEXTO + LARGURA_VALOR


def formatar_csv(valor: Decimal) -> str:
    """Valor para o CSV: vírgula decimal, sem símbolo nem milhar (ex.: 1234,56)."""
    return f"{valor:.2f}".replace(".", ",")


def formatar_brl(valor: Decimal) -> str:
    """Valor em reais para o terminal (ex.: R$ 1.234,56)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_titulo(titulo: str) -> str:
    """Título centralizado entre '=' na largura do resumo."""
    return f" {titulo} ".center(LARGURA_TOTAL, "=")


def formatar_linha(texto: str, valor: Decimal) -> str:
    """Texto alinhado à esquerda e valor em R$ alinhado à direita."""
    return f"{texto:<{LARGURA_TEXTO}}{formatar_brl(valor):>{LARGURA_VALOR}}"


def gravar_csv(orcamento: Orcamento, caminho: Path) -> None:
    """Grava a projeção de 12 meses, uma linha por mês.
    Erro ao abrir/escrever (OSError) sobe para quem chamou: a main decide o que fazer."""
    with open(caminho, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["Mês", "Aluguel", "Parcela da taxa", "Total do mês"])

        for linha in orcamento.projecao:
            escritor.writerow(
                [
                    linha.mes,
                    formatar_csv(linha.aluguel),
                    formatar_csv(linha.parcela_taxa),
                    formatar_csv(linha.total_mes),
                ]
            )


def imprimir_resumo(orcamento: Orcamento) -> None:
    """Mostra os itens do aluguel, a taxa contratual
    e o valor a pagar em cada mês."""
    print(formatar_titulo("RESUMO DO ORÇAMENTO"))
    for texto, valor in orcamento.itens:
        print(formatar_linha(texto, valor))
    print("-" * LARGURA_TOTAL)
    print(formatar_linha("ALUGUEL MENSAL", orcamento.aluguel_mensal))

    print()
    print(formatar_titulo("TAXA CONTRATUAL"))
    print(formatar_linha("Total", orcamento.taxa_total))

    quantidade_parcelas = len(orcamento.parcelas)
    if quantidade_parcelas == 1:
        print("Pagamento à vista")
    else:
        print(f"Parcelado em {quantidade_parcelas}x")
        for numero, parcela in enumerate(orcamento.parcelas, start=1):
            print(formatar_linha(f"  Parcela {numero}", parcela))

    # Mês a mês enquanto tem parcela (a última pode diferir em centavos);
    # depois o valor é sempre o aluguel, numa linha só.
    print()
    print(formatar_titulo("VALOR MENSAL A PAGAR"))
    for linha in orcamento.projecao[:quantidade_parcelas]:
        print(formatar_linha(f"  Mês {linha.mes}", linha.total_mes))
    primeiro_sem_parcela = quantidade_parcelas + 1
    ultimo_mes = len(orcamento.projecao)
    print(
        formatar_linha(
            f"  Meses {primeiro_sem_parcela} a {ultimo_mes}",
            orcamento.aluguel_mensal,
        )
    )
    print("=" * LARGURA_TOTAL)
