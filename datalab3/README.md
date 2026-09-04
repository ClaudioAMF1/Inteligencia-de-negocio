# DataLab 3-B1 — Explorando dados com o Power BI

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - DataLab3-B1 (2026.2S).pdf` | Enunciado da atividade |
| `ine_dataset_correcoes_avaliacoes.xlsx` | Base de dados (46 alunos, 13 variáveis) |
| `idp_ine_datalab3.pbix` | Relatório do Power BI, com as 4 análises em 4 páginas |
| `imagens/` | Prints das 4 páginas do relatório |
| `entrega/` | Entrega final no template do aluno (`.docx` e `.pdf`) |

## As quatro análises

| Página do relatório | Análise pedida | Visual |
| --- | --- | --- |
| P1-Indicadores | Análise 1 — Indicadores de desempenho | 3 cartões: `id`, `nota_final`, `total_faltas` |
| P2-Análise de Correlação | Análise 2 — Nota x Faltas | Dispersão: X `total_faltas`, Y `nota_final` |
| P3-Distribuição de Notas | Análise 3 — Distribuição das notas | Colunas clusterizadas por `nr_matricula` + linha de média |
| P4-Evolução das Notas | Análise 4 — Evolução das notas | Área com `nota_prova_p1`, `p2` e `p3` |

Todas as páginas têm caixa de texto com o título e a logomarca da instituição,
como pede o enunciado.

## Como reproduzir

```bash
pip install pypdf python-docx openpyxl matplotlib
python3 scripts/01_atualiza_pbix_datalab3.py      # identificação do aluno no .pbix
python3 scripts/02_renderiza_paginas_datalab3.py  # imagens das 4 páginas
python3 scripts/03_gera_entrega_datalab3.py       # .docx e .pdf da entrega
```

> As imagens em `imagens/` são geradas a partir da mesma base carregada no
> relatório, reproduzindo o layout e as agregações de cada página do `.pbix`.
> Para substituí-las por capturas de tela do Power BI Desktop, basta trocar os
> arquivos `.png` e rodar novamente o script `03`.
