# Autor: Claudio da Aparecida Meireles Filho - matrícula 2321070
# Objetivo: DataLab 6-B1 - viabilidade econômica de projeto com o cálculo do
#           VP, do VPL e da TIR em Python
# Disciplina: Inteligência de Negócio (INE) - Prof. Bruno Miranda - 2026.2S
#
# Instalação do pacote usado no cálculo financeiro:
#     !pip install numpy-financial

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import numpy_financial as npf

ALUNO = "Claudio da Aparecida Meireles Filho"
MATRICULA = "2321070"

# Parâmetros do problema
# APORTE_INICIAL -> desembolso feito hoje para tirar o projeto do papel (t = 0)
# DESEMBOLSOS    -> resultado líquido de cada período seguinte
# TX_JUROS       -> taxa mínima de atratividade (TMA) usada para descontar
# NR_PERIODOS    -> número de períodos analisados

APORTE_INICIAL = -180_000.00
DESEMBOLSOS = [55_000.00, 62_000.00, 68_000.00, 74_000.00, 80_000.00]
TX_JUROS = 0.1175        # 11,75% ao ano
NR_PERIODOS = len(DESEMBOLSOS)

# O vetor de fluxo de caixa começa no período zero, com o aporte inicial negativo.
VETOR_FLUXO_CAIXA = [APORTE_INICIAL] + DESEMBOLSOS

GRAFICO = Path(__file__).resolve().parent / "imagens" / "analise_tir.png"


def reais(valor):
    """Formata no padrão brasileiro: 1.234.567,89."""
    return f"R$ {valor:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def porcento(taxa):
    return f"{taxa:.2%}".replace(".", ",")


def calcula_valor_presente(vl_futuro, tx_juros, nr_periodos):
    """Traz um valor futuro para a data de hoje: VP = VF / (1 + r)^n."""
    return vl_futuro / (1 + tx_juros) ** nr_periodos


def calcula_vpl(tx_juros, vetor_fluxo_caixa):
    """Valor Presente Líquido: soma dos valores presentes de todo o fluxo,
    incluindo o aporte inicial, que entra negativo no período zero."""
    return npf.npv(tx_juros, vetor_fluxo_caixa)


def calcula_tir(vetor_fluxo_caixa):
    """Taxa Interna de Retorno: a taxa que zera o VPL do projeto."""
    return npf.irr(vetor_fluxo_caixa)


def plota_analise_tir(vetor_fluxo_caixa, tir, tx_juros):
    """Desenha a curva do VPL em função da taxa e marca a TIR, onde ela cruza o zero."""
    eixo_x = np.linspace(0, 0.35, 200)
    vpl = np.array([calcula_vpl(i, vetor_fluxo_caixa) for i in eixo_x])

    figura, eixo = plt.subplots(figsize=(10, 6), dpi=110)
    eixo.plot(eixo_x, vpl, "--", color="#09124f", linewidth=2, label="VPL do projeto")
    eixo.axhline(0, color="#BDBDBD", linewidth=1)
    eixo.plot(tir, 0, "*", color="#E66C37", markersize=20,
              label=f"TIR = {porcento(tir)}")
    eixo.axvline(tx_juros, color="#1AAB40", linewidth=1.5, linestyle=":",
                 label=f"TMA = {porcento(tx_juros)}")

    eixo.set_title("TIR - Análise da Taxa Interna de Retorno", fontsize=15,
                   fontweight="bold", color="#09124f")
    eixo.set_xlabel("Taxa de juros - i", fontsize=11)
    eixo.set_ylabel("VPL (R$)", fontsize=11)
    eixo.legend(frameon=False, fontsize=10)
    eixo.grid(color="#EAEAEA")
    eixo.set_axisbelow(True)
    figura.text(0.99, 0.01, f"{ALUNO} ({MATRICULA})", ha="right", fontsize=9,
                color="#616161")

    GRAFICO.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(GRAFICO, facecolor="white")
    plt.close(figura)


def main():
    print("=" * 68)
    print("DataLab 6-B1 - Cálculo do VP, do VPL e da TIR")
    print(f"Aluno: {ALUNO}")
    print(f"Matrícula: {MATRICULA}")
    print("=" * 68)

    print("\nParâmetros escolhidos")
    print(f"  Aporte inicial (t = 0)     : {reais(APORTE_INICIAL)}")
    print(f"  Taxa mínima de atratividade: {porcento(TX_JUROS)} ao ano")
    print(f"  Períodos analisados (n)    : {NR_PERIODOS} anos")

    print("\nFluxo de caixa e valor presente de cada período")
    print(f"  {'Período':>8}  {'Fluxo de caixa':>18}  {'Valor presente':>18}")
    total_entradas = 0.0
    for periodo, valor in enumerate(VETOR_FLUXO_CAIXA):
        vl_presente = calcula_valor_presente(valor, TX_JUROS, periodo)
        total_entradas += vl_presente if periodo else 0.0
        print(f"  {periodo:>8}  {reais(valor):>18}  {reais(vl_presente):>18}")

    vpl = calcula_vpl(TX_JUROS, VETOR_FLUXO_CAIXA)
    tir = calcula_tir(VETOR_FLUXO_CAIXA)
    indice_lucratividade = total_entradas / abs(APORTE_INICIAL)

    print("\nResultado")
    print(f"  VP das entradas            : {reais(total_entradas)}")
    print(f"  VPL do projeto             : {reais(vpl)}")
    print(f"  TIR do projeto             : {porcento(tir)} ao ano")
    print(f"  Índice de lucratividade    : "
          f"{indice_lucratividade:.2f}".replace(".", ","))

    print("\nDecisão")
    if vpl > 0 and tir > TX_JUROS:
        print(f"  Projeto VIÁVEL: o VPL é positivo e a TIR de {porcento(tir)} supera")
        print(f"  a taxa mínima de atratividade de {porcento(TX_JUROS)} ao ano.")
        print(f"  Folga de {porcento(tir - TX_JUROS)} antes de o projeto deixar de compensar.")
    else:
        print(f"  Projeto INVIÁVEL nas condições atuais: o VPL é {reais(vpl)} e a")
        print(f"  TIR de {porcento(tir)} não supera a TMA de {porcento(TX_JUROS)}.")

    plota_analise_tir(VETOR_FLUXO_CAIXA, tir, TX_JUROS)
    print(f"\nGráfico da análise da TIR salvo em: {GRAFICO.name}")


if __name__ == "__main__":
    main()
