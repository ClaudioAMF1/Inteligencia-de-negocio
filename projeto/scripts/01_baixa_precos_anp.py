"""
Projeto aplicado - baixa a série histórica de preços da ANP e guarda só
Brasília (DF) e Goiânia (GO).

Fonte: ANP - Série histórica de preços de combustíveis (Levantamento de Preços),
https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis

Cada arquivo semestral nacional tem ~70 MB descompactado. Para não ocupar disco,
os CSVs são lidos em fluxo, linha a linha, direto da conexão, e só as linhas das
duas capitais são gravadas. Os arquivos compactados (2022 em diante) são baixados
para um temporário, filtrados e apagados.

Cada semestre vira um arquivo em projeto/dados/anp/, então o script pode ser
interrompido e retomado sem baixar de novo o que já foi processado.
"""
import csv
import io
import os
import re
import ssl
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PASTA = RAIZ / "projeto" / "dados" / "anp"
BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca/"

# Última década completa e o semestre mais recente publicado.
SEMESTRES = [(ano, sem) for ano in range(2016, 2026) for sem in (1, 2)] + [(2026, 1)]
CAPITAIS = {("DF", "BRASILIA"), ("GO", "GOIANIA")}

COLUNAS = ["Estado", "Municipio", "Revenda", "CNPJ", "Bairro", "Produto",
           "Data", "Valor de Venda", "Bandeira"]
ORIGEM = {"Estado": "Estado - Sigla", "Municipio": "Municipio", "Revenda": "Revenda",
          "CNPJ": "CNPJ da Revenda", "Bairro": "Bairro", "Produto": "Produto",
          "Data": "Data da Coleta", "Valor de Venda": "Valor de Venda", "Bandeira": "Bandeira"}


DATA = re.compile(r"^\d{2}/\d{2}/\d{4}$")
CNPJ = re.compile(r"^\s*\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\s*$")
TENTATIVAS = 4


class ArquivoInvalido(Exception):
    """O servidor devolveu algo que não é o semestre completo."""


def url(ano, sem):
    if (ano, sem) == (2022, 1):
        return BASE + "precos-semestrais-ca.zip"  # nome publicado pela ANP para 2022-01
    extensao = "zip" if ano >= 2022 else "csv"
    return BASE + f"ca-{ano}-{sem:02d}.{extensao}"


def contexto_ssl():
    pacote = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
    return ssl.create_default_context(cafile=pacote) if Path(pacote).exists() else None


def texto(linha):
    """Os arquivos antigos vêm em Latin-1 e os novos em UTF-8 com BOM."""
    try:
        return linha.decode("utf-8-sig")
    except UnicodeDecodeError:
        return linha.decode("latin-1")


def campos_da_linha(campos, cabecalho):
    """Devolve os campos da linha pelo nome da coluna.

    Algumas linhas da ANP trazem ";" dentro do nome do posto ou do endereço, sem
    aspas, e ficam com colunas a mais. Nesses casos as colunas são localizadas pelas
    pontas: Regiao, Estado e Municipio no começo; de Produto até Bandeira no fim;
    o CNPJ pelo formato, e o nome do posto é tudo o que fica entre Municipio e CNPJ.
    """
    if len(campos) == len(cabecalho):
        return {nome: campos[i] for nome, i in cabecalho.items()}
    if len(campos) < len(cabecalho):
        return None
    fim = ["Produto", "Data da Coleta", "Valor de Venda", "Valor de Compra", "Unidade de Medida", "Bandeira"]
    linha = {"Regiao - Sigla": campos[0], "Estado - Sigla": campos[1], "Municipio": campos[2]}
    linha.update({nome: campos[i - len(fim)] for i, nome in enumerate(fim)})
    linha["Cep"], linha["Bairro"] = campos[-7], campos[-8]
    meio = campos[3:-8]
    posicao = next((i for i, c in enumerate(meio) if CNPJ.match(c)), None)
    if posicao is None:
        return None
    linha["CNPJ da Revenda"] = meio[posicao]
    linha["Revenda"] = ";".join(meio[:posicao])
    return linha


def filtra(linhas, destino, semestre):
    """Lê o CSV nacional e grava só as duas capitais. Confere que o arquivo é o
    semestre inteiro: a última coleta precisa cair no último mês do semestre."""
    escritor = csv.DictWriter(destino, fieldnames=COLUNAS)
    escritor.writeheader()
    leitor = csv.reader((texto(l) for l in linhas), delimiter=";")
    cabecalho = None
    lidas = gravadas = descartadas = 0
    ultimo_mes = 0
    for campos in leitor:
        if not campos or not "".join(campos).strip():
            continue
        if cabecalho is None:
            if campos[0].lstrip().startswith("<"):
                raise ArquivoInvalido("o servidor devolveu uma página HTML, não o CSV")
            cabecalho = {nome.strip(): i for i, nome in enumerate(campos)}
            continue
        lidas += 1
        linha = campos_da_linha(campos, cabecalho)
        if linha is None or not DATA.match(linha["Data da Coleta"].strip()):
            descartadas += 1
            continue
        ultimo_mes = max(ultimo_mes, int(linha["Data da Coleta"].strip()[3:5]))
        if (linha["Estado - Sigla"].strip(), linha["Municipio"].strip()) not in CAPITAIS:
            continue
        escritor.writerow({c: linha[ORIGEM[c]].strip() for c in COLUNAS})
        gravadas += 1
    esperado = 6 if semestre == 1 else 12
    if ultimo_mes != esperado:
        raise ArquivoInvalido(f"arquivo incompleto: a última coleta é do mês {ultimo_mes}, esperado {esperado}")
    return lidas, gravadas, descartadas


def processa(ano, sem, ctx):
    destino = PASTA / f"ca-{ano}-{sem:02d}.csv"
    if destino.exists():
        return "já processado"
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            return baixa_semestre(ano, sem, ctx, destino)
        except Exception as erro:  # 503 do servidor, conexão cortada, arquivo incompleto
            if tentativa == TENTATIVAS:
                raise
            espera = 30 * 2 ** (tentativa - 1)
            print(f"{ano}-{sem:02d}: tentativa {tentativa} falhou ({erro}); nova tentativa em {espera}s", flush=True)
            time.sleep(espera)


def baixa_semestre(ano, sem, ctx, destino):
    endereco = url(ano, sem)
    temporario = destino.with_suffix(".parcial")
    requisicao = urllib.request.Request(endereco)
    with urllib.request.urlopen(requisicao, context=ctx, timeout=120) as resposta, \
            temporario.open("w", newline="", encoding="utf-8") as saida:
        if endereco.endswith(".zip"):
            with tempfile.TemporaryFile() as pacote:
                while bloco := resposta.read(1 << 20):
                    pacote.write(bloco)
                pacote.seek(0)
                with zipfile.ZipFile(pacote) as arquivo:
                    interno = next(n for n in arquivo.namelist() if n.lower().endswith(".csv"))
                    with arquivo.open(interno) as fluxo:
                        lidas, gravadas, descartadas = filtra(fluxo, saida, sem)
        else:
            lidas, gravadas, descartadas = filtra(resposta, saida, sem)
    temporario.rename(destino)
    return (f"{lidas:>9} linhas lidas, {gravadas:>6} de Brasília e Goiânia, "
            f"{descartadas} descartadas por formato inválido")


def main():
    PASTA.mkdir(parents=True, exist_ok=True)
    ctx = contexto_ssl()
    for ano, sem in SEMESTRES:
        try:
            print(f"{ano}-{sem:02d}: {processa(ano, sem, ctx)}", flush=True)
        except Exception as erro:  # um semestre com falha não derruba os outros
            print(f"{ano}-{sem:02d}: FALHOU - {erro}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
