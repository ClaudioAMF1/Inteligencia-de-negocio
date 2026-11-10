"""
Projeto aplicado - renderiza o dashboard: uma página por pergunta do projeto.

Mesmo layout dos DataLabs (tela 1920x1080, título, pergunta, identificação da
dupla e logomarca). Os números vêm de projeto/dados/indicadores.json e
projeto/dados/painel_mensal.csv, gerados pelo script 03.
"""
import csv
import json
import zipfile
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False  # "R$" não é fórmula
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "projeto" / "dados"
SAIDA = RAIZ / "projeto" / "imagens"
PACOTE_LOGO = RAIZ / "datalab3" / "idp_ine_datalab3.pbix"
LOGO = "Report/StaticResources/RegisteredResources/Logomarca_pequena_IDP4803064698123293.jpg"

DUPLA = "Claudio da Aparecida Meireles Filho (2321070)  e  Felipe Pereira Dutra (2321017)"
AZUL_IDP = "#09124f"
COR = {"Brasília": "#118DFF", "Goiânia": "#E66C37"}
CINZA = "#616161"
FONTE = ("Fontes: ANP - Levantamento de Preços de Combustíveis; IBGE - PNAD Contínua; "
         "Banco Central - IPCA (SGS 433).")
DPI, LARGURA, ALTURA = 100, 19.20, 10.80


def reais(v, casas=2):
    return "R$ " + f"{v:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def milhar(n):
    return f"{n:,}".replace(",", ".")


def pct(v, casas=1):
    return f"{v * 100:.{casas}f}%".replace(".", ",")


def mes_br(m):
    nomes = "jan fev mar abr mai jun jul ago set out nov dez".split()
    return f"{nomes[int(m[5:]) - 1]}/{m[:4]}"


def moldura(numero, titulo, pergunta):
    fig = plt.figure(figsize=(LARGURA, ALTURA), dpi=DPI, facecolor="white")
    fig.text(0.045, 0.93, f"Projeto Aplicado  |  {titulo}", ha="left", va="center",
             fontsize=29, fontweight="bold", color=AZUL_IDP)
    fig.text(0.045, 0.875, f"Pergunta {numero}: {pergunta}", ha="left", va="center",
             fontsize=16, color=CINZA)
    fig.text(0.045, 0.832, DUPLA, ha="left", va="center", fontsize=14, fontweight="bold",
             color="#242424")
    fig.add_artist(plt.Line2D([0.045, 0.955], [0.805, 0.805], color="#E1E1E1", linewidth=1.5,
                              transform=fig.transFigure))
    with zipfile.ZipFile(PACOTE_LOGO) as pacote, pacote.open(LOGO) as arquivo:
        logo = mpimg.imread(arquivo, format="jpg")
    eixo = fig.add_axes([0.875, 0.82, 0.08, 0.15])
    eixo.imshow(logo)
    eixo.axis("off")
    fig.text(0.045, 0.025, FONTE, ha="left", va="center", fontsize=11, color=CINZA, style="italic")
    return fig


def cartao(fig, pos, valor, rotulo, cor, tamanho=34, detalhe=None):
    eixo = fig.add_axes(pos)
    eixo.set_xlim(0, 1)
    eixo.set_ylim(0, 1)
    eixo.axis("off")
    eixo.add_patch(FancyBboxPatch((0.01, 0.02), 0.98, 0.96, boxstyle="round,pad=0,rounding_size=0.04",
                                  facecolor="white", edgecolor="#E1E1E1", linewidth=1.5))
    eixo.add_patch(FancyBboxPatch((0.01, 0.02), 0.022, 0.96, boxstyle="square,pad=0",
                                  facecolor=cor, edgecolor="none"))
    eixo.text(0.52, 0.64 if detalhe else 0.6, valor, ha="center", va="center", fontsize=tamanho,
              fontweight="bold", color=cor)
    eixo.text(0.52, 0.33 if detalhe else 0.25, rotulo, ha="center", va="center", fontsize=15, color=CINZA)
    if detalhe:
        eixo.text(0.52, 0.13, detalhe, ha="center", va="center", fontsize=12, color=CINZA)


def estiliza(eixo, grade="y"):
    for lado in ("top", "right"):
        eixo.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        eixo.spines[lado].set_color("#E1E1E1")
    eixo.tick_params(colors=CINZA, labelsize=13)
    if grade:
        eixo.grid(axis=grade, color="#EEEEEE", linewidth=1)
    eixo.set_axisbelow(True)


def anos_no_eixo(eixo, inicio, fim):
    """Marca só anos inteiros no eixo x, sem decimais."""
    passo = 1 if fim - inicio <= 6 else 2
    anos = list(range(int(inicio), int(fim) + 1, passo))
    eixo.set_xticks(anos)
    eixo.set_xticklabels([str(a) for a in anos])


def salva(fig, nome):
    SAIDA.mkdir(parents=True, exist_ok=True)
    fig.savefig(SAIDA / nome, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"  projeto/imagens/{nome}")


def painel():
    with (DADOS / "painel_mensal.csv").open(encoding="utf-8") as f:
        return [{**l, "media": float(l["media"]),
                 "media_real": float(l["media_real"]) if l["media_real"] else None}
                for l in csv.DictReader(f)]


# ---------------------------------------------------------------------- páginas
def pagina1(ind):
    p1 = ind["p1"]
    fig = moldura(1, "Brasília x Goiânia: onde se paga mais caro",
                  "Em qual capital o consumidor paga mais caro pelo etanol e pela gasolina?")
    periodo = f"{mes_br(p1['meses'][0])} a {mes_br(p1['meses'][1])}"
    for i, produto in enumerate(("Etanol", "Gasolina")):
        dados = p1["produtos"][produto]
        eixo = fig.add_axes([0.06 + i * 0.47, 0.46, 0.40, 0.245])
        for j, cidade in enumerate(("Brasília", "Goiânia")):
            d = dados[cidade]
            eixo.plot([d["minimo"], d["maximo"]], [j, j], color=COR[cidade], linewidth=14,
                      alpha=0.35, solid_capstyle="round")
            eixo.plot(d["media"], j, "o", color=COR[cidade], markersize=17)
            eixo.text(d["minimo"], j + 0.28, reais(d["minimo"]), ha="center", fontsize=12, color=CINZA)
            eixo.text(d["maximo"], j + 0.28, reais(d["maximo"]), ha="center", fontsize=12, color=CINZA)
            eixo.text(d["media"], j - 0.36, f"média {reais(d['media'])}", ha="center", fontsize=13,
                      color=COR[cidade], fontweight="bold")
        eixo.set_yticks([0, 1])
        eixo.set_yticklabels(["Brasília", "Goiânia"], fontsize=15)
        eixo.set_ylim(-0.7, 1.6)
        valores = [dados[c][k] for c in ("Brasília", "Goiânia") for k in ("minimo", "maximo")]
        eixo.set_xlim(min(valores) - 0.15, max(valores) + 0.15)
        eixo.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: reais(v)))
        mais_cara = "Brasília" if dados["diferenca_media"] > 0 else "Goiânia"
        eixo.set_title(f"{produto}: mais caro em {mais_cara} (+{reais(abs(dados['diferenca_media']))}/litro)",
                       loc="left", fontsize=17, color="#242424", pad=12)
        estiliza(eixo, grade="x")

        serie = fig.add_axes([0.06 + i * 0.47, 0.09, 0.40, 0.28])
        for cidade in ("Brasília", "Goiânia"):
            anual = p1["serie_anual"][f"{cidade}|{produto}"]
            anos = sorted(anual, key=int)
            serie.plot([int(a) for a in anos], [anual[a] for a in anos], color=COR[cidade],
                       linewidth=3, marker="o", label=cidade)
        serie.set_title(f"{produto}: preço médio anual (R$/litro)", loc="left", fontsize=14, color=CINZA)
        todos = [int(a) for c in ("Brasília", "Goiânia") for a in p1["serie_anual"][f"{c}|{produto}"]]
        anos_no_eixo(serie, min(todos), max(todos))
        serie.legend(frameon=False, fontsize=12)
        serie.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: reais(v)))
        estiliza(serie)
    fig.text(0.06, 0.778, f"Faixa entre o menor e o maior preço coletado em cada semana, em média, de {periodo}. "
             "O ponto é o preço médio.", fontsize=13, color=CINZA)
    salva(fig, "pagina1_bsb_x_gyn.png")


def pagina2(ind):
    p2 = ind["p2"]
    fig = moldura(2, "Quanto da renda vai para o tanque",
                  "Que percentual da renda vai para o combustível em cada capital?")
    anos = sorted(p2["anos"], key=int)
    ultimo = anos[-1]
    for i, cidade in enumerate(("Brasília", "Goiânia")):
        d = p2["anos"][ultimo][cidade]
        cartao(fig, [0.045 + i * 0.46, 0.57, 0.43, 0.2], pct(d["percentual"]),
               f"{cidade}: {p2['litros_mes']} L de gasolina / renda per capita ({ultimo})", COR[cidade],
               tamanho=40, detalhe=f"gasto de {reais(d['gasto_mensal'])} sobre renda de {reais(d['renda_per_capita'], 0)}")
    eixo = fig.add_axes([0.06, 0.1, 0.88, 0.38])
    for cidade in ("Brasília", "Goiânia"):
        xs = [int(a) for a in anos if cidade in p2["anos"][a]]
        ys = [p2["anos"][str(a)][cidade]["percentual"] for a in xs]
        eixo.plot(xs, ys, color=COR[cidade], linewidth=3.5, marker="o", markersize=9, label=cidade)
        for x, y in zip(xs, ys):
            eixo.annotate(pct(y, 0), (x, y), textcoords="offset points", xytext=(0, 10), ha="center",
                          fontsize=11, color=COR[cidade])
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: pct(v, 0)))
    eixo.set_title("Custo de 100 litros de gasolina por mês como % da renda domiciliar per capita",
                   loc="left", fontsize=15, color="#242424", pad=10)
    eixo.legend(frameon=False, fontsize=13)
    eixo.set_ylim(0, max(v[c]["percentual"] for v in p2["anos"].values() for c in v) * 1.25)
    estiliza(eixo)
    fig.text(0.06, 0.05, "100 L/mês ≈ 1.000 km com um carro que faz 10 km/l. Renda: IBGE, DF para Brasília "
             "e Goiás para Goiânia (o IBGE não publica a renda anual por município).",
             fontsize=12, color=CINZA)
    salva(fig, "pagina2_peso_na_renda.png")


def pagina3(ind):
    p3 = ind["p3"]
    fig = moldura(3, "Quanto se economiza pesquisando",
                  "Na mesma cidade e na mesma semana, quanto custa a diferença entre o posto mais caro e o mais barato?")
    periodo = f"{mes_br(p3['meses'][0])} a {mes_br(p3['meses'][1])}"
    for i, cidade in enumerate(("Brasília", "Goiânia")):
        d = p3["cidades"][cidade]
        cartao(fig, [0.045 + i * 0.46, 0.57, 0.205, 0.2], reais(d["spread_medio"]),
               f"{cidade}: por litro", COR[cidade], tamanho=36, detalhe="mais caro - mais barato")
        cartao(fig, [0.27 + i * 0.46, 0.57, 0.205, 0.2], reais(d["economia_tanque"]),
               f"{cidade}: por tanque", COR[cidade], tamanho=36, detalhe=f"tanque de {p3['tanque_litros']} L")
    eixo = fig.add_axes([0.06, 0.1, 0.88, 0.37])
    largura = 0.38
    anos = sorted({int(a) for c in p3["cidades"].values() for a in c["por_ano"]})
    for j, cidade in enumerate(("Brasília", "Goiânia")):
        por_ano = p3["cidades"][cidade]["por_ano"]
        xs = [a + (j - 0.5) * largura for a in anos if str(a) in por_ano]
        ys = [por_ano[str(a)] for a in anos if str(a) in por_ano]
        eixo.bar(xs, ys, width=largura, color=COR[cidade], label=cidade)
    eixo.set_xticks(anos)
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: reais(v)))
    eixo.set_title("Diferença média entre o posto mais caro e o mais barato na semana (gasolina, R$/litro)",
                   loc="left", fontsize=15, color="#242424", pad=10)
    eixo.legend(frameon=False, fontsize=13)
    estiliza(eixo)
    fig.text(0.06, 0.785, f"Cartões: média das semanas de {periodo}, só semanas com pelo menos 5 postos coletados.",
             fontsize=13, color=CINZA)
    salva(fig, "pagina3_economia_pesquisando.png")


def pagina4(ind):
    p4 = ind["p4"]
    fig = moldura(4, "Quando o etanol compensou",
                  "Em que períodos o etanol custou menos de 70% da gasolina em cada capital?")
    for i, cidade in enumerate(("Brasília", "Goiânia")):
        d = p4["cidades"][cidade]
        cartao(fig, [0.045 + i * 0.46, 0.6, 0.43, 0.17], f"{len(d['meses_compensou'])} de {d['total_meses']} meses",
               f"{cidade}: meses em que o etanol compensou", COR[cidade], tamanho=34,
               detalhe=f"razão etanol/gasolina no último mês: {pct(d['razao_ultimo_mes'])}")
    eixo = fig.add_axes([0.06, 0.1, 0.88, 0.42])
    for cidade in ("Brasília", "Goiânia"):
        razoes = p4["cidades"][cidade]["razao_mensal"]
        meses = sorted(razoes)
        xs = [int(m[:4]) + (int(m[5:]) - 1) / 12 for m in meses]
        eixo.plot(xs, [razoes[m] for m in meses], color=COR[cidade], linewidth=2.5, label=cidade)
    eixo.axhline(p4["limite"], color=AZUL_IDP, linewidth=2, linestyle="--")
    eixo.axhspan(0, p4["limite"], color="#1AAB40", alpha=0.07)
    eixo.text(eixo.get_xlim()[0] + 0.1, p4["limite"] - 0.015, "abaixo de 70%: etanol compensa",
              fontsize=13, color="#148036", va="top", fontweight="bold")
    eixo.set_ylim(0.55, 0.95)
    anos_no_eixo(eixo, *[int(m[:4]) for m in (min(min(c["razao_mensal"]) for c in p4["cidades"].values()),
                                               max(max(c["razao_mensal"]) for c in p4["cidades"].values()))])
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: pct(v, 0)))
    eixo.set_title("Preço médio do etanol como % do preço médio da gasolina, mês a mês", loc="left",
                   fontsize=15, color="#242424", pad=10)
    eixo.legend(frameon=False, fontsize=13, loc="upper right")
    estiliza(eixo)
    salva(fig, "pagina4_paridade_etanol.png")


def pagina5(ind):
    p5 = ind["p5"]
    fig = moldura(5, "A bandeira faz diferença no bolso?",
                  "Postos BR, Ipiranga e Shell cobram diferente dos postos de bandeira branca?")
    periodo = f"{mes_br(p5['meses'][0])} a {mes_br(p5['meses'][1])}"
    ordem = ["BR (Vibra)", "Ipiranga", "Shell (Raízen)", "Outras bandeiras", "Bandeira branca"]
    for i, cidade in enumerate(("Brasília", "Goiânia")):
        dados = p5["cidades"][cidade]
        bandeiras = [b for b in ordem if b in dados]
        eixo = fig.add_axes([0.13 + i * 0.47, 0.15, 0.34, 0.54])
        valores = [dados[b]["desvio_medio"] for b in bandeiras]
        cores = ["#1AAB40" if v < 0 else COR[cidade] for v in valores]
        rotulos = [f"{b}\n{milhar(dados[b]['coletas'])} coletas, {dados[b]['postos']} postos" for b in bandeiras]
        barras = eixo.barh(rotulos, valores, color=cores, height=0.6)
        limite = max(abs(v) for v in valores) * 2.2
        for barra, v in zip(barras, valores):
            sinal = "+" if v >= 0 else "-"
            eixo.text(v + (limite * 0.03 if v >= 0 else -limite * 0.03), barra.get_y() + barra.get_height() / 2,
                      f"{sinal}{reais(abs(v), 3)}", va="center", ha="left" if v >= 0 else "right",
                      fontsize=14, color="#242424", fontweight="bold")
        eixo.axvline(0, color="#9E9E9E", linewidth=1)
        eixo.set_xlim(-limite, limite)
        # Eixo em centavos por litro, com marcas a cada 2 centavos.
        eixo.xaxis.set_major_locator(plt.MultipleLocator(0.02))
        eixo.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{round(v * 100):+d}".replace("+0", "0")))
        eixo.set_xlabel("centavos por litro em relação à média da semana", fontsize=12, color=CINZA)
        eixo.tick_params(axis="y", labelsize=14)
        eixo.set_title(cidade, loc="left", fontsize=19, color=COR[cidade], fontweight="bold", pad=10)
        estiliza(eixo, grade="x")
        eixo.invert_yaxis()
    fig.text(0.07, 0.765, f"Gasolina, {periodo}. Cada barra é quanto o posto daquela bandeira cobra, em média, "
             "acima ou abaixo da média da cidade na mesma semana (R$/litro).", fontsize=13, color=CINZA)
    salva(fig, "pagina5_bandeiras.png")


def pagina6(ind, linhas):
    p6 = ind["p6"]
    fig = moldura(6, "Quanto da alta é alta de verdade",
                  "Descontada a inflação (IPCA), o preço real da gasolina subiu ou caiu?")
    for i, cidade in enumerate(("Brasília", "Goiânia")):
        d = p6["cidades"][cidade]
        a0, a1 = d["anos"]
        cartao(fig, [0.045 + i * 0.46, 0.6, 0.205, 0.17], pct(d["variacao_nominal"]),
               f"{cidade}: nominal {a0}-{a1}", COR[cidade], tamanho=34)
        cartao(fig, [0.27 + i * 0.46, 0.6, 0.205, 0.17], pct(d["variacao_real"]),
               f"{cidade}: real {a0}-{a1}", AZUL_IDP, tamanho=34)
    eixo = fig.add_axes([0.06, 0.1, 0.88, 0.42])
    for cidade in ("Brasília", "Goiânia"):
        serie = sorted((l for l in linhas if l["cidade"] == cidade and l["produto"] == "Gasolina"
                        and l["media_real"]), key=lambda l: l["mes"])
        xs = [int(l["mes"][:4]) + (int(l["mes"][5:]) - 1) / 12 for l in serie]
        eixo.plot(xs, [l["media"] for l in serie], color=COR[cidade], linewidth=1.8, alpha=0.55,
                  linestyle="--", label=f"{cidade} - nominal")
        eixo.plot(xs, [l["media_real"] for l in serie], color=COR[cidade], linewidth=3,
                  label=f"{cidade} - real (R$ de {mes_br(p6['base_real'])})")
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: reais(v)))
    meses = [l["mes"] for l in linhas if l["produto"] == "Gasolina" and l["media_real"]]
    anos_no_eixo(eixo, int(min(meses)[:4]), int(max(meses)[:4]))
    eixo.set_title("Gasolina: preço médio mensal nominal (tracejado) e real, corrigido pelo IPCA",
                   loc="left", fontsize=15, color="#242424", pad=10)
    eixo.legend(frameon=False, fontsize=12, ncol=2, loc="upper left")
    estiliza(eixo)
    fig.text(0.06, 0.05, f"IPCA acumulado no período: {pct(p6['ipca_acumulado'])}. "
             "Preço real = preço do mês x (índice do IPCA na data-base / índice do mês).",
             fontsize=12, color=CINZA)
    salva(fig, "pagina6_preco_real.png")


def main():
    ind = json.loads((DADOS / "indicadores.json").read_text(encoding="utf-8"))
    linhas = painel()
    pagina1(ind)
    pagina2(ind)
    pagina3(ind)
    pagina4(ind)
    pagina5(ind)
    pagina6(ind, linhas)


if __name__ == "__main__":
    main()
