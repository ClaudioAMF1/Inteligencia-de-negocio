# DataLab 8-B2 - Mercado de trabalho em TI no Brasil

**Aluno:** Lucas Fiche Ungarelli Borges

**RA / matrícula:** 2021068

Inteligência de Negócio (INE), Prof. Bruno Miranda, IDP, 2º semestre de 2026.

## Entrega

| Arquivo | Conteúdo |
| --- | --- |
| [Relatório em PDF](entrega/IDP_INE_DataLab8-B2_Lucas_Fiche_Ungarelli_Borges.pdf) | Template oficial do IDP, evidência do dataset, cinco páginas de dashboard e análise técnica |
| [Relatório editável](entrega/IDP_INE_DataLab8-B2_Lucas_Fiche_Ungarelli_Borges.docx) | Versão em Word da entrega |
| [Dashboard em PDF](entrega/dashboard_datalab8.pdf) | As cinco respostas em páginas horizontais |
| [Dashboard HTML](entrega/dashboard_datalab8.html) | Visualizador independente com abas e navegação por setas; baixar e abrir no navegador |
| [Dataset tratado](dados/apinfo_2025.csv) | 664 registros do Brasil e dos três estados da Região Sul |
| [Comparativo CLT/PJ](dados/comparativo_clt_pj.csv) | 81 perfis nacionais com ambos os vínculos publicados |
| [Comparativo regional](dados/comparativo_estados.csv) | 24 comparações de quatro cargos, dois vínculos e três estados |
| [Enunciado](enunciado_datalab8.pdf) | Requisitos da atividade |

O dashboard foi gerado em Python. O HTML apresenta páginas estáticas e não contém filtros de dados; não há arquivo Power BI `.pbix`. A identidade visual, a logomarca IDP e a estrutura da entrega seguem os DataLabs anteriores do repositório.

## Dados desta versão

Esta versão usa as tabelas **Brasil, Paraná, Rio Grande do Sul e Santa Catarina** da **APINFO 2025**. A comparação regional seleciona **Arquiteto de Sistemas, Desenvolvedor Full-Stack, Desenvolvedor Front-End e Desenvolvedor Back-End**.

O recorte estadual e os cargos comparados são diferentes da versão de Claudio. Os indicadores da tabela Brasil permanecem iguais, pois utilizam a mesma edição nacional da pesquisa. O relatório e os gráficos apresentam resultados e interpretações próprios para o recorte da Região Sul.

A pesquisa foi realizada pela internet entre agosto e setembro de 2025, com 26.174 participantes no levantamento completo e maior concentração no Sudeste e no Sul. As tabelas foram consultadas em 24/10/2026. Os valores são mensais, nominais e agregados, sem atualização monetária.

| Fonte | URL |
| --- | --- |
| Pesquisa e metodologia | https://www.apinfo2.com/apinfo/informacao/p25sumario.cfm |
| Brasil | https://www.apinfo2.com/apinfo/informacao/p25sal-br.cfm |
| Paraná | https://www.apinfo2.com/apinfo/informacao/p25sal-pr.cfm |
| Rio Grande do Sul | https://www.apinfo2.com/apinfo/informacao/p25sal-rs.cfm |
| Santa Catarina | https://www.apinfo2.com/apinfo/informacao/p25sal-sc.cfm |

Os HTMLs preservados estão em `dados/brutos/`. O arquivo `dados/fontes.json` registra URLs, data de coleta e hashes SHA-256. O extrator verifica o ano informado nas páginas para impedir a mistura de edições.

## Respostas

| Página | Resultado e critério |
| --- | --- |
| A - Média nacional | **R$ 8.535,48**, média simples dos 164 valores publicados; excluindo a bolsa de estágio, **R$ 8.577,07** |
| B - Cargo destaque | **Gerente de TI**: R$ 18.803 CLT e R$ 21.007 PJ, média simples de R$ 19.905 |
| C - Ganho médio PJ/CLT | **27,53%**, média de `(PJ / CLT - 1) × 100` nos 81 perfis nacionais pareados |
| D - Extremos | Brasil: máximo de **R$ 21.007** (Gerente de TI PJ), mínimo de **R$ 1.757** (bolsa de Estagiário) e menor salário sem bolsa de **R$ 2.047** (Assistente de Informática CLT) |
| E - Estados | As 24 referências escolhidas ficam abaixo do valor Brasil do mesmo cargo e vínculo; SC lidera regionalmente em seis pares e RS em dois |

Na base completa coletada, o maior valor continua sendo R$ 21.007 na tabela Brasil. O menor passa a R$ 1.499, bolsa de Estagiário no Paraná. As médias simples das tabelas estaduais são R$ 7.554,92 no PR, R$ 7.709,10 no RS e R$ 8.064,95 em SC.

A maior distância regional entre os perfis selecionados é de Desenvolvedor Full-Stack PJ no Paraná: R$ 11.190 diante de R$ 13.701 no Brasil, diferença de -18,33%. A menor é de Desenvolvedor Back-End CLT em SC: R$ 6.950 diante de R$ 7.201, diferença de -3,49%.

### Limites de interpretação

- As tabelas não informam número de respondentes por cargo e vínculo. A média das referências não equivale à média salarial ponderada dos trabalhadores ou dos 26.174 participantes.
- Brasil não é somado aos estados na formação de indicadores nacionais.
- Estágio é identificado como bolsa, mesmo quando a fonte usa a coluna CLT.
- A média dos percentuais PJ/CLT é 27,53%; a variação entre as médias dos mesmos pares é 27,29%. São medidas diferentes.
- O comparativo não equaliza benefícios, impostos, férias e intervalos sem faturamento, nem estima renda líquida.
- Os resultados regionais dos quatro cargos não devem ser generalizados para todos os trabalhadores dos estados.

## Tratamento e dicionário

Cada registro representa **ano × localidade × perfil × vínculo da fonte**. As quatro tabelas têm 83 perfis cada, totalizando 664 linhas, 656 valores publicados e oito ausentes, sem chaves duplicadas. CLT e PJ foram transformados em linhas. Valores vazios foram preservados como nulos.

| Campo | Significado |
| --- | --- |
| `ano_pesquisa` | 2025 |
| `uf`, `localidade` | BR/Brasil, PR/Paraná, RS/Rio Grande do Sul ou SC/Santa Catarina |
| `cargo`, `especialidade`, `perfil` | Cargo e especialidade; perfil combina ambos para evitar misturar funções |
| `vinculo_fonte` | CLT ou PJ, conforme o rótulo original |
| `natureza` | `remuneracao` ou `bolsa_estagio` |
| `salario_mensal_brl` | Valor numérico mensal em reais, vazio quando não publicado |
| `situacao` | `publicado` ou `nao_publicado` |
| `valor_original`, `especialidade_original` | Conteúdo original preservado para auditoria |
| `linha_fonte`, `fonte_url` | Posição na tabela e origem do registro |

Espaços excedentes foram removidos e pontos de milhar convertidos. `Phyton` foi normalizado para `Python` e `Java Script` para `JavaScript`. O CSV usa UTF-8 com BOM, vírgula como delimitador e ponto decimal. Na importação em Excel/Power BI em português, usar Texto/CSV e localidade Inglês (Estados Unidos) para a coluna numérica.

## Reprodução

Na raiz do repositório, com Python 3.10 ou posterior:

```bash
python -m pip install -r datalab8_lucas/requirements.txt
python datalab8_lucas/prepara_dados.py
python datalab8_lucas/renderiza_dashboard.py
python datalab8_lucas/gera_entrega.py
python -m unittest discover -s datalab8_lucas -p 'test_*.py' -v
```

`prepara_dados.py` usa os HTMLs preservados por padrão. A opção `--baixar` atualiza as fontes diretamente da APINFO e recalcula os indicadores. O script de entrega depende do template em `docs/`, do módulo `scripts/entrega.py` e do LibreOffice (`soffice`). A logomarca é extraída do pacote `datalab3/idp_ine_datalab3.pbix`.

As observações descritivas do relatório correspondem ao recorte preservado de 2025. Se a fonte ou a seleção mudar, revisar também textos e rótulos antes de gerar uma nova entrega.

## Validação

Sete testes verificam conversão monetária, ausências, normalizações, classificação do estágio, contagens, chaves únicas, estatísticas nacionais sem duplicação com estados, comparação pareada, extremos, equivalência regional, liderança dos estados e rejeição de páginas de outro ano. Os arquivos finais são revisados visualmente, incluindo nome e RA nas cinco páginas do dashboard.
