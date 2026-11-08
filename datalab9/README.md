# DataLab 9-B2 · Indicadores do mercado de trabalho

**Aluno:** Claudio da Aparecida Meireles Filho  
**Matrícula:** 2321070  
**Recorte:** Distrito Federal, 4º trimestre de 2025, sexo total, pessoas de 14 anos ou mais.

Implementação em R dos cinco indicadores solicitados, com dados oficiais da PNAD
Contínua trimestral. O relatório segue o template do aluno enviado para esta
atividade, com identificação na capa, no cabeçalho do código e na saída do console.

## Entrega

- [Relatório em PDF](entrega/DataLab_9B2_Claudio_2321070.pdf)
- [Relatório editável em Word](entrega/DataLab_9B2_Claudio_2321070.docx)
- [Código em R](indicadores_mercado_trabalho.R)
- [Dados de entrada](dados_pnad.csv), [resultados](resultados.csv) e [console](console.txt)
- [Resposta original do SIDRA](fontes/sidra_4093_2025t4_df_sc.json) e [proveniência](fontes/proveniencia.json)

## Fórmulas e resultados

Todas as razões abaixo são multiplicadas por 100. PIA é a população de 14 anos ou
mais; FT é a força de trabalho; PO são os ocupados; PD, os desocupados; PI, os
ocupados em situação de informalidade.

| Indicador | Razão | Resultado |
| --- | --- | ---: |
| Participação na força de trabalho | FT / PIA | 67,10% |
| Taxa de ocupação | PO / FT | 93,23% |
| Taxa de desocupação | PD / FT | 6,77% |
| Taxa de informalidade | PI / PO | 27,10% |
| Grau de formalização | (PO − PI) / PO | 72,90% |
| Nível da ocupação, complementar | PO / PIA | 62,56% |

As [notas metodológicas do IBGE](fontes/notas_metodologicas_ibge.pdf), página 18,
distinguem **taxa de ocupação** de **nível da ocupação**. Ambos aparecem para tornar
explícito o denominador adotado. A formalização é definida neste trabalho como o
complemento da proxy de informalidade do IBGE, e não somente carteira assinada.

Entradas em **mil pessoas**: PIA 2.489; FT 1.670; PO 1.557; PD 113; PI 422.
O complemento formal calculado é 1.135 mil pessoas. Os totais são estimativas
agregadas já expandidas pelo IBGE; não há aplicação adicional de pesos amostrais.
Como esses totais foram publicados arredondados, os percentuais recalculados
podem diferir na última casa das taxas oficiais. O nível da ocupação, por exemplo,
resulta em 62,56%, enquanto a taxa publicada pelo IBGE com base não arredondada é
62,5%. A validação admite diferença inferior a 0,1 ponto percentual.

## Executar

O cálculo usa somente R base. Foi executado com R 4.3.3. Não requer pacotes extras
nem acesso à internet: os totais oficiais estão no próprio script, e o CSV permite
auditá-los. No terminal, a partir da raiz do repositório:

```bash
cd datalab9
Rscript --vanilla indicadores_mercado_trabalho.R > console.txt
```

No RStudio, abra o arquivo `.R`, defina a pasta do script como diretório de
trabalho em **Session → Set Working Directory → To Source File Location** e clique
em **Source**. O script imprime os resultados e grava `resultados.csv` no diretório
de trabalho. As imagens do relatório são capturas diretas das janelas: R interativo
no terminal gráfico stterm e código aberto no GNU nano, em modo de leitura. Não
são capturas do RStudio. Os PNGs originais, o registro da sessão e os hashes estão
em [`capturas/`](capturas/).

Para testar, execute da raiz do repositório:

```bash
Rscript --vanilla scripts/testa_datalab9.R
```

São 19 checagens do Distrito Federal e 23 de Santa Catarina, 42 no total. Incluem exemplo com resposta conhecida,
valores ausentes ou infinitos, totais negativos, denominadores nulos, consistência
dos grupos, tolerância de arredondamento, extremos de informalidade e comparação
com as taxas de referência publicadas pelo IBGE.

## Reproduzir as duas entregas

Os scripts Python de preparação e montagem usam `python-docx` e `matplotlib`. A
conversão para PDF requer LibreOffice. O template desta atividade foi preservado
em `fontes/template_aluno.docx`, sem alterar o template das atividades anteriores.

```bash
python3 scripts/14_prepara_datalab9.py
(cd datalab9 && Rscript --vanilla indicadores_mercado_trabalho.R > console.txt)
(cd datalab9_lucas && Rscript --vanilla indicadores_mercado_trabalho.R > console.txt)
Rscript --vanilla scripts/testa_datalab9.R
python3 scripts/16_captura_datalab9.py --r /caminho/para/R
python3 scripts/15_gera_entregas_datalab9.py
soffice --headless --convert-to pdf --outdir datalab9/entrega datalab9/entrega/DataLab_9B2_Claudio_2321070.docx
soffice --headless --convert-to pdf --outdir datalab9_lucas/entrega datalab9_lucas/entrega/DataLab_9B2_Lucas_2021068.docx
```

A captura requer Linux, Xvfb, Openbox, stterm, xdotool, ImageMagick, nano e o
comando `script`. O script 16 abre o R, executa o arquivo com `source()` e captura
a janela sem redesenhar seu conteúdo; depois abre o código no editor. O script 15
confere os hashes das capturas, do código e dos dados antes de montar os documentos.
As capturas já incluídas podem ser reutilizadas se esses arquivos não mudaram.

O script de preparação lê a resposta arquivada da API. Ele regenera as entradas e
os perfis, sem substituir a fonte por valores mais recentes. As implementações
R ficam nos próprios arquivos: vetor nomeado no DF e leitura de CSV seguida de
uma tabela de numeradores e denominadores em SC.

## Fontes

- [IBGE SIDRA, tabela 4093](https://sidra.ibge.gov.br/tabela/4093): variáveis 1641, 4088, 4090, 4092, 4723; referências 4096, 4097, 4099 e 12466.
- [Consulta reproduzível da API](fontes/consulta_url.txt): UFs 53 e 42, período 202504, sexo Total 6794.
- [IBGE, notas metodológicas da PNAD Contínua](https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Notas_metodologicas/notas_metodologicas.pdf), página 18.
- [IBGE, divulgação do 4º trimestre de 2025](https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45908-pnad-continua-trimestral-desocupacao-recua-em-seis-das-27-ufs-no-4-trimestre-de-2025).

Consulta em 06/11/2026. Os quatro arquivos `enunciado_*.png` são os anexos da
atividade enviados pelo usuário. A outra versão está em [datalab9_lucas](../datalab9_lucas/).
