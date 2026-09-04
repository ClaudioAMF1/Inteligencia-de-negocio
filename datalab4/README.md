# DataLab 4-B1 — Série histórica do World Bank Open Data

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## Série escolhida

| | |
| --- | --- |
| Indicador | `IT.NET.USER.ZS` — Individuals using the Internet (% of population) |
| Recorte | Brasil (BRA), com América Latina e Caribe (LCN) e Mundo (WLD) como comparação |
| Período | 1990–2024 (Brasil); 2005–2024 no gráfico comparativo |
| Fonte primária | ITU — World Telecommunication/ICT Indicators Database |
| **Link da fonte** | <https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=BR> |
| Pacote usado | `dados/API_IT.NET.USER.ZS_DS2_en_csv_v2_33086.zip` (atualizado em 2026-07-13) |

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - DataLab4-B1 (2026.2S).pdf` | Enunciado da atividade |
| `dados/API_IT.NET.USER.ZS_*.zip` | Pacote CSV original baixado do portal |
| `dados/serie_internet.csv` | Série tratada (ano × entidade), gerada pelo script 04 |
| `powerbi/serie_worldbank.m` | Consulta Power Query que carrega a série pela API do World Bank |
| `powerbi/serie_worldbank_csv.m` | Mesma carga a partir do CSV baixado, com Unpivot |
| `imagens/` | Os três gráficos da série |
| `entrega/` | Entrega final no template do aluno (`.docx` e `.pdf`) |

## Os três gráficos

1. **Evolução no Brasil (1990–2024)** — a curva em S da difusão da Internet, com os marcos
   de 10%, 50% e do valor atual.
2. **Variação anual em pontos percentuais** — mostra *onde* o ritmo mudou: quase nada nos
   anos 1990, decolagem nos anos 2000 e 2010, o pico de +7,4 p.p. em 2020 e a
   desaceleração depois.
3. **Brasil × América Latina e Caribe × Mundo** — dá contexto: o Brasil termina em 84,5%,
   13,3 p.p. acima da média mundial.

## O movimento encontrado

A série é uma curva em S clássica de difusão de tecnologia. Fica praticamente parada na
década de 1990 (+0,23 p.p. por ano), decola nos anos 2000 e 2010 (+3,72 e +3,47 p.p. por
ano), cruza a metade da população em 2013, dá o maior salto de toda a série em 2020
(+7,4 p.p., o ano da pandemia) e entra em saturação em seguida — o crescimento cai para
+2,11 p.p. por ano e a série chega a 84,5% em 2024. Os pequenos recuos de 2021 e 2022
(-0,81 p.p. somados) são compatíveis com revisão metodológica da pesquisa domiciliar, não
com perda real de usuários. A leitura completa está no PDF da entrega.

## Como reproduzir

```bash
pip install python-docx matplotlib
python3 scripts/04_prepara_serie_datalab4.py      # trata o pacote CSV do World Bank
python3 scripts/05_renderiza_graficos_datalab4.py # gera os três gráficos
python3 scripts/06_gera_entrega_datalab4.py       # monta o .docx e o .pdf da entrega
```

Para atualizar a série, baixe o CSV novamente na página do indicador, salve o `.zip` em
`dados/` e rode os três scripts na ordem — todos os números citados na entrega são
recalculados a partir do arquivo, nenhum está digitado à mão.
