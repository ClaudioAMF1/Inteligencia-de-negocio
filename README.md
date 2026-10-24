# Inteligência de Negócio (INE) — IDP, 2º semestre de 2026

Atividades avaliativas da disciplina, Prof. Bruno Miranda.

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Dupla no projeto aplicado:** Felipe Pereira Dutra — **Matrícula:** 2321017
**Curso:** Ciência da Computação / Engenharia de Software

## Entregas

| Atividade | Tema | Entrega |
| --- | --- | --- |
| [DataLab 3-B1](datalab3/) | Explorando dados com o Power BI | [PDF](datalab3/entrega/) · [relatório `.pbix`](datalab3/idp_ine_datalab3.pbix) |
| [DataLab 4-B1](datalab4/) | Série histórica do World Bank Open Data | [PDF](datalab4/entrega/) |
| [DataLab 5-B1](datalab5/) | Valor Presente com Python | [PDF](datalab5/entrega/) · [código](datalab5/viabilidade_valor_presente.py) |
| [DataLab 6-B1](datalab6/) | VPL e TIR com Python | [PDF](datalab6/entrega/) · [código](datalab6/viabilidade_vpl_tir.py) |
| [DataLab 8-B2](datalab8/) | Mercado de trabalho em TI no Brasil — APINFO 2025 | [PDF](datalab8/entrega/IDP_INE_DataLab8-B2_Claudio_Meireles.pdf) · [dashboard](datalab8/entrega/dashboard_datalab8.pdf) · [dataset](datalab8/dados/apinfo_2025.csv) |
| [Pré-projeto](preprojeto/) | Avaliação Continuada — escopo do projeto aplicado final | [PDF](preprojeto/entrega/) |

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
| `scripts/07_gera_preprojeto.py` | Monta o pré-projeto da Avaliação Continuada |
| `scripts/08_renderiza_prints_labs.py` | Renderiza os prints de código e console dos DataLabs 5 e 6 |
| `scripts/09_gera_entrega_datalab5.py` | Monta a entrega do DataLab 5 |
| `scripts/10_gera_entrega_datalab6.py` | Monta a entrega do DataLab 6 |
| `scripts/11_prepara_dados_datalab8.py` | Extrai e trata as tabelas APINFO 2025 e calcula os indicadores |
| `scripts/12_renderiza_dashboard_datalab8.py` | Gera as cinco páginas do dashboard e a evidência do dataset |
| `scripts/13_gera_entrega_datalab8.py` | Monta a entrega do DataLab 8 no template oficial, em Word e PDF |
| `scripts/entrega.py` | Módulo comum: preenche o template `.docx` e converte para PDF |

### Dependências

```bash
pip install python-docx openpyxl matplotlib numpy-financial pygments pillow
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
python3 scripts/07_gera_preprojeto.py
python3 datalab5/viabilidade_valor_presente.py
python3 datalab6/viabilidade_vpl_tir.py
python3 scripts/08_renderiza_prints_labs.py
python3 scripts/09_gera_entrega_datalab5.py
python3 scripts/10_gera_entrega_datalab6.py
```

O DataLab 8 usa dependências e instruções próprias em [`datalab8/README.md`](datalab8/README.md).
