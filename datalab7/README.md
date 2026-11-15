# DataLab 7-B2 — Análise financeira, custos e receitas da firma

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## O que o enunciado pede

| Item | Onde está |
| --- | --- |
| a. Usar o dataset tratado como em sala | `dados/dados_financeiros_tratados.csv` e `powerbi/tratamento.m` |
| b. Uma página do dashboard por pergunta | `imagens/pagina1_*.png` a `pagina7_*.png` |
| c. Nome e matrícula em cada página | Cabeçalho de todas as páginas |
| d. Evidências no documento da tarefa | `entrega/` — print e resposta abaixo de cada pergunta |
| e. Entrega em PDF | `entrega/IDP.INE - Atividade Avaliativa 7-B2 - ....pdf` |

## Respostas

| # | Pergunta | Resposta |
| --- | --- | --- |
| 1 | Total de receitas | **R$ 1.920.089,00** |
| 2 | Total de despesas | **R$ 1.152.917,00** |
| 3 | Margem de lucro | **39,96%** — lucro de R$ 767.172,00; a margem cai a cada ano: 48,7% → 38,6% → 34,5% |
| 4 | Receitas por componente | Vendas concentra 70,8% (R$ 1.359.336); Franquias é a menor (R$ 61.600) |
| 5 | Despesas x média | Média de R$ 192.152,83; Administrativo, Tecnologia e Salários ficam acima e somam 85% das despesas |
| 6 | Matriz tipo / componente / ano | Salários e Impostos mais que triplicaram; Franquias cai todo ano |
| 7 | Maiores e menores segmentos | Receita: Vendas (maior), Franquias (menor). Despesa: Administrativo (maior), Marketing (menor, R$ 283 abaixo de Segurança) |

## Pontos do dataset

- **Não há o ano de 2021.** A série vai de jan/2019 a dez/2020 e depois de jan/2022 a dez/2022.
- **Publicidade tem receita negativa** em mai, jul e ago de 2020. Os valores foram mantidos como vieram.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - DataLab7-B2 (2026.2S).pdf` | Enunciado |
| `dados/ine_datalab7b2_dados_financeiros.xlsx` | Dataset original do professor |
| `dados/dados_financeiros_tratados.csv` | Dataset tratado (formato longo, 432 linhas) |
| `imagens/` | As 7 páginas do dashboard |
| `powerbi/tratamento.m` | Tratamento no Power Query |
| `powerbi/medidas.dax` | Medidas DAX |
| `entrega/` | Documento da tarefa preenchido (`.docx` e `.pdf`) |

## Montando o dashboard no Power BI

As páginas em `imagens/` foram renderizadas a partir do dataset tratado, reproduzindo
o layout de relatório do Power BI, porque o Power BI Desktop não roda no ambiente onde
elas foram geradas. Para montar o dashboard de verdade:

1. Carregue o dataset com `powerbi/tratamento.m` e nomeie a consulta como `dados`.
2. Crie as medidas de `powerbi/medidas.dax`.
3. Monte uma página por pergunta, com caixa de texto de título e de nome/matrícula:

| Página | Visual | Campos |
| --- | --- | --- |
| 1 | Cartão + colunas | `Total Receitas`; eixo `Ano` |
| 2 | Cartão + colunas | `Total Despesas`; eixo `Ano` |
| 3 | 4 cartões + linha | `Total Receitas`, `Total Despesas`, `Lucro`, `Margem de Lucro`; eixo `Ano` |
| 4 | Barras clusterizadas | eixo `Componente`, valor `Total Receitas` |
| 5 | Colunas + linha média | eixo `Componente`, valor `Total Despesas`; linha média no painel Análise |
| 6 | Matriz | linhas `Tipo` > `Componente`, colunas `Ano`, valor `Valor` |
| 7 | Barras + cartões | `Componente` por `Tipo`, ordenado por valor |

Depois, salve um print de cada página por cima dos `.png` em `imagens/` e rode o script
13 — o PDF se refaz com os prints do Power BI.

## Como reproduzir

```bash
python3 scripts/11_trata_dados_datalab7.py       # trata o dataset
python3 scripts/12_renderiza_dashboard_datalab7.py # gera as 7 páginas
python3 scripts/13_gera_entrega_datalab7.py      # preenche o documento e gera o PDF
```
