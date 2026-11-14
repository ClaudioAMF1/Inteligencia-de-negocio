"""
DataLab 10-B2 - coleta dos preços de fechamento na fonte oficial da B3.

A B3 publica um arquivo por pregão com as cotações de todos os papéis (Séries
Históricas, layout COTAHIST). Este script volta no calendário a partir de uma data,
baixa os arquivos diários até juntar 30 pregões e extrai o preço de fechamento
(PREULT) dos três ativos escolhidos no mercado à vista, lote padrão.

O download usa o curl: o site da B3 recusa o cliente HTTP padrão do Python. Os
arquivos baixados ficam em datalab10/dados/cotahist/ (fora do git) e não são
baixados de novo.

Saída: datalab10/dados/fechamento_b3.csv (data e um preço por ativo), que é o dado
usado no cabeçalho de risco_retorno_carteira.py.
"""
import csv
import subprocess
import sys
import time
import zipfile
from datetime import date, timedelta
from pathlib import Path

ATIVOS = ["PETR4", "VALE3", "ITUB4"]
PREGOES = 30
ULTIMO_DIA = date(2026, 11, 13)          # última sexta-feira antes da entrega
URL = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D{:%d%m%Y}.ZIP"
DADOS = Path(__file__).resolve().parent / "dados"
SAIDA = DADOS / "fechamento_b3.csv"
CACHE = DADOS / "cotahist"
PAUSA = 5                                 # segundos entre downloads


def baixa(dia):
    """Caminho do arquivo diário, baixado se ainda não estiver no cache."""
    destino = CACHE / f"COTAHIST_D{dia:%d%m%Y}.ZIP"
    if not destino.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        temporario = destino.with_suffix(".parcial")
        # A B3 limita a frequência de downloads: espaço as requisições e, se ela
        # recusar (403/429), espero mais antes de tentar de novo.
        for tentativa in range(5):
            time.sleep(PAUSA)
            codigo = subprocess.run(["curl", "-sS", "-o", str(temporario), "-w", "%{http_code}", URL.format(dia)],
                                    capture_output=True, text=True, check=True).stdout
            if codigo in ("200", "404"):
                break
            temporario.unlink(missing_ok=True)
            print(f"{dia:%d/%m/%Y}: HTTP {codigo}, nova tentativa em {60 * (tentativa + 1)} s", flush=True)
            time.sleep(60 * (tentativa + 1))
        else:
            raise RuntimeError(f"{dia}: a B3 recusou o download")
        temporario.rename(destino)
    return destino


def pregao(dia):
    """Fechamentos dos ATIVOS num dia, ou None se não houve pregão."""
    arquivo = baixa(dia)
    if not zipfile.is_zipfile(arquivo):           # feriado: a B3 não tem arquivo para o dia
        return None
    with zipfile.ZipFile(arquivo) as pacote:
        texto = pacote.read(pacote.namelist()[0]).decode("latin-1")
    precos = {}
    for linha in texto.splitlines():
        if linha[0:2] != "01":                    # 00 = cabeçalho, 99 = rodapé
            continue
        codigo = linha[12:24].strip()
        if codigo in ATIVOS and linha[10:12] == "02" and linha[24:27] == "010":
            if linha[2:10] != f"{dia:%Y%m%d}":
                raise ValueError(f"arquivo de {dia} traz a data {linha[2:10]}")
            precos[codigo] = int(linha[108:121]) / 100   # PREULT, com 2 casas implícitas
    if not precos:
        return None
    faltando = set(ATIVOS) - set(precos)
    if faltando:
        raise ValueError(f"{dia}: sem cotação de {', '.join(sorted(faltando))}")
    return precos


def main():
    linhas, dia = [], ULTIMO_DIA
    while len(linhas) < PREGOES:
        if dia.weekday() < 5:
            precos = pregao(dia)
            print(f"{dia:%d/%m/%Y}: " + ("sem pregão" if precos is None else
                  "  ".join(f"{a} {precos[a]:.2f}" for a in ATIVOS)), flush=True)
            if precos:
                linhas.append((dia, precos))
        dia -= timedelta(days=1)
    linhas.reverse()
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["data"] + ATIVOS)
        for dia, precos in linhas:
            w.writerow([dia.isoformat()] + [f"{precos[a]:.2f}" for a in ATIVOS])
    print(f"{len(linhas)} pregões de {linhas[0][0]:%d/%m/%Y} a {linhas[-1][0]:%d/%m/%Y} -> {SAIDA}")


if __name__ == "__main__":
    sys.exit(main())
