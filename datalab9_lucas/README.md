# DataLab 9-B2 · Indicadores do mercado de trabalho

**Aluno:** Lucas Fiche Ungarelli Borges  
**Matrícula:** 2021068  
**Recorte:** Santa Catarina, 4º trimestre de 2025, sexo total, pessoas de 14 anos ou mais.

Versão do laboratório com dados de Santa Catarina, código em R, resultados da
execução e interpretação dos resultados no template oficial enviado.

## Entrega

Os dois relatórios mantêm os títulos originais “Solução do DevLab” e
“Descrição técnica do laboratório”, seguidos das perguntas “Qual foi o objetivo
do DevLab?”, “Quais foram as técnicas utilizadas?” e “O que você aprendeu?”.
As diferenças ficam nos dados, código, respostas e análises.

- [Relatório em PDF](entrega/DataLab_9B2_Lucas_2021068.pdf)
- [Relatório editável em Word](entrega/DataLab_9B2_Lucas_2021068.docx)
- [Código em R](indicadores_mercado_trabalho.R)
- [Dados de entrada](dados_pnad.csv), [resultados](resultados.csv) e [console](console.txt)
- [Resposta original do SIDRA](../datalab9/fontes/sidra_4093_2025t4_df_sc.json) e [proveniência](../datalab9/fontes/proveniencia.json)

## Fórmulas e resultados

PIA é a população de 14 anos ou mais; FT é a força de trabalho; PO são os ocupados;
PD, os desocupados; PI, os ocupados em situação de informalidade. As razões são
multiplicadas por 100.

| Indicador | Razão | Resultado |
| --- | --- | ---: |
| Participação na força de trabalho | FT / PIA | 67,91% |
| Taxa de ocupação | PO / FT | 97,84% |
| Taxa de desocupação | PD / FT | 2,16% |
| Taxa de informalidade | PI / PO | 25,72% |
| Grau de formalização | (PO − PI) / PO | 74,28% |
| Nível da ocupação, complementar | PO / PIA | 66,44% |

Entradas em **mil pessoas**: PIA 6.759; FT 4.590; PO 4.491; PD 99; PI 1.155.
O complemento formal calculado é 3.336 mil pessoas. São estimativas agregadas
já expandidas pelo IBGE, sem nova aplicação de pesos amostrais.

A **taxa de ocupação** usa a força de trabalho; o **nível da ocupação** usa a
população em idade de trabalhar, conforme as notas metodológicas do IBGE. O grau
de formalização é o complemento da proxy de informalidade do IBGE. Os totais
publicados são arredondados, o que pode produzir diferenças pequenas em relação
às taxas oficiais calculadas sobre os totais sem arredondamento.

## Executar

Foi utilizado R 4.3.3, sem pacotes adicionais. O script lê `dados_pnad.csv`
e pode ser executado sem conexão à internet. Mantenha o CSV e o código na mesma pasta. A partir da raiz do repositório:

```bash
cd datalab9_lucas
Rscript --vanilla indicadores_mercado_trabalho.R > console.txt
```

No RStudio, abra o arquivo `.R`, use **Session → Set Working Directory → To Source
File Location** e clique em **Source**. O script imprime uma tabela com numeradores, denominadores e taxas, e grava
`resultados.csv` no diretório de trabalho. A função `montar_taxas` recebe um
`data.frame` de uma linha e preserva os componentes de cada percentual.
A formatação com duas casas decimais é aplicada somente à exibição.

Da raiz do repositório, `Rscript --vanilla scripts/testa_datalab9.R` executa 23
checagens deste recorte e 19 do Distrito Federal, 42 no total. A [documentação de reprodução](../datalab9/README.md#reproduzir-as-duas-entregas)
detalha como regenerar os relatórios.

## Organização do relatório

O documento apresenta os dados e o método, duas páginas de código, o console
com interpretação e a descrição técnica. O gráfico de composição mostra
três bases distintas: população em idade de trabalhar, força de trabalho e
pessoas ocupadas. Cada barra soma 100% dentro do seu próprio grupo.

As três imagens do código e do console são capturas diretas de janelas: R
interativo no terminal gráfico stterm e código aberto no GNU nano. Os originais,
o registro da execução e os hashes estão em [`capturas/`](capturas/). Não são
prints do RStudio nem imagens desenhadas a partir do texto.

## Fontes

- [IBGE SIDRA, tabela 4093](https://sidra.ibge.gov.br/tabela/4093): UF 42, período 202504, sexo Total 6794.
- [Consulta da API](../datalab9/fontes/consulta_url.txt), [metadados](../datalab9/fontes/metadados_4093.json) e [notas metodológicas](../datalab9/fontes/notas_metodologicas_ibge.pdf), página 18.
- [IBGE, divulgação do 4º trimestre de 2025](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45908-pnad-continua-trimestral-desocupacao-recua-em-seis-das-27-ufs-no-4-trimestre-de-2025).

Consulta em 06/11/2026. O template e o enunciado estão preservados em
[`../datalab9/fontes/`](../datalab9/fontes/).
