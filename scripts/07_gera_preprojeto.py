"""
Avaliação Continuada (Pré-projeto) - gera a entrega em .docx e .pdf.

O enunciado pede cinco itens: a dupla, a empresa/segmento, a área de negócio e o
tema, as perguntas que o estudo se propõe a resolver e as bases de dados com o
link da fonte. O template oficial do pré-projeto só é publicado no AVA, então o
documento é montado sobre o "[Template aluno]" da disciplina: a capa e a tabela
de identificação são as mesmas, e o corpo é reescrito com as seções do enunciado.
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from entrega import (PRETO, RAIZ, TEMPLATE, _acha, _clona_depois, _normaliza,
                     _para_pdf, _sem_lista, _texto)

SAIDA = RAIZ / "preprojeto" / "entrega"
ARQUIVO = "IDP.INE - Pré-projeto (Avaliação Continuada) - Claudio Meireles e Felipe Dutra"

DUPLA = [
    ("Claudio da Aparecida Meireles Filho", "2321070"),
    ("Felipe Pereira Dutra", "2321017"),
]

TIPO_ATIVIDADE = "Avaliação Continuada (Pré-projeto) - Projeto Aplicado"
ENTREGA = "25/09/2026"

SEGMENTO = (
    "Segmento de revenda de combustíveis no Brasil - os postos revendedores que vendem "
    "gasolina comum, etanol hidratado, diesel S-10 e GNV ao consumidor final, e as "
    "distribuidoras cujas bandeiras esses postos carregam. O estudo olha o mercado "
    "nacional e abre um recorte para o Distrito Federal, mercado onde a dupla mora e "
    "cujo comportamento de preço pretende comparar com o das demais unidades da federação."
)

AREA_E_TEMA = [
    ("Área de negócio: ", "Precificação e Inteligência de Mercado (pricing). É a área que "
     "decide o preço de bomba, acompanha o preço praticado pela concorrência e monitora a "
     "posição competitiva da rede em cada praça."),
    ("Tema: ", "Comportamento do preço de revenda de combustíveis no Brasil. O trabalho vai "
     "medir como o preço evoluiu ao longo do tempo, o quanto ele varia entre regiões e "
     "unidades da federação, qual é a dispersão de preço dentro de uma mesma cidade e em "
     "que condições o etanol se torna vantajoso frente à gasolina."),
    ("Por que esse tema: ", "combustível é um preço que todo consumidor acompanha e que toda "
     "rede de postos precisa decidir toda semana, e a ANP publica a coleta de preços posto a "
     "posto em série aberta e longa. Isso dá ao projeto um conjunto de dados com dimensão "
     "geográfica, dimensão de tempo e dimensão de produto - exatamente o formato que o "
     "Power BI explora bem - sem depender de dado proprietário de nenhuma empresa."),
]

PERGUNTAS = [
    "Como evoluiu o preço médio de revenda da gasolina comum, do etanol hidratado e do "
    "diesel S-10 no Brasil na última década, e quanto dessa alta se sustenta depois de "
    "descontada a inflação medida pelo IPCA?",

    "Quanto o preço do mesmo produto varia entre as regiões e as unidades da federação? "
    "Qual é a distância entre a UF mais cara e a mais barata em cada ano, e em que posição "
    "desse ranking está o Distrito Federal?",

    "Qual é a dispersão de preço dentro de um mesmo município na mesma semana de coleta? "
    "Em outras palavras: quanto o consumidor economiza, em reais por litro, saindo do posto "
    "mais caro para o mais barato da sua cidade?",

    "Em quais unidades da federação e em quais períodos o etanol hidratado foi vantajoso "
    "frente à gasolina comum, usando a regra de paridade de 70% entre os dois preços?",

    "Existe diferença consistente de preço entre postos bandeirados e postos de bandeira "
    "branca? A diferença é a mesma em todas as regiões do país?",
]

BASES = [
    ("ANP - Série histórica de preços de combustíveis",
     "Base principal. Levantamento de Preços de Combustíveis: coleta semanal do preço "
     "praticado em postos revendedores, com região, UF, município, produto, data da coleta, "
     "valor de venda e bandeira. Série disponível desde 2004.",
     "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis"),

    ("ANP - Vendas de derivados de petróleo e etanol",
     "Base de apoio. Volume mensal de vendas por unidade da federação e por produto, usado "
     "para ponderar as médias de preço pelo tamanho de cada mercado e para dar contexto de "
     "demanda às variações observadas.",
     "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/vendas-de-derivados-de-petroleo-e-etanol"),

    ("IBGE / SIDRA - IPCA (tabela 1737)",
     "Base de apoio. Índice Nacional de Preços ao Consumidor Amplo, usado como deflator para "
     "converter os preços nominais da ANP em preços reais e separar alta de combustível de "
     "inflação geral.",
     "https://sidra.ibge.gov.br/tabela/1737"),
]


def _remove_ate(inicio, fim):
    """Apaga tudo o que vem depois de `inicio` até `fim`, inclusive."""
    corpo = inicio._element.getparent()
    apagando = False
    for elemento in list(corpo):
        if elemento is inicio._element:
            apagando = True
            continue
        if not apagando:
            continue
        corpo.remove(elemento)
        if elemento is fim._element:
            break


def _preenche_capa(documento):
    rotulos = {
        "Disciplina:": "Inteligência de Negócio (INE)",
        "Professor:": "Bruno Miranda",
        "Tipo de atividade:": TIPO_ATIVIDADE,
        "Semestre": "2° semestre de 2026",
        "Departamento / Curso:": "Ciência da Computação / Engenharia de Software",
    }
    for linha in documento.tables[0].rows:
        rotulo = linha.cells[0].text.strip()
        if rotulo in rotulos:
            _normaliza(_texto(linha.cells[1].paragraphs[0], rotulos[rotulo]))


def _preenche_dupla(documento):
    """O template traz uma linha de nome e uma de matrícula; a dupla precisa de duas de cada."""
    tabela = documento.tables[1]
    modelo_nome = copy.deepcopy(tabela.rows[0]._element)
    modelo_matricula = copy.deepcopy(tabela.rows[1]._element)

    for _ in range(len(DUPLA) - 1):
        tabela._element.append(copy.deepcopy(modelo_nome))
        tabela._element.append(copy.deepcopy(modelo_matricula))

    for indice, (nome, matricula) in enumerate(DUPLA):
        linha_nome = tabela.rows[indice * 2]
        linha_matricula = tabela.rows[indice * 2 + 1]
        _normaliza(_texto(linha_nome.cells[0].paragraphs[0], f"Aluno {indice + 1}:"))
        _normaliza(_texto(linha_nome.cells[1].paragraphs[0], nome))
        _normaliza(_texto(linha_matricula.cells[0].paragraphs[0], "Matrícula:"))
        _normaliza(_texto(linha_matricula.cells[1].paragraphs[0], matricula))


def _rotulo(ancora, texto):
    """Subtítulo de item do enunciado (a, b, c, d, e), com respiro acima."""
    paragrafo = _corrido(ancora, texto)
    paragrafo.paragraph_format.space_before = Pt(14)
    paragrafo.paragraph_format.space_after = Pt(4)
    for run in paragrafo.runs:
        run.bold = True
    return paragrafo


def _corrido(ancora, texto, negrito_ate=None):
    """Acrescenta um parágrafo de texto corrido depois da âncora."""
    paragrafo = _normaliza(_sem_lista(_clona_depois(ancora, texto)))
    paragrafo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragrafo.paragraph_format.first_line_indent = Pt(0)
    paragrafo.paragraph_format.left_indent = Pt(0)
    for run in paragrafo.runs:
        run.bold = False
    if negrito_ate:
        # separa o rótulo do parágrafo em um run próprio, para destacá-lo em negrito
        restante = paragrafo.runs[0]
        restante.text = texto[len(negrito_ate):]
        rotulo = copy.deepcopy(restante._element)
        restante._element.addprevious(rotulo)
        paragrafo.runs[0].text = negrito_ate
        paragrafo.runs[0].bold = True
    return paragrafo


def _tabela_de_bases(documento, ancora):
    """Monta a tabela das bases de dados e a posiciona logo após a âncora."""
    tabela = documento.add_table(rows=1, cols=3)
    tabela.style = documento.tables[0].style
    tabela.autofit = False
    _com_bordas(tabela)

    for celula, titulo in zip(tabela.rows[0].cells, ("Base de dados", "Conteúdo e uso no estudo", "Link da fonte")):
        paragrafo = _normaliza(_texto(celula.paragraphs[0], titulo))
        for run in paragrafo.runs:
            run.bold = True
            run.font.size = Pt(9)

    for nome, descricao, link in BASES:
        celulas = tabela.add_row().cells
        for celula, conteudo, negrito in ((celulas[0], nome, True),
                                          (celulas[1], descricao, False),
                                          (celulas[2], link, False)):
            paragrafo = _normaliza(_texto(celula.paragraphs[0], conteudo))
            for run in paragrafo.runs:
                run.bold = negrito
                run.font.size = Pt(9)

    larguras = (Inches(1.65), Inches(2.85), Inches(1.70))
    for linha in tabela.rows:
        for celula, largura in zip(linha.cells, larguras):
            celula.width = largura

    ancora._element.addnext(tabela._element)
    return tabela


def _com_bordas(tabela):
    """O template não define estilo de tabela, então as bordas vão no XML."""
    propriedades = tabela._element.find(qn("w:tblPr"))
    bordas = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borda = OxmlElement(f"w:{lado}")
        borda.set(qn("w:val"), "single")
        borda.set(qn("w:sz"), "4")
        borda.set(qn("w:color"), "BFBFBF")
        bordas.append(borda)
    propriedades.append(bordas)


def main():
    documento = Document(TEMPLATE)
    _preenche_capa(documento)
    _preenche_dupla(documento)

    # Seção 1: reaproveita o primeiro título do template.
    titulo1 = _acha(documento, "Solução do DevLab")
    _texto(titulo1, "A dupla, o segmento e o tema")

    ancora = _acha(documento, "[Cole aqui o print")
    _texto(ancora, "")
    ancora = _rotulo(ancora, "a) A dupla do trabalho de projeto aplicado")
    for indice, (nome, matricula) in enumerate(DUPLA, start=1):
        ancora = _corrido(ancora, f"Aluno {indice}: {nome} - matrícula {matricula}.")
    ancora = _rotulo(ancora, "b) A empresa / segmento abordado")
    ancora = _corrido(ancora, SEGMENTO)
    ancora = _rotulo(ancora, "c) Área de negócio e tema")
    for rotulo, conteudo in AREA_E_TEMA:
        ancora = _corrido(ancora, rotulo + conteudo, negrito_ate=rotulo)

    # Seção 2: reaproveita o segundo título do template.
    titulo2 = _acha(documento, "Descrição técnica do laboratório")
    _texto(titulo2, "Perguntas de pesquisa e bases de dados")

    ancora = _acha(documento, "[Descreva tecnicamente")
    _normaliza(_texto(ancora, "d) Quais são as perguntas que o estudo se propõe a resolver?"))
    ancora.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    ancora.paragraph_format.space_after = Pt(6)
    for run in ancora.runs:
        run.bold = True
        run.italic = False

    # O template traz três perguntas como itens de uma lista, separadas por linhas em branco.
    # Fico com o primeiro item como molde da lista e removo o resto do bloco.
    molde = _acha(documento, "Qual foi o objetivo do DevLab?")
    ultimo = _acha(documento, "O que você aprendeu?")
    _remove_ate(molde, ultimo)

    atual = molde
    for indice, pergunta in enumerate(PERGUNTAS):
        if indice:
            atual = _clona_depois(atual, "")
        _normaliza(_texto(atual, pergunta))
        atual.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in atual.runs:
            run.bold = False

    ancora = _rotulo(atual, "e) Quais bases de dados serão utilizadas?")
    ancora = _corrido(
        ancora,
        "Todas as bases são públicas e de download livre, sem cadastro. A base principal é a "
        "coleta de preços da ANP; as outras duas entram como apoio para ponderação e para "
        "correção monetária. Os arquivos também estão espelhados no Portal Brasileiro de "
        "Dados Abertos (dados.gov.br).",
    )
    tabela = _tabela_de_bases(documento, ancora)
    # a tabela entrou logo depois da âncora, então o fechamento é criado e movido para depois dela
    fechamento = _corrido(ancora, f"Data de entrega do pré-projeto: {ENTREGA}.")
    fechamento.paragraph_format.space_before = Pt(12)
    tabela._element.addnext(fechamento._element)

    SAIDA.mkdir(parents=True, exist_ok=True)
    destino_docx = SAIDA / f"{ARQUIVO}.docx"
    destino_pdf = SAIDA / f"{ARQUIVO}.pdf"
    documento.save(destino_docx)
    _para_pdf(destino_docx, destino_pdf)
    print(f"  {destino_docx.relative_to(RAIZ)}")
    print(f"  {destino_pdf.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
