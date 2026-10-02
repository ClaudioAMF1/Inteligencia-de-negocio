# Avaliação Continuada — Pré-projeto do Projeto Aplicado

**Dupla:** Claudio da Aparecida Meireles Filho (2321070) e Felipe Pereira Dutra (2321017)
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## Título

**Preço de combustível e peso no orçamento do consumidor: uma comparação entre
Brasília e Goiânia**

## O que o enunciado pede

A entrega usa o **Template IDP.INE — Modelo de Projeto de Inteligência de Negócio**,
publicado pelo professor. Cada item do enunciado cai em uma seção do template:

| Item do enunciado | Onde está no documento |
| --- | --- |
| a. As duplas do trabalho de projeto aplicado | Autores, na capa |
| b. A empresa / segmento que será abordado | *A empresa que você irá abordar* |
| c. Área de negócio e tema | *Área de negócio e o tema abordado* |
| d. Perguntas que o estudo se propõe a resolver | Tabela *Pergunta(s) negocial(ais)* — 6 perguntas |
| e. Bases de dados e link da fonte | Tabela *Base de dados / Link público* — 4 bases |

## Escopo

**Público-alvo: a população, o consumidor que abastece.** O mesmo dado que uma área de
pricing usa para monitorar a concorrência é virado para o outro lado do balcão: onde se
paga mais caro, quanto se economiza pesquisando e quanto do salário vai para o tanque.

**Empresas / segmento:** revenda de combustíveis em Brasília e Goiânia, pelas bandeiras
nomeadas na coleta da ANP — Vibra Energia (BR), Ipiranga e Raízen (Shell) — mais os postos
de bandeira branca.

**Área de negócio:** Precificação e Inteligência de Mercado (*pricing*), aplicada do ponto
de vista do consumidor.

**Tema:** preço de revenda de gasolina comum, etanol hidratado e diesel S-10 nas duas
capitais, do mínimo ao máximo coletado, e o peso desse preço no orçamento das famílias.

### As seis perguntas

1. Brasília ou Goiânia: onde se paga mais caro, do preço mínimo ao máximo?
2. Que percentual da renda média mensal vai para o combustível em cada capital?
3. Quanto o consumidor economiza pesquisando antes de abastecer?
4. Em que períodos o etanol compensou frente à gasolina em cada capital?
5. A bandeira do posto faz diferença no bolso?
6. Descontado o IPCA, o preço real subiu ou caiu na última década?

> O cálculo do peso na renda usa um consumo de referência de **100 litros de gasolina por
> mês** — cerca de 1.000 km rodados com um carro que faz 10 km/l.

## Bases de dados

| Base | Papel | Link |
| --- | --- | --- |
| ANP — Série histórica de preços de combustíveis | Principal (preço posto a posto) | <https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis> |
| IBGE / SIDRA — PNAD Contínua, tabela 5437 | Renda média por UF (DF e GO) | <https://sidra.ibge.gov.br/tabela/5437> |
| IBGE / SIDRA — IPCA, tabela 1737 | Deflator | <https://sidra.ibge.gov.br/tabela/1737> |
| ANP — Vendas de derivados de petróleo e biocombustíveis | Volume por UF e produto | <https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/vendas-de-derivados-de-petroleo-e-biocombustiveis> |

Todas são públicas, de download livre e sem cadastro.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - Pré-ProjetoFinal-B1 (2026.2S).pdf` | Enunciado da atividade |
| `entrega/` | Entrega final (`.docx` e `.pdf`), no template oficial |
| `../docs/Template IDP.INE - Modelo de Projeto...docx` | Template oficial usado na entrega |

## Como reproduzir

```bash
python3 scripts/07_gera_preprojeto.py
```

> Todo o conteúdo (título, autores, texto das seções, perguntas e bases) fica em
> constantes no topo de `scripts/07_gera_preprojeto.py`. Para mudar qualquer item, basta
> editar a constante e rodar o script de novo.
