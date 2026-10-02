"""
DataLab 6-B1 - gera a entrega em .docx e .pdf a partir do template do aluno.

Os números citados saem da execução real de datalab6/viabilidade_vpl_tir.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from entrega import RAIZ, gerar

IMAGENS = RAIZ / "datalab6" / "imagens"
SAIDA = RAIZ / "datalab6" / "entrega"

PRINTS = [
    ("Código do exercício (1/4) - parâmetros do projeto e vetor de fluxo de caixa.",
     IMAGENS / "codigo_1.png"),
    ("Código do exercício (2/4) - funções de valor presente, VPL e TIR.",
     IMAGENS / "codigo_2.png"),
    ("Código do exercício (3/4) - gráfico da análise da TIR.",
     IMAGENS / "codigo_3.png"),
    ("Código do exercício (4/4) - impressão dos resultados e da decisão.",
     IMAGENS / "codigo_4.png"),
    ("Saída do console, com os valores calculados e a identificação do aluno.",
     IMAGENS / "console.png"),
    ("Gráfico da análise da TIR: o VPL em função da taxa, com a TIR no cruzamento do zero.",
     IMAGENS / "analise_tir.png"),
]

INTRODUCAO = (
    "O laboratório estendeu o cálculo do Valor Presente do DataLab 5 para a avaliação "
    "completa de um projeto de investimento. Sobre um fluxo de caixa com aporte inicial "
    "negativo e cinco anos de resultado, foram calculados o Valor Presente de cada período, "
    "o Valor Presente Líquido (VPL) e a Taxa Interna de Retorno (TIR), usando o pacote "
    "numpy-financial. O trabalho termina com o gráfico do VPL em função da taxa de juros, "
    "que mostra visualmente onde está a TIR."
)

OBJETIVO = [
    "Sair do cálculo de um valor isolado e chegar à decisão de investir ou não. O VPL "
    "responde \"quanto esse projeto cria de valor, em reais de hoje\" e a TIR responde \"até "
    "que taxa de juros ele ainda compensa\". Juntas, as duas medidas sustentam a decisão de "
    "aprovar ou recusar o projeto.",

    "Os parâmetros que escolhi: aporte inicial de R$ 180.000,00 no período zero, resultados "
    "líquidos de R$ 55.000,00, R$ 62.000,00, R$ 68.000,00, R$ 74.000,00 e R$ 80.000,00 nos "
    "cinco anos seguintes, e taxa mínima de atratividade de 11,75% ao ano.",

    "O resultado: VPL de R$ 60.945,82 e TIR de 23,73% ao ano. Como o VPL é positivo e a TIR "
    "supera a taxa mínima de atratividade em 11,98 pontos percentuais, o projeto é viável, e "
    "com folga confortável antes de deixar de compensar.",
]

TECNICAS = [
    "Montagem do fluxo de caixa: o aporte inicial entra como valor negativo na posição zero "
    "do vetor, e os resultados de cada ano nas posições seguintes. Essa convenção importa, "
    "porque npf.npv trata o primeiro elemento como já estando na data de hoje, sem desconto.",

    "Cálculo financeiro com numpy-financial: npf.npv(taxa, fluxo) para o VPL e npf.irr(fluxo) "
    "para a TIR. A TIR não tem fórmula fechada - é a raiz do polinômio do VPL - e a biblioteca "
    "a encontra numericamente, o que evita implementar o método iterativo na mão.",

    "Indicadores complementares: o valor presente período a período, somado, dá o VP das "
    "entradas (R$ 240.945,82), e dividido pelo aporte inicial dá o índice de lucratividade "
    "(1,34), que mostra quanto de valor presente o projeto devolve por real investido.",

    "Visualização com matplotlib: a curva do VPL é avaliada em 200 taxas entre 0% e 35% com "
    "numpy.linspace, a linha do zero marca o ponto de equilíbrio e a TIR aparece como "
    "estrela exatamente no cruzamento. A linha vertical da taxa mínima de atratividade foi "
    "acrescentada para deixar a folga visível no próprio gráfico.",
]

APRENDIZADO = [
    "Que o VPL já embute a decisão. Não é preciso comparar com nada: VPL positivo significa "
    "que o projeto cria valor acima da taxa exigida, e VPL negativo significa que o mesmo "
    "dinheiro renderia mais na alternativa representada pela taxa de desconto.",

    "Qual é o tamanho real do custo do tempo. A soma simples do fluxo de caixa do meu "
    "exercício dá R$ 159.000,00, mas o VPL a 11,75% ao ano é de R$ 60.945,82. Os "
    "R$ 98.054,18 de diferença são exatamente o que o desconto cobra por os recebimentos "
    "estarem espalhados ao longo de cinco anos.",

    "Que a TIR é a leitura de margem de segurança do projeto. Com TIR de 23,73% contra uma "
    "taxa mínima de 11,75%, a taxa de juros teria de dobrar antes de o projeto deixar de "
    "compensar. O gráfico mostra isso melhor que o número isolado: a curva cruza o zero bem "
    "à direita da linha da taxa mínima.",

    "Que a TIR tem limites que o VPL não tem. Ela pressupõe um fluxo que troca de sinal uma "
    "única vez - aqui, do aporte negativo para os resultados positivos. Um fluxo que voltasse "
    "a ficar negativo no meio do caminho poderia ter mais de uma TIR, e nesse caso o VPL "
    "continua confiável enquanto a TIR deixa de ser.",
]


def main():
    faltando = [str(caminho) for _, caminho in PRINTS if not Path(caminho).exists()]
    if faltando:
        raise SystemExit("rode antes os scripts 08 e o exercício; imagens ausentes: "
                         + ", ".join(faltando))

    SAIDA.mkdir(parents=True, exist_ok=True)
    base = "IDP.INE - Atividade Avaliativa 6-B1 - Claudio da Aparecida Meireles Filho"
    gerar(
        destino_docx=SAIDA / f"{base}.docx",
        destino_pdf=SAIDA / f"{base}.pdf",
        tipo_atividade="DataLab 6-B1 - Viabilidade econômica com cálculo do VPL e da TIR em Python",
        introducao=INTRODUCAO,
        prints=PRINTS,
        objetivo=OBJETIVO,
        tecnicas=TECNICAS,
        aprendizado=APRENDIZADO,
    )


if __name__ == "__main__":
    main()
