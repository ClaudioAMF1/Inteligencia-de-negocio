"""
DataLab 4-B1 - prepara a série histórica escolhida no World Bank Open Data.

Indicador: IT.NET.USER.ZS - "Individuals using the Internet (% of population)"
Fonte....: https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=BR

O script lê o pacote CSV baixado do portal (botão "Download" > "CSV" na página do
indicador) e recorta três séries: Brasil, América Latina e Caribe, e Mundo. O
arquivo do portal vem no formato largo, com quatro linhas de cabeçalho e uma
coluna por ano; aqui ele é convertido para o formato longo que os gráficos e o
Power BI consomem.

Uso:
    python3 scripts/04_prepara_serie_datalab4.py [caminho-do-csv-ou-zip]

Sem argumento, o script procura o pacote em datalab4/dados/.
"""
import csv
import io
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "datalab4" / "dados"
SAIDA = DADOS / "serie_internet.csv"

INDICADOR = "IT.NET.USER.ZS"
# Código da entidade no World Bank -> nome curto usado nos gráficos e no CSV final.
ENTIDADES = {
    "BRA": "Brasil",
    "LCN": "América Latina e Caribe",
    "WLD": "Mundo",
}


def localiza_pacote(argumento):
    if argumento:
        caminho = Path(argumento)
        if not caminho.exists():
            raise SystemExit(f"arquivo não encontrado: {caminho}")
        return caminho

    candidatos = sorted(
        [c for c in DADOS.glob(f"*{INDICADOR}*") if c.suffix.lower() in (".csv", ".zip")]
    )
    if not candidatos:
        raise SystemExit(
            f"nenhum pacote do indicador {INDICADOR} encontrado em {DADOS.relative_to(RAIZ)}.\n"
            "Baixe o CSV em https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=BR\n"
            "(botão Download > CSV) e salve o arquivo nessa pasta."
        )
    return candidatos[-1]


def linhas_do_pacote(caminho):
    """Devolve as linhas do CSV do indicador, esteja ele solto ou dentro do .zip."""
    if caminho.suffix.lower() == ".zip":
        with zipfile.ZipFile(caminho) as pacote:
            internos = [n for n in pacote.namelist()
                        if n.lower().endswith(".csv") and not n.startswith("Metadata")]
            if not internos:
                raise SystemExit(f"{caminho.name} não contém o CSV do indicador")
            bruto = pacote.read(internos[0])
    else:
        bruto = caminho.read_bytes()

    texto = bruto.decode("utf-8-sig")
    return list(csv.reader(io.StringIO(texto)))


def cabecalho_e_dados(linhas):
    """O CSV do portal traz linhas de aviso antes do cabeçalho real."""
    for indice, linha in enumerate(linhas):
        if linha and linha[0].strip('"') == "Country Name":
            return linha, linhas[indice + 1:]
    raise SystemExit("cabeçalho 'Country Name' não encontrado no CSV do World Bank")


def data_de_atualizacao(linhas):
    """Lê a linha 'Last Updated Date' que o portal grava no topo do arquivo."""
    for linha in linhas:
        if linha and linha[0].strip('"') == "Last Updated Date":
            return linha[1].strip()
    return ""


def main():
    pacote = localiza_pacote(sys.argv[1] if len(sys.argv) > 1 else None)
    linhas = linhas_do_pacote(pacote)
    cabecalho, corpo = cabecalho_e_dados(linhas)
    atualizado_em = data_de_atualizacao(linhas)

    anos = [(indice, int(valor)) for indice, valor in enumerate(cabecalho)
            if re.fullmatch(r"\d{4}", valor.strip())]
    coluna_codigo = cabecalho.index("Country Code")

    valores = {}
    for linha in corpo:
        if len(linha) <= coluna_codigo:
            continue
        codigo = linha[coluna_codigo].strip()
        if codigo not in ENTIDADES:
            continue
        for indice, ano in anos:
            bruto = linha[indice].strip() if indice < len(linha) else ""
            if bruto:
                valores.setdefault(ano, {})[ENTIDADES[codigo]] = round(float(bruto), 4)

    faltando = set(ENTIDADES.values()) - {nome for ano in valores.values() for nome in ano}
    if faltando:
        raise SystemExit("séries ausentes no pacote: " + ", ".join(sorted(faltando)))

    # As séries têm coberturas diferentes (o Brasil começa bem antes dos agregados),
    # então o arquivo guarda a união dos anos e deixa em branco o que o portal não publica.
    nomes = list(ENTIDADES.values())
    anos_publicados = sorted(valores)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["ano"] + nomes)
        for ano in anos_publicados:
            escritor.writerow([ano] + [valores[ano].get(nome, "") for nome in nomes])

    print(f"origem: {pacote.name} (dados atualizados em {atualizado_em})")
    print(f"{SAIDA.relative_to(RAIZ)} gerado: {anos_publicados[0]}-{anos_publicados[-1]}")
    for nome in nomes:
        cobertura = sorted(ano for ano in valores if nome in valores[ano])
        print(f"  {nome}: {len(cobertura)} anos ({cobertura[0]}-{cobertura[-1]})")


if __name__ == "__main__":
    main()
