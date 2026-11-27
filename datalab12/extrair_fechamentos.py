# Claudio da Aparecida Meireles Filho | Matrícula 2321070
"""Extrai os últimos 30 pregões até 26/11/2026 do COTAHIST anual da B3."""

import argparse
import csv
from datetime import date
from pathlib import Path
from zipfile import ZipFile

ATIVOS = ("ABEV3", "ITUB4", "SUZB3")
DATA_LIMITE = b"20261126"
DESTINO = Path(__file__).resolve().parent / "dados" / "fechamentos.csv"


def extrair(arquivo):
    dias = {}
    with ZipFile(arquivo) as pacote, pacote.open("COTAHIST_A2026.TXT") as linhas:
        for linha in linhas:
            if linha[:2] != b"01" or linha[10:12] != b"02" or linha[24:27] != b"010":
                continue
            dia = linha[2:10]
            if dia > DATA_LIMITE:
                continue
            cotacoes = dias.setdefault(dia, {})
            papel = linha[12:24].strip().decode("ascii")
            if papel in ATIVOS:
                if papel in cotacoes or int(linha[210:217]) != 1:
                    raise ValueError(f"Registro ambíguo ou cotação não unitária: {dia!r}, {papel}")
                cotacoes[papel] = int(linha[108:121])  # PREULT em centavos

    pregoes = sorted(dias)[-30:]
    if len(pregoes) != 30 or pregoes[-1] != DATA_LIMITE:
        raise ValueError("O arquivo precisa incluir 30 pregões e alcançar 26/11/2026.")
    registros = []
    for dia in pregoes:
        cotacoes = dias[dia]
        if set(cotacoes) != set(ATIVOS) or min(cotacoes.values()) <= 0:
            raise ValueError(f"Falta um fechamento válido em {dia.decode()}.")
        data = date.fromisoformat(dia.decode()).isoformat()
        registros.append([data, *(f"{cotacoes[a] / 100:.2f}" for a in ATIVOS)])
    return registros


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("arquivo", type=Path, help="Caminho de COTAHIST_A2026.ZIP")
    registros = extrair(parser.parse_args().arquivo)
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with DESTINO.open("w", encoding="utf-8", newline="") as saida:
        escritor = csv.writer(saida, lineterminator="\n")
        escritor.writerow(["data", *ATIVOS])
        escritor.writerows(registros)
    print(f"{len(registros)} pregões de {registros[0][0]} a {registros[-1][0]}.")
