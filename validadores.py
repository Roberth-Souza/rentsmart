"""Conjunto de validadores de entrada do RentSmart"""

from imoveis import Apartamento, Casa, Estudio

SIM_NAO = {True: {"s", "sim"}, False: {"n", "nao", "não"}}
OPCOES_TIPO = {"1": Casa, "2": Apartamento, "3": Estudio}


def validar_inteiro(resposta: str, minimo: int, maximo: int | None) -> int:
    """Recebe um texto, tenta converter para inteiro e verifica se ele está entre o mínimo e o máximo.
    Aqui o máximo pode ser None, por conta do Estúdio, onde não há limite explícito de vagas"""
    try:
        resposta_inteira = int(resposta)
    except ValueError:
        raise ValueError("Digite um número inteiro")

    if resposta_inteira < minimo:
        raise ValueError(f"{resposta_inteira} é um valor menor que o mínimo ({minimo})")

    if maximo is None:
        return resposta_inteira

    if resposta_inteira > maximo:
        raise ValueError(
            f"O valor {resposta_inteira} não está dentro do mínimo ({minimo}) e máximo ({maximo}) permitidos"
        )

    return resposta_inteira


def validar_sim_nao(resposta: str) -> bool:
    """Valida se o parâmetro resposta está entre o conjunto de respostas válidas
    de sim ou não"""
    resposta_parseada = resposta.strip().lower()

    for prefixo, respostas in SIM_NAO.items():
        if resposta_parseada in respostas:
            return prefixo

    raise ValueError('Digite somente "s" ou "n"')


def validar_imovel(resposta: str) -> type[Casa] | type[Apartamento] | type[Estudio]:
    """Valida se o parâmetro resposta está entre as opções de imóvel válidas"""
    resposta_parseada = resposta.strip().lower()
    imovel = OPCOES_TIPO.get(resposta_parseada)
    if imovel is not None:
        return imovel

    raise ValueError("Digite uma opção válida")
