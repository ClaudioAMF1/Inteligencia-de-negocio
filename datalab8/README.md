# DataLab 8-B2 — Mercado de trabalho em TI no Brasil

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070

**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## Entrega

| Arquivo | Conteúdo |
| --- | --- |
| [Relatório em PDF](entrega/IDP_INE_DataLab8-B2_Claudio_Meireles.pdf) | Template oficial do aluno, evidência do tratamento, cinco páginas de dashboard e descrição técnica |
| [Relatório editável](entrega/IDP_INE_DataLab8-B2_Claudio_Meireles.docx) | Mesma entrega em Word |
| [Dashboard em PDF](entrega/dashboard_datalab8.pdf) | Somente as cinco páginas, em formato horizontal |
| [Dashboard HTML](entrega/dashboard_datalab8.html) | Versão independente com abas; baixar e abrir no navegador, sem servidor ou conexão |
| [Dataset tratado](dados/apinfo_2025.csv) | 664 linhas, com valores ausentes, origem e natureza de cada referência preservados |
| [Comparativo CLT/PJ](dados/comparativo_clt_pj.csv) | 81 pares nacionais e cálculo do ganho relativo por perfil |
| [Comparativo estadual](dados/comparativo_estados.csv) | 24 comparações: quatro cargos, dois vínculos e três estados |
| [Imagens](imagens/) | Saídas geradas em Python para o dashboard e a evidência do dataset |

O formato segue os DataLabs 3 e 4: template da disciplina, logomarca IDP, gráficos em azul, identificação do aluno, arquivos de origem e scripts de reprodução. O dashboard desta atividade foi construído em Python; o HTML navega entre páginas estáticas, sem filtros de dados. Não é um arquivo `.pbix`.

## Fonte e recorte

Pesquisa **APINFO 2025**, realizada pela internet de agosto a setembro de 2025, com 26.174 participantes na pesquisa inteira. Tabelas consultadas em **24/10/2026**:

- [Sumário e contexto](https://www.apinfo2.com/apinfo/informacao/p25sumario.cfm)
- [Brasil](https://www.apinfo2.com/apinfo/informacao/p25sal-br.cfm)
- [São Paulo](https://www.apinfo2.com/apinfo/informacao/p25sal-sp.cfm)
- [Rio de Janeiro](https://www.apinfo2.com/apinfo/informacao/p25sal-rj.cfm)
- [Minas Gerais](https://www.apinfo2.com/apinfo/informacao/p25sal-mg.cfm)

Os HTMLs consultados estão em `dados/brutos/`. O arquivo `dados/fontes.json` registra URLs, data de coleta e SHA-256 das quatro tabelas. Os valores se referem a 2025, sem atualização monetária. São referências agregadas publicadas; não são microdados dos participantes nem salários oferecidos em anúncios.

## Respostas e critérios

| Página | Resposta | Critério |
| --- | --- | --- |
| A — Média nacional | **R$ 8.535,48**; sem a bolsa de estágio, **R$ 8.577,07** | Média simples dos 164 valores válidos da tabela Brasil; sem bolsa são 163 |
| B — Cargo destaque | **Gerente de TI**, com R$ 18.803 CLT e R$ 21.007 PJ | Lidera nos dois vínculos; média simples do par de R$ 19.905 |
| C — Ganho médio PJ/CLT | **27,53%** | Média de `(PJ / CLT - 1) × 100` nos 81 perfis com ambos os valores |
| D — Extremos | Brasil: R$ 21.007 (Gerente de TI PJ), R$ 1.757 (bolsa de Estagiário) e R$ 2.047 (menor sem bolsa, Assistente de Informática CLT) | Extremos publicados, não máximos e mínimos individuais |
| E — Comparação regional | SP e RJ acima da referência Brasil; MG abaixo, nos oito pares selecionados | Gerente de TI, Cientista de dados, Analista Cibersegurança e Engenheiro de dados; CLT e PJ separados |

Na base completa coletada (Brasil e os três estados), o maior valor é R$ 22.185, para Gerente de TI PJ em SP, e o menor é R$ 1.555, para bolsa de Estagiário em MG. A página D apresenta também esses extremos para distinguir o recorte nacional do conjunto coletado.

Não há quantidade de respondentes por perfil e vínculo nas tabelas. Portanto, a média de A não é a média salarial ponderada dos trabalhadores ou dos 26.174 participantes. Brasil não é somado aos estados para calcular a referência nacional.

Em C, o ganho entre as médias dos mesmos pares, `(média PJ / média CLT - 1) × 100`, seria **27,29%**. Ele é apresentado como medida complementar e não substitui a média dos percentuais. Nenhum cálculo equivale salário líquido, benefícios ou custos dos regimes de contratação.

## Dataset e tratamento

Grão: uma linha por **ano × localidade × perfil × vínculo da fonte**. Cada uma das quatro tabelas tem 83 perfis; após transformar CLT e PJ em linhas, a base tem 664 registros. Há 656 valores publicados, oito ausentes e nenhuma chave duplicada.

| Campo | Significado |
| --- | --- |
| `ano_pesquisa` | 2025 |
| `uf`, `localidade` | BR/Brasil ou uma das três UFs; BR é agregado nacional |
| `cargo`, `especialidade`, `perfil` | Cargo e especialidade da referência; perfil combina ambos |
| `vinculo_fonte` | Nome da coluna original: CLT ou PJ |
| `natureza` | `remuneracao` ou `bolsa_estagio` |
| `salario_mensal_brl` | Valor numérico mensal em reais; vazio quando não publicado |
| `situacao` | `publicado` ou `nao_publicado` |
| `valor_original`, `especialidade_original` | Textos preservados para conferir conversões |
| `linha_fonte`, `fonte_url` | Posição da linha de dados na tabela e URL de origem |

Conversões: espaços normalizados, ponto de milhar removido e número decimal interpretado. `Phyton` vira `Python` e `Java Script` vira `JavaScript`, mantendo o original. Estágio é marcado como bolsa, embora apareça na coluna CLT da fonte. Valores ausentes não viram zero. O CSV usa UTF-8 com BOM, vírgula como delimitador e ponto decimal. No Excel/Power BI em português, use a importação de Texto/CSV e a localidade Inglês (Estados Unidos) para a coluna numérica.

## Como reproduzir

Na raiz do repositório, com Python 3.10 ou posterior:

```bash
python -m pip install -r datalab8/requirements.txt
python scripts/11_prepara_dados_datalab8.py
python scripts/12_renderiza_dashboard_datalab8.py
python scripts/13_gera_entrega_datalab8.py
python -m unittest discover -s datalab8 -p 'test_*.py' -v
```

O script 11 trabalha com os HTMLs preservados e roda sem rede por padrão. `--baixar` atualiza os arquivos diretamente da APINFO, registra a nova data de coleta e recalcula o dataset. O script 12 gera as imagens, o PDF do dashboard e o HTML navegável. O script 13 preenche o template da pasta `docs/` e converte o Word para PDF com LibreOffice (`soffice`).

Os dados da comparação e os indicadores vêm dos arquivos tratados; as observações descritivas do relatório correspondem ao recorte preservado de 2025. Ao trocar a edição ou o recorte, revise também essas observações e os rótulos. A logomarca do dashboard é reaproveitada do pacote `datalab3/idp_ine_datalab3.pbix`.

## Validação

Os testes verificam separadores monetários, valores ausentes, normalizações, identidade dos perfis, estatísticas nacionais sem duplicação com os estados, comparação pareada e referências regionais do mesmo cargo/vínculo. Os resultados também foram conferidos diretamente contra os HTMLs e os PDFs foram revisados página por página.
