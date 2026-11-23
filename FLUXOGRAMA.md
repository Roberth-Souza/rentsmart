# RentSmart — Fluxograma

> Fluxo do programa: entradas, cálculo do aluguel, taxa contratual e saídas. Caixas com borda dupla `[[ ]]` = sub-processo
> "Ler resposta válida" (diagrama 2), reaproveitado em toda pergunta.
>
> O fluxo principal está dividido em 3 partes ligadas por conectores: o círculo **A** no fim da parte 1.1
> continua no círculo **A** do início da parte 1.2, e assim por diante.

## 1. Fluxo principal

### 1.1 Entrada de dados

```mermaid
flowchart TD
    INI([Início]) --> TIPO[["Ler tipo de imóvel (menu)<br/>1 casa · 2 apartamento · 3 estúdio"]]
    TIPO --> QUAL{"Tipo?"}

    QUAL -->|apartamento| AQ[["Ler nº de quartos (1 ou 2)"]]
    AQ --> AG[["Ler garagem (s/n)"]]
    AG --> AC[["Ler se tem crianças (s/n)"]]

    QUAL -->|casa| CQ[["Ler nº de quartos (1 ou 2)"]]
    CQ --> CG[["Ler garagem (s/n)"]]

    QUAL -->|estúdio| EP[["Ler pacote de 2 vagas (s/n)"]]
    EP -->|sim| EA[["Ler vagas adicionais (≥ 0)<br/>vagas = 2 + adicionais"]]

    AC --> PARC[["Ler nº de parcelas da taxa (1 a 5)"]]
    CG --> PARC
    EP -->|"não (vagas = 0)"| PARC
    EA --> PARC

    PARC --> CA((A))
```

### 1.2 Cálculo: aluguel mensal e taxa contratual

```mermaid
flowchart LR
    CA((A)) --> ALUGUEL

    subgraph ALUGUEL ["Aluguel mensal"]
        direction TB
        BASE["aluguel = base do tipo<br/>apto 700 · casa 900 · estúdio 1200"]
        BASE --> Q2{"2 quartos?"}
        Q2 -->|sim| ADQ["+ adicional do quarto<br/>apto 200 · casa 250"]
        Q2 -->|não| GAR{"Tem garagem?"}
        ADQ --> GAR

        GAR -->|"sim, casa/apto"| G1["+ 300 (1 vaga)"]
        GAR -->|"sim, estúdio"| G2["+ 250 (pacote 2 vagas)<br/>+ 60 × (vagas − 2)"]
        GAR -->|não| DESC{"Apartamento<br/>sem crianças?"}
        G1 --> DESC
        G2 --> DESC

        DESC -->|sim| D5["− 5% sobre o subtotal<br/>(base + quarto + garagem)"]
        DESC -->|não| FINAL["aluguel mensal final"]
        D5 --> FINAL
    end

    subgraph TAXA_CONTRATUAL ["Taxa contratual — separada do aluguel"]
        TAXA["parcela da taxa contratual = 2000 / N<br/>arredondada em 2 casas<br/>última parcela absorve a diferença"]
    end

    ALUGUEL --> TAXA_CONTRATUAL
    TAXA_CONTRATUAL --> CB((B))
```

### 1.3 Projeção de 12 meses e saídas

```mermaid
flowchart TD
    CB((B)) --> M1

    subgraph PROJECAO ["Projeção de 12 meses — calculada antes de qualquer saída"]
        M1["mes = 1"]
        M1 --> MQ{"mes ≤ 12?"}
        MQ -->|sim| LIN["parcela_taxa = parcela do mês se mes ≤ N, senão 0,00<br/>total_mes = aluguel + parcela_taxa<br/>guarda a linha do mês"]
        LIN --> INC["mes = mes + 1"]
        INC --> MQ
    end

    MQ -->|não| RES[/"Mostra resumo no terminal<br/>base · adicionais · desconto · aluguel final<br/>bloco separado: taxa total, N parcelas, valores<br/>valor a pagar: meses 1..N com parcela, meses N+1..12"/]

    RES --> CSV[/"Grava arquivo .csv na pasta do projeto<br/>(12 linhas já calculadas)"/]
    CSV --> OK{"Salvou?"}
    OK -->|sim| CAM[/"Mostra o caminho do arquivo"/]
    OK -->|não| CSV2[/"Mostra o motivo<br/>grava na pasta do usuário"/]
    CSV2 --> OK2{"Salvou?"}
    OK2 -->|sim| CAM
    OK2 -->|não| ERR[/"Mostra erro: CSV não foi salvo"/]
    CAM --> FIM([Fim])
    ERR --> FIM
```

## 2. Sub-processo: Ler resposta válida

```mermaid
flowchart TD
    S([Ler resposta válida]) --> P[/"Mostra pergunta, lê resposta"/]
    P --> V{"Resposta válida?<br/>tipo certo e dentro da faixa"}
    V -->|não| E[/"Mostra erro: o que era esperado"/]
    E --> P
    V -->|sim| R([Devolve resposta])
```
