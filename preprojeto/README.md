# Avaliação Continuada — Pré-projeto do Projeto Aplicado

**Dupla:** Claudio da Aparecida Meireles Filho (2321070) e Felipe Pereira Dutra (2321017)
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026
**Entrega:** 25/09/2026

## O que o enunciado pede

| Item | Onde está no documento |
| --- | --- |
| a. As duplas do trabalho de projeto aplicado | Seção 1, item a |
| b. A empresa / segmento que será abordado | Seção 1, item b |
| c. Área de negócio e tema | Seção 1, item c |
| d. Perguntas que o estudo se propõe a resolver | Seção 2, item d |
| e. Bases de dados e link da fonte | Seção 2, item e |

## Escopo escolhido

**Segmento:** revenda de combustíveis no Brasil — postos revendedores e as distribuidoras
cujas bandeiras eles carregam, com recorte para o Distrito Federal.

**Área de negócio:** Precificação e Inteligência de Mercado (*pricing*).

**Tema:** comportamento do preço de revenda de combustíveis — evolução no tempo, diferenças
entre regiões e UFs, dispersão de preço dentro da mesma cidade e paridade etanol/gasolina.

O tema de Segurança Pública foi deliberadamente evitado: ele aparece no enunciado apenas
como exemplo de referência.

## Bases de dados

| Base | Papel | Link |
| --- | --- | --- |
| ANP — Série histórica de preços de combustíveis | Principal | <https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis> |
| ANP — Vendas de derivados de petróleo e etanol | Apoio (volume/demanda) | <https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/vendas-de-derivados-de-petroleo-e-etanol> |
| IBGE / SIDRA — IPCA (tabela 1737) | Apoio (deflator) | <https://sidra.ibge.gov.br/tabela/1737> |

Todas são públicas, de download livre e sem cadastro.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - Pré-ProjetoFinal-B1 (2026.2S).pdf` | Enunciado da atividade |
| `entrega/` | Entrega final (`.docx` e `.pdf`) |

## Como reproduzir

```bash
python3 scripts/07_gera_preprojeto.py
```

> O template oficial do pré-projeto só é publicado no AVA. Enquanto ele não sai, o
> documento é montado sobre o `[Template aluno]` da disciplina: capa e tabela de
> identificação são as mesmas e o corpo traz as seções do enunciado. Quando o template
> oficial chegar, o conteúdo está todo centralizado no topo de
> `scripts/07_gera_preprojeto.py` e pode ser transposto sem reescrever o texto.
