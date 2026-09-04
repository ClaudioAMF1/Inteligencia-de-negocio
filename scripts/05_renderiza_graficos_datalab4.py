"""
DataLab 4-B1 - gera os três gráficos da série histórica escolhida.

Série: Indivíduos usando a Internet (% da população) - IT.NET.USER.ZS
Fonte: World Bank Open Data - https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=BR

Gráfico 1 - evolução do Brasil ao longo de toda a série publicada (1990-2024).
Gráfico 2 - variação anual em pontos percentuais, que mostra onde o movimento acelerou.
Gráfico 3 - Brasil x América Latina e Caribe x Mundo, para dar contexto ao movimento.
"""
import csv
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
SERIE = RAIZ / "datalab4" / "dados" / "serie_internet.csv"
SAIDA = RAIZ / "datalab4" / "imagens"
# A logomarca vem do próprio pacote do Power BI do DataLab 3, para manter a
# identidade visual das duas entregas.
PACOTE_PBIX = RAIZ / "datalab3" / "idp_ine_datalab3.pbix"
LOGO_NO_PACOTE = "Report/StaticResources/RegisteredResources/Logomarca_pequena_IDP4803064698123293.jpg"

ALUNO = "Claudio da Aparecida Meireles Filho (2321070)"
FONTE = "Fonte: World Bank Open Data - Individuals using the Internet (% of population), IT.NET.USER.ZS"
AZUL_IDP = "#09124f"
CORES = {"Brasil": "#118DFF", "América Latina e Caribe": "#E66C37", "Mundo": "#6B007B"}
CINZA = "#616161"

DPI = 100
LARGURA, ALTURA = 16.0, 9.0


def carrega_serie():
    """Lê o CSV longo produzido pelo script 04, ignorando os anos sem valor."""
    series = {nome: {} for nome in CORES}
    with SERIE.open(encoding="utf-8") as arquivo:
        for linha in csv.DictReader(arquivo):
            ano = int(linha["ano"])
            for nome in series:
                if linha[nome]:
                    series[nome][ano] = float(linha[nome])
    return series


def moldura(titulo, subtitulo):
    figura = plt.figure(figsize=(LARGURA, ALTURA), dpi=DPI, facecolor="white")
    figura.text(0.06, 0.925, titulo, ha="left", va="center",
                fontsize=27, fontweight="bold", color=AZUL_IDP)
    figura.text(0.06, 0.868, subtitulo, ha="left", va="center", fontsize=15, color=CINZA)
    figura.text(0.06, 0.030, FONTE, ha="left", va="center", fontsize=11, color=CINZA)
    figura.text(0.94, 0.030, ALUNO, ha="right", va="center", fontsize=11, color=CINZA)

    with zipfile.ZipFile(PACOTE_PBIX) as pacote, pacote.open(LOGO_NO_PACOTE) as arquivo:
        logo = mpimg.imread(arquivo, format="jpg")
    eixo_logo = figura.add_axes([0.868, 0.868, 0.072, 0.096])
    eixo_logo.imshow(logo)
    eixo_logo.axis("off")
    return figura


def estiliza(eixo):
    for lado in ("top", "right"):
        eixo.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        eixo.spines[lado].set_color("#E1E1E1")
    eixo.tick_params(colors=CINZA, labelsize=12)
    eixo.grid(axis="y", color="#EEEEEE", linewidth=1)
    eixo.set_axisbelow(True)


def salva(figura, nome):
    SAIDA.mkdir(parents=True, exist_ok=True)
    caminho = SAIDA / nome
    figura.savefig(caminho, dpi=DPI, facecolor="white")
    plt.close(figura)
    print(f"  {caminho.relative_to(RAIZ)}")


def grafico1(series):
    """Evolução da série no Brasil, com marcação dos pontos que explicam o movimento."""
    brasil = series["Brasil"]
    anos = sorted(brasil)
    valores = [brasil[a] for a in anos]

    figura = moldura(
        "Brasil: pessoas usando a Internet",
        f"% da população, {anos[0]}-{anos[-1]}",
    )
    eixo = figura.add_axes([0.06, 0.12, 0.88, 0.70])
    eixo.plot(anos, valores, color=CORES["Brasil"], linewidth=3)
    eixo.fill_between(anos, valores, color=CORES["Brasil"], alpha=0.15)

    # Marcos que sustentam a leitura da curva em S.
    meio = next(a for a in anos if brasil[a] >= 50)
    for ano, texto, deslocamento in (
        (anos[0], f"{anos[0]}: {brasil[anos[0]]:.1f}%".replace(".", ","), 6),
        (meio, f"{meio}: metade da população".replace(".", ","), 8),
        (anos[-1], f"{anos[-1]}: {brasil[anos[-1]]:.1f}%".replace(".", ","), -14),
    ):
        eixo.plot([ano], [brasil[ano]], "o", color=CORES["Brasil"], markersize=9)
        eixo.annotate(texto, (ano, brasil[ano]), textcoords="offset points",
                      xytext=(deslocamento, 14), fontsize=13, color=AZUL_IDP,
                      fontweight="bold", ha="left" if deslocamento >= 0 else "right")

    eixo.set_ylim(0, 100)
    eixo.set_ylabel("% da população", fontsize=14, color=CINZA, labelpad=10)
    eixo.set_xlim(anos[0], anos[-1])
    eixo.set_xticks([a for a in anos if a % 5 == 0] + [anos[-1]])
    estiliza(eixo)
    salva(figura, "grafico1_evolucao_brasil.png")


def grafico2(series):
    """Quanto a série avançou a cada ano, em pontos percentuais."""
    brasil = series["Brasil"]
    anos = sorted(brasil)
    variacoes = [(ano, brasil[ano] - brasil[ano - 1]) for ano in anos[1:]]

    figura = moldura(
        "Quanto a Internet avançou a cada ano no Brasil",
        f"variação anual em pontos percentuais, {variacoes[0][0]}-{variacoes[-1][0]}",
    )
    eixo = figura.add_axes([0.06, 0.14, 0.88, 0.68])

    maior = max(variacoes, key=lambda item: item[1])
    cores = [CORES["Brasil"] if ano != maior[0] else "#12239E" for ano, _ in variacoes]
    cores = [cor if valor >= 0 else CORES["América Latina e Caribe"]
             for cor, (_, valor) in zip(cores, variacoes)]
    eixo.bar([a for a, _ in variacoes], [v for _, v in variacoes], color=cores, width=0.75)
    eixo.axhline(0, color="#BDBDBD", linewidth=1)

    rotulo_maior = f"{maior[1]:.1f}".replace(".", ",")
    eixo.annotate(f"{maior[0]}: +{rotulo_maior} p.p.",
                  (maior[0], maior[1]), textcoords="offset points", xytext=(0, 12),
                  ha="center", fontsize=13, fontweight="bold", color="#12239E")

    eixo.set_ylabel("pontos percentuais no ano", fontsize=14, color=CINZA, labelpad=10)
    eixo.set_xticks([a for a, _ in variacoes if a % 5 == 0])
    estiliza(eixo)
    salva(figura, "grafico2_variacao_anual.png")


def grafico3(series):
    """Brasil comparado aos agregados da região e do mundo."""
    comuns = sorted(set(series["Brasil"]) & set(series["Mundo"]) & set(series["América Latina e Caribe"]))

    figura = moldura(
        "Brasil, América Latina e Mundo: quem está conectado",
        f"% da população usando a Internet, {comuns[0]}-{comuns[-1]}",
    )
    eixo = figura.add_axes([0.06, 0.12, 0.88, 0.70])

    for nome, cor in CORES.items():
        valores = [series[nome][ano] for ano in comuns]
        eixo.plot(comuns, valores, color=cor, linewidth=3, label=nome)
        eixo.annotate(f"{valores[-1]:.1f}%".replace(".", ","), (comuns[-1], valores[-1]),
                      textcoords="offset points", xytext=(10, -4), fontsize=13,
                      fontweight="bold", color=cor)

    eixo.set_ylim(0, 100)
    eixo.set_xlim(comuns[0], comuns[-1] + 1.5)
    eixo.set_xticks([a for a in comuns if a % 5 == 0] + [comuns[-1]])
    eixo.set_ylabel("% da população", fontsize=14, color=CINZA, labelpad=10)
    eixo.legend(loc="upper left", frameon=False, fontsize=14, labelcolor=CINZA)
    estiliza(eixo)
    salva(figura, "grafico3_comparativo.png")


def main():
    if not SERIE.exists():
        raise SystemExit("rode antes o script 04 para gerar datalab4/dados/serie_internet.csv")
    series = carrega_serie()
    grafico1(series)
    grafico2(series)
    grafico3(series)


if __name__ == "__main__":
    main()
