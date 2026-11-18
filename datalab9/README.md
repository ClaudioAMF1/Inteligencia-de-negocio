# DataLab 9-B2 — Cálculo dos principais indicadores do mercado de trabalho

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

Implementação em R dos cinco indicadores da aula (Semana 13), calculados a partir dos
**microdados da PNAD Contínua do 3º trimestre de 2026**, com os pesos amostrais do IBGE,
para o Brasil e o Distrito Federal. A entrega usa o Template de Aluno das demais atividades.

- [Entrega em PDF](entrega/IDP.INE%20-%20Atividade%20Avaliativa%209-B2%20-%20Claudio%20da%20Aparecida%20Meireles%20Filho.pdf) e [Word](entrega/IDP.INE%20-%20Atividade%20Avaliativa%209-B2%20-%20Claudio%20da%20Aparecida%20Meireles%20Filho.docx)
- [Código em R](indicadores_pnad_microdados.R)
- [Resultados em CSV](resultados/indicadores_032026.csv) e [gráfico](resultados/indicadores_brasil_df.png)

## Indicadores (definições da aula)

| Indicador | Fórmula | Brasil | DF | IBGE (Brasil / DF) |
| --- | --- | ---: | ---: | --- |
| 1. Taxa de participação na força de trabalho | força de trabalho / PIA | 62,18% | 67,98% | 62,2% / 68,0% |
| 2. Taxa de ocupação (ou emprego) | ocupados / PIA | 58,98% | 64,28% | 59,0% / 64,3% |
| 3. Taxa de desemprego (ou desocupação) | desocupados / força de trabalho | 5,15% | 5,45% | 5,2% / 5,4% |
| 4. Taxa de informalidade | informais / ocupados | 37,46% | 26,73% | 37,5% / 26,7% |
| 5. Grau de formalização do emprego | formais / ocupados | 59,08% | 70,27% | não publicado |

PIA = pessoas de 14 anos ou mais. A taxa de ocupação da aula (ocupados / PIA) é o que o IBGE
publica como *nível da ocupação*.

**Informal** segue a definição do IBGE:
- empregado sem carteira no setor privado ou doméstico;
- empregador ou conta própria sem CNPJ;
- trabalhador familiar auxiliar.

**Formal** segue a definição da aula:
- carteira assinada;
- militar ou estatutário;
- empregador ou conta própria com CNPJ.

Informal e formal não somam 100%: a diferença são os empregados do setor público sem
carteira (3,46% dos ocupados no Brasil e 3,00% no DF).

**Validação.** Os totais estimados batem exatamente com os do SIDRA (tabela 4093) no Brasil:
- PIA: 175.729 mil;
- força de trabalho: 109.266 mil;
- ocupados: 103.638 mil;
- desocupados: 5.628 mil;
- informais: 38.819 mil.

As oito taxas que o IBGE publica coincidem com as calculadas na casa decimal divulgada. O
script imprime as duas lado a lado.

## Como reproduzir

Requer R com os pacotes `data.table`, `survey` e `jsonlite`. Os microdados (240 MB) são
baixados do servidor do IBGE na primeira execução e ficam em `dados/microdados/`, fora do
git.

```bash
cd datalab9
Rscript --vanilla indicadores_pnad_microdados.R      # ~2 min; no RStudio: Source
cd ..
python3 scripts/08_renderiza_prints_labs.py datalab9  # prints do código e do console
cp datalab9/resultados/indicadores_brasil_df.png datalab9/imagens/
python3 scripts/17_gera_entrega_datalab9.py           # entrega no template (precisa do LibreOffice)
```

| Caminho | O que é |
| --- | --- |
| `indicadores_pnad_microdados.R` | O exercício |
| `dados/sidra_4093_032026_brasil_df.json` | Taxas e totais oficiais do SIDRA (API), para conferência |
| `resultados/` | CSV dos indicadores e gráfico Brasil × DF |
| `imagens/` | Prints do código, do console e o gráfico usados na entrega |
| `entrega/IDP.INE - Atividade Avaliativa 9-B2 - …` | Entrega no Template de Aluno |

## Versão anterior

A pasta também guarda uma versão anterior desta atividade:
- código: `indicadores_mercado_trabalho.R`;
- entrega: `entrega/DataLab_9B2_Claudio_2321070.*`;
- documentação: [README_versao_sidra.md](README_versao_sidra.md).

Essa versão:
- calcula os indicadores com os totais prontos do SIDRA para o 4º trimestre de 2025;
- usa outro template;
- define a taxa de ocupação como ocupados / força de trabalho.

A versão desta página segue as fórmulas dos slides da aula.
