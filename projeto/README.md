# Projeto Aplicado — Preço de combustível e peso no orçamento do consumidor

**Uma comparação entre Brasília e Goiânia**

**Dupla:** Claudio da Aparecida Meireles Filho (2321070) e Felipe Pereira Dutra (2321017)
**Disciplina:** Inteligência de Negócio (INE), Prof. Bruno Miranda, 2º semestre de 2026
**Público-alvo:** o consumidor que abastece o próprio carro

## Entregas

| Item | Onde está |
| --- | --- |
| Relatório final, no template do projeto | [`entrega/`](entrega/) (`.docx` e `.pdf`) |
| Dashboard, com uma página por pergunta | [`imagens/`](imagens/) (`pagina1` a `pagina6`) |
| Apresentação | Slides publicados no claude.ai (link enviado à dupla) |
| Dados tratados | [`dados/`](dados/) |
| Código | [`scripts/`](scripts/) |

## Respostas (jan/2016 a jun/2026)

| # | Pergunta | Resposta |
| --- | --- | --- |
| 1 | Brasília × Goiânia: onde o litro é mais caro? | Nos últimos 12 meses (jul/2025 a jun/2026), Goiânia ficou R$ 0,09 mais cara por litro no etanol (R$ 4,76 × R$ 4,67) e na gasolina (R$ 6,51 × R$ 6,41). A vantagem muda ao longo do tempo: a gasolina foi mais barata em Brasília em 9 de 11 anos, e o etanol em 3 de 11. |
| 2 | Quanto da renda vai para o combustível? | Em 2025, 100 L de gasolina por mês equivaliam a **14,2%** da renda domiciliar per capita do DF e a **26,6%** da de Goiás, 1,9 vez mais. O pico foi em 2021 (23,8% e 48,1%). |
| 3 | Quanto se economiza pesquisando? | Na mesma semana, a diferença entre o posto mais caro e o mais barato foi de R$ 0,56/L em Brasília e R$ 0,47/L em Goiânia: **R$ 27,77** e **R$ 23,46** por tanque de 50 L. |
| 4 | Quando o etanol compensou (regra dos 70%)? | Em **66 de 125 meses** em Goiânia e em **23 de 125** em Brasília. Em jun/2026 compensava nas duas cidades (65,9% e 63,6%). |
| 5 | A bandeira faz diferença? | Pouca. A BR é a mais cara nas duas capitais (+R$ 0,026 e +R$ 0,038 acima da média da semana). A distância entre a bandeira mais cara e a mais barata chega a R$ 3,45 por tanque, bem menos que a economia de pesquisar o posto. |
| 6 | Quanto da alta é real? | A gasolina subiu 74,2% (Brasília) e 73,1% (Goiânia) em valores nominais. Descontado o IPCA (68,2% no período), a alta real foi de **8,0%** e **7,3%**. |

## Bases de dados

| Base | Uso | Link |
| --- | --- | --- |
| ANP: Série histórica de preços de combustíveis | Preço posto a posto, com bandeira | <https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis> |
| IBGE: microdados da PNAD Contínua (visitas anuais) | Renda domiciliar per capita do DF e de GO | <https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/> |
| Banco Central: SGS, série 433 | IPCA mensal (deflator) | <https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json> |

## Como reproduzir

```bash
pip install python-docx matplotlib pillow
python3 projeto/scripts/01_baixa_precos_anp.py     # ~20 min; retoma de onde parou
python3 projeto/scripts/02_renda_per_capita_pnad.py # usa o cache de dados/renda_microdados_cache.json
python3 projeto/scripts/03_calcula_indicadores.py
python3 projeto/scripts/04_renderiza_dashboard.py
python3 projeto/scripts/05_gera_relatorio.py        # precisa do LibreOffice para gerar o PDF
```

| Script | O que faz |
| --- | --- |
| `01_baixa_precos_anp.py` | Baixa os 21 arquivos semestrais da ANP e filtra Brasília e Goiânia em fluxo. Confere se cada arquivo chegou até o último mês do semestre e tenta de novo se vier truncado. |
| `02_renda_per_capita_pnad.py` | Calcula a renda domiciliar per capita (VD5002, peso V1032) dos microdados da PNAD. Para se o valor de 2025 não bater com o oficial (DF R$ 4.538, GO R$ 2.407). |
| `03_calcula_indicadores.py` | Monta o painel mensal e o `indicadores.json` com as respostas das seis perguntas. |
| `04_renderiza_dashboard.py` | Gera as seis páginas do dashboard (1920×1080), com nomes e matrículas da dupla. |
| `05_gera_relatorio.py` | Preenche o template do projeto e converte para PDF. Todo número do texto sai do `indicadores.json`. |

## Decisões e limitações

- **Renda:** o pré-projeto previa a tabela 5437 do SIDRA, que não aceita extração automatizada. A renda domiciliar per capita foi calculada dos microdados com a definição do IBGE e validada contra o valor oficial de 2025.
- **Renda estadual:** o IBGE não publica renda anual por município, então Goiânia usa a renda de Goiás. Por isso o peso do combustível em Goiânia tende a estar superestimado.
- **2022 no DF:** poucos domicílios de renda muito alta na amostra fazem o 1% mais rico concentrar cerca de 16% da renda, contra 8% a 10% de 2023 a 2025. Isso puxa a média de 2022 para cima.
- **Pesos da PNAD:** a série usa os pesos atuais (recalibrados pelo Censo 2022). Os anos antigos diferem alguns por cento do que foi publicado na época; o CSV traz o valor oficial ao lado.
- **ANP:** a coleta é semanal e por amostra, em dias diferentes em cada capital, e não há dados de set/2020. As comparações são feitas por semana e por mês.
- **Bandeiras:** entram BR, Ipiranga, Shell e bandeira branca, cada grupo com pelo menos 30 coletas e 3 postos. As marcas pequenas ficam de fora.
