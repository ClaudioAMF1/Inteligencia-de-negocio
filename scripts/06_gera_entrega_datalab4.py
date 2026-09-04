"""
DataLab 4-B1 - gera a entrega em .docx e .pdf a partir do template do aluno.

Todos os números citados na explicação do movimento da série são calculados aqui
a partir de datalab4/dados/serie_internet.csv, que por sua vez vem do pacote CSV
oficial do World Bank Open Data. Nada é digitado à mão.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrega import RAIZ, gerar

SERIE = RAIZ / "datalab4" / "dados" / "serie_internet.csv"
IMAGENS = RAIZ / "datalab4" / "imagens"
SAIDA = RAIZ / "datalab4" / "entrega"

FONTE_URL = "https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=BR"
INDICADOR = "IT.NET.USER.ZS - Individuals using the Internet (% of population)"

PRINTS = [
    ("Gráfico 1 - Evolução da série no Brasil: % da população usando a Internet.",
     IMAGENS / "grafico1_evolucao_brasil.png"),
    ("Gráfico 2 - Variação anual da série, em pontos percentuais.",
     IMAGENS / "grafico2_variacao_anual.png"),
    ("Gráfico 3 - Brasil comparado à América Latina e Caribe e ao Mundo.",
     IMAGENS / "grafico3_comparativo.png"),
]


def numero(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


def carrega():
    series = {}
    with SERIE.open(encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for nome in leitor.fieldnames[1:]:
            series[nome] = {}
        arquivo.seek(0)
        for linha in csv.DictReader(arquivo):
            for nome in series:
                if linha[nome]:
                    series[nome][int(linha["ano"])] = float(linha[nome])
    return series


def indicadores(series):
    """Extrai da série os números que sustentam a explicação do movimento."""
    brasil = series["Brasil"]
    anos = sorted(brasil)
    variacao = {ano: brasil[ano] - brasil[ano - 1] for ano in anos[1:]}

    def media(inicio, fim):
        janela = [v for ano, v in variacao.items() if inicio <= ano <= fim]
        return sum(janela) / len(janela)

    maior_ano = max(variacao, key=variacao.get)
    quedas = sorted(ano for ano, v in variacao.items() if v < 0)
    comuns = sorted(set(brasil) & set(series["Mundo"]) & set(series["América Latina e Caribe"]))

    return {
        "primeiro": anos[0], "ultimo": anos[-1],
        "valor_ultimo": brasil[anos[-1]],
        "ano_10": next(a for a in anos if brasil[a] >= 10),
        "ano_50": next(a for a in anos if brasil[a] >= 50),
        "ano_80": next(a for a in anos if brasil[a] >= 80),
        "media_90": media(1991, 1999), "media_00": media(2000, 2009),
        "media_10": media(2010, 2019), "media_20": media(2020, anos[-1]),
        "maior_ano": maior_ano, "maior_valor": variacao[maior_ano],
        "quedas": quedas,
        "queda_total": sum(variacao[a] for a in quedas),
        "fora": 100 - brasil[anos[-1]],
        "comum_inicio": comuns[0], "comum_fim": comuns[-1],
        "mundo_fim": series["Mundo"][comuns[-1]],
        "lcn_fim": series["América Latina e Caribe"][comuns[-1]],
        "dif_mundo_inicio": brasil[comuns[0]] - series["Mundo"][comuns[0]],
        "dif_mundo_fim": brasil[comuns[-1]] - series["Mundo"][comuns[-1]],
        "dif_lcn_fim": brasil[comuns[-1]] - series["América Latina e Caribe"][comuns[-1]],
    }


def textos(d):
    introducao = (
        f"A série escolhida é \"{INDICADOR}\", do World Bank Open Data, recortada para o "
        f"Brasil entre {d['primeiro']} e {d['ultimo']}. O indicador mede o percentual da "
        "população que usou a Internet, de qualquer local, nos últimos três meses; a fonte "
        "primária é a base de telecomunicações da União Internacional de Telecomunicações "
        f"(ITU). Fonte dos dados: {FONTE_URL}. A mesma base traz os agregados de América "
        "Latina e Caribe e do Mundo, usados no terceiro gráfico como referência de "
        "comparação."
    )

    objetivo = [
        "Aplicar no DataLab 4 o que foi explorado no DataLab 3, trocando a base acadêmica por "
        "uma série histórica pública: escolher um indicador, entender como ele é medido, "
        "construir gráficos que revelem o movimento da série e explicar o que esse movimento "
        "significa.",
        f"A pergunta que o trabalho responde é: em que ritmo a população brasileira entrou na "
        f"Internet, e onde esse ritmo mudou? Em {d['primeiro']} o indicador era praticamente "
        f"zero; em {d['ultimo']} chega a {numero(d['valor_ultimo'])}% da população.",
        f"Link da fonte de dados: {FONTE_URL}",
    ]

    tecnicas = [
        "Obtenção dos dados: download do pacote CSV do indicador na página do World Bank Open "
        "Data. O arquivo vem no formato largo (uma linha por país e uma coluna por ano) e com "
        "quatro linhas de cabeçalho antes dos dados.",
        "Tratamento: recorte das entidades Brasil (BRA), América Latina e Caribe (LCN) e Mundo "
        "(WLD), transposição das colunas de ano para o formato longo (ano, entidade, valor) e "
        "descarte dos anos sem publicação. No Power BI o mesmo tratamento é feito no Power "
        "Query com Unpivot de Colunas; o arquivo datalab4/powerbi/serie_worldbank.m traz a "
        "consulta que baixa a série direto da API do World Bank.",
        "Cálculo: além do valor absoluto do indicador, foi calculada a variação anual em "
        "pontos percentuais (valor do ano menos valor do ano anterior), que é a medida que "
        "mostra aceleração e desaceleração de uma série de estoque como esta.",
        "Visualizações: gráfico de linha com área para a evolução da série, gráfico de colunas "
        "para a variação anual e gráfico de linhas múltiplas para o comparativo com os "
        "agregados regional e mundial. Os três trazem título, unidade, citação da fonte e a "
        "logomarca da instituição.",
    ]

    aprendizado = [
        f"O movimento da série é uma curva em S clássica de difusão de tecnologia. Na década "
        f"de 1990 o indicador anda de lado: o avanço médio é de apenas "
        f"{numero(d['media_90'], 2)} ponto percentual por ano, e o Brasil só passa de 10% da "
        f"população em {d['ano_10']}.",
        f"A fase de decolagem vai dos anos 2000 até o fim da década de 2010, sustentada pela "
        f"banda larga e depois pela Internet móvel: o avanço médio sobe para "
        f"{numero(d['media_00'], 2)} p.p. por ano nos anos 2000 e {numero(d['media_10'], 2)} "
        f"p.p. por ano na década de 2010. É nesse período que a série cruza a marca da metade "
        f"da população, em {d['ano_50']}.",
        f"O maior salto isolado de toda a série acontece em {d['maior_ano']}, com "
        f"+{numero(d['maior_valor'])} p.p. em um único ano - o ano da pandemia de COVID-19, em "
        f"que trabalho, aula e serviço público migraram para o ambiente digital. Foi também "
        f"quando o indicador ultrapassou os 80% ({d['ano_80']}).",
        f"Depois do salto a curva achata. Em {' e '.join(str(a) for a in d['quedas'])} a série "
        f"registra pequenos recuos, somando {numero(abs(d['queda_total']), 2)} p.p.; recuos "
        "dessa magnitude em um indicador de estoque costumam refletir revisão metodológica e "
        "mudança na base amostral da pesquisa domiciliar, e não perda real de usuários. Em "
        "seguida o crescimento retorna, mas em ritmo bem menor: a média do período mais "
        f"recente é de {numero(d['media_20'], 2)} p.p. por ano. É o comportamento esperado de "
        "uma curva de saturação - quanto mais perto do teto, mais caro fica conectar cada "
        "ponto percentual seguinte.",
        f"O comparativo dá a dimensão do resultado: em {d['comum_fim']} o Brasil está em "
        f"{numero(d['valor_ultimo'])}%, contra {numero(d['lcn_fim'])}% da América Latina e "
        f"Caribe e {numero(d['mundo_fim'])}% do Mundo. A distância do Brasil para a média "
        f"mundial cresceu de {numero(d['dif_mundo_inicio'])} p.p. em {d['comum_inicio']} para "
        f"{numero(d['dif_mundo_fim'])} p.p. em {d['comum_fim']}, enquanto a diferença para a "
        f"própria região é hoje de apenas {numero(d['dif_lcn_fim'])} p.p.",
        f"O que sobra como leitura de negócio: os {numero(d['fora'])}% da população que ainda "
        f"estão fora em {d['ultimo']} são o grupo mais difícil de alcançar, e o gráfico de "
        "variação anual mostra que o ritmo atual não os conecta no curto prazo. Aprendi também "
        "que, numa série de estoque, o gráfico do nível conta metade da história - foi o "
        "gráfico da variação anual que localizou exatamente onde o movimento mudou.",
    ]
    return introducao, objetivo, tecnicas, aprendizado


def main():
    if not SERIE.exists():
        raise SystemExit("rode antes o script 04 para gerar datalab4/dados/serie_internet.csv")
    faltando = [str(caminho) for _, caminho in PRINTS if not Path(caminho).exists()]
    if faltando:
        raise SystemExit("rode antes o script 05; imagens ausentes: " + ", ".join(faltando))

    introducao, objetivo, tecnicas, aprendizado = textos(indicadores(carrega()))
    SAIDA.mkdir(parents=True, exist_ok=True)
    base = "IDP.INE - Atividade Avaliativa 4-B1 - Claudio da Aparecida Meireles Filho"
    gerar(
        destino_docx=SAIDA / f"{base}.docx",
        destino_pdf=SAIDA / f"{base}.pdf",
        tipo_atividade="DataLab 4-B1 - Série histórica do World Bank Open Data",
        introducao=introducao,
        prints=PRINTS,
        objetivo=objetivo,
        tecnicas=tecnicas,
        aprendizado=aprendizado,
    )


if __name__ == "__main__":
    main()
