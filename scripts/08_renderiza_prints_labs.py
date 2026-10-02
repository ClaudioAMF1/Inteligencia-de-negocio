"""
DataLabs 5-B1 e 6-B1 - gera os prints que evidenciam o trabalho.

O enunciado pede o print do exercício. Como os scripts rodam aqui no terminal e
não no Colab, as evidências são montadas no mesmo formato das células do
notebook usado em aula: o código com numeração de linha e, abaixo, a saída real
do console. O HTML é renderizado pelo Chromium em modo headless.
"""
import html
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

RAIZ = Path(__file__).resolve().parent.parent
CHROMIUM = Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
LARGURA = 980
LINHAS_POR_IMAGEM = 38

LABS = {
    "datalab5": RAIZ / "datalab5" / "viabilidade_valor_presente.py",
    "datalab6": RAIZ / "datalab6" / "viabilidade_vpl_tir.py",
}

ESTILO = """
* { box-sizing: border-box; }
body { margin: 0; padding: 16px; background: #ffffff;
       font-family: 'DejaVu Sans Mono', 'Liberation Mono', monospace; }
.celula { border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden;
          margin-bottom: 14px; }
.rotulo { background: #f1f3f4; color: #5f6368; font-size: 12px;
          padding: 5px 12px; border-bottom: 1px solid #e0e0e0;
          font-family: 'DejaVu Sans', sans-serif; }
.codigo { background: #f8f9fa; padding: 10px 12px; }
.saida { background: #ffffff; padding: 10px 12px; color: #202124;
         font-size: 14px; line-height: 1.45; white-space: pre; }
pre { margin: 0; font-size: 14px; line-height: 1.5; }
table.highlighttable { border-spacing: 0; width: 100%; }
td.linenos { color: #9aa0a6; text-align: right; padding-right: 12px;
             user-select: none; vertical-align: top; }
td.code { width: 100%; vertical-align: top; }
"""


def _celula(rotulo, corpo, classe):
    return (f'<div class="celula"><div class="rotulo">{rotulo}</div>'
            f'<div class="{classe}">{corpo}</div></div>')


def _html(blocos):
    formatador = HtmlFormatter(style="default")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{ESTILO}\n"
            f"{formatador.get_style_defs('.highlight')}</style></head>"
            f"<body>{''.join(blocos)}</body></html>")


def _renderiza(conteudo_html, destino):
    """Abre o HTML no Chromium headless, tira o print e corta a sobra em branco."""
    with tempfile.TemporaryDirectory() as temporario:
        pagina = Path(temporario) / "pagina.html"
        pagina.write_text(conteudo_html, encoding="utf-8")
        bruto = Path(temporario) / "bruto.png"
        subprocess.run(
            [str(CHROMIUM), "--headless", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=2",
             f"--window-size={LARGURA},4000", f"--screenshot={bruto}",
             pagina.as_uri()],
            check=True, capture_output=True,
        )
        imagem = Image.open(bruto).convert("RGB")
        # o Chromium devolve a janela inteira; corto tudo o que ficou branco embaixo
        caixa = Image.new("RGB", imagem.size, "white")
        from PIL import ImageChops
        diferenca = ImageChops.difference(imagem, caixa).convert("L")
        limites = diferenca.getbbox()
        if limites:
            margem = 16
            imagem = imagem.crop((0, 0, imagem.width, min(imagem.height, limites[3] + margem)))
        destino.parent.mkdir(parents=True, exist_ok=True)
        imagem.save(destino)
    print(f"  {destino.relative_to(RAIZ)}")


def _partes_do_codigo(fonte):
    """Quebra o código em pedaços que caibam numa imagem legível. Um resto muito
    curto no fim vira uma imagem quase vazia, então ele volta para o pedaço anterior."""
    linhas = fonte.rstrip("\n").split("\n")
    cortes = list(range(0, len(linhas), LINHAS_POR_IMAGEM))
    if len(cortes) > 1 and len(linhas) - cortes[-1] < LINHAS_POR_IMAGEM // 4:
        cortes.pop()
    for ordem, inicio in enumerate(cortes):
        fim = cortes[ordem + 1] if ordem + 1 < len(cortes) else len(linhas)
        yield inicio + 1, "\n".join(linhas[inicio:fim])


def _executa(script):
    """Roda o exercício e devolve a saída real do console."""
    resultado = subprocess.run([sys.executable, str(script)],
                               capture_output=True, text=True, check=True)
    return resultado.stdout.rstrip("\n")


def main():
    if not CHROMIUM.exists():
        raise SystemExit(f"Chromium não encontrado em {CHROMIUM}")

    for lab, script in LABS.items():
        saida = RAIZ / lab / "imagens"
        print(f"{lab}:")
        fonte = script.read_text(encoding="utf-8")

        for indice, (primeira, trecho) in enumerate(_partes_do_codigo(fonte), start=1):
            formatador = HtmlFormatter(linenos="table", linenostart=primeira)
            corpo = highlight(trecho, PythonLexer(), formatador)
            rotulo = f"{script.name} - linhas {primeira} a {primeira + trecho.count(chr(10))}"
            _renderiza(_html([_celula(rotulo, corpo, "codigo")]),
                       saida / f"codigo_{indice}.png")

        console = html.escape(_executa(script))
        _renderiza(_html([_celula("Saída do console", console, "saida")]),
                   saida / "console.png")


if __name__ == "__main__":
    main()
