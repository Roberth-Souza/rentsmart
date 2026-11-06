"""Tipos de imóvel do RentSmart e as regras de preço de cada um"""

from decimal import Decimal
from typing import ClassVar, override


class Imovel:
    NOME: ClassVar[str]
    ALUGUEL_BASE: ClassVar[Decimal]
    ADICIONAL_QUARTO: ClassVar[Decimal]
    QUARTOS_MIN: ClassVar[int] = 1
    QUARTOS_MAX: ClassVar[int] = 2
    VALOR_VAGA: ClassVar[Decimal] = Decimal(300)
    TEXTO_DESCONTO: ClassVar[str] = "Desconto"

    def __init__(self, quartos: int, vagas: int) -> None:
        self.quartos: int = quartos
        self.vagas: int = vagas

    def adicional_quarto(self) -> Decimal:
        if self.quartos == 2:
            return self.ADICIONAL_QUARTO
        return Decimal(0)

    def garagem(self) -> Decimal:
        if self.vagas:
            return self.VALOR_VAGA
        return Decimal(0)

    def desconto(self) -> Decimal:
        return Decimal(0)

    def itens(self) -> list[tuple[str, Decimal]]:
        itens: list[tuple[str, Decimal]] = []
        itens.append((f"Aluguel base ({self.NOME})", self.ALUGUEL_BASE))
        quarto_adicional = self.adicional_quarto()
        if quarto_adicional:
            itens.append(("Adicional 2º quarto", quarto_adicional))

        if self.vagas:
            palavra_vaga = "vaga" if self.vagas == 1 else "vagas"
            itens.append((f"Garagem ({self.vagas} {palavra_vaga})", self.garagem()))

        valor_desconto = self.desconto()

        if valor_desconto:
            itens.append((self.TEXTO_DESCONTO, -valor_desconto))

        return itens

    def aluguel_mensal(self) -> Decimal:
        aluguel_mensal = Decimal(0)

        for _texto, valor in self.itens():
            aluguel_mensal += valor

        return aluguel_mensal


class Casa(Imovel):
    NOME: ClassVar[str] = "casa"
    ALUGUEL_BASE: ClassVar[Decimal] = Decimal(900)
    ADICIONAL_QUARTO: ClassVar[Decimal] = Decimal(250)


class Apartamento(Imovel):
    NOME: ClassVar[str] = "apartamento"
    ALUGUEL_BASE: ClassVar[Decimal] = Decimal(700)
    ADICIONAL_QUARTO: ClassVar[Decimal] = Decimal(200)
    TEXTO_DESCONTO: ClassVar[str] = "Desconto sem crianças (5%)"

    def __init__(self, quartos: int, vagas: int, criancas: bool) -> None:
        super().__init__(
            quartos,
            vagas,
        )
        self.criancas: bool = criancas

    @override
    def desconto(self) -> Decimal:
        if not self.criancas:
            total = self.ALUGUEL_BASE + self.adicional_quarto() + self.garagem()

            return total * Decimal("0.05")
        return Decimal(0)


class Estudio(Imovel):
    NOME: ClassVar[str] = "estúdio"
    ALUGUEL_BASE: ClassVar[Decimal] = Decimal(1200)
    PACOTE_DUAS_VAGAS: ClassVar[Decimal] = Decimal(250)
    VAGA_EXTRA: ClassVar[Decimal] = Decimal(60)

    def __init__(self, vagas: int) -> None:
        # O estúdio não tem quartos declarados no enunciado, por isto fixei em 1
        # Para ser ler como uma estrutura só
        super().__init__(quartos=1, vagas=vagas)

    @override
    def garagem(self) -> Decimal:
        if self.vagas:
            return self.PACOTE_DUAS_VAGAS + self.VAGA_EXTRA * (self.vagas - 2)
        return Decimal(0)
