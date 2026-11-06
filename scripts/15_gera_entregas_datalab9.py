"""Monta os relatórios do DataLab 9-B2 no template oficial enviado pelo aluno.

Pré-requisito: executar os scripts R em cada pasta, gerando console.txt e
resultados.csv. As imagens são renderizações do código e da saída real, sem
simular uma captura do RStudio. Conversão e inspeção visual são etapas externas.
"""
import csv
import json
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont

import entrega

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "datalab9/fontes/template_aluno.docx"
NAVY = "102C41"
SIDRA = "https://sidra.ibge.gov.br/tabela/4093"
NOTAS = ("https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
         "Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/"
         "Notas_metodologicas/notas_metodologicas.pdf")
RELEASE = ("https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/"
           "2013-agencia-de-noticias/releases/45908-pnad-continua-trimestral-"
           "desocupacao-recua-em-seis-das-27-ufs-no-4-trimestre-de-2025")


def br(value, digits=2):
    return f"{value:,.{digits}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def visual_text(lines, path, title, first_line=None, code=False):
    """Renderiza texto legível; a origem é sempre o arquivo entregue."""
    width = 1560
    font = ImageFont.truetype("DejaVuSansMono.ttf", 32)
    title_font = ImageFont.truetype("DejaVuSans.ttf", 30)
    small = ImageFont.truetype("DejaVuSansMono.ttf", 24)
    step = 43
    image = Image.new("RGB", (width, 112 + step * len(lines)), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 78), fill="#102C41")
    draw.text((32, 21), title, font=title_font, fill="white")
    for i, line in enumerate(lines):
        y = 94 + i * step
        x = 32
        if first_line is not None:
            draw.text((18, y + 4), str(first_line+i).rjust(2), font=small, fill="#6B7280")
            x = 81
        assert draw.textlength(line, font=font) + x < width - 15, (path, line)
        color = "#55705B" if code and line.lstrip().startswith("#") else "#202937"
        draw.text((x, y), line, font=font, fill=color)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def para(doc, text, size=11, bold=False, after=7):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.1
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.left_indent = Pt(0)
    p.paragraph_format.right_indent = Pt(0)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor(0, 0, 0)
    r.bold = bold
    return p


def heading(doc, text, new_page=False):
    p = para(doc, text, 15, True, 10)
    p.style = doc.styles["Heading 1"]
    p.paragraph_format.page_break_before = new_page
    p.paragraph_format.keep_with_next = True
    for r in p.runs:
        r.font.color.rgb = RGBColor(0,0,0)
        r.font.size = Pt(15)
    return p


def table(doc, headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers))
    t.autofit = False
    for col, width in zip(t.columns, widths):
        col.width = Inches(width)
    for cells, values, index in [(t.rows[0].cells, headers, -1)] + [
        (t.add_row().cells, row, i) for i, row in enumerate(rows)
    ]:
        for j, (cell, value) in enumerate(zip(cells, values)):
            cell.width = Inches(widths[j])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cell.text = str(value)
            props = cell._tc.get_or_add_tcPr()
            fill = OxmlElement("w:shd")
            fill.set(qn("w:fill"), NAVY if index == -1 else ("F2F5F7" if index % 2 else "FFFFFF"))
            props.append(fill)
            margins = OxmlElement("w:tcMar")
            for side in ("top", "left", "bottom", "right"):
                node = OxmlElement("w:"+side);node.set(qn("w:w"), "85");node.set(qn("w:type"), "dxa");margins.append(node)
            props.append(margins)
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                if j == len(headers)-1:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                for r in p.runs:
                    r.font.name = "Arial";r.font.size = Pt(10)
                    r.bold = index == -1
                    r.font.color.rgb = RGBColor.from_string("FFFFFF" if index == -1 else "000000")
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement("w:"+side)
        for key, value in {"val":"single", "sz":"4", "color":"D9D9D9"}.items():
            border.set(qn("w:"+key), value)
        borders.append(border)
    t._tbl.tblPr.append(borders)
    header = OxmlElement("w:tblHeader");t.rows[0]._tr.get_or_add_trPr().append(header)
    for row in t.rows:
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
    para(doc, "", after=1, size=3)
    return t


def picture(doc, image, caption):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(image), width=Inches(6.2))
    c = para(doc, caption, 9, after=4)
    for r in c.runs:r.italic = True


def hyperlink(doc, title, url):
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    p = para(doc, "", 9, after=5)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), doc.part.relate_to(url, RT.HYPERLINK, is_external=True))
    r = OxmlElement("w:r");pr = OxmlElement("w:rPr")
    for tag, val in [("color","195D91"),("sz","18")]:
        node=OxmlElement("w:"+tag);node.set(qn("w:val"),val);pr.append(node)
    r.append(pr);text=OxmlElement("w:t");text.text=title;r.append(text);h.append(r);p._p.append(h)


def build(folder):
    base = ROOT / folder
    p = json.loads((base/"perfil.json").read_text())
    d = p["totais"]
    with (base/"resultados.csv").open(encoding="utf-8") as f:
        results = list(csv.DictReader(f))
    rates = [float(r["percentual"]) for r in results]
    code = (base/"indicadores_mercado_trabalho.R").read_text().splitlines()
    console = (base/"console.txt").read_text().splitlines()
    assert p["nome"] in "\n".join(code) and p["nome"] in "\n".join(console)
    assert p["matricula"] in "\n".join(console)
    images = base/"imagens"
    visual_text(code[:42], images/"codigo_1.png", "Código R | dados, validação e fórmulas", 1, True)
    visual_text(code[42:], images/"codigo_2.png", "Código R | execução e apresentação", 43, True)
    visual_text(console, images/"console.png", "Saída real de Rscript | DataLab 9 B2")

    doc = Document(TEMPLATE)
    entrega.ALUNO, entrega.MATRICULA = p["nome"], p["matricula"]
    entrega._preenche_tabelas(doc, "DataLab 9-B2 - Indicadores do mercado de trabalho")
    start = next(x for x in doc.paragraphs if x.text.strip() == "Solução do DevLab")._p
    body = doc._element.body
    remove = False
    for child in list(body):
        if child is start:remove=True
        if remove and child.tag != qn("w:sectPr"):body.remove(child)
    for style_name in ["Normal", "Heading 1", "Heading 2"]:
        style=doc.styles[style_name];style.font.name="Arial";style.font.color.rgb=RGBColor(0,0,0)
    doc.core_properties.author=p["nome"]
    doc.core_properties.title="DataLab 9 B2 Indicadores do mercado de trabalho"
    doc.core_properties.subject=f'{p["nome"]} | Matrícula {p["matricula"]} | {p["estado"]}'

    heading(doc, "Solução do DataLab")
    recorte = "do Distrito Federal" if p["sigla"] == "DF" else "de Santa Catarina"
    para(doc, f'Calculei os cinco indicadores em R com dados {recorte}, '
         'no 4º trimestre de 2025. O recorte considera pessoas de 14 anos ou mais, '
         'de ambos os sexos, na PNAD Contínua trimestral do IBGE.', 11)
    para(doc, "Dados utilizados", 11, True, 5)
    table(doc, ["Grupo populacional", "Sigla", "Mil pessoas"], [
        ("População em idade de trabalhar", "PIA", br(d["pia"],0)),
        ("Pessoas na força de trabalho", "FT", br(d["ft"],0)),
        ("Pessoas ocupadas", "PO", br(d["ocupados"],0)),
        ("Pessoas desocupadas", "PD", br(d["desocupados"],0)),
        ("Ocupados em situação de informalidade", "PI", br(d["informais"],0)),
        ("Ocupados formais calculados", "PO − PI", br(d["ocupados"]-d["informais"],0))
    ], [3.83, .82, 1.55])
    para(doc, "Indicadores calculados", 11, True, 5)
    table(doc, ["Indicador", "Fórmula × 100", "Resultado"], [
        (r["indicador"].replace(" (complementar)", "*"), r["formula"],br(float(r["percentual"]))+"%")
        for r in results
    ], [3.24, 1.66, 1.30])
    para(doc, "* O nível da ocupação foi incluído para distinguir as bases de cálculo. "
         "Nas notas metodológicas do IBGE, a taxa de ocupação divide os ocupados pela "
         "força de trabalho; o nível da ocupação usa a população em idade de trabalhar.", 10)
    para(doc, "Neste trabalho, o grau de formalização é a proporção complementar à "
         "proxy de informalidade do IBGE: (PO − PI) / PO × 100. Abrange vínculos e "
         "atividades formais, não apenas empregados com carteira assinada.", 10)
    para(doc, "Fonte: SIDRA 4093, sexo Total, 2025T4. Os totais são estimativas "
         "já expandidas e arredondadas em mil pessoas. As taxas recalculadas podem "
         "diferir na última casa das taxas publicadas pelo IBGE. Consulta em 06/11/2026.", 9)

    heading(doc, "Código em R", new_page=True)
    picture(doc, images/"codigo_1.png", "Figura 1. Dados oficiais, validações e implementação das fórmulas. Código do arquivo entregue.")
    heading(doc, "Código em R e apresentação da saída", new_page=True)
    picture(doc, images/"codigo_2.png", "Figura 2. Execução da função, identificação do aluno e exportação dos resultados.")
    para(doc, "O script usa apenas funções do R base. Os dados ficam no próprio "
         "arquivo para permitir a execução sem conexão à internet; o CSV e a "
         "resposta original da API permitem conferir os valores utilizados.", 10)

    heading(doc, "Saída da execução", new_page=True)
    picture(doc, images/"console.png", "Figura 3. Texto da saída real de Rscript 4.3.3, renderizado para leitura no relatório.")
    if p["sigla"] == "DF":
        interpretation = (
            f'No Distrito Federal, {br(rates[0])}% da população em idade de trabalhar '
            f'integrava a força de trabalho. Entre essas pessoas, {br(rates[2])}% '
            f'estavam desocupadas. Dos {br(d["ocupados"],0)} mil ocupados, '
            f'{br(d["informais"],0)} mil estavam na informalidade, o que corresponde '
            f'a {br(rates[3])}%. A formalização calculada foi de {br(rates[4])}%.'
        )
    else:
        interpretation = (
            f'Em Santa Catarina, a força de trabalho reunia {br(d["ft"],0)} mil '
            f'pessoas e {br(d["desocupados"],0)} mil estavam desocupadas. A taxa '
            f'de desocupação calculada foi de {br(rates[2])}%. Entre os ocupados, '
            f'{br(rates[3])}% estavam na informalidade e {br(rates[4])}% no '
            f'complemento formal. O nível da ocupação foi de {br(rates[5])}% da '
            'população em idade de trabalhar.'
        )
    para(doc, interpretation, 11)

    heading(doc, "Descrição técnica do laboratório", new_page=True)
    para(doc, "O laboratório aplicou razões e percentuais a grupos populacionais "
         "da PNAD Contínua. A função calcular_indicadores separa a validação dos "
         "totais, o cálculo das taxas e a apresentação dos resultados.", 11)
    para(doc, "Qual foi o objetivo do DataLab?", 11, True, 5)
    if p["sigla"] == "DF":
        objective = ("Implementar em R a participação na força de trabalho, a ocupação, "
                     "a desocupação, a informalidade e a formalização, usando o Distrito "
                     "Federal como recorte. Cada indicador responde a uma pergunta "
                     "diferente sobre a inserção da população no mercado de trabalho.")
        learned = (f'A escolha do denominador muda a interpretação. No meu recorte, '
                   f'{br(rates[1])}% da força de trabalho estava ocupada, enquanto '
                   f'{br(rates[5])}% da população em idade de trabalhar tinha ocupação. '
                   'Pessoas fora da força de trabalho entram apenas no denominador '
                   'desta segunda medida. Também é necessário distinguir a informalidade '
                   'da simples ausência de carteira assinada.')
    else:
        objective = ("Calcular os cinco indicadores solicitados com o recorte de Santa "
                     "Catarina e registrar uma execução reproduzível em R. Além de "
                     "obter as taxas, o exercício permite conferir como os totais "
                     "populacionais se relacionam e qual grupo cada percentual descreve.")
        learned = (f'Uma taxa de desocupação de {br(rates[2])}% se refere às pessoas '
                   'na força de trabalho, e não a todos os habitantes. A informalidade '
                   f'de {br(rates[3])}% usa outra base: somente os ocupados. Aprendi '
                   'também que os percentuais de informalidade e formalização somam '
                   '100% pela definição adotada, enquanto participação e desocupação '
                   'não são parcelas complementares.')
    para(doc, objective)
    para(doc, "Quais foram as técnicas utilizadas?", 11, True, 5)
    para(doc, "Usei um vetor nomeado com os totais do SIDRA, uma função para calcular "
         "as seis razões e um data.frame para organizar os resultados. O console "
         "mostra nome, matrícula, recorte, entradas e saídas. O arquivo resultados.csv "
         "guarda os percentuais sem o arredondamento aplicado apenas na apresentação.")
    para(doc, "As validações rejeitam valores ausentes, negativos ou infinitos, "
         "denominadores zerados e grupos incompatíveis. A identidade FT = PO + PD "
         "admite diferença de até mil pessoas por arredondamento. As 19 checagens "
         "automatizadas deste recorte cobrem exemplos de cálculo e casos inválidos.")
    para(doc, "O que você aprendeu?", 11, True, 5)
    para(doc, learned)
    para(doc, "Critério de informalidade e fontes", 11, True, 5)
    para(doc, "A proxy do IBGE reúne empregados do setor privado e trabalhadores "
         "domésticos sem carteira, empregadores e trabalhadores por conta própria "
         "sem CNPJ e trabalhadores familiares auxiliares. Esta atividade usa "
         "estimativas agregadas já ponderadas pelo IBGE; não reestima microdados "
         "nem calcula erros amostrais.", 10)
    hyperlink(doc, "IBGE SIDRA · Tabela 4093 · dados e taxas de referência", SIDRA)
    hyperlink(doc, "IBGE · Notas metodológicas · definições na página 18", NOTAS)
    hyperlink(doc, "IBGE · Divulgação do 4º trimestre de 2025 · informalidade", RELEASE)
    para(doc, "Consulta em 06/11/2026. A consulta da API, a resposta original e a "
         "identificação das variáveis estão na pasta fontes da entrega.", 9)
    dest=base/"entrega";dest.mkdir(exist_ok=True)
    name=f'DataLab_9B2_{"Claudio" if p["sigla"]=="DF" else "Lucas"}_{p["matricula"]}'
    doc.save(dest/f"{name}.docx")
    print(dest/f"{name}.docx")


if __name__ == "__main__":
    import sys
    for folder in (sys.argv[1:] or ["datalab9", "datalab9_lucas"]):
        build(folder)
