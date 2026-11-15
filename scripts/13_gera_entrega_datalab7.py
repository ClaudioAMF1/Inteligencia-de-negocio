"""
DataLab 7-B2 - gera a entrega em .docx e .pdf no documento da tarefa.

O professor disponibilizou um documento próprio para esta atividade, com a
descrição e as sete perguntas. Ele é preenchido assim:
- a tabela de identificação ganha as linhas de aluno e matrícula;
- antes das perguntas entra uma seção curta com o tratamento dos dados;
- abaixo de cada pergunta entram o print da página do dashboard que a responde
  e a resposta por escrito.

Os números das respostas são calculados aqui a partir do dataset tratado, para
ficarem sempre iguais aos das páginas do dashboard.
"""
import copy
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from entrega import PRETO, RAIZ, _clona_depois, _para_pdf, _texto

TEMPLATE = RAIZ / "docs" / "IDP.INE - Atividade Avaliativa - DataLab 7-B2 (Prof. Bruno Miranda, 2026.2S).docx"
DADOS = RAIZ / "datalab7" / "dados" / "dados_financeiros_tratados.csv"
IMAGENS = RAIZ / "datalab7" / "imagens"
SAIDA = RAIZ / "datalab7" / "entrega"
ARQUIVO = "IDP.INE - Atividade Avaliativa 7-B2 - Claudio da Aparecida Meireles Filho"

TAMANHO_TEXTO = 12  # corpo do documento do professor
ALUNO = "Claudio da Aparecida Meireles Filho"
MATRICULA = "2321070"

PAGINAS = [
    "pagina1_total_receitas.png",
    "pagina2_total_despesas.png",
    "pagina3_margem_lucro.png",
    "pagina4_receitas_componente.png",
    "pagina5_despesas_media.png",
    "pagina6_matriz_tipo_componente_ano.png",
    "pagina7_segmentos.png",
]


def reais(valor, casas=2):
    texto = f"{valor:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")
    return f"R$ {texto}"


def pct(valor, casas=1):
    return f"{valor * 100:.{casas}f}%".replace(".", ",")


def carrega():
    with DADOS.open(encoding="utf-8") as arquivo:
        return [{**l, "Ano": int(l["Ano"]), "Valor": float(l["Valor"])} for l in csv.DictReader(arquivo)]


def indicadores(registros):
    tipo, tipo_ano, comp, comp_ano = (defaultdict(float) for _ in range(4))
    for r in registros:
        tipo[r["Tipo"]] += r["Valor"]
        tipo_ano[(r["Tipo"], r["Ano"])] += r["Valor"]
        comp[(r["Tipo"], r["Componente"])] += r["Valor"]
        comp_ano[(r["Tipo"], r["Componente"], r["Ano"])] += r["Valor"]
    anos = sorted({r["Ano"] for r in registros})
    receitas = {c: v for (t, c), v in comp.items() if t == "Receitas"}
    despesas = {c: v for (t, c), v in comp.items() if t == "Despesas"}
    return tipo, tipo_ano, receitas, despesas, comp_ano, anos


def respostas(registros):
    tipo, tipo_ano, receitas, despesas, comp_ano, anos = indicadores(registros)
    a0, a1 = anos[0], anos[-1]
    R, D = tipo["Receitas"], tipo["Despesas"]
    lucro = R - D
    cresc = lambda t: tipo_ano[(t, a1)] / tipo_ano[(t, a0)] - 1
    margem = {a: (tipo_ano[("Receitas", a)] - tipo_ano[("Despesas", a)]) / tipo_ano[("Receitas", a)] for a in anos}
    media = D / len(despesas)
    rec_ord = sorted(receitas, key=receitas.get, reverse=True)
    desp_ord = sorted(despesas, key=despesas.get, reverse=True)
    acima = [c for c in desp_ord if despesas[c] > media]
    abaixo = [c for c in desp_ord if despesas[c] <= media]
    peso_acima = sum(despesas[c] for c in acima) / D
    sal = lambda a: comp_ano[("Despesas", "Salários", a)]
    imp = lambda a: comp_ano[("Despesas", "Impostos", a)]
    alu = lambda a: comp_ano[("Receitas", "Aluguéis", a)]
    # quanto cada despesa aumentou, em reais, do primeiro ao último ano
    aumento = {c: comp_ano[("Despesas", c, a1)] - comp_ano[("Despesas", c, a0)] for c in despesas}
    mais_subiu = sorted(aumento, key=aumento.get, reverse=True)
    fra = [comp_ano[("Receitas", "Franquias", a)] for a in anos]
    menor_desp, penultima = desp_ord[-1], desp_ord[-2]

    def lista(itens):
        return ", ".join(itens[:-1]) + " e " + itens[-1]

    return [
        f"O total de receitas foi de {reais(R)}, somando os 36 meses do dataset "
        f"({', '.join(map(str, anos))}). A receita anual cresceu de {reais(tipo_ano[('Receitas', a0)], 0)} "
        f"em {a0} para {reais(tipo_ano[('Receitas', a1)], 0)} em {a1}, alta de {pct(cresc('Receitas'))}.",

        f"O total de despesas foi de {reais(D)}. As despesas anuais foram de "
        f"{reais(tipo_ano[('Despesas', a0)], 0)} em {a0} para {reais(tipo_ano[('Despesas', a1)], 0)} em {a1}, "
        f"alta de {pct(cresc('Despesas'))} - ritmo mais que o dobro do crescimento das receitas no mesmo período.",

        f"A margem de lucro foi de {pct(lucro / R, 2)}: lucro de {reais(lucro)} (receitas menos despesas) "
        f"sobre receitas de {reais(R)}. O ponto de atenção é a tendência: a margem caiu ano a ano, de "
        + " para ".join(f"{pct(margem[a])} em {a}" for a in anos)
        + ", consequência direta de as despesas crescerem mais rápido que as receitas.",

        "O total de receitas por componente foi: "
        + "; ".join(f"{c}, {reais(receitas[c], 0)} ({pct(receitas[c] / R)})" for c in rec_ord)
        + f". A receita é muito concentrada: {rec_ord[0]} responde sozinha por {pct(receitas[rec_ord[0]] / R)} do total.",

        f"A média de despesas por componente é de {reais(media)} (total de despesas dividido pelos "
        f"{len(despesas)} componentes). Ficam acima da média {lista(acima)}, que juntos concentram "
        f"{pct(peso_acima)} de todas as despesas; ficam abaixo {lista(abaixo)}. "
        f"{desp_ord[0]} é o caso extremo, com {pct(despesas[desp_ord[0]] / media - 1, 0)} acima da média.",

        f"A matriz organiza os valores na hierarquia Tipo > Componente, com uma coluna por ano. Ela "
        f"mostra três movimentos que os totais escondem: Salários ({reais(sal(a0), 0)} para "
        f"{reais(sal(a1), 0)}) e Impostos ({reais(imp(a0), 0)} para {reais(imp(a1), 0)}) mais que "
        f"triplicaram entre {a0} e {a1}, os maiores crescimentos entre as despesas; Aluguéis passaram de "
        f"{reais(alu(a0), 0)} para {reais(alu(a1), 0)}, o maior "
        f"crescimento entre as receitas; e Franquias é a única receita que caiu em todos os anos "
        f"({' → '.join(reais(v, 0) for v in fra)}). O dataset não traz o ano de 2021.",

        f"Nas receitas, o maior segmento é {rec_ord[0]} ({reais(receitas[rec_ord[0]], 0)}) e o menor é "
        f"{rec_ord[-1]} ({reais(receitas[rec_ord[-1]], 0)}). Nas despesas, o maior é {desp_ord[0]} "
        f"({reais(despesas[desp_ord[0]], 0)}) e o menor é {menor_desp} ({reais(despesas[menor_desp], 0)}), "
        f"praticamente empatado com {penultima} - apenas {reais(despesas[penultima] - despesas[menor_desp], 0)} "
        f"de diferença. Para o plano estratégico, os dados apontam três frentes: reduzir a dependência de "
        f"{rec_ord[0]}, que concentra {pct(receitas[rec_ord[0]] / R)} da receita; rever o modelo de "
        f"{rec_ord[-1]}, a menor receita e a única em queda contínua; e conter {desp_ord[0]}, a maior "
        f"despesa, e {mais_subiu[0]}, a que mais aumentou em reais (+{reais(aumento[mais_subiu[0]], 0)} "
        f"entre {a0} e {a1}) - juntas, elas respondem por "
        f"{pct((aumento[desp_ord[0]] + aumento[mais_subiu[0]]) / sum(aumento.values()), 0)} do "
        f"crescimento das despesas que derrubou a margem.",
    ]


TRATAMENTO = [
    "Tratamento dos dados",
    "O dataset ine_datalab7b2_dados_financeiros.xlsx vem no formato largo: uma linha para cada um "
    "dos 12 componentes (6 de receita e 6 de despesa) e uma coluna para cada um dos 36 meses, com os "
    "valores gravados como texto no padrão brasileiro (\"30000,00\"). Antes da análise ele foi "
    "tratado com os mesmos passos feitos em sala no Power Query: promover a primeira linha a "
    "cabeçalho; transformar as colunas de mês em linhas (Unpivot), mantendo Tipo e Componente fixos; "
    "converter o valor de texto para número decimal com a localidade pt-BR; e converter o mês para "
    "data, derivando a coluna Ano. O resultado é uma tabela longa com 432 linhas (12 componentes x 36 "
    "meses), que é a base de todas as páginas do dashboard.",
    "Dois pontos do dataset foram mantidos como vieram e sinalizados nas páginas: a série não tem o "
    "ano de 2021 (vai de jan/2019 a dez/2020 e depois de jan/2022 a dez/2022), e Publicidade tem três "
    "meses com receita negativa em 2020.",
]


def _identificacao(documento):
    tabela = documento.tables[0]
    modelo = tabela.rows[-1]._tr
    for rotulo, valor in (("Nome do aluno:", ALUNO), ("Matrícula:", MATRICULA)):
        linha = copy.deepcopy(modelo)
        tabela._tbl.append(linha)
        celulas = tabela.rows[-1].cells
        _texto(celulas[0].paragraphs[0], rotulo)
        _texto(celulas[1].paragraphs[0], valor)


def _paragrafo_texto(ancora, texto, negrito=False, italico=False, tamanho=TAMANHO_TEXTO, alinhamento=None):
    paragrafo = _clona_depois(ancora, texto)
    paragrafo.alignment = alinhamento if alinhamento is not None else WD_ALIGN_PARAGRAPH.JUSTIFY
    # o clone herdaria o "manter com o próximo" da imagem; aqui o texto corre livre
    paragrafo.paragraph_format.keep_with_next = False
    for run in paragrafo.runs:
        run.bold = negrito
        run.italic = italico
        run.font.color.rgb = PRETO
        if tamanho:
            run.font.size = Pt(tamanho)
    return paragrafo


def _imagem(ancora, caminho):
    paragrafo = _clona_depois(ancora, "")
    for run in paragrafo.runs:
        run._element.getparent().remove(run._element)
    paragrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragrafo.paragraph_format.keep_with_next = True
    paragrafo.paragraph_format.space_before = Pt(6)
    paragrafo.add_run().add_picture(str(caminho), width=Inches(6.2))
    return paragrafo


def _acha(documento, inicio):
    for paragrafo in documento.paragraphs:
        if paragrafo.text.strip().startswith(inicio):
            return paragrafo
    raise SystemExit(f"trecho não encontrado no documento da tarefa: {inicio!r}")


def main():
    faltando = [p for p in PAGINAS if not (IMAGENS / p).exists()]
    if faltando:
        raise SystemExit("rode antes o script 12; páginas ausentes: " + ", ".join(faltando))

    documento = Document(TEMPLATE)
    _identificacao(documento)

    # Seção de tratamento, logo antes da lista de perguntas.
    ancora = _acha(documento, "Responda cuidadosamente")
    anterior = ancora._element.getprevious()
    from docx.text.paragraph import Paragraph
    base = Paragraph(anterior, ancora._parent)
    atual = _paragrafo_texto(base, TRATAMENTO[0], negrito=True)
    for texto in TRATAMENTO[1:]:
        atual = _paragrafo_texto(atual, texto)
    _paragrafo_texto(atual, "")

    # A frase de abertura das perguntas acompanha a pergunta 1, em vez de ficar sozinha.
    ancora.paragraph_format.keep_with_next = True

    # Abaixo de cada pergunta: o print da página e a resposta.
    for numero, (pagina, resposta) in enumerate(zip(PAGINAS, respostas(carrega())), start=1):
        pergunta = _acha(documento, f"{numero}- ")
        pergunta.paragraph_format.space_before = Pt(14)
        # a pergunta acompanha a página do dashboard na quebra de página
        pergunta.paragraph_format.keep_with_next = True
        for run in pergunta.runs:
            run.bold = True
        atual = _imagem(pergunta, IMAGENS / pagina)
        atual = _paragrafo_texto(atual, f"Página {numero} do dashboard.", italico=True, tamanho=9,
                                 alinhamento=WD_ALIGN_PARAGRAPH.CENTER)
        atual = _paragrafo_texto(atual, "Resposta: " + resposta)
        rotulo = atual.runs[0]
        rotulo.text = resposta
        destaque = copy.deepcopy(rotulo._element)
        rotulo._element.addprevious(destaque)
        atual.runs[0].text = "Resposta: "
        atual.runs[0].bold = True

    SAIDA.mkdir(parents=True, exist_ok=True)
    destino_docx = SAIDA / f"{ARQUIVO}.docx"
    destino_pdf = SAIDA / f"{ARQUIVO}.pdf"
    documento.save(destino_docx)
    _para_pdf(destino_docx, destino_pdf)
    print(f"  {destino_docx.relative_to(RAIZ)}")
    print(f"  {destino_pdf.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
