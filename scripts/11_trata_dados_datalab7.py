"""
DataLab 7-B2 - tratamento do dataset de dados financeiros da firma.

O arquivo do professor vem no formato largo: uma linha por componente (Vendas,
Salários, ...) e uma coluna por mês, com os valores gravados como texto no
padrão brasileiro ("30000,00"). Para analisar no Power BI, ele precisa estar no
formato longo - uma linha por componente e por mês - com valor numérico e data
de verdade. São os mesmos passos feitos em sala no Power Query:

1. promover a primeira linha a cabeçalho;
2. transformar as colunas de mês em linhas (Unpivot);
3. converter o valor de texto para número, trocando a vírgula decimal;
4. converter a coluna de mês para data e derivar o ano.
"""
import csv
from datetime import datetime
from pathlib import Path

import openpyxl

RAIZ = Path(__file__).resolve().parent.parent
ORIGEM = RAIZ / "datalab7" / "dados" / "ine_datalab7b2_dados_financeiros.xlsx"
DESTINO = RAIZ / "datalab7" / "dados" / "dados_financeiros_tratados.csv"


def numero(texto):
    """'30.000,00' ou '30000,00' -> 30000.0"""
    if isinstance(texto, (int, float)):
        return float(texto)
    return float(str(texto).strip().replace(".", "").replace(",", "."))


def carrega_longo():
    """Lê o dataset original e devolve as linhas já no formato longo."""
    aba = openpyxl.load_workbook(ORIGEM, data_only=True)["DadosFinanceiros"]
    linhas = list(aba.iter_rows(values_only=True))
    cabecalho, corpo = linhas[0], linhas[1:]
    meses = [(indice, datetime.strptime(rotulo, "%d/%m/%Y").date())
             for indice, rotulo in enumerate(cabecalho) if indice >= 2]

    registros = []
    for linha in corpo:
        tipo, componente = linha[0], linha[1]
        if not tipo:
            continue
        for indice, data in meses:
            registros.append({
                "Tipo": tipo,
                "Componente": componente,
                "Data": data,
                "Ano": data.year,
                "Valor": numero(linha[indice]),
            })
    return registros


def main():
    registros = carrega_longo()
    with DESTINO.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["Tipo", "Componente", "Data", "Ano", "Valor"])
        escritor.writeheader()
        for registro in registros:
            escritor.writerow({**registro, "Data": registro["Data"].isoformat()})

    anos = sorted({r["Ano"] for r in registros})
    negativos = [r for r in registros if r["Valor"] < 0]
    print(f"{DESTINO.relative_to(RAIZ)}: {len(registros)} linhas")
    print(f"  componentes: {len({(r['Tipo'], r['Componente']) for r in registros})}")
    print(f"  anos presentes: {anos}")
    print(f"  valores negativos: {len(negativos)}")


if __name__ == "__main__":
    main()
