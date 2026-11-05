"""Orçamento: taxa contratual, projeção de 12 meses e montagem do orçamento."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from imoveis import Imovel

CENTAVO = Decimal("0.01")
MESES_PROJECAO = 12


@dataclass(frozen=True)
class LinhaProjecao:
    """Um mês da projeção de 12 meses"""

    mes: int
    aluguel: Decimal
    parcela_taxa: Decimal
    total_mes: Decimal


@dataclass(frozen=True)
class Orcamento:
    """Resultado do orcamento, informações para a interface"""

    itens: list[tuple[str, Decimal]]
    aluguel_mensal: Decimal
    taxa_total: Decimal
    parcelas: list[Decimal]
    projecao: list[LinhaProjecao]


class TaxaContratual:
    """Taxa contratual (valor na constante VALOR),
    parcelada entre PARCELAS_MIN e PARCELAS_MAX vezes"""

    VALOR: Decimal = Decimal(2000)
    PARCELAS_MIN: int = 1
    PARCELAS_MAX: int = 5

    def __init__(self, parcelas_totais: int) -> None:
        self.parcelas_totais: int = parcelas_totais

    def parcelas(self) -> list[Decimal]:
        """Devolve o valor de cada parcela, em ordem.
        Arredondadas para centavos"""

        lista_parcelas: list[Decimal] = []
        parcela = self.VALOR / self.parcelas_totais
        parcela = parcela.quantize(CENTAVO, ROUND_HALF_UP)

        for _ in range(self.parcelas_totais - 1):
            lista_parcelas.append(parcela.quantize(CENTAVO, ROUND_HALF_UP))

        # a última absorve a diferença para a soma fechar exatamente em VALOR
        # (EX: VALOR = 2000; em 3x → 666,67 + 666,67 + 666,66).

        ultima_parcela = self.VALOR - sum(lista_parcelas)
        lista_parcelas.append(ultima_parcela.quantize(CENTAVO))

        return lista_parcelas


def montar_orcamento(imovel: Imovel, taxa: TaxaContratual) -> Orcamento:
    """Calcula aluguel, parcelas da taxa e a projeção de 12 meses."""
    projecao: list[LinhaProjecao] = []
    itens = imovel.itens()
    aluguel = imovel.aluguel_mensal()
    lista_parcelas = taxa.parcelas()
    quantidade_parcelas = len(lista_parcelas)

    for mes in range(MESES_PROJECAO):
        mes_atual = mes + 1  # O range começa em 0, e o mes em 1, por isso o + 1 aqui
        if mes < quantidade_parcelas:
            parcela_taxa = lista_parcelas[mes]
        else:
            parcela_taxa = Decimal(0)

        total_mes = aluguel + parcela_taxa
        projecao.append(
            LinhaProjecao(
                mes=mes_atual,
                aluguel=aluguel,
                parcela_taxa=parcela_taxa,
                total_mes=total_mes,
            )
        )

    return Orcamento(
        itens=itens,
        aluguel_mensal=aluguel,
        taxa_total=taxa.VALOR,
        parcelas=lista_parcelas,
        projecao=projecao,
    )
