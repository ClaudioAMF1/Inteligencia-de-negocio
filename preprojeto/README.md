# Avaliação Continuada — Pré-projeto do Projeto Aplicado

**Dupla:** Claudio da Aparecida Meireles Filho (2321070) e Felipe Pereira Dutra (2321017)
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026
**Entrega:** 25/09/2026

## O que o enunciado pede

A entrega usa o **Template IDP.INE — Modelo de Projeto de Inteligência de Negócio**,
publicado pelo professor. Cada item do enunciado cai em uma seção do template:

| Item do enunciado | Onde está no documento |
| --- | --- |
| a. As duplas do trabalho de projeto aplicado | Autores, na capa |
| b. A empresa / segmento que será abordado | *A empresa que você irá abordar* |
| c. Área de negócio e tema | *Área de negócio e o tema abordado* |
| d. Perguntas que o estudo se propõe a resolver | Tabela *Pergunta(s) negocial(ais)* — 5 perguntas |
| e. Bases de dados e link da fonte | Tabela *Base de dados / Link público* — 3 bases |

## Escopo escolhido

**Título do projeto:** Precificação de combustíveis no Brasil: evolução, diferenças
regionais e dispersão de preço na revenda.

**Empresas / segmento:** revenda de combustíveis no Brasil, sob a ótica das distribuidoras
que aparecem nomeadas no campo *Bandeira* da coleta da ANP — Vibra Energia (BR), Ipiranga
e Raízen (Shell) — mais os postos de bandeira branca. Recorte nacional com abertura para o
Distrito Federal.

**Área de negócio:** Precificação e Inteligência de Mercado (*pricing*).

**Tema:** comportamento do preço de revenda de gasolina comum, etanol hidratado e diesel
S-10 — evolução no tempo, diferenças entre regiões e UFs, dispersão de preço dentro da
mesma cidade, paridade etanol/gasolina e efeito da bandeira.

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
| `entrega/` | Entrega final (`.docx` e `.pdf`), no template oficial |
| `../docs/Template IDP.INE - Modelo de Projeto...docx` | Template oficial usado na entrega |

## Como reproduzir

```bash
python3 scripts/07_gera_preprojeto.py
```

> Todo o conteúdo (título, autores, texto das seções, perguntas e bases) fica em
> constantes no topo de `scripts/07_gera_preprojeto.py`. Para mudar qualquer item, basta
> editar a constante e rodar o script de novo.
