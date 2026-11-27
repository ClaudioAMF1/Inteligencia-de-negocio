"""Preenche o template do aluno com as evidências e a análise da DataLab 12-B2."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.shared import Inches, Pt, RGBColor

from entrega import (
    ALUNO, MARCADOR_DESCRICAO, MARCADOR_PRINT, RAIZ, TEMPLATE,
    _acha, _normaliza, _para_pdf, _preenche_tabelas, _texto,
)

LAB = RAIZ / "datalab12"
TITULO = "DataLab 12-B2 – Simulação do Risco Esperado versus Volatilidade Esperada"
FONTE = (
    "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/"
    "market-data/historico/mercado-a-vista/cotacoes-historicas/"
)


def formatar(paragrafo, tamanho=11, antes=0, depois=4):
    formato = paragrafo.paragraph_format
    formato.left_indent = formato.right_indent = formato.first_line_indent = Pt(0)
    formato.space_before, formato.space_after = Pt(antes), Pt(depois)
    formato.line_spacing = 1.10
    paragrafo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in paragrafo.runs:
        run.font.name = "Arial"
        run.font.size = Pt(tamanho)
        run.font.color.rgb = RGBColor.from_string("172B39")
        run.italic = False
    return paragrafo


def figura(ancora, caminho, legenda, largura=6.15):
    p = ancora.insert_paragraph_before()
    formatar(p, depois=1)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1
    p.paragraph_format.keep_with_next = True
    imagem = p.add_run().add_picture(str(caminho), width=Inches(largura))
    imagem._inline.docPr.set("descr", legenda)
    p = formatar(ancora.insert_paragraph_before(legenda), tamanho=9, depois=8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].italic = True


def link(paragrafo, texto, url):
    vinculo = OxmlElement("w:hyperlink")
    vinculo.set(qn("r:id"), paragrafo.part.relate_to(url, RT.HYPERLINK, is_external=True))
    run = paragrafo.add_run(texto)
    run.font.name = "Arial"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor.from_string("145078")
    run.underline = True
    vinculo.append(run._r)
    paragrafo._p.append(vinculo)


def main():
    doc = Document(TEMPLATE)
    doc.core_properties.title = TITULO
    doc.core_properties.author = ALUNO
    _preenche_tabelas(doc, TITULO)
    solucao = _acha(doc, "Solução do DevLab")
    corpo = doc.paragraphs
    inicio = next(i for i, p in enumerate(corpo) if p._p is solucao._p)
    for p in corpo[inicio:]:
        if not p.text.strip() and not p._p.xpath(".//w:sectPr"):
            p._p.getparent().remove(p._p)

    marcador = _acha(doc, MARCADOR_PRINT)
    figura(marcador, LAB / "imagens/codigo_python.png",
           "Figura 1. Cabeçalho do arquivo Python e trecho que sorteia os pesos e calcula o risco.")
    figura(marcador, LAB / "imagens/console_python.png",
           "Figura 2. Console da execução em Python com os resultados por ação e por carteira.")
    marcador._p.getparent().remove(marcador._p)

    descricao = _acha(doc, "Descrição técnica do laboratório")
    descricao.paragraph_format.page_break_before = True
    introducao = _acha(doc, MARCADOR_DESCRICAO)
    formatar(_normaliza(_texto(introducao,
        "Cada ponto representa uma distribuição do capital entre Ambev (ABEV3), Itaú Unibanco "
        "(ITUB4) e Suzano (SUZB3). A posição horizontal mostra a volatilidade. A vertical "
        "mostra o retorno médio diário.")))
    perguntas = [_acha(doc, t) for t in ("Qual foi o objetivo do DevLab?",
                "Quais foram as técnicas utilizadas?", "O que você aprendeu?")]
    figura(perguntas[0], LAB / "resultados/risco_retorno.png",
           "Figura 3. Risco e retorno das 200 combinações e da carteira de pesos iguais, de 14/10 a 26/11/2026.",
           largura=5.8)
    respostas = [
        "Avaliar como o peso de cada ação muda o risco e o retorno da carteira. Para comparar "
        "as combinações em condições iguais, usei os mesmos pregões e tomei como referência "
        "uma divisão de um terço do capital para cada empresa.",
        "Extraí da B3 os fechamentos de 30 pregões, sem ajuste por proventos. Calculei os 29 "
        "retornos diários dividindo cada preço pelo do pregão anterior e subtraindo 1. Em "
        "Python, sorteei 200 trios de pesos e dividi cada trio pela soma. Estimei o retorno "
        "pela média ponderada dos retornos médios das ações e a volatilidade pela raiz "
        "quadrada da variância da carteira, calculada com a matriz de covariâncias amostrais.",
        "A divisão em partes iguais teve volatilidade diária de 1,292%. A carteira 184 chegou "
        "a 0,939% com 51,41% em Suzano. Os retornos de Suzano e Itaú tiveram correlação de "
        "−0,68 no período, o que ajudou a reduzir a oscilação conjunta. Já a carteira 81, "
        "com 81,83% em Suzano, obteve o maior retorno médio entre as sorteadas (0,706% ao dia), "
        "com volatilidade de 1,635%.",
    ]
    for pergunta, resposta in zip(perguntas, respostas):
        pergunta.paragraph_format.space_before = Pt(4)
        pergunta.paragraph_format.space_after = Pt(2)
        pergunta.paragraph_format.keep_with_next = True
        for run in pergunta.runs:
            run.bold = True
        p = doc.add_paragraph(resposta)
        pergunta._p.addnext(p._p)
        formatar(p, depois=4)
    p = formatar(doc.add_paragraph("Fonte dos fechamentos em reais. "), tamanho=9, antes=3)
    link(p, "B3, série COTAHIST, campo PREULT.", FONTE)

    destino = LAB / "entrega" / "DataLab12_Claudio_2321070.docx"
    destino.parent.mkdir(exist_ok=True)
    doc.save(destino)
    _para_pdf(destino, destino.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
