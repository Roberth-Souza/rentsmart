"""Testes do RentSmart: orçamentos de referência e validadores da entrada.

Rodar: python test_orcamentos.py   (também roda com: pytest)

Nenhum teste passa pelo input(): os objetos são criados direto
e os validadores recebem o texto como se o usuário tivesse digitado.
Os valores esperados foram calculados à mão, separados do código.
"""

from collections.abc import Callable
from decimal import Decimal

from imoveis import Apartamento, Casa, Estudio
from orcamento import MESES_PROJECAO, Orcamento, TaxaContratual, montar_orcamento
from validadores import validar_imovel, validar_inteiro, validar_sim_nao

# ---------- Auxiliares ----------


def conferir_orcamento(
    orcamento: Orcamento,
    aluguel_esperado: Decimal,
    parcelas_esperadas: list[Decimal],
    soma_esperada: Decimal,
) -> None:
    """Confere aluguel, taxa e as 12 linhas da projeção contra o gabarito."""
    assert orcamento.aluguel_mensal == aluguel_esperado
    assert orcamento.taxa_total == Decimal(2000)
    assert orcamento.parcelas == parcelas_esperadas
    assert sum(orcamento.parcelas) == orcamento.taxa_total

    assert len(orcamento.projecao) == MESES_PROJECAO
    for linha in orcamento.projecao:
        # Meses 1..N pagam a parcela N; do mês N+1 em diante, parcela 0
        if linha.mes <= len(parcelas_esperadas):
            parcela = parcelas_esperadas[linha.mes - 1]
        else:
            parcela = Decimal(0)
        assert linha.aluguel == aluguel_esperado
        assert linha.parcela_taxa == parcela
        assert linha.total_mes == aluguel_esperado + parcela

    meses = [linha.mes for linha in orcamento.projecao]
    assert meses == list(range(1, MESES_PROJECAO + 1))

    soma = sum(linha.total_mes for linha in orcamento.projecao)
    assert soma == soma_esperada


def mensagem_de_erro(validador: Callable[..., object], *args: object) -> str | None:
    """Chama o validador e devolve a mensagem do ValueError, ou None se ele aceitou."""
    try:
        _ = validador(*args)  # só interessa se levanta erro
    except ValueError as erro:
        return str(erro)
    return None


# ---------- A. Orçamentos de referência (calculados à mão) ----------


def test_caso_1_apartamento_1_quarto_com_criancas_sem_garagem_1x() -> None:
    imovel = Apartamento(quartos=1, vagas=0, criancas=True)

    assert imovel.itens() == [("Aluguel base (apartamento)", Decimal(700))]

    conferir_orcamento(
        montar_orcamento(imovel, TaxaContratual(1)),
        aluguel_esperado=Decimal(700),
        parcelas_esperadas=[Decimal(2000)],
        soma_esperada=Decimal(10400),
    )


def test_caso_2_apartamento_2_quartos_sem_criancas_com_garagem_3x() -> None:
    imovel = Apartamento(quartos=2, vagas=1, criancas=False)

    # Desconto de 5% sobre o subtotal com os adicionais: base + quarto + garagem
    assert imovel.itens() == [
        ("Aluguel base (apartamento)", Decimal(700)),
        ("Adicional 2º quarto", Decimal(200)),
        ("Garagem (1 vaga)", Decimal(300)),
        ("Desconto sem crianças (5%)", Decimal(-60)),
    ]

    # 2000 / 3 não fecha em centavos: a última parcela absorve a diferença
    conferir_orcamento(
        montar_orcamento(imovel, TaxaContratual(3)),
        aluguel_esperado=Decimal(1140),
        parcelas_esperadas=[Decimal("666.67"), Decimal("666.67"), Decimal("666.66")],
        soma_esperada=Decimal(15680),
    )


def test_caso_3_casa_2_quartos_com_garagem_5x() -> None:
    imovel = Casa(quartos=2, vagas=1)

    # Casa não tem linha de desconto
    assert imovel.itens() == [
        ("Aluguel base (casa)", Decimal(900)),
        ("Adicional 2º quarto", Decimal(250)),
        ("Garagem (1 vaga)", Decimal(300)),
    ]

    conferir_orcamento(
        montar_orcamento(imovel, TaxaContratual(5)),
        aluguel_esperado=Decimal(1450),
        parcelas_esperadas=[Decimal(400)] * 5,
        soma_esperada=Decimal(19400),
    )


def test_caso_4_estudio_0_vagas_2x() -> None:
    imovel = Estudio(vagas=0)

    # Garagem é opcional: estúdio sem vagas não cobra o pacote
    assert imovel.itens() == [("Aluguel base (estúdio)", Decimal(1200))]

    conferir_orcamento(
        montar_orcamento(imovel, TaxaContratual(2)),
        aluguel_esperado=Decimal(1200),
        parcelas_esperadas=[Decimal(1000)] * 2,
        soma_esperada=Decimal(16400),
    )


def test_caso_5_estudio_4_vagas_4x() -> None:
    imovel = Estudio(vagas=4)

    # Pacote de 2 vagas (250) + 2 adicionais × 60 = 370
    assert imovel.itens() == [
        ("Aluguel base (estúdio)", Decimal(1200)),
        ("Garagem (4 vagas)", Decimal(370)),
    ]

    conferir_orcamento(
        montar_orcamento(imovel, TaxaContratual(4)),
        aluguel_esperado=Decimal(1570),
        parcelas_esperadas=[Decimal(500)] * 4,
        soma_esperada=Decimal(20840),
    )


# ---------- B. Validadores (validadores.py) ----------


def test_validar_inteiro_aceita_dentro_da_faixa() -> None:
    assert validar_inteiro("1", 1, 2) == 1
    assert validar_inteiro("2", 1, 2) == 2
    assert validar_inteiro("5", 1, 5) == 5
    assert validar_inteiro(" 3 ", 1, 5) == 3  # int() ignora espaços nas pontas


def test_validar_inteiro_sem_maximo() -> None:
    # Vagas adicionais do estúdio: mínimo 0, sem teto (o enunciado não dá limite)
    assert validar_inteiro("0", 0, None) == 0
    assert validar_inteiro("100", 0, None) == 100
    assert mensagem_de_erro(validar_inteiro, "-1", 0, None) is not None


def test_validar_inteiro_recusa_fora_da_faixa() -> None:
    assert mensagem_de_erro(validar_inteiro, "0", 1, 2) is not None
    assert mensagem_de_erro(validar_inteiro, "3", 1, 2) is not None
    assert mensagem_de_erro(validar_inteiro, "6", 1, 5) is not None


def test_validar_inteiro_recusa_texto_que_nao_e_inteiro() -> None:
    # A mensagem do int() sai em inglês; o validador troca por uma em português
    for resposta in ["abc", "", "1.5", "dois"]:
        assert mensagem_de_erro(validar_inteiro, resposta, 1, 2) == (
            "Digite um número inteiro"
        )


def test_validar_sim_nao_aceita_variacoes() -> None:
    for resposta in ["s", "sim", "S", " Sim "]:
        assert validar_sim_nao(resposta) is True
    for resposta in ["n", "nao", "não", "NÃO", " N "]:
        assert validar_sim_nao(resposta) is False


def test_validar_sim_nao_recusa_outras_respostas() -> None:
    for resposta in ["", "talvez", "y", "1"]:
        assert mensagem_de_erro(validar_sim_nao, resposta) == (
            'Digite somente "s" ou "n"'
        )


def test_validar_imovel_devolve_a_classe() -> None:
    assert validar_imovel("1") is Casa
    assert validar_imovel("2") is Apartamento
    assert validar_imovel("3") is Estudio
    assert validar_imovel(" 2 ") is Apartamento


def test_validar_imovel_recusa_opcao_invalida() -> None:
    for resposta in ["", "0", "4", "casa"]:
        assert mensagem_de_erro(validar_imovel, resposta) == "Digite uma opção válida"


TESTES: list[Callable[[], None]] = [
    test_caso_1_apartamento_1_quarto_com_criancas_sem_garagem_1x,
    test_caso_2_apartamento_2_quartos_sem_criancas_com_garagem_3x,
    test_caso_3_casa_2_quartos_com_garagem_5x,
    test_caso_4_estudio_0_vagas_2x,
    test_caso_5_estudio_4_vagas_4x,
    test_validar_inteiro_aceita_dentro_da_faixa,
    test_validar_inteiro_sem_maximo,
    test_validar_inteiro_recusa_fora_da_faixa,
    test_validar_inteiro_recusa_texto_que_nao_e_inteiro,
    test_validar_sim_nao_aceita_variacoes,
    test_validar_sim_nao_recusa_outras_respostas,
    test_validar_imovel_devolve_a_classe,
    test_validar_imovel_recusa_opcao_invalida,
]


if __name__ == "__main__":
    # Um assert que falhar interrompe aqui e o traceback mostra qual teste e qual linha
    for teste in TESTES:
        teste()
        print(f"OK  {teste.__name__}")
    print(f"\n{len(TESTES)} testes passaram.")
