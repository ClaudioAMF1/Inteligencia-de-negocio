"""
DataLab 3-B1 - Inteligência de Negócio (IDP)

Reabre o pacote .pbix (formato PBIR, baseado em JSON), aplica a identificação do
aluno em todas as páginas e corrige os títulos das páginas 2 e 3, que estavam
repetindo o título da página 1. Ao final regrava o pacote preservando a ordem e o
método de compressão das partes originais.
"""
import json
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "datalab3" / "idp_ine_datalab3.pbix"
# O pacote veio do Power BI como .pbix.zip; depois da primeira execução o próprio
# .pbix já atualizado passa a ser a origem, o que deixa o script idempotente.
ORIGEM = DESTINO if DESTINO.exists() else RAIZ / "datalab3" / "idp_ine_datalab3.pbix.zip"

ALUNO = "Claudio da Aparecida Meireles Filho (2321070)"
NOME_ANTERIOR = "Lucas Fiche Ungarelli Borges (2021068)"

# Título correto de cada página, na ordem em que as análises são pedidas no enunciado.
TITULOS = {
    "P1-Indicadores": "Datalab3 - Indicadores de Desempenho Acadêmico",
    "P2-Análise de Correlação": "Datalab3 - Análise de Correlação: Nota Final x Faltas",
    "P3-Distribuição de Notas": "Datalab3 - Distribuição das Notas",
    "P4-Evolução das Notas": "Datalab3 - Evolução das Notas P1 e P2",
}


def textos(visual):
    """Devolve os textRuns de uma caixa de texto (visualType == textbox)."""
    objetos = visual.get("visual", {}).get("objects", {}).get("general", [])
    for obj in objetos:
        for paragrafo in obj.get("properties", {}).get("paragraphs", []):
            for run in paragrafo.get("textRuns", []):
                yield run


def main():
    if not ORIGEM.exists():
        raise SystemExit(f"pacote de origem não encontrado: {ORIGEM}")

    origem_zip = zipfile.ZipFile(ORIGEM)
    ordem = origem_zip.infolist()
    partes = {info.filename: origem_zip.read(info.filename) for info in ordem}

    # Mapeia cada página pelo displayName para saber qual título aplicar.
    pagina_de = {}
    for nome in partes:
        if nome.endswith("/page.json"):
            pagina = json.loads(partes[nome])
            pagina_de[nome.rsplit("/", 1)[0]] = pagina["displayName"]

    trocas_nome = 0
    trocas_titulo = 0
    identificacoes = 0
    for nome, conteudo in list(partes.items()):
        if not nome.endswith("/visual.json"):
            continue
        visual = json.loads(conteudo)
        if visual.get("visual", {}).get("visualType") != "textbox":
            continue

        diretorio_pagina = nome.split("/visuals/")[0]
        titulo_esperado = TITULOS[pagina_de[diretorio_pagina]]

        alterado = False
        for run in textos(visual):
            valor = run.get("value", "")
            if valor in (NOME_ANTERIOR, ALUNO):
                identificacoes += 1
                if valor != ALUNO:
                    run["value"] = ALUNO
                    trocas_nome += 1
                    alterado = True
            elif valor.startswith("Datalab3") and valor != titulo_esperado:
                run["value"] = titulo_esperado
                trocas_titulo += 1
                alterado = True

        if alterado:
            partes[nome] = json.dumps(visual, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    if identificacoes != len(pagina_de):
        raise SystemExit(
            f"esperava 1 caixa de identificação por página ({len(pagina_de)}), achei {identificacoes}"
        )

    origem_zip.close()
    with zipfile.ZipFile(DESTINO, "w") as destino_zip:
        for info in ordem:
            destino_zip.writestr(info, partes[info.filename])

    print(f"{DESTINO.relative_to(RAIZ)} gerado")
    print(f"  identificação do aluno presente em {identificacoes} páginas "
          f"({trocas_nome} substituições nesta execução)")
    print(f"  títulos corrigidos nesta execução: {trocas_titulo}")


if __name__ == "__main__":
    main()
