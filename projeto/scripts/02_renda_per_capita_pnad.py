"""
Projeto aplicado - renda domiciliar per capita do Distrito Federal e de Goiás.

Indicador: rendimento domiciliar per capita nominal, o mesmo que o IBGE publica
todo ano por estado (base do rateio do FPE). Definição do IBGE: razão entre o
total dos rendimentos domiciliares e o total dos moradores.

Por que calcular em vez de baixar pronto: o portal do IBGE (SIDRA e Agência de
Notícias) recusa acesso automatizado. Os microdados da PNAD Contínua, porém,
ficam no servidor de arquivos do IBGE, que é acessível. A partir deles:

    renda per capita = soma(peso x VD5002) / soma(peso)

sobre os moradores, excluídos pensionistas, empregados domésticos e seus
parentes (V2005 = 17, 18, 19), que o IBGE não conta como moradores para esse fim.
VD5002 é o rendimento efetivo domiciliar per capita; o peso é V1032.

Validação: o cálculo de 2025 reproduz exatamente o valor oficial publicado pelo
IBGE em fev/2026 (DF R$ 4.538 e GO R$ 2.407). O script confere isso antes de
gravar e para se não bater.

Todos os anos usam os pesos atuais dos microdados (recalibrados pelo Censo 2022
em 2025). Por isso os anos antigos diferem alguns por cento dos valores que o
IBGE publicou na época, com os pesos de então; essa diferença fica registrada
no CSV, ao lado do valor oficial de cada ano.

Visitas: o IBGE usa a 1ª visita da PNAD; em 2020 e 2021, por causa da pandemia,
usou a 5ª.
"""
import csv
import io
import json
import os
import re
import ssl
import tempfile
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "projeto" / "dados"
SAIDA = DADOS / "renda_per_capita_df_go.csv"
CACHE = DADOS / "renda_microdados_cache.json"
VISITAS = ("https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
           "Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/")

UFS = {"53": "DF", "52": "GO"}
EXCLUIDOS = {"17", "18", "19"}
VARIAVEL = "VD5002"
ANOS = list(range(2016, 2026))

# Valores oficiais publicados pelo IBGE (R$ nominais). 2016-2021: PDFs do servidor de
# arquivos do IBGE; 2025: release de fev/2026, com os mesmos pesos dos microdados atuais.
OFICIAIS = {
    2016: {"DF": 2351, "GO": 1140}, 2017: {"DF": 2548, "GO": 1277},
    2018: {"DF": 2460, "GO": 1323}, 2019: {"DF": 2686, "GO": 1306},
    2020: {"DF": 2475, "GO": 1258}, 2021: {"DF": 2513, "GO": 1276},
    2025: {"DF": 4538, "GO": 2407},
}
ANO_VALIDACAO = 2025


def visita(ano):
    return 5 if ano in (2020, 2021) else 1


def ctx():
    pacote = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
    return ssl.create_default_context(cafile=pacote) if Path(pacote).exists() else None


def baixa(url, destino=None):
    with urllib.request.urlopen(url, context=ctx(), timeout=300) as resposta:
        if destino is None:
            return resposta.read()
        while bloco := resposta.read(1 << 20):
            destino.write(bloco)


def arquivos_do_ano(ano):
    v = visita(ano)
    base = f"{VISITAS}Visita_{v}/"
    dados = baixa(base + "Dados/").decode("utf-8", "replace")
    docs = baixa(base + "Documentacao/").decode("utf-8", "replace")
    zip_ano = re.search(rf'href="(PNADC_{ano}_visita{v}(?:_\d+)?\.zip)"', dados).group(1)
    entrada = re.search(rf'href="(input_PNADC_{ano}_visita{v}(?:_\d+)?\.txt)"', docs).group(1)
    return base + "Dados/" + zip_ano, base + "Documentacao/" + entrada


def posicoes(url_input):
    texto = baixa(url_input).decode("latin-1")
    return {m.group(2): (int(m.group(1)) - 1, int(m.group(3)))
            for m in re.finditer(r"@0*(\d+)\s+(\w+)\s+\$?(\d+)\.", texto)}


def calcula(ano):
    """Renda per capita (VD5002) ponderada para DF e GO em um ano."""
    url_zip, url_input = arquivos_do_ano(ano)
    pos = posicoes(url_input)
    campo = lambda linha, nome: linha[pos[nome][0]:pos[nome][0] + pos[nome][1]].strip()
    soma = {uf: 0.0 for uf in UFS.values()}
    peso_total = {uf: 0.0 for uf in UFS.values()}
    with tempfile.TemporaryFile() as pacote:
        baixa(url_zip, pacote)
        pacote.seek(0)
        with zipfile.ZipFile(pacote) as arquivo:
            interno = next(n for n in arquivo.namelist() if n.lower().endswith(".txt"))
            with arquivo.open(interno) as fluxo:
                for linha in io.TextIOWrapper(fluxo, encoding="latin-1"):
                    uf = UFS.get(campo(linha, "UF"))
                    if uf is None or campo(linha, "V2005") in EXCLUIDOS:
                        continue
                    valor = campo(linha, VARIAVEL)
                    if valor in ("", "."):
                        continue
                    peso = float(campo(linha, "V1032"))
                    soma[uf] += peso * float(valor)
                    peso_total[uf] += peso
    return {uf: round(soma[uf] / peso_total[uf], 2) for uf in UFS.values()}


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    for ano in [ANO_VALIDACAO] + [a for a in ANOS if a != ANO_VALIDACAO]:
        if str(ano) not in cache:
            cache[str(ano)] = calcula(ano)
            CACHE.write_text(json.dumps(cache, indent=1), encoding="utf-8")
        print(f"{ano}: DF R$ {cache[str(ano)]['DF']:.2f} | GO R$ {cache[str(ano)]['GO']:.2f}", flush=True)
        if ano == ANO_VALIDACAO:
            diferenca = max(abs(round(cache[str(ano)][uf]) - OFICIAIS[ano][uf]) for uf in UFS.values())
            print(f"  validação contra o oficial de {ano}: diferença máxima R$ {diferenca}", flush=True)
            if diferenca > 2:
                raise SystemExit("o cálculo não reproduz o valor oficial; nada foi gravado")

    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ano", "uf", "renda_per_capita", "renda_oficial_publicada", "visita_pnad"])
        for ano in ANOS:
            for uf in UFS.values():
                oficial = OFICIAIS.get(ano, {}).get(uf, "")
                w.writerow([ano, uf, round(cache[str(ano)][uf]), oficial, visita(ano)])
    print(f"gravado: {SAIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
