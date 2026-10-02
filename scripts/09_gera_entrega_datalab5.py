"""
DataLab 5-B1 - gera a entrega em .docx e .pdf a partir do template do aluno.

Os números citados saem da execução real de datalab5/viabilidade_valor_presente.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from entrega import RAIZ, gerar

IMAGENS = RAIZ / "datalab5" / "imagens"
SAIDA = RAIZ / "datalab5" / "entrega"

PRINTS = [
    ("Código do exercício (1/2) - parâmetros escolhidos e função de valor presente.",
     IMAGENS / "codigo_1.png"),
    ("Código do exercício (2/2) - versão defensiva da função, impressão dos resultados "
     "e simulação de cenários de taxa.",
     IMAGENS / "codigo_2.png"),
    ("Saída do console, com o valor calculado e a identificação do aluno.",
     IMAGENS / "console.png"),
]

INTRODUCAO = (
    "O laboratório trouxe para Python o conceito que sustenta toda análise de viabilidade "
    "econômica: o valor do dinheiro no tempo. A função calcula_valor_presente traz um valor "
    "futuro para a data de hoje pela fórmula VP = VF / (1 + r)^n, e uma segunda versão, "
    "defensiva, protege o cálculo contra um denominador inválido. Sobre essa base foi feita "
    "uma simulação de cenários, variando a taxa de juros para medir o impacto no valor "
    "presente."
)

OBJETIVO = [
    "Responder, em código, a uma pergunta de decisão: quanto preciso aplicar hoje para ter "
    "um valor determinado no futuro, dada uma taxa de juros e um prazo? É o primeiro passo "
    "de qualquer análise de viabilidade - sem trazer os valores para a mesma data, não dá "
    "para comparar projetos nem decidir investimento.",

    "Os parâmetros que escolhi para o exercício: valor futuro desejado de R$ 250.000,00, "
    "taxa de juros de 11,75% ao ano e 6 anos de prazo. O valor presente calculado foi de "
    "R$ 128.367,42, ou seja, R$ 121.632,58 do montante final vêm dos juros do período e não "
    "do capital que preciso aportar hoje.",
]

TECNICAS = [
    "Modelagem do cálculo em função: calcula_valor_presente(vl_futuro, tx_juros, "
    "nr_periodos) isola a fórmula VP = VF / (1 + r)^n em um único lugar, o que permite "
    "reaproveitá-la na simulação sem repetir a conta.",

    "Programação defensiva: a versão calcula_valor_presente_pro confere o denominador "
    "(1 + r)^n antes de dividir e levanta um erro explícito quando a taxa torna o cálculo "
    "inválido, em vez de deixar a divisão estourar ou devolver um número sem sentido.",

    "Simulação de cenários: um vetor de taxas percorrido em laço, aplicando a mesma função a "
    "cada cenário. No exercício, as taxas vão de 9,75% a 13,75% ao ano, faixa que cobre as "
    "oscilações plausíveis da taxa de referência no prazo analisado.",

    "Apresentação dos resultados: f-strings com alinhamento de coluna para montar a tabela no "
    "console, e funções auxiliares que formatam valores no padrão brasileiro (R$ 128.367,42 e "
    "11,75%) em vez do padrão americano que o Python usa por omissão.",
]

APRENDIZADO = [
    "Que a taxa precisa entrar na fórmula em notação decimal, não como o número do "
    "percentual. Usar 11,75 no lugar de 0,1175 faz (1 + r) virar 12,75, e o valor presente do "
    "meu exercício cai de R$ 128.367,42 para R$ 0,06. O cálculo roda sem erro nenhum e "
    "entrega um resultado absurdo: é o tipo de engano que não aparece como exceção, só como "
    "número errado, e por isso vale sempre conferir a ordem de grandeza do resultado.",

    "Que o valor presente é muito sensível à taxa. No exercício, mover a taxa de 9,75% para "
    "13,75% ao ano - quatro pontos percentuais - muda o valor presente de R$ 143.058,23 para "
    "R$ 115.406,85, uma diferença de R$ 27.651,38 sobre o mesmo valor futuro. Daí a "
    "importância de analisar cenários em vez de trabalhar com uma taxa única.",

    "Que o expoente n multiplica esse efeito: como o prazo está no expoente e não no "
    "multiplicador, o impacto de cada ano a mais é composto. É isso que explica por que, em "
    "6 anos, quase metade do valor futuro do exercício é juro e não capital aplicado.",

    "Que separar a função de cálculo da função de apresentação paga rápido. A mesma "
    "calcula_valor_presente_pro serviu para o cenário base e para os cinco cenários "
    "simulados, sem nenhuma linha duplicada.",
]


def main():
    faltando = [str(caminho) for _, caminho in PRINTS if not Path(caminho).exists()]
    if faltando:
        raise SystemExit("rode antes o script 08; imagens ausentes: " + ", ".join(faltando))

    SAIDA.mkdir(parents=True, exist_ok=True)
    base = "IDP.INE - Atividade Avaliativa 5-B1 - Claudio da Aparecida Meireles Filho"
    gerar(
        destino_docx=SAIDA / f"{base}.docx",
        destino_pdf=SAIDA / f"{base}.pdf",
        tipo_atividade="DataLab 5-B1 - Viabilidade econômica com cálculo do Valor Presente em Python",
        introducao=INTRODUCAO,
        prints=PRINTS,
        objetivo=OBJETIVO,
        tecnicas=TECNICAS,
        aprendizado=APRENDIZADO,
    )


if __name__ == "__main__":
    main()
