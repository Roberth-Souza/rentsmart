"""Ponto de entrada do RentSmart: pergunta, monta o orçamento, mostra e salva.

Rodar: python main.py
"""

from pathlib import Path

from entrada import ler_resposta_valida
from imoveis import Apartamento, Casa, Estudio, Imovel
from orcamento import TaxaContratual, montar_orcamento
from saida import gravar_csv, imprimir_resumo
from validadores import OPCOES_TIPO, validar_imovel, validar_inteiro, validar_sim_nao

# Sempre na pasta do projeto, independente de onde o comando foi rodado
CAMINHO_CSV = Path(__file__).parent / "projecao_12_meses.csv"


def ler_quartos(classe: type[Imovel]) -> int:
    """Pergunta o nº de quartos usando a faixa da classe escolhida."""
    minimo = classe.QUARTOS_MIN
    maximo = classe.QUARTOS_MAX
    return ler_resposta_valida(
        f"Quantos quartos? ({minimo}-{maximo}) ", validar_inteiro, minimo, maximo
    )


def ler_vaga_garagem() -> int:
    """Casa/apartamento: 1 vaga opcional. Converte o s/n em nº de vagas."""
    quer_garagem = ler_resposta_valida(
        "Deseja 1 vaga de garagem? (s/n) ", validar_sim_nao
    )
    return 1 if quer_garagem else 0


def ler_vagas_estudio() -> int:
    """Estúdio: 0 vagas, ou o pacote de 2 + quantas adicionais o cliente quiser."""
    quer_pacote = ler_resposta_valida(
        "Deseja o pacote de 2 vagas de garagem? (s/n) ", validar_sim_nao
    )
    if not quer_pacote:
        return 0

    adicionais = ler_resposta_valida(
        "Quantas vagas adicionais além das 2? (0 ou mais) ", validar_inteiro, 0, None
    )
    return 2 + adicionais


def ler_imovel() -> Imovel:
    """Mostra o menu, faz as perguntas do tipo escolhido e cria o imóvel.

    Único ponto do programa que ramifica por tipo (CLASSES.md §4.8):
    cada tipo pede perguntas e argumentos diferentes.
    """
    print("Tipo de imóvel:")
    for opcao, classe_opcao in OPCOES_TIPO.items():
        print(f"  {opcao} - {classe_opcao.NOME.capitalize()}")
    classe = ler_resposta_valida("Opção: ", validar_imovel)

    if classe is Casa:
        quartos = ler_quartos(classe)
        vagas = ler_vaga_garagem()
        return Casa(quartos, vagas)

    if classe is Apartamento:
        quartos = ler_quartos(classe)
        vagas = ler_vaga_garagem()
        criancas = ler_resposta_valida("Tem crianças? (s/n) ", validar_sim_nao)
        return Apartamento(quartos, vagas, criancas)

    # Sobrou o estúdio: não pergunta quartos (fixo em 1 dentro da classe)
    vagas = ler_vagas_estudio()
    return Estudio(vagas)


def ler_taxa() -> TaxaContratual:
    """Pergunta em quantas parcelas paga a taxa contratual (1 = à vista)."""
    minimo = TaxaContratual.PARCELAS_MIN
    maximo = TaxaContratual.PARCELAS_MAX
    parcelas = ler_resposta_valida(
        f"Em quantas parcelas deseja pagar a taxa contratual? ({minimo}-{maximo}) ",
        validar_inteiro,
        minimo,
        maximo,
    )
    return TaxaContratual(parcelas)


def main() -> None:
    print("===== RentSmart — Orçamento de locação =====\n")
    imovel = ler_imovel()
    taxa = ler_taxa()

    orcamento = montar_orcamento(imovel, taxa)
    print()
    imprimir_resumo(orcamento)

    # gravar_csv deixa o erro subir; quem decide o que fazer é a main (CLASSES.md §5.2)
    try:
        gravar_csv(orcamento, CAMINHO_CSV)
    except OSError as erro:
        print(f"\nNão foi possível salvar o CSV: {erro}")
        return

    print(f"\nProjeção de 12 meses salva em: {CAMINHO_CSV}")


if __name__ == "__main__":
    # Ctrl+C (KeyboardInterrupt) ou fim da entrada (EOFError) encerram sem traceback
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nOrçamento cancelado.")
