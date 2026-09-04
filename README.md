# Inteligência de Negócio (INE) — IDP, 2º semestre de 2026

Atividades avaliativas da disciplina, Prof. Bruno Miranda.

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Curso:** Ciência da Computação / Engenharia de Software

## Entregas

| Atividade | Tema | Entrega |
| --- | --- | --- |
| [DataLab 3-B1](datalab3/) | Explorando dados com o Power BI | [PDF](datalab3/entrega/) · [relatório `.pbix`](datalab3/idp_ine_datalab3.pbix) |
| [DataLab 4-B1](datalab4/) | Série histórica do World Bank Open Data | [PDF](datalab4/entrega/) |

Cada pasta tem um `README.md` com o detalhe da atividade, as análises construídas e o
passo a passo para reproduzir a entrega.

## Scripts

Tudo o que está em `datalab3/` e `datalab4/` é reproduzível a partir dos dados de origem:

| Script | O que faz |
| --- | --- |
| `scripts/01_atualiza_pbix_datalab3.py` | Aplica a identificação do aluno e corrige os títulos das páginas do `.pbix` |
| `scripts/02_renderiza_paginas_datalab3.py` | Renderiza as 4 páginas do relatório do Power BI em imagem |
| `scripts/03_gera_entrega_datalab3.py` | Monta a entrega do DataLab 3 no template do aluno |
| `scripts/04_prepara_serie_datalab4.py` | Trata o pacote CSV do World Bank e gera a série longa |
| `scripts/05_renderiza_graficos_datalab4.py` | Gera os 3 gráficos da série histórica |
| `scripts/06_gera_entrega_datalab4.py` | Monta a entrega do DataLab 4 no template do aluno |
| `scripts/entrega.py` | Módulo comum: preenche o template `.docx` e converte para PDF |

### Dependências

```bash
pip install python-docx openpyxl matplotlib
```

A conversão para PDF usa o LibreOffice (`soffice`), que precisa estar instalado com o
módulo Writer.

```bash
python3 scripts/01_atualiza_pbix_datalab3.py
python3 scripts/02_renderiza_paginas_datalab3.py
python3 scripts/03_gera_entrega_datalab3.py
python3 scripts/04_prepara_serie_datalab4.py
python3 scripts/05_renderiza_graficos_datalab4.py
python3 scripts/06_gera_entrega_datalab4.py
```
