# Autor: Claudio da Aparecida Meireles Filho - matrícula 2321070
# Objetivo: DataLab 5-B1 - viabilidade econômica de projeto com o cálculo do
#           Valor Presente (VP) em Python
# Disciplina: Inteligência de Negócio (INE) - Prof. Bruno Miranda - 2026.2S

# Parâmetros do problema
# vl_futuro   -> valor desejado no futuro (VF)
# tx_juros    -> taxa de juros de referência do período (r), em decimal
# nr_periodos -> número de períodos analisados (n)

ALUNO = "Claudio da Aparecida Meireles Filho"
MATRICULA = "2321070"

# Parâmetros escolhidos para este exercício
VL_FUTURO = 250_000.00   # quero ter R$ 250 mil ao fim do projeto
TX_JUROS = 0.1175        # 11,75% ao ano
NR_PERIODOS = 6          # 6 anos

# Vetor de taxas para a simulação de cenários. Em um caso real viria da API do
# BACEN, de um dataset baixado ou de um banco de dados; aqui são as taxas anuais
# de referência que quero testar.
VETOR_TX_JUROS = [0.0975, 0.1075, 0.1175, 0.1275, 0.1375]


def reais(valor):
    """Formata no padrão brasileiro: 1.234.567,89."""
    return f"R$ {valor:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def porcento(taxa):
    return f"{taxa:.2%}".replace(".", ",")


def calcula_valor_presente(vl_futuro, tx_juros, nr_periodos):
    """Traz um valor futuro para a data de hoje: VP = VF / (1 + r)^n."""
    vl_presente = vl_futuro / (1 + tx_juros) ** nr_periodos
    return vl_presente


def calcula_valor_presente_pro(vl_futuro, tx_juros, nr_periodos):
    """Versão defensiva: protege contra denominador nulo ou negativo, que
    aconteceria com uma taxa de -100% ou pior."""
    nr_denominador = (1 + tx_juros) ** nr_periodos

    if nr_denominador > 0:
        return vl_futuro / nr_denominador

    raise ValueError(f"taxa de juros inválida para o cálculo: {tx_juros}")


def main():
    print("=" * 68)
    print("DataLab 5-B1 - Cálculo do Valor Presente")
    print(f"Aluno: {ALUNO}")
    print(f"Matrícula: {MATRICULA}")
    print("=" * 68)

    print("\nParâmetros escolhidos")
    print(f"  Valor futuro desejado (VF) : {reais(VL_FUTURO)}")
    print(f"  Taxa de juros (r)          : {porcento(TX_JUROS)} ao ano")
    print(f"  Períodos analisados (n)    : {NR_PERIODOS} anos")

    vl_presente = calcula_valor_presente(VL_FUTURO, TX_JUROS, NR_PERIODOS)
    print("\nResultado")
    print(f"  Valor presente (VP)        : {reais(vl_presente)}")
    print(f"  Juros embutidos no período : {reais(VL_FUTURO - vl_presente)}")

    print("\nSimulação de cenários de taxa")
    print(f"  {'Taxa a.a.':>10}  {'Valor presente':>18}  {'vs. cenário base':>18}")
    base = calcula_valor_presente_pro(VL_FUTURO, TX_JUROS, NR_PERIODOS)
    for tx in VETOR_TX_JUROS:
        vl_calculado = calcula_valor_presente_pro(VL_FUTURO, tx, NR_PERIODOS)
        print(f"  {porcento(tx):>10}  {reais(vl_calculado):>18}  "
              f"{reais(vl_calculado - base):>18}")

    print("\nLeitura: quanto maior a taxa de juros, menor o valor que preciso")
    print("aplicar hoje para chegar ao mesmo valor futuro.")


if __name__ == "__main__":
    main()
