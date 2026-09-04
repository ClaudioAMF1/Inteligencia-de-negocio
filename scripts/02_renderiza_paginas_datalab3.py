"""
DataLab 3-B1 - Inteligência de Negócio (IDP)

Reproduz, a partir da mesma base carregada no Power BI
(ine_dataset_correcoes_avaliacoes.xlsx), as quatro páginas do relatório
idp_ine_datalab3.pbix em imagens 1920x1080. As imagens são usadas como evidência
do trabalho no PDF de entrega.

Cada página respeita o layout, as agregações e as cores do tema Fluent 2 definidos
no próprio pacote .pbix.
"""
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import openpyxl

RAIZ = Path(__file__).resolve().parent.parent
PLANILHA = RAIZ / "datalab3" / "ine_dataset_correcoes_avaliacoes.xlsx"
PACOTE = RAIZ / "datalab3" / "idp_ine_datalab3.pbix"
SAIDA = RAIZ / "datalab3" / "imagens"
LOGO_NO_PACOTE = "Report/StaticResources/RegisteredResources/Logomarca_pequena_IDP4803064698123293.jpg"

ALUNO = "Claudio da Aparecida Meireles Filho (2321070)"
AZUL_IDP = "#09124f"
# Paleta Fluent 2, na ordem em que o tema do relatório a expõe.
CORES = ["#118DFF", "#12239E", "#E66C37", "#6B007B"]
COR_CARTAO = "#6B007B"   # ThemeDataColor ColorId 3, usada nos cartões
COR_MEDIA = "#148036"    # ThemeDataColor ColorId 9 (#1AAB40) escurecida em 25%
CINZA = "#616161"

# A tela do relatório é 1920x1080; trabalho em polegadas para casar com o Power BI.
DPI = 100
LARGURA, ALTURA = 19.20, 10.80


def carrega_dados():
    """Lê a aba 'dados' já com os valores calculados das fórmulas."""
    planilha = openpyxl.load_workbook(PLANILHA, data_only=True)
    aba = planilha["dados"]
    linhas = list(aba.iter_rows(values_only=True))
    cabecalho = list(linhas[0])
    registros = []
    for linha in linhas[1:]:
        registro = dict(zip(cabecalho, linha))
        if registro.get("id") is None:
            continue  # linhas em branco no fim da planilha
        registros.append(registro)
    return registros


def moldura(titulo):
    """Cria a página do relatório: fundo branco, título, identificação e logo."""
    figura = plt.figure(figsize=(LARGURA, ALTURA), dpi=DPI, facecolor="white")
    figura.text(0.44, 0.885, titulo, ha="center", va="center",
                fontsize=34, fontweight="bold", color=AZUL_IDP)
    figura.text(0.44, 0.815, ALUNO, ha="center", va="center",
                fontsize=15, fontweight="bold", color="#242424")

    with zipfile.ZipFile(PACOTE) as pacote, pacote.open(LOGO_NO_PACOTE) as arquivo:
        logo = mpimg.imread(arquivo, format="jpg")
    eixo_logo = figura.add_axes([0.824, 0.790, 0.0876, 0.129])
    eixo_logo.imshow(logo)
    eixo_logo.axis("off")
    return figura


def estiliza(eixo):
    """Aplica o acabamento de eixos usado pelos visuais do Power BI."""
    for lado in ("top", "right"):
        eixo.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        eixo.spines[lado].set_color("#E1E1E1")
    eixo.tick_params(colors=CINZA, labelsize=13)
    eixo.grid(axis="y", color="#EAEAEA", linewidth=1)
    eixo.set_axisbelow(True)


def salva(figura, nome):
    SAIDA.mkdir(parents=True, exist_ok=True)
    caminho = SAIDA / nome
    figura.savefig(caminho, dpi=DPI, facecolor="white")
    plt.close(figura)
    print(f"  {caminho.relative_to(RAIZ)}")


def pagina1(dados):
    """Análise 1: três cartões (id, nota_final, total_faltas)."""
    figura = moldura("Datalab3 - Indicadores de Desempenho Acadêmico")

    total_alunos = sum(1 for d in dados if d["id"] is not None)
    notas = [d["nota_final"] for d in dados if d["nota_final"] is not None]
    faltas = [d["total_faltas"] for d in dados if d["total_faltas"] is not None]

    cartoes = [
        (f"{total_alunos}", "id"),
        (f"{sum(notas) / len(notas):.2f}".replace(".", ","), "Média de nota_final"),
        (f"{sum(faltas) / len(faltas):.2f}".replace(".", ","), "Média de total_faltas"),
    ]
    for indice, (valor, rotulo) in enumerate(cartoes):
        esquerda = 0.114 + indice * 0.2425
        eixo = figura.add_axes([esquerda, 0.205, 0.212, 0.435])
        eixo.set_xticks([])
        eixo.set_yticks([])
        for lado in eixo.spines.values():
            lado.set_color("#E1E1E1")
        eixo.text(0.5, 0.58, valor, ha="center", va="center",
                  fontsize=54, fontweight="bold", color=COR_CARTAO)
        eixo.text(0.5, 0.24, rotulo, ha="center", va="center",
                  fontsize=18, color=CINZA)
    salva(figura, "analise1_indicadores.png")


def pagina2(dados):
    """Análise 2: dispersão total_faltas (X) x nota_final (Y)."""
    figura = moldura("Datalab3 - Análise de Correlação: Nota Final x Faltas")
    eixo = figura.add_axes([0.09, 0.09, 0.83, 0.66])

    pares = [(d["total_faltas"], d["nota_final"]) for d in dados
             if d["total_faltas"] is not None and d["nota_final"] is not None]
    eixo.scatter([x for x, _ in pares], [y for _, y in pares],
                 s=70, color=CORES[0], alpha=0.75, edgecolors="white", linewidths=0.6)

    eixo.set_xlabel("Quantidade de Faltas", fontsize=22, color=CINZA, labelpad=12)
    eixo.set_ylabel("Nota Final", fontsize=22, color=CINZA, labelpad=12)
    eixo.set_title("Quantidade de Faltas e Nota Final", fontsize=20,
                   color="#242424", loc="left", pad=14)
    estiliza(eixo)
    eixo.grid(axis="x", color="#EAEAEA", linewidth=1)
    salva(figura, "analise2_correlacao.png")


def pagina3(dados):
    """Análise 3: colunas clusterizadas nr_matricula x nota_final, com linha de média."""
    figura = moldura("Datalab3 - Distribuição das Notas")
    eixo = figura.add_axes([0.075, 0.155, 0.855, 0.595])

    # O visual agrega por matrícula usando Máximo de nota_final e ordena decrescente.
    por_matricula = {}
    for d in dados:
        if d["nr_matricula"] is None or d["nota_final"] is None:
            continue
        chave = str(int(d["nr_matricula"]))
        por_matricula[chave] = max(por_matricula.get(chave, 0), d["nota_final"])
    serie = sorted(por_matricula.items(), key=lambda item: item[1], reverse=True)
    valores = [v for _, v in serie]

    eixo.bar(range(len(serie)), valores, color=CORES[0], width=0.8)
    media = sum(valores) / len(valores)
    eixo.axhline(media, color=COR_MEDIA, linewidth=3, alpha=0.75)
    eixo.text(len(serie) * 0.995, media + 0.18,
              f"Linha média 1  {media:.2f}".replace(".", ","),
              ha="right", fontsize=16, color=COR_MEDIA, fontweight="bold")

    eixo.set_xlim(-1, len(serie))
    eixo.set_xticks(range(len(serie)))
    eixo.set_xticklabels([m for m, _ in serie], rotation=90, fontsize=9)
    eixo.set_xlabel(f"nr_matricula ({len(serie)} matrículas, ordenadas por nota_final)",
                    fontsize=17, color=CINZA, labelpad=10)
    eixo.set_ylabel("Máximo de nota_final", fontsize=17, color=CINZA, labelpad=10)
    estiliza(eixo)
    salva(figura, "analise3_distribuicao.png")


def pagina4(dados):
    """Análise 4: gráfico de área com nota_prova_p1, p2 e p3 por matrícula."""
    figura = moldura("Datalab3 - Evolução das Notas P1 e P2")
    eixo = figura.add_axes([0.075, 0.155, 0.855, 0.595])

    # O visual ordena as matrículas pela Média de nota_prova_p1, em ordem decrescente.
    por_matricula = {}
    for d in dados:
        if d["nr_matricula"] is None:
            continue
        chave = str(int(d["nr_matricula"]))
        acumulado = por_matricula.setdefault(chave, {"p1": [], "p2": [], "p3": []})
        for origem, destino in (("nota_prova_p1", "p1"), ("nota_prova_p2", "p2"), ("nota_prova_p3", "p3")):
            if d[origem] is not None:
                acumulado[destino].append(d[origem])

    def media(lista):
        return sum(lista) / len(lista) if lista else 0.0

    serie = sorted(por_matricula.items(), key=lambda item: media(item[1]["p1"]), reverse=True)
    eixo_x = range(len(serie))
    rotulos = [
        ("Média de nota_prova_p1", "p1"),
        ("Média de nota_prova_p2", "p2"),
        ("Média de nota_prova_p3", "p3"),
    ]
    for indice, (rotulo, chave) in enumerate(rotulos):
        valores = [media(dados_matricula[chave]) for _, dados_matricula in serie]
        eixo.fill_between(eixo_x, valores, color=CORES[indice], alpha=0.45)
        eixo.plot(eixo_x, valores, color=CORES[indice], linewidth=1.8, label=rotulo)

    eixo.set_xlim(0, len(serie) - 1)
    eixo.set_ylim(bottom=0)
    eixo.set_xticks(range(len(serie)))
    eixo.set_xticklabels([m for m, _ in serie], rotation=90, fontsize=9)
    eixo.set_xlabel(f"nr_matricula ({len(serie)} matrículas, ordenadas por nota_prova_p1)",
                    fontsize=17, color=CINZA, labelpad=10)
    eixo.set_ylabel("Nota das provas", fontsize=17, color=CINZA, labelpad=10)
    eixo.legend(loc="upper right", frameon=False, fontsize=15, labelcolor=CINZA)
    estiliza(eixo)
    salva(figura, "analise4_evolucao.png")


def main():
    dados = carrega_dados()
    print(f"{len(dados)} registros lidos de {PLANILHA.name}")
    pagina1(dados)
    pagina2(dados)
    pagina3(dados)
    pagina4(dados)


if __name__ == "__main__":
    main()
