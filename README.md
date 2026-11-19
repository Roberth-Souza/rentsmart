# RentSmart

Orçamento de locação da R.M Imóveis em Python com Orientação a Objetos.
O programa pergunta as características da locação, calcula o aluguel mensal e a taxa contratual, mostra um resumo no terminal e gera a projeção de 12 meses em CSV.

## Requisitos

- Python 3.12 ou superior.
- Só a biblioteca padrão: nada para instalar.

## Como rodar

Na pasta do projeto:

```bash
python main.py
```

Dependendo do sistema, o comando pode ser `python3` (Linux/macOS) ou `py` (Windows).

## Saída

- **Terminal:** itens do aluguel (base, adicionais, desconto), aluguel mensal, taxa contratual com as parcelas e o valor a pagar em cada mês.
- **CSV:** `projecao_12_meses.csv`, salvo na pasta do projeto (de onde quer que o comando seja rodado). Uma linha por mês com aluguel, parcela da taxa e total. Usa `;` como separador e vírgula decimal: abre direto no Excel ou LibreOffice.

## Testes

```bash
python test_orcamentos.py
```

Confere 5 orçamentos calculados à mão (um de cada tipo de imóvel, com e sem adicionais/desconto) e os validadores da entrada.

## Decisões sobre o enunciado

Pontos que o enunciado deixa em aberto:

| ponto | decisão |
|---|---|
| Desconto de 5% (apartamento sem crianças) | Incide sobre base + 2º quarto + garagem: "após a aplicação dos adicionais", no plural. |
| Parcelas da taxa | Arredondadas em centavos; a última absorve a diferença (3x = 666,67 + 666,67 + 666,66). |
| Projeção no CSV | Aluguel e parcela da taxa em colunas separadas, mais o total do mês. |
| Quartos | Só 1 ou 2: o enunciado não define preço para 3 ou mais. |
| Garagem de casa/apartamento | Opcional, no máximo 1 vaga. |
| Garagem do estúdio | Opcional: 0 vagas ou o pacote de 2 + adicionais, sem limite máximo. |

## Estrutura

```
rentsmart/
├── main.py             # ponto de entrada: pergunta, monta o orçamento, mostra e salva
├── entrada.py          # repete a pergunta até a resposta ser válida
├── validadores.py      # validam e convertem cada resposta (sem input/print)
├── imoveis.py          # Imovel e as filhas Casa, Apartamento, Estudio: regras de preço
├── orcamento.py        # TaxaContratual, projeção de 12 meses e montagem do orçamento
├── saida.py            # resumo no terminal e gravação do CSV
├── test_orcamentos.py  # testes
└── FLUXOGRAMA.md       # fluxo do programa
```
