# DataLab 8-B2 — Mercado de trabalho em TI no Brasil

**Aluno:** Claudio da Aparecida Meireles Filho — **Matrícula:** 2321070
**Disciplina:** Inteligência de Negócio (INE) — Prof. Bruno Miranda — 2º semestre de 2026

## Fonte

Pesquisa salarial **APINFO 2025** (coleta pela internet, ago–set/2025, 26.174 participantes),
tabelas de rendimento mensal por cargo, com colunas CLT e PJ:

- Brasil — <https://www.apinfo2.com/apinfo/informacao/p25sal-br.cfm>
- São Paulo — <https://www.apinfo2.com/apinfo/informacao/p25sal-sp.cfm>
- Rio de Janeiro — <https://www.apinfo2.com/apinfo/informacao/p25sal-rj.cfm>
- Minas Gerais — <https://www.apinfo2.com/apinfo/informacao/p25sal-mg.cfm>

## Respostas

| # | Pergunta | Resposta |
| --- | --- | --- |
| a | Salário médio no Brasil | **R$ 8.535,48** (média simples das 164 referências publicadas); R$ 8.577,07 sem a bolsa de estágio |
| b | Cargo de maior remuneração | **Gerente de TI** — R$ 18.803 CLT e R$ 21.007 PJ |
| c | Ganho médio PJ sobre CLT | **+27,53%** (média dos percentuais de 81 pares de perfis) |
| d | Maior e menor valor | Maior: R$ 21.007 (Gerente de TI, PJ). Menor: R$ 1.757 (bolsa de Estagiário); sem estágio, R$ 2.047 (Assistente de Informática, CLT) |
| e | 3 estados x média nacional | Em Gerente de TI, Cientista de dados, Analista de Cibersegurança e Engenheiro de dados, **SP e RJ ficam acima** da referência nacional e **MG fica abaixo** |

## Base construída

664 linhas: 83 perfis profissionais × 4 localidades × 2 vínculos. São 656 valores
publicados e 8 ausentes; os ausentes foram mantidos como nulos, sem estimativa.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| `IDP.INE - DataLab8-B2 (2026.2S).pdf` | Enunciado |
| `entrega/` | Entrega final em PDF |

> O documento de entrega cita os HTMLs originais, o CSV tratado e os scripts como
> anexos. Eles não estão neste repositório: só o PDF foi adicionado.
