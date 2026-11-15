"""
Projeto aplicado - consolida as bases e calcula os indicadores das seis perguntas.

Entradas (geradas pelos scripts 01 e 02 e pela API do Banco Central):
  projeto/dados/anp/ca-*.csv              coletas da ANP em Brasília e Goiânia
  projeto/dados/renda_per_capita_df_go.csv renda domiciliar per capita (IBGE)
  projeto/dados/ipca_mensal.csv            IPCA mensal (BCB/SGS 433)

Saídas:
  projeto/dados/painel_mensal.csv  preço médio, mínimo e máximo por cidade, produto e mês
  projeto/dados/indicadores.json   números que respondem às seis perguntas
"""
import csv
import json
import os
import ssl
import statistics as st
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DADOS = RAIZ / "projeto" / "dados"
IPCA = DADOS / "ipca_mensal.csv"
URL_IPCA = ("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
            "?formato=json&dataInicial=01/01/2015&dataFinal=31/12/2026")

CIDADE = {"DF": "Brasília", "GO": "Goiânia"}
UF_DA_CIDADE = {"Brasília": "DF", "Goiânia": "GO"}
PRODUTOS = {"GASOLINA": "Gasolina", "GASOLINA COMUM": "Gasolina",
            "ETANOL": "Etanol", "ETANOL HIDRATADO": "Etanol",
            "DIESEL S10": "Diesel S10", "OLEO DIESEL S10": "Diesel S10"}
LITROS_MES = 100      # consumo de referência: ~1.000 km com 10 km/l
TANQUE = 50           # litros de um tanque cheio de carro de passeio
PARIDADE = 0.70       # etanol compensa quando custa menos de 70% da gasolina
MIN_COLETAS_BANDEIRA = 30
MIN_POSTOS_BANDEIRA = 3


def bandeira(nome):
    """Agrupa as várias razões sociais de uma mesma distribuidora."""
    n = nome.upper()
    if "PETROBRAS" in n or "VIBRA" in n or n == "BR":
        return "BR (Vibra)"
    if "RAIZEN" in n or "RAÍZEN" in n or "SHELL" in n:
        return "Shell (Raízen)"
    if "IPIRANGA" in n or n == "CBPI":
        return "Ipiranga"
    if "BRANCA" in n:
        return "Bandeira branca"
    return "Outras bandeiras"


def numero(texto):
    return float(texto.replace(".", "").replace(",", ".")) if "," in texto else float(texto)


def carrega_coletas():
    coletas = []
    for arquivo in sorted((DADOS / "anp").glob("ca-*.csv")):
        with arquivo.open(encoding="utf-8") as f:
            for l in csv.DictReader(f):
                produto = PRODUTOS.get(l["Produto"].strip().upper())
                if not produto or not l["Valor de Venda"]:
                    continue
                dia = datetime.strptime(l["Data"], "%d/%m/%Y").date()
                ano_iso, semana_iso, _ = dia.isocalendar()
                coletas.append({
                    "cidade": CIDADE[l["Estado"]], "produto": produto, "data": dia,
                    "mes": dia.strftime("%Y-%m"), "ano": dia.year,
                    "semana": f"{ano_iso}-S{semana_iso:02d}",
                    "preco": numero(l["Valor de Venda"]), "cnpj": l["CNPJ"].strip(),
                    "bandeira": bandeira(l["Bandeira"]),
                })
    return coletas


def carrega_ipca():
    """Índice acumulado do IPCA (base: primeiro mês da série = 1)."""
    if not IPCA.exists():
        pacote = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
        contexto = ssl.create_default_context(cafile=pacote) if Path(pacote).exists() else None
        with urllib.request.urlopen(URL_IPCA, context=contexto, timeout=60) as r:
            serie = json.load(r)
        with IPCA.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["mes", "variacao_pct"])
            for item in serie:
                d = datetime.strptime(item["data"], "%d/%m/%Y")
                w.writerow([d.strftime("%Y-%m"), item["valor"]])
    indice, acumulado = {}, 1.0
    with IPCA.open(encoding="utf-8") as f:
        for l in csv.DictReader(f):
            acumulado *= 1 + float(l["variacao_pct"]) / 100
            indice[l["mes"]] = acumulado
    return indice


def carrega_renda():
    renda = {}
    with (DADOS / "renda_per_capita_df_go.csv").open(encoding="utf-8") as f:
        for l in csv.DictReader(f):
            renda[(int(l["ano"]), l["uf"])] = float(l["renda_per_capita"])
    return renda


def agrupa(coletas, *chaves):
    grupos = defaultdict(list)
    for c in coletas:
        grupos[tuple(c[k] for k in chaves)].append(c["preco"])
    return grupos


def main():
    coletas = carrega_coletas()
    ipca = carrega_ipca()
    renda = carrega_renda()
    ultimo_mes = max(c["mes"] for c in coletas)
    base_real = ultimo_mes if ultimo_mes in ipca else max(ipca)
    print(f"{len(coletas)} coletas válidas | {min(c['mes'] for c in coletas)} a {ultimo_mes}")

    # ---------------------------------------------------------------- painel mensal
    mensal = agrupa(coletas, "cidade", "produto", "mes")
    painel = []
    for (cidade, produto, mes), precos in sorted(mensal.items()):
        media = st.mean(precos)
        fator = ipca[base_real] / ipca[mes] if mes in ipca else None
        painel.append({"cidade": cidade, "produto": produto, "mes": mes,
                       "media": round(media, 4), "minimo": min(precos), "maximo": max(precos),
                       "coletas": len(precos),
                       "media_real": round(media * fator, 4) if fator else ""})
    with (DADOS / "painel_mensal.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(painel[0]))
        w.writeheader()
        w.writerows(painel)
    media_mes = {(p["cidade"], p["produto"], p["mes"]): p["media"] for p in painel}

    meses_com_coleta = {c["mes"] for c in coletas}
    primeiro_mes = min(meses_com_coleta)
    calendario, (a, m) = [], (int(primeiro_mes[:4]), int(primeiro_mes[5:]))
    while f"{a}-{m:02d}" <= ultimo_mes:
        calendario.append(f"{a}-{m:02d}")
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    ind = {"periodo": {"inicio": primeiro_mes, "fim": ultimo_mes,
                       "coletas": len(coletas), "postos": len({c["cnpj"] for c in coletas}),
                       "meses_sem_coleta": [m for m in calendario if m not in meses_com_coleta],
                       "base_real": base_real}}

    # ------------------------------------------------- P1: Brasília x Goiânia, mín/méd/máx
    ultimos12 = sorted({c["mes"] for c in coletas})[-12:]
    recente = [c for c in coletas if c["mes"] in ultimos12]
    p1 = {"meses": [ultimos12[0], ultimos12[-1]], "produtos": {}}
    for produto in ("Etanol", "Gasolina"):
        linha = {}
        for cidade in ("Brasília", "Goiânia"):
            semanal = agrupa([c for c in recente if c["cidade"] == cidade and c["produto"] == produto],
                             "semana")
            linha[cidade] = {"minimo": round(st.mean(min(v) for v in semanal.values()), 3),
                             "media": round(st.mean(st.mean(v) for v in semanal.values()), 3),
                             "maximo": round(st.mean(max(v) for v in semanal.values()), 3)}
        linha["diferenca_media"] = round(linha["Brasília"]["media"] - linha["Goiânia"]["media"], 3)
        p1["produtos"][produto] = linha
    p1["serie_anual"] = {}
    for produto in ("Etanol", "Gasolina"):
        for cidade in ("Brasília", "Goiânia"):
            anual = agrupa([c for c in coletas if c["cidade"] == cidade and c["produto"] == produto], "ano")
            p1["serie_anual"][f"{cidade}|{produto}"] = {a: round(st.mean(v), 3) for (a,), v in sorted(anual.items())}
    ind["p1"] = p1

    # ------------------------------------------------- P2: peso do combustível na renda
    p2 = {"litros_mes": LITROS_MES, "anos": {}}
    for cidade, uf in UF_DA_CIDADE.items():
        anual = p1["serie_anual"][f"{cidade}|Gasolina"]
        for ano, preco in anual.items():
            if (ano, uf) in renda:
                gasto = preco * LITROS_MES
                p2["anos"].setdefault(str(ano), {})[cidade] = {
                    "preco_medio": preco, "gasto_mensal": round(gasto, 2),
                    "renda_per_capita": renda[(ano, uf)],
                    "percentual": round(gasto / renda[(ano, uf)], 4)}
    ind["p2"] = p2

    # ------------------------------------------------- P3: dispersão dentro da cidade
    p3 = {"meses": [ultimos12[0], ultimos12[-1]], "tanque_litros": TANQUE, "cidades": {}}
    for cidade in ("Brasília", "Goiânia"):
        semanal = agrupa([c for c in recente if c["cidade"] == cidade and c["produto"] == "Gasolina"],
                         "semana")
        spreads = [max(v) - min(v) for v in semanal.values() if len(v) >= 5]
        p3["cidades"][cidade] = {
            "spread_medio": round(st.mean(spreads), 3),
            "spread_maximo": round(max(spreads), 3),
            "economia_tanque": round(st.mean(spreads) * TANQUE, 2),
            "semanas": len(spreads),
            "postos_por_semana": round(st.mean(len(v) for v in semanal.values()), 1)}
        historico = agrupa([c for c in coletas if c["cidade"] == cidade and c["produto"] == "Gasolina"],
                           "ano", "semana")
        por_ano = defaultdict(list)
        for (ano, _), v in historico.items():
            if len(v) >= 5:
                por_ano[ano].append(max(v) - min(v))
        p3["cidades"][cidade]["por_ano"] = {a: round(st.mean(v), 3) for a, v in sorted(por_ano.items())}
    ind["p3"] = p3

    # ------------------------------------------------- P4: paridade etanol / gasolina
    p4 = {"limite": PARIDADE, "cidades": {}}
    for cidade in ("Brasília", "Goiânia"):
        meses = sorted(m for (c, p, m) in media_mes if c == cidade and p == "Etanol"
                       and (cidade, "Gasolina", m) in media_mes)
        razoes = {m: round(media_mes[(cidade, "Etanol", m)] / media_mes[(cidade, "Gasolina", m)], 4)
                  for m in meses}
        compensou = [m for m, r in razoes.items() if r < PARIDADE]
        p4["cidades"][cidade] = {"razao_mensal": razoes, "meses_compensou": compensou,
                                 "total_meses": len(razoes),
                                 "razao_media": round(st.mean(razoes.values()), 4),
                                 "razao_ultimo_mes": razoes[meses[-1]]}
    ind["p4"] = p4

    # ------------------------------------------------- P5: bandeira x bandeira branca
    p5 = {"meses": [ultimos12[0], ultimos12[-1]], "cidades": {}}
    for cidade in ("Brasília", "Goiânia"):
        do_ano = [c for c in recente if c["cidade"] == cidade and c["produto"] == "Gasolina"]
        semanal_media = {s: st.mean(v) for (s,), v in agrupa(do_ano, "semana").items()}
        # Diferença para a média da semana, para não confundir bandeira com o momento da coleta.
        desvios, postos = defaultdict(list), defaultdict(set)
        for c in do_ano:
            desvios[c["bandeira"]].append(c["preco"] - semanal_media[c["semana"]])
            postos[c["bandeira"]].add(c["cnpj"])
        # A pergunta compara as três grandes distribuidoras com a bandeira branca; o grupo
        # "Outras bandeiras" junta marcas pequenas (poucos postos) e fica fora da comparação.
        # Um grupo só entra com coletas e postos suficientes para não retratar um posto isolado.
        p5["cidades"][cidade] = {b: {"desvio_medio": round(st.mean(v), 3), "coletas": len(v),
                                     "postos": len(postos[b]),
                                     "preco_medio": round(st.mean(c["preco"] for c in do_ano if c["bandeira"] == b), 3)}
                                 for b, v in sorted(desvios.items()) if b != "Outras bandeiras"
                                 and len(v) >= MIN_COLETAS_BANDEIRA and len(postos[b]) >= MIN_POSTOS_BANDEIRA}
    ind["p5"] = p5

    # ------------------------------------------------- P6: preço real (deflacionado pelo IPCA)
    p6 = {"base_real": base_real, "cidades": {}}
    for cidade in ("Brasília", "Goiânia"):
        serie = [p for p in painel if p["cidade"] == cidade and p["produto"] == "Gasolina" and p["media_real"] != ""]
        anual_nom, anual_real = defaultdict(list), defaultdict(list)
        for p in serie:
            anual_nom[int(p["mes"][:4])].append(p["media"])
            anual_real[int(p["mes"][:4])].append(p["media_real"])
        anos = sorted(anual_nom)
        primeiro, ultimo = anos[0], anos[-1]
        nom = {a: round(st.mean(v), 3) for a, v in anual_nom.items()}
        real = {a: round(st.mean(v), 3) for a, v in anual_real.items()}
        p6["cidades"][cidade] = {"nominal": nom, "real": real,
                                 "variacao_nominal": round(nom[ultimo] / nom[primeiro] - 1, 4),
                                 "variacao_real": round(real[ultimo] / real[primeiro] - 1, 4),
                                 "anos": [primeiro, ultimo]}
    ipca_periodo = ipca[base_real] / ipca[f"{ind['periodo']['inicio']}"]
    p6["ipca_acumulado"] = round(ipca_periodo - 1, 4)
    ind["p6"] = p6

    (DADOS / "indicadores.json").write_text(json.dumps(ind, ensure_ascii=False, indent=1), encoding="utf-8")
    print("gravado: projeto/dados/painel_mensal.csv e projeto/dados/indicadores.json")


if __name__ == "__main__":
    main()
