# DataLab 6-B1 — Viabilidade econômica com o cálculo do VPL e da TIR em Python

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## O que o enunciado pede

| Item | Onde está |
| --- | --- |
| a. Escolher aporte inicial, taxa, desembolsos e períodos próprios | Constantes no topo de `viabilidade_vpl_tir.py` |
| b. Imprimir o valor calculado no console | Seções *Resultado* e *Decisão* da saída |
| c. Imprimir nome e matrícula no console | Cabeçalho da saída |
| d. Salvar no formato do Template de Aluno | `entrega/` (`.docx` e `.pdf`) |

## Parâmetros escolhidos e resultado

| | |
| --- | --- |
| Aporte inicial (t = 0) | −R$ 180.000,00 |
| Resultados dos anos 1 a 5 | R$ 55.000 · 62.000 · 68.000 · 74.000 · 80.000 |
| Taxa mínima de atratividade | 11,75% ao ano |
| VP das entradas | R$ 240.945,82 |
| **VPL do projeto** | **R$ 60.945,82** |
| **TIR do projeto** | **23,73% ao ano** |
| Índice de lucratividade | 1,34 |

**Decisão: projeto viável.** O VPL é positivo e a TIR supera a taxa mínima de
atratividade em 11,98 pontos percentuais. A soma simples do fluxo seria R$ 159.000,00 —
a diferença de R$ 98.054,18 para o VPL é o custo de os recebimentos estarem espalhados
por cinco anos.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - DataLab6-B1 (2026.2S).pdf` | Enunciado da atividade |
| `viabilidade_vpl_tir.py` | O exercício, incluindo o gráfico da TIR |
| `imagens/` | Prints do código, da saída do console e o gráfico da TIR |
| `entrega/` | Entrega no Template de Aluno (`.docx` e `.pdf`) |

## Dependências

```bash
pip install numpy-financial matplotlib
```

## Como reproduzir

```bash
python3 datalab6/viabilidade_vpl_tir.py       # roda o exercício e gera o gráfico
python3 scripts/08_renderiza_prints_labs.py   # gera os prints
python3 scripts/10_gera_entrega_datalab6.py   # monta a entrega
```
