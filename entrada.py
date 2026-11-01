"""Lida com a entrada de dados do usuário"""

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def ler_resposta_valida(pergunta: str, validador: Callable[..., T], *args: object) -> T:
    """Recebe uma pergunta e repete ela até que o validador (uma função passada como parâmetro)
    retorne sem erros"""
    while True:
        try:
            return validador(input(pergunta), *args)
        except ValueError as error:
            print(error)
