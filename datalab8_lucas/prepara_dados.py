"""Extrai as tabelas públicas APINFO 2025 e calcula as respostas do DataLab 8."""
import argparse
import csv
import hashlib
import json
import re
import statistics
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html

RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "datalab8_lucas" / "dados"
BRUTOS = DADOS / "brutos"
BASE_URL = "https://www.apinfo2.com/apinfo/informacao/"
LOCAIS = {"BR": "Brasil", "PR": "Paraná", "RS": "Rio Grande do Sul", "SC": "Santa Catarina"}
CARGOS = ["Arquiteto de Sistemas", "Desenvolvedor Full-Stack", "Desenvolvedor Front-End", "Desenvolvedor Back-End"]


def limpar(texto):
    return " ".join(texto.split())


def numero(texto):
    if not texto:
        return None
    if not re.fullmatch(r"\d{1,3}(?:\.\d{3})*(?:,\d{2})?|\d+(?:,\d{2})?", texto):
        raise ValueError(f"Valor monetário inesperado: {texto!r}")
    return float(texto.replace(".", "").replace(",", "."))


def extrair(caminho, uf):
    raiz = html.fromstring(caminho.read_bytes())
    texto_pagina = limpar(raiz.text_content())
    trecho = texto_pagina.split("Pesquisa feita", 1)[-1][:140]
    if "2025" not in trecho:
        raise ValueError(f"{uf}: a página não identifica a pesquisa de 2025")
    candidatas = []
    for tabela in raiz.xpath("//table"):
        linhas = [[limpar(c.text_content()) for c in tr.xpath("./td|./th")]
                  for tr in tabela.xpath(".//tr")]
        if linhas and linhas[0] == ["Cargo", "Especialidade", "CLT", "PJ"]:
            candidatas.append(linhas[1:])
    if len(candidatas) != 1:
        raise ValueError(f"{uf}: esperada uma tabela salarial, encontradas {len(candidatas)}")
    registros = []
    for posicao, linha in enumerate(candidatas[0], start=1):
        if len(linha) != 4 or not linha[0]:
            raise ValueError(f"{uf}: linha inválida {linha!r}")
        cargo, especialidade_fonte, clt, pj = linha
        especialidade = {"Phyton": "Python", "Java Script": "JavaScript"}.get(especialidade_fonte, especialidade_fonte)
        perfil = cargo + (" - " + especialidade if especialidade else "")
        for vinculo, valor in [("CLT", clt), ("PJ", pj)]:
            registros.append({
                "ano_pesquisa": 2025, "uf": uf, "localidade": LOCAIS[uf],
                "cargo": cargo, "especialidade": especialidade, "perfil": perfil,
                "vinculo_fonte": vinculo,
                "natureza": "bolsa_estagio" if cargo == "Estagiário" else "remuneracao",
                "salario_mensal_brl": numero(valor),
                "situacao": "publicado" if valor else "nao_publicado",
                "valor_original": valor, "especialidade_original": especialidade_fonte,
                "linha_fonte": posicao,
                "fonte_url": BASE_URL + f"p25sal-{uf.lower()}.cfm",
            })
    return registros


def gravar_csv(nome, linhas):
    with (DADOS / nome).open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(linhas[0]), lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(linhas)


def calcular(registros):
    nacionais = [r for r in registros if r["uf"] == "BR"]
    validos = [r for r in nacionais if r["salario_mensal_brl"] is not None]
    pares = {}
    for r in nacionais:
        pares.setdefault(r["perfil"], {"perfil": r["perfil"]})[r["vinculo_fonte"]] = r["salario_mensal_brl"]
    completos = []
    for par in pares.values():
        if par["CLT"] is not None and par["PJ"] is not None:
            completos.append({**par, "diferenca_brl": par["PJ"] - par["CLT"],
                "ganho_pj_pct": (par["PJ"] / par["CLT"] - 1) * 100,
                "media_perfil_brl": statistics.mean([par["CLT"], par["PJ"]])})
    completos.sort(key=lambda r: r["media_perfil_brl"], reverse=True)
    consulta = {(r["uf"], r["perfil"], r["vinculo_fonte"]): r for r in registros}
    comparativo = []
    for cargo in CARGOS:
        for vinculo in ["CLT", "PJ"]:
            brasil = consulta[("BR", cargo, vinculo)]["salario_mensal_brl"]
            for uf in ["PR", "RS", "SC"]:
                valor = consulta[(uf, cargo, vinculo)]["salario_mensal_brl"]
                if brasil is None or valor is None:
                    raise ValueError(f"Comparação indisponível: {cargo}, {vinculo}, {uf}")
                comparativo.append({"cargo": cargo, "vinculo": vinculo, "uf": uf,
                    "salario_estado_brl": valor, "referencia_brasil_brl": brasil,
                    "diferenca_brl": valor - brasil, "diferenca_pct": (valor / brasil - 1) * 100})
    salarios = [r for r in validos if r["natureza"] != "bolsa_estagio"]
    base_valida = [r for r in registros if r["salario_mensal_brl"] is not None]
    media_clt_pares = statistics.mean(r["CLT"] for r in completos)
    media_pj_pares = statistics.mean(r["PJ"] for r in completos)
    resumo = {
        "ano_pesquisa": 2025,
        "perfis_brasil": len(pares), "referencias_brasil_validas": len(validos),
        "referencias_brasil_ausentes": len(nacionais) - len(validos),
        "media_referencias_brasil": statistics.mean(r["salario_mensal_brl"] for r in validos),
        "media_sem_bolsa_estagio": statistics.mean(r["salario_mensal_brl"] for r in salarios),
        "media_clt_coluna_fonte": statistics.mean(r["salario_mensal_brl"] for r in validos if r["vinculo_fonte"] == "CLT"),
        "media_pj": statistics.mean(r["salario_mensal_brl"] for r in validos if r["vinculo_fonte"] == "PJ"),
        "pares_clt_pj": len(completos),
        "ganho_pj_medio_pct": statistics.mean(r["ganho_pj_pct"] for r in completos),
        "media_clt_pares": media_clt_pares, "media_pj_pares": media_pj_pares,
        "razao_das_medias_pares_pct": (media_pj_pares / media_clt_pares - 1) * 100,
        "lider": completos[0],
        "maior_referencia": max(validos, key=lambda r: r["salario_mensal_brl"]),
        "menor_referencia": min(validos, key=lambda r: r["salario_mensal_brl"]),
        "menor_sem_bolsa": min(salarios, key=lambda r: r["salario_mensal_brl"]),
        "maior_base_coletada": max(base_valida, key=lambda r: r["salario_mensal_brl"]),
        "menor_base_coletada": min(base_valida, key=lambda r: r["salario_mensal_brl"]),
        "top10": completos[:10],
        "ganhos_top5": sorted(completos, key=lambda r: r["ganho_pj_pct"], reverse=True)[:5],
        "ganhos_bottom5": sorted(completos, key=lambda r: r["ganho_pj_pct"])[:5],
    }
    return resumo, completos, comparativo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baixar", action="store_true", help="Atualiza os HTMLs diretamente da APINFO.")
    args = parser.parse_args()
    BRUTOS.mkdir(parents=True, exist_ok=True)
    if args.baixar:
        nomes = ["p25sumario"] + [f"p25sal-{uf.lower()}" for uf in LOCAIS]
        for nome in nomes:
            with urllib.request.urlopen(BASE_URL + nome + ".cfm", timeout=40) as resposta:
                (BRUTOS / (nome + ".html")).write_bytes(resposta.read())
        data_coleta = datetime.now(ZoneInfo("America/Sao_Paulo")).date().isoformat()
    else:
        existente = DADOS / "fontes.json"
        data_coleta = json.loads(existente.read_text())["data_coleta"] if existente.exists() else "2026-10-24"
    registros = []
    fontes = []
    for uf in LOCAIS:
        caminho = BRUTOS / f"p25sal-{uf.lower()}.html"
        lote = extrair(caminho, uf)
        registros.extend(lote)
        fontes.append({"uf": uf, "arquivo": "brutos/" + caminho.name,
            "url": BASE_URL + caminho.stem + ".cfm", "sha256": hashlib.sha256(caminho.read_bytes()).hexdigest(),
            "linhas_perfis": len(lote) // 2})
    chaves = [(r["ano_pesquisa"], r["uf"], r["perfil"], r["vinculo_fonte"]) for r in registros]
    if len(chaves) != len(set(chaves)):
        raise ValueError("Chaves repetidas no dataset")
    if any(r["salario_mensal_brl"] is not None and r["salario_mensal_brl"] <= 0 for r in registros):
        raise ValueError("Há valor monetário não positivo")
    resumo, pares, comparativo = calcular(registros)
    gravar_csv("apinfo_2025.csv", registros)
    gravar_csv("comparativo_clt_pj.csv", pares)
    gravar_csv("comparativo_estados.csv", comparativo)
    for nome, objeto in [("indicadores.json", resumo), ("fontes.json", {
        "data_coleta": data_coleta, "pesquisa": "APINFO 2025", "coleta_pesquisa": "agosto a setembro de 2025",
        "participantes_pesquisa_inteira": 26174, "fontes": fontes,
        "sumario_url": BASE_URL + "p25sumario.cfm",
        "nota": "Dados agregados publicados; não há microdados nem contagens por cargo/vínculo."
    }), ("validacao.json", {
        "linhas": len(registros), "valores_validos": sum(r["salario_mensal_brl"] is not None for r in registros),
        "valores_ausentes": sum(r["salario_mensal_brl"] is None for r in registros),
        "chaves_duplicadas": 0, "localidades": list(LOCAIS),
        "pares_brasil": len(pares), "comparacoes_estaduais": len(comparativo),
        "normalizacoes": {"Phyton": "Python", "Java Script": "JavaScript"},
        "regra": "Vazios preservados; BR não é somado aos estados; estágio identificado como bolsa."
    })]:
        (DADOS / nome).write_text(json.dumps(objeto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Tabelas: {len(LOCAIS)}; perfis por tabela: {resumo['perfis_brasil']}")
    print(f"Dataset: {len(registros)} linhas; {sum(r['salario_mensal_brl'] is None for r in registros)} valores ausentes; 0 chaves repetidas")
    print(f"Brasil: {resumo['referencias_brasil_validas']} referências válidas; média = {resumo['media_referencias_brasil']:.2f}")
    print(f"CLT x PJ: {len(pares)} pares; ganho percentual médio = {resumo['ganho_pj_medio_pct']:.4f}%")
    print(f"Comparativo estadual: {len(comparativo)} comparações (4 cargos x 2 vínculos x 3 estados)")


if __name__ == "__main__":
    main()
