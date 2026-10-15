"""
DataLab 7-B2 - renderiza as sete páginas do dashboard, uma por pergunta.

Cada página segue o layout de relatório do Power BI usado no DataLab 3 (tela de
1920x1080, título, identificação do aluno e logomarca) e responde a uma das
perguntas do enunciado com o visual que o Power BI usaria para ela: cartão,
gráfico de colunas, barras com linha de média e matriz com hierarquia.

Os números vêm de datalab7/dados/dados_financeiros_tratados.csv (script 11).
"""
import csv
import zipfile
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "datalab7" / "dados" / "dados_financeiros_tratados.csv"
SAIDA = RAIZ / "datalab7" / "imagens"
PACOTE_LOGO = RAIZ / "datalab3" / "idp_ine_datalab3.pbix"
LOGO = "Report/StaticResources/RegisteredResources/Logomarca_pequena_IDP4803064698123293.jpg"

ALUNO = "Claudio da Aparecida Meireles Filho (2321070)"
AZUL_IDP = "#09124f"
COR = {"Receitas": "#118DFF", "Despesas": "#E66C37", "Lucro": "#1AAB40"}
DESTAQUE_MAIOR = "#12239E"
DESTAQUE_MENOR = "#D64550"
CINZA = "#616161"
CINZA_CLARO = "#C8C6C4"
NOTA_ANOS = "O dataset não traz o ano de 2021: a série vai de jan/2019 a dez/2020 e de jan/2022 a dez/2022."

DPI = 100
LARGURA, ALTURA = 19.20, 10.80


# ---------------------------------------------------------------- dados
def carrega():
    with DADOS.open(encoding="utf-8") as arquivo:
        return [{**linha, "Ano": int(linha["Ano"]), "Valor": float(linha["Valor"])}
                for linha in csv.DictReader(arquivo)]


def soma(registros, *chaves):
    total = defaultdict(float)
    for r in registros:
        total[tuple(r[c] for c in chaves) if len(chaves) > 1 else r[chaves[0]]] += r["Valor"]
    return dict(total)


# ---------------------------------------------------------------- formatação
def reais(valor, casas=2):
    texto = f"{valor:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")
    return f"R$ {texto}"


def porcento(valor, casas=2):
    return f"{valor * 100:.{casas}f}%".replace(".", ",")


# ---------------------------------------------------------------- moldura
def moldura(numero, titulo, pergunta):
    figura = plt.figure(figsize=(LARGURA, ALTURA), dpi=DPI, facecolor="white")
    figura.text(0.045, 0.925, f"DataLab 7-B2  |  {titulo}", ha="left", va="center",
                fontsize=30, fontweight="bold", color=AZUL_IDP)
    figura.text(0.045, 0.868, f"Pergunta {numero}: {pergunta}", ha="left", va="center",
                fontsize=17, color=CINZA)
    figura.text(0.045, 0.823, ALUNO, ha="left", va="center", fontsize=15,
                fontweight="bold", color="#242424")
    figura.add_artist(plt.Line2D([0.045, 0.955], [0.795, 0.795], color="#E1E1E1",
                                 linewidth=1.5, transform=figura.transFigure))

    with zipfile.ZipFile(PACOTE_LOGO) as pacote, pacote.open(LOGO) as arquivo:
        logo = mpimg.imread(arquivo, format="jpg")
    eixo_logo = figura.add_axes([0.875, 0.815, 0.08, 0.15])
    eixo_logo.imshow(logo)
    eixo_logo.axis("off")
    return figura


def cartao(figura, posicao, valor, rotulo, cor, tamanho=46):
    eixo = figura.add_axes(posicao)
    eixo.set_xlim(0, 1)
    eixo.set_ylim(0, 1)
    eixo.axis("off")
    eixo.add_patch(FancyBboxPatch((0.01, 0.02), 0.98, 0.96, boxstyle="round,pad=0,rounding_size=0.04",
                                  facecolor="white", edgecolor="#E1E1E1", linewidth=1.5))
    eixo.add_patch(FancyBboxPatch((0.01, 0.02), 0.025, 0.96, boxstyle="square,pad=0",
                                  facecolor=cor, edgecolor="none"))
    eixo.text(0.52, 0.60, valor, ha="center", va="center", fontsize=tamanho,
              fontweight="bold", color=cor)
    eixo.text(0.52, 0.24, rotulo, ha="center", va="center", fontsize=17, color=CINZA)


def estiliza(eixo, grade="y"):
    for lado in ("top", "right"):
        eixo.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        eixo.spines[lado].set_color("#E1E1E1")
    eixo.tick_params(colors=CINZA, labelsize=14)
    if grade:
        eixo.grid(axis=grade, color="#EEEEEE", linewidth=1)
    eixo.set_axisbelow(True)


def nota(figura, texto):
    figura.text(0.045, 0.03, texto, ha="left", va="center", fontsize=12,
                color=CINZA, style="italic")


def salva(figura, nome):
    SAIDA.mkdir(parents=True, exist_ok=True)
    caminho = SAIDA / nome
    figura.savefig(caminho, dpi=DPI, facecolor="white")
    plt.close(figura)
    print(f"  {caminho.relative_to(RAIZ)}")


def colunas_por_ano(figura, posicao, por_ano, cor, titulo):
    eixo = figura.add_axes(posicao)
    anos = sorted(por_ano)
    valores = [por_ano[a] for a in anos]
    barras = eixo.bar([str(a) for a in anos], valores, color=cor, width=0.55)
    for barra, valor in zip(barras, valores):
        eixo.text(barra.get_x() + barra.get_width() / 2, valor, reais(valor, 0),
                  ha="center", va="bottom", fontsize=15, color="#242424", fontweight="bold")
    eixo.set_title(titulo, loc="left", fontsize=18, color="#242424", pad=16)
    eixo.set_ylim(0, max(valores) * 1.18)
    eixo.set_yticks([])
    eixo.spines["left"].set_visible(False)
    estiliza(eixo, grade=None)
    return eixo


# ---------------------------------------------------------------- páginas
def pagina_total(registros, numero, tipo, pergunta, arquivo):
    figura = moldura(numero, f"Total de {tipo.lower()}", pergunta)
    do_tipo = [r for r in registros if r["Tipo"] == tipo]
    total = sum(r["Valor"] for r in do_tipo)
    cartao(figura, [0.045, 0.30, 0.36, 0.40], reais(total), f"Total de {tipo.lower()}",
           COR[tipo], tamanho=50)
    colunas_por_ano(figura, [0.48, 0.12, 0.47, 0.58], soma(do_tipo, "Ano"), COR[tipo],
                    f"{tipo} por ano")
    nota(figura, NOTA_ANOS)
    salva(figura, arquivo)


def pagina_margem(registros):
    figura = moldura(3, "Margem de lucro", "Qual foi a margem de lucro?")
    por_tipo = soma(registros, "Tipo")
    receitas, despesas = por_tipo["Receitas"], por_tipo["Despesas"]
    lucro = receitas - despesas

    largura = 0.205
    for indice, (valor, rotulo, cor) in enumerate([
        (reais(receitas, 0), "Receitas", COR["Receitas"]),
        (reais(despesas, 0), "Despesas", COR["Despesas"]),
        (reais(lucro, 0), "Lucro (receitas - despesas)", COR["Lucro"]),
        (porcento(lucro / receitas), "Margem (lucro ÷ receitas)", AZUL_IDP),
    ]):
        cartao(figura, [0.045 + indice * (largura + 0.023), 0.55, largura, 0.21],
               valor, rotulo, cor, tamanho=34)

    por_ano = soma(registros, "Ano", "Tipo")
    anos = sorted({a for a, _ in por_ano})
    margens = [(por_ano[(a, "Receitas")] - por_ano[(a, "Despesas")]) / por_ano[(a, "Receitas")]
               for a in anos]
    eixo = figura.add_axes([0.06, 0.11, 0.88, 0.36])
    rotulos = [str(a) for a in anos]
    eixo.plot(rotulos, margens, color=AZUL_IDP, linewidth=3.5, marker="o", markersize=12)
    for rotulo, margem in zip(rotulos, margens):
        eixo.annotate(porcento(margem, 1), (rotulo, margem), textcoords="offset points",
                      xytext=(0, 14), ha="center", fontsize=16, fontweight="bold", color=AZUL_IDP)
    eixo.set_ylim(min(margens) * 0.8, max(margens) * 1.15)
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: porcento(v, 0)))
    eixo.set_title("Margem de lucro por ano", loc="left", fontsize=18, color="#242424", pad=12)
    estiliza(eixo)
    nota(figura, NOTA_ANOS)
    salva(figura, "pagina3_margem_lucro.png")


def pagina_receitas_componente(registros):
    figura = moldura(4, "Receitas por componente", "Qual foi o total de receitas por componente?")
    por_componente = soma([r for r in registros if r["Tipo"] == "Receitas"], "Componente")
    total = sum(por_componente.values())
    ordem = sorted(por_componente, key=por_componente.get)

    eixo = figura.add_axes([0.16, 0.10, 0.70, 0.64])
    valores = [por_componente[c] for c in ordem]
    barras = eixo.barh(ordem, valores, color=COR["Receitas"], height=0.62)
    for barra, valor in zip(barras, valores):
        eixo.text(valor + total * 0.006, barra.get_y() + barra.get_height() / 2,
                  f"{reais(valor, 0)}  ({porcento(valor / total, 1)})",
                  va="center", fontsize=15, color="#242424")
    eixo.set_xlim(0, max(valores) * 1.30)
    eixo.set_xticks([])
    eixo.spines["bottom"].set_visible(False)
    eixo.tick_params(axis="y", labelsize=17)
    estiliza(eixo, grade=None)
    eixo.set_title(f"Total de receitas: {reais(total)}", loc="left", fontsize=18,
                   color="#242424", pad=14)
    nota(figura, "Publicidade tem três meses com valor negativo em 2020 (mai, jul e ago); "
                 "os valores foram mantidos como vieram no dataset.")
    salva(figura, "pagina4_receitas_componente.png")


def pagina_despesas_media(registros):
    figura = moldura(5, "Despesas por componente x média",
                     "Qual foi o total de despesas por componente em relação à média de despesas?")
    por_componente = soma([r for r in registros if r["Tipo"] == "Despesas"], "Componente")
    media = sum(por_componente.values()) / len(por_componente)
    ordem = sorted(por_componente, key=por_componente.get, reverse=True)
    valores = [por_componente[c] for c in ordem]

    eixo = figura.add_axes([0.07, 0.12, 0.87, 0.60])
    cores = [COR["Despesas"] if v >= media else "#F2B39A" for v in valores]
    barras = eixo.bar(ordem, valores, color=cores, width=0.6)
    for barra, valor in zip(barras, valores):
        diferenca = valor - media
        sinal = "+" if diferenca >= 0 else "-"
        eixo.text(barra.get_x() + barra.get_width() / 2, valor,
                  f"{reais(valor, 0)}\n{sinal}{porcento(abs(diferenca) / media, 0)} vs. média",
                  ha="center", va="bottom", fontsize=13.5, color="#242424")
    eixo.axhline(media, color=AZUL_IDP, linewidth=2.5, linestyle="--")
    eixo.text(len(ordem) - 0.5, media, f"  Média: {reais(media)}", va="bottom", ha="right",
              fontsize=16, fontweight="bold", color=AZUL_IDP)
    eixo.set_ylim(0, max(valores) * 1.22)
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: reais(v, 0)))
    eixo.tick_params(axis="x", labelsize=16)
    estiliza(eixo)
    nota(figura, "Média = total de despesas dividido pelos seis componentes. "
                 "Barras escuras ficam acima da média; barras claras, abaixo.")
    salva(figura, "pagina5_despesas_media.png")


def pagina_matriz(registros):
    figura = moldura(6, "Receitas e despesas por componente e ano",
                     "Qual foi o total de receitas e despesas por componente e por ano, "
                     "com a hierarquia tipo / componente?")
    anos = sorted({r["Ano"] for r in registros})
    celulas = soma(registros, "Tipo", "Componente", "Ano")
    por_tipo_ano = soma(registros, "Tipo", "Ano")
    por_ano = soma(registros, "Ano")

    eixo = figura.add_axes([0.045, 0.07, 0.91, 0.70])
    eixo.set_xlim(0, 1)
    eixo.set_ylim(0, 1)
    eixo.axis("off")

    colunas = [0.0, 0.40, 0.55, 0.70, 0.85]
    cabecalho = ["Tipo / Componente"] + [str(a) for a in anos] + ["Total"]
    linhas = []
    for tipo in ("Receitas", "Despesas"):
        componentes = sorted({c for t, c, _ in celulas if t == tipo},
                             key=lambda c: -sum(celulas.get((tipo, c, a), 0) for a in anos))
        valores_tipo = [por_tipo_ano[(tipo, a)] for a in anos]
        linhas.append(("tipo", f"▾ {tipo}", valores_tipo + [sum(valores_tipo)], tipo))
        for componente in componentes:
            valores = [celulas.get((tipo, componente, a), 0) for a in anos]
            linhas.append(("componente", componente, valores + [sum(valores)], tipo))
    valores_total = [por_ano[a] for a in anos]
    linhas.append(("total", "Total", valores_total + [sum(valores_total)], None))

    altura = 1 / (len(linhas) + 1.3)
    y = 1 - altura
    eixo.add_patch(plt.Rectangle((0, y), 1, altura, facecolor=AZUL_IDP, edgecolor="none"))
    for x, rotulo in zip(colunas, cabecalho):
        alinhamento = "left" if x == 0 else "right"
        posicao = 0.01 if x == 0 else x + 0.135
        eixo.text(posicao, y + altura / 2, rotulo, ha=alinhamento, va="center",
                  fontsize=16, fontweight="bold", color="white")

    for indice, (nivel, rotulo, valores, tipo) in enumerate(linhas):
        y -= altura
        if nivel == "tipo":
            fundo, peso, recuo, cor_texto = "#EEF5FD" if tipo == "Receitas" else "#FDF1EC", "bold", 0.01, COR[tipo]
        elif nivel == "total":
            fundo, peso, recuo, cor_texto = "#E8E8E8", "bold", 0.01, "#242424"
        else:
            fundo, peso, recuo, cor_texto = ("white" if indice % 2 else "#FAFAFA"), "normal", 0.04, "#242424"
        eixo.add_patch(plt.Rectangle((0, y), 1, altura, facecolor=fundo, edgecolor="#E1E1E1", linewidth=0.6))
        eixo.text(recuo, y + altura / 2, rotulo, ha="left", va="center", fontsize=15,
                  fontweight=peso, color=cor_texto)
        for x, valor in zip(colunas[1:], valores):
            eixo.text(x + 0.135, y + altura / 2, reais(valor, 0), ha="right", va="center",
                      fontsize=15, fontweight=peso, color="#242424")
    nota(figura, NOTA_ANOS)
    salva(figura, "pagina6_matriz_tipo_componente_ano.png")


def pagina_segmentos(registros):
    figura = moldura(7, "Segmentos de maior e menor peso",
                     "Onde receitas e despesas são maiores e menores, para o plano estratégico?")
    blocos = {}
    for tipo in ("Receitas", "Despesas"):
        por_componente = soma([r for r in registros if r["Tipo"] == tipo], "Componente")
        blocos[tipo] = (por_componente, max(por_componente, key=por_componente.get),
                        min(por_componente, key=por_componente.get))

    cartoes = [
        ("Maior receita", blocos["Receitas"][1], blocos["Receitas"][0][blocos["Receitas"][1]], DESTAQUE_MAIOR),
        ("Menor receita", blocos["Receitas"][2], blocos["Receitas"][0][blocos["Receitas"][2]], DESTAQUE_MENOR),
        ("Maior despesa", blocos["Despesas"][1], blocos["Despesas"][0][blocos["Despesas"][1]], DESTAQUE_MAIOR),
        ("Menor despesa", blocos["Despesas"][2], blocos["Despesas"][0][blocos["Despesas"][2]], DESTAQUE_MENOR),
    ]
    largura = 0.205
    for indice, (rotulo, componente, valor, cor) in enumerate(cartoes):
        cartao(figura, [0.045 + indice * (largura + 0.023), 0.60, largura, 0.17],
               componente, f"{rotulo}: {reais(valor, 0)}", cor, tamanho=30)

    for indice, tipo in enumerate(("Receitas", "Despesas")):
        por_componente, maior, menor = blocos[tipo]
        ordem = sorted(por_componente, key=por_componente.get)
        valores = [por_componente[c] for c in ordem]
        cores = [DESTAQUE_MAIOR if c == maior else DESTAQUE_MENOR if c == menor else CINZA_CLARO
                 for c in ordem]
        eixo = figura.add_axes([0.11 + indice * 0.47, 0.08, 0.30, 0.45])
        barras = eixo.barh(ordem, valores, color=cores, height=0.62)
        total = sum(valores)
        for barra, valor in zip(barras, valores):
            eixo.text(valor + max(valores) * 0.02, barra.get_y() + barra.get_height() / 2,
                      f"{reais(valor, 0)} ({porcento(valor / total, 1)})", va="center",
                      fontsize=13, color="#242424")
        eixo.set_xlim(0, max(valores) * 1.55)
        eixo.set_xticks([])
        eixo.spines["bottom"].set_visible(False)
        eixo.tick_params(axis="y", labelsize=15)
        eixo.set_title(f"{tipo} por componente", loc="left", fontsize=18,
                       color=COR[tipo], fontweight="bold", pad=10)
        estiliza(eixo, grade=None)
    nota(figura, "Azul-escuro: maior componente do tipo. Vermelho: menor. "
                 "Marketing e Segurança ficam a apenas R$ 283 de distância entre si.")
    salva(figura, "pagina7_segmentos.png")


def main():
    if not DADOS.exists():
        raise SystemExit("rode antes scripts/11_trata_dados_datalab7.py")
    registros = carrega()
    print(f"{len(registros)} registros lidos")
    pagina_total(registros, 1, "Receitas", "Qual foi o total de receitas?", "pagina1_total_receitas.png")
    pagina_total(registros, 2, "Despesas", "Qual foi o total de despesas?", "pagina2_total_despesas.png")
    pagina_margem(registros)
    pagina_receitas_componente(registros)
    pagina_despesas_media(registros)
    pagina_matriz(registros)
    pagina_segmentos(registros)


if __name__ == "__main__":
    main()
