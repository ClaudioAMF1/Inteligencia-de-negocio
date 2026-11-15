# DataLab 10-B2 — Relação risco versus retorno em carteiras de investimento

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## O que o enunciado pede

| Item | Onde está |
| --- | --- |
| 1. Escolher 3 ativos da B3 | PETR4 (petróleo), VALE3 (mineração) e ITUB4 (bancos) |
| 2. Coletar 30 dias de fechamento e analisar risco × retorno | 30 pregões de 01/10/2026 a 13/11/2026, em `risco_retorno_carteira.py` |
| 3a. Evidenciar os dados no cabeçalho do algoritmo | Bloco *DADOS UTILIZADOS* e arrays de preços no topo do script |
| 3b. Nome e matrícula na primeira linha do console | Primeira linha da saída |
| Evidências | `imagens/` e entrega em `entrega/` (`.docx` e `.pdf`) |

## Dados

Os preços vêm dos arquivos oficiais de Séries Históricas da B3 (`COTAHIST_DDDMMAAAA.ZIP`):
fechamento do dia (campo PREULT), mercado à vista, lote padrão, sem ajuste por proventos.
O script `coleta_cotacoes_b3.py` baixa os arquivos e grava `dados/fechamento_b3.csv`; os
preços desse CSV foram copiados para o cabeçalho do algoritmo, como pede o enunciado.

## Resultados

| Ativo | Retorno médio diário | Risco (desvio-padrão diário) | Variação no período |
| --- | --- | --- | --- |
| PETR4 | −0,27% | 3,20% | −8,98% |
| VALE3 | −0,33% | 2,10% | −9,67% |
| ITUB4 | −0,08% | 3,64% | −4,26% |

- **Período de queda para os três ativos.** Quem perdeu menos (ITUB4) oscilou mais, e o mais estável (VALE3) perdeu mais.
- **Correlação:** PETR4 × ITUB4 = 0,51; PETR4 × VALE3 = −0,26; VALE3 × ITUB4 = −0,09.
- **Carteira com 1/3 em cada ativo:** retorno de −0,23% ao dia com risco de 1,97%, contra 2,98% da média ponderada do risco dos ativos. A diversificação reduziu o risco em **33,76%**.
- **Simulação de 10.000 carteiras:**
  - menor risco: 28,5% PETR4, 64,4% VALE3 e 7,1% ITUB4, com risco de 1,50% e retorno de −0,30% ao dia;
  - maior retorno: praticamente 100% ITUB4, com retorno de −0,08% e risco de 3,63%.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `coleta_cotacoes_b3.py` | Baixa os arquivos diários da B3 e extrai os fechamentos |
| `dados/fechamento_b3.csv` | Os 30 fechamentos coletados |
| `risco_retorno_carteira.py` | O exercício, no modelo do algoritmo da aula |
| `imagens/` | Prints do código e do console, e o gráfico de risco × retorno |
| `entrega/` | Entrega no Template de Aluno (`.docx` e `.pdf`) |

## Como reproduzir

```bash
pip install numpy pandas matplotlib
python3 datalab10/coleta_cotacoes_b3.py            # opcional: refaz a coleta (usa curl)
python3 datalab10/risco_retorno_carteira.py        # roda a análise e gera o gráfico
python3 scripts/08_renderiza_prints_labs.py datalab10
python3 scripts/14_gera_entrega_datalab10.py
```
