# RentSmart — Fluxograma

> Fluxo do programa: entradas, cálculo do aluguel, taxa contratual e saídas. Caixas com borda dupla `[[ ]]` = sub-processo
> "Ler resposta válida" (diagrama 2), reaproveitado em toda pergunta.

## 1. Fluxo principal

```mermaid
flowchart TD
    INI([Início]) --> TIPO[["Ler tipo de imóvel<br/>apartamento / casa / estúdio"]]
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

    subgraph ALUGUEL ["Aluguel mensal"]
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

    PARC --> BASE
    FINAL --> TAXA
    TAXA --> RES[/"Mostra resumo no terminal<br/>base · adicionais · desconto · aluguel final<br/>bloco separado: taxa total, N parcelas, valores"/]

    RES --> M1["mes = 1"]
    M1 --> MQ{"mes ≤ 12?"}
    MQ -->|sim| LIN["parcela_taxa = parcela do mês se mes ≤ N, senão 0,00<br/>total_mes = aluguel + parcela_taxa<br/>adiciona linha ao CSV"]
    LIN --> INC["mes = mes + 1"]
    INC --> MQ
    MQ -->|não| CSV[/"Salva arquivo .csv"/]
    CSV --> FIM([Fim])
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
