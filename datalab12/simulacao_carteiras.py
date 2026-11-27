# Claudio da Aparecida Meireles Filho | Matrícula 2321070
# DataLab 12-B2 | Simulação de carteiras com três ações da B3
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

PASTA = Path(__file__).resolve().parent
ATIVOS = ["ABEV3", "ITUB4", "SUZB3"]
SEMENTE = 2321070


def simular_carteiras(retornos):
    medias = retornos.mean().to_numpy()
    covariancia = retornos.cov().to_numpy()
    gerador = np.random.default_rng(SEMENTE)
    carteiras = []
    for _ in range(200):
        pesos = gerador.random(len(ATIVOS))
        pesos /= pesos.sum()
        retorno = pesos @ medias
        volatilidade = np.sqrt(pesos @ covariancia @ pesos)
        carteiras.append([*pesos, retorno, volatilidade])
    quadro = pd.DataFrame(carteiras, columns=[*ATIVOS, "retorno", "volatilidade"])
    quadro.index = pd.RangeIndex(1, len(quadro) + 1, name="carteira")
    return quadro


def ler_fechamentos():
    arquivo = PASTA / "dados" / "fechamentos.csv"
    precos = pd.read_csv(arquivo, parse_dates=["data"]).set_index("data")[ATIVOS]
    datas = precos.index
    if len(precos) != 30 or not datas.is_unique or not datas.is_monotonic_increasing:
        raise ValueError("O CSV deve conter 30 pregões distintos, em ordem crescente.")
    if datas.hasnans or not np.isfinite(precos).all().all() or (precos <= 0).any().any():
        raise ValueError("Todas as datas e todos os fechamentos devem ser válidos.")
    return precos


def percentual(valor, casas=3):
    return f"{valor:.{casas}%}".replace(".", ",")


def imprimir_resultados(precos, retornos, destaques):
    inicio, fim = precos.index[[0, -1]]
    print("DataLab 12-B2 | Simulação de 200 carteiras")
    print(f"B3 | {inicio:%d/%m/%Y} a {fim:%d/%m/%Y} | {len(precos)} pregões"
          f" | {len(retornos)} retornos diários")
    print(f"Sorteio dos pesos | Semente {SEMENTE}")
    print("\nAção       Fech. inicial    Fech. final    Retorno/dia     Vol./dia")
    for ativo in ATIVOS:
        inicial, final = precos[ativo].iloc[[0, -1]]
        valores = [f"R$ {v:.2f}".replace(".", ",") for v in (inicial, final)]
        media = percentual(retornos[ativo].mean())
        desvio = percentual(retornos[ativo].std())
        print(f"{ativo:<8}{valores[0]:>15}{valores[1]:>15}{media:>15}{desvio:>13}")
    print("\nCarteira                  ABEV3    ITUB4    SUZB3    Retorno/dia    Vol./dia")
    for nome, linha in destaques.items():
        pesos = "".join(f"{percentual(linha[a], 2):>9}" for a in ATIVOS)
        media = percentual(linha["retorno"])
        desvio = percentual(linha["volatilidade"])
        print(f"{nome:<22}{pesos}{media:>15}{desvio:>12}")
    print("\nVolatilidade = desvio-padrão dos retornos diários.")


def desenhar_grafico(carteiras, destaques, destino):
    fig, eixo = plt.subplots(figsize=(8.8, 4.8), layout="constrained")
    eixo.set_axisbelow(True)
    eixo.grid(color="#DDE2E6", linewidth=0.7)
    eixo.axhline(0, color="#8A959E", linewidth=1)
    eixo.scatter(carteiras.volatilidade, carteiras.retorno, s=24,
                 color="#45769B", alpha=0.65, linewidths=0, label="Carteiras sorteadas")
    estilos = [("D", "#007668"), ("s", "#182D42"), ("^", "#AF4A16")]
    for (nome, linha), (marca, cor) in zip(destaques.items(), estilos):
        eixo.scatter(linha.volatilidade, linha.retorno, marker=marca, s=100,
                     color=cor, edgecolors="white", linewidths=1, zorder=4, label=nome)
    escala = FuncFormatter(lambda x, _: percentual(x, 1))
    eixo.xaxis.set_major_formatter(escala)
    eixo.yaxis.set_major_formatter(escala)
    eixo.set_xlabel("Volatilidade diária")
    eixo.set_ylabel("Retorno médio diário")
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.spines[["left", "bottom"]].set_color("#9AA5AC")
    eixo.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2,
                frameon=False, fontsize=9)
    fig.savefig(destino, dpi=180, facecolor="white")
    plt.close(fig)


def main():
    print("Claudio da Aparecida Meireles Filho | Matrícula 2321070", flush=True)
    precos = ler_fechamentos()
    retornos = precos.pct_change(fill_method=None).iloc[1:]
    carteiras = simular_carteiras(retornos)
    minimo = carteiras.volatilidade.idxmin()
    maximo = carteiras.retorno.idxmax()
    pesos_iguais = np.full(len(ATIVOS), 1 / len(ATIVOS))
    serie_igual = retornos @ pesos_iguais
    referencia = pd.Series([*pesos_iguais, serie_igual.mean(), serie_igual.std()],
                           index=carteiras.columns)
    destaques = {f"Menor risco #{minimo}": carteiras.loc[minimo],
                 "Pesos iguais": referencia,
                 f"Maior retorno #{maximo}": carteiras.loc[maximo]}
    imprimir_resultados(precos, retornos, destaques)
    destino = PASTA / "resultados"
    destino.mkdir(exist_ok=True)
    carteiras.to_csv(destino / "carteiras.csv", float_format="%.12f")
    desenhar_grafico(carteiras, destaques, destino / "risco_retorno.png")


if __name__ == "__main__":
    main()
