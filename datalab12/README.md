# DataLab 12-B2 — Simulação de carteiras da B3

Claudio da Aparecida Meireles Filho · Matrícula 2321070 · Inteligência de Negócio · IDP

O estudo usa 30 fechamentos por ação, de **14/10/2026 a 26/11/2026**, para comparar 200 carteiras de Ambev (ABEV3), Itaú Unibanco (ITUB4) e Suzano (SUZB3). A divisão em partes iguais serve de referência adicional.

## Entrega

- [Relatório em PDF](entrega/DataLab12_Claudio_2321070.pdf) e [versão editável](entrega/DataLab12_Claudio_2321070.docx)
- [Código em Python](simulacao_carteiras.py) e [fechamentos em reais](dados/fechamentos.csv)
- [Captura do código aberto no editor](imagens/codigo_python.png) e [captura do console do Python](imagens/console_python.png)
- [Saída da execução](resultados/console.txt), [gráfico](resultados/risco_retorno.png) e [200 carteiras com pesos, retorno e volatilidade](resultados/carteiras.csv)

## Resultados

| Carteira | ABEV3 | ITUB4 | SUZB3 | Retorno médio diário | Volatilidade diária |
| --- | ---: | ---: | ---: | ---: | ---: |
| Menor volatilidade entre as sorteadas (184) | 34,45% | 14,15% | 51,41% | 0,392% | 0,939% |
| Pesos iguais | ⅓ | ⅓ | ⅓ | 0,151% | 1,292% |
| Maior retorno entre as sorteadas (81) | 15,20% | 2,97% | 81,83% | 0,706% | 1,635% |

As 30 observações de preços geram 29 variações entre pregões. Para cada sorteio, o algoritmo do slide divide três valores aleatórios pela soma. O retorno estimado é a soma dos retornos médios diários ponderados pelos pesos. A volatilidade é a raiz de `w @ covariancia @ w`, com a covariância amostral dos retornos diários. A semente 2321070 permite reproduzir a mesma sequência.

Os percentuais da tabela estão arredondados. O CSV registra pesos e indicadores em frações decimais. Os resultados descrevem a janela analisada e os fechamentos usados capturam apenas a variação de preço.

## Executar

Com Python 3.11 ou superior, execute estes comandos na pasta que contém `simulacao_carteiras.py`. O arquivo `dados/fechamentos.csv` já acompanha o programa.

```bash
python -m pip install numpy pandas matplotlib
python simulacao_carteiras.py
```

O console começa com o nome e a matrícula. O programa grava o CSV das carteiras e o gráfico na pasta `resultados/`.

## Origem das cotações

O extrator seleciona o mercado à vista (010), lote padrão (02) e fator unitário. Lê o preço do último negócio, campo PREULT, nas posições 109 a 121. São preços nominais em reais, sem ajuste por proventos. [Série histórica da B3](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/cotacoes-historicas/) · [Layout oficial](https://www.b3.com.br/data/files/33/67/B9/50/D84057102C784E47AC094EA8/SeriesHistoricas_Layout.pdf)

Para refazer o CSV a partir da fonte, baixe o arquivo anual e passe o ZIP ao extrator. O corte em 26/11/2026 continua valendo quando a B3 atualiza o arquivo com pregões posteriores. [COTAHIST_A2026.ZIP](https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2026.ZIP)

```bash
python extrair_fechamentos.py COTAHIST_A2026.ZIP
```

O ZIP utilizado traz 26/11/2026 no cabeçalho e tem SHA-256 `7108a2195ec65236f6894f3c7030533211ca2267a32ebdc2f93cbf9e9be6fd27`. O SHA-256 do CSV entregue é `e0dce14aa1921b20b1a399f4968a70a7db2b851e9d1a65dbb88dfb2f89622e43`.
