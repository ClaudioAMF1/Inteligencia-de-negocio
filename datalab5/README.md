# DataLab 5-B1 — Viabilidade econômica com o cálculo do Valor Presente em Python

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## O que o enunciado pede

| Item | Onde está |
| --- | --- |
| a. Escolher valor, taxa de juros e períodos próprios | Constantes no topo de `viabilidade_valor_presente.py` |
| b. Imprimir o valor calculado no console | Seção *Resultado* da saída |
| c. Imprimir nome e matrícula no console | Cabeçalho da saída |
| d. Salvar no formato do Template de Aluno | `entrega/` (`.docx` e `.pdf`) |

## Parâmetros escolhidos e resultado

| | |
| --- | --- |
| Valor futuro desejado (VF) | R$ 250.000,00 |
| Taxa de juros (r) | 11,75% ao ano |
| Períodos analisados (n) | 6 anos |
| **Valor presente (VP)** | **R$ 128.367,42** |
| Juros embutidos no período | R$ 121.632,58 |

A simulação varia a taxa de 9,75% a 13,75% ao ano: o valor presente vai de
R$ 143.058,23 a R$ 115.406,85 — R$ 27.651,38 de diferença sobre o mesmo valor futuro.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - DataLab5-B1 (2026.2S).pdf` | Enunciado da atividade |
| `viabilidade_valor_presente.py` | O exercício; roda sozinho, sem dependências externas |
| `imagens/` | Prints do código e da saída do console |
| `entrega/` | Entrega no Template de Aluno (`.docx` e `.pdf`) |

## Como reproduzir

```bash
python3 datalab5/viabilidade_valor_presente.py   # roda o exercício
python3 scripts/08_renderiza_prints_labs.py      # gera os prints
python3 scripts/09_gera_entrega_datalab5.py      # monta a entrega
```
