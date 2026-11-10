"""
Projeto aplicado - relatório final no template oficial do projeto.

Usa o "Template IDP.INE - Modelo de Projeto de Inteligência de Negócio" (docs/),
o mesmo do pré-projeto: capa, empresa, área e tema, perguntas e bases. Depois das
seções do template entram metodologia, resultados (print do dashboard e resposta
de cada pergunta), conclusões e limitações.

Todo número citado no texto vem de projeto/dados/indicadores.json.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph

from entrega import PRETO, _para_pdf, _texto

especificacao = importlib.util.spec_from_file_location("pre", RAIZ / "scripts" / "07_gera_preprojeto.py")
pre = importlib.util.module_from_spec(especificacao)
especificacao.loader.exec_module(pre)

DADOS = RAIZ / "projeto" / "dados"
IMAGENS = RAIZ / "projeto" / "imagens"
SAIDA = RAIZ / "projeto" / "entrega"
ARQUIVO = "IDP.INE - Projeto Aplicado - Claudio Meireles e Felipe Dutra"

PAGINAS = ["pagina1_bsb_x_gyn.png", "pagina2_peso_na_renda.png", "pagina3_economia_pesquisando.png",
           "pagina4_paridade_etanol.png", "pagina5_bandeiras.png", "pagina6_preco_real.png"]

BASES = [
    ("ANP - Série histórica de preços de combustíveis (Levantamento de Preços). Base principal: "
     "preço posto a posto, por município e bandeira.",
     "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis"),
    ("IBGE - Microdados da PNAD Contínua (visitas anuais). Renda domiciliar per capita do DF e de Goiás.",
     "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Anual/Microdados/Visita/"),
    ("Banco Central - SGS, série 433 (IPCA mensal, calculado pelo IBGE). Deflator dos preços.",
     "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"),
]


# ---------------------------------------------------------------- formatação
def reais(v, casas=2):
    return "R$ " + f"{v:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def pct(v, casas=1):
    return f"{v * 100:.{casas}f}%".replace(".", ",")


def milhar(n):
    return f"{n:,}".replace(",", ".")


def decimal(v, casas=1):
    return f"{v:.{casas}f}".replace(".", ",")


def mes_br(m):
    nomes = "jan fev mar abr mai jun jul ago set out nov dez".split()
    return f"{nomes[int(m[5:]) - 1]}/{m[:4]}"


def faixas_de_meses(meses):
    """['2019-01','2019-02','2019-05'] -> 'jan/2019 a fev/2019, mai/2019'"""
    if not meses:
        return "nenhum mês"
    numero = lambda m: int(m[:4]) * 12 + int(m[5:]) - 1
    grupos, atual = [], [meses[0]]
    for m in meses[1:]:
        if numero(m) == numero(atual[-1]) + 1:
            atual.append(m)
        else:
            grupos.append(atual)
            atual = [m]
    grupos.append(atual)
    return ", ".join(mes_br(g[0]) if len(g) == 1 else f"{mes_br(g[0])} a {mes_br(g[-1])}" for g in grupos)


# ---------------------------------------------------------------- textos
def textos(ind):
    p1, p2, p3, p4, p5, p6 = (ind[f"p{i}"] for i in range(1, 7))
    periodo12 = f"{mes_br(p1['meses'][0])} a {mes_br(p1['meses'][1])}"

    et, ga = p1["produtos"]["Etanol"], p1["produtos"]["Gasolina"]
    barata = lambda d: "Goiânia" if d["diferenca_media"] > 0 else "Brasília"
    cara = lambda d: "Brasília" if d["diferenca_media"] > 0 else "Goiânia"

    def anos_mais_barato(produto, cidade):
        a = p1["serie_anual"][f"{cidade}|{produto}"]
        b = p1["serie_anual"][f"{'Brasília' if cidade == 'Goiânia' else 'Goiânia'}|{produto}"]
        comuns = sorted(set(a) & set(b), key=int)
        return sum(1 for ano in comuns if a[ano] < b[ano]), len(comuns)

    n_et, t_et = anos_mais_barato("Etanol", barata(et))
    n_ga, t_ga = anos_mais_barato("Gasolina", barata(ga))
    r1 = (f"Nos últimos 12 meses da série ({periodo12}), o etanol custou em média "
          f"{reais(et['Goiânia']['media'])} por litro em Goiânia e {reais(et['Brasília']['media'])} em Brasília: "
          f"é mais caro em {cara(et)}, por {reais(abs(et['diferenca_media']))} o litro. Na gasolina, a média foi "
          f"{reais(ga['Goiânia']['media'])} em Goiânia e {reais(ga['Brasília']['media'])} em Brasília, mais cara em "
          f"{cara(ga)} por {reais(abs(ga['diferenca_media']))}. Considerando o menor e o maior preço coletado em "
          f"cada semana, o etanol vai de {reais(et['Goiânia']['minimo'])} a {reais(et['Goiânia']['maximo'])} em "
          f"Goiânia e de {reais(et['Brasília']['minimo'])} a {reais(et['Brasília']['maximo'])} em Brasília. "
          f"Ao longo da série, o etanol foi mais barato em {barata(et)} em {n_et} de {t_et} anos, e a gasolina, "
          f"em {barata(ga)} em {n_ga} de {t_ga} anos"
          + (" - um padrão estável, não um efeito do último ano." if min(n_et / t_et, n_ga / t_ga) >= 0.7
             else " - ou seja, a vantagem de uma capital sobre a outra muda ao longo do tempo."))

    anos2 = sorted(p2["anos"], key=int)
    a0, a1 = anos2[0], anos2[-1]
    d0, d1 = p2["anos"][a0], p2["anos"][a1]
    razao = d1["Goiânia"]["percentual"] / d1["Brasília"]["percentual"]
    sentido = lambda c: "subiu" if d1[c]["percentual"] > d0[c]["percentual"] else "caiu"
    pico = {c: max((a for a in anos2 if c in p2["anos"][a]), key=lambda a: p2["anos"][a][c]["percentual"])
            for c in ("Brasília", "Goiânia")}
    r2 = (f"Em {a1}, 100 litros de gasolina por mês custavam {reais(d1['Brasília']['gasto_mensal'])} em Brasília, "
          f"o equivalente a {pct(d1['Brasília']['percentual'])} da renda domiciliar per capita do Distrito "
          f"Federal ({reais(d1['Brasília']['renda_per_capita'], 0)}). Em Goiânia, o mesmo consumo custava "
          f"{reais(d1['Goiânia']['gasto_mensal'])}, ou {pct(d1['Goiânia']['percentual'])} da renda per capita de "
          f"Goiás ({reais(d1['Goiânia']['renda_per_capita'], 0)}): o tanque pesa {decimal(razao)} vezes mais no "
          f"orçamento goiano. Em {a0}, os percentuais eram {pct(d0['Brasília']['percentual'])} e "
          f"{pct(d0['Goiânia']['percentual'])}; o peso {sentido('Brasília')} em Brasília e {sentido('Goiânia')} "
          f"em Goiânia. O ano de maior peso foi {pico['Brasília']} em Brasília "
          f"({pct(p2['anos'][pico['Brasília']]['Brasília']['percentual'])}) e {pico['Goiânia']} em Goiânia "
          f"({pct(p2['anos'][pico['Goiânia']]['Goiânia']['percentual'])}).")

    b3, g3 = p3["cidades"]["Brasília"], p3["cidades"]["Goiânia"]
    r3 = (f"Na mesma cidade e na mesma semana, a diferença entre o posto mais caro e o mais barato de gasolina foi, "
          f"em média, de {reais(b3['spread_medio'])} por litro em Brasília e {reais(g3['spread_medio'])} em Goiânia "
          f"({periodo12}). Num tanque de {p3['tanque_litros']} litros, pesquisar antes de abastecer vale "
          f"{reais(b3['economia_tanque'])} em Brasília e {reais(g3['economia_tanque'])} em Goiânia. Nas semanas "
          f"de maior dispersão, a diferença chegou a {reais(b3['spread_maximo'])} por litro em Brasília e "
          f"{reais(g3['spread_maximo'])} em Goiânia.")

    b4, g4 = p4["cidades"]["Brasília"], p4["cidades"]["Goiânia"]
    r4 = (f"Aplicando a regra dos 70%, o etanol compensou em {len(g4['meses_compensou'])} de {g4['total_meses']} "
          f"meses em Goiânia e em {len(b4['meses_compensou'])} de {b4['total_meses']} meses em Brasília. A "
          f"razão média entre os preços foi de {pct(g4['razao_media'])} em Goiânia e {pct(b4['razao_media'])} "
          f"em Brasília. Em Goiânia, os períodos favoráveis ao etanol foram: "
          f"{faixas_de_meses(g4['meses_compensou'])}. Em Brasília: {faixas_de_meses(b4['meses_compensou'])}. "
          f"No último mês da série, a razão era de {pct(g4['razao_ultimo_mes'])} em Goiânia e "
          f"{pct(b4['razao_ultimo_mes'])} em Brasília.")

    def resumo_bandeira(cidade):
        dados = p5["cidades"][cidade]
        branca = dados.get("Bandeira branca")
        marcas = {b: v for b, v in dados.items() if b not in ("Bandeira branca", "Outras bandeiras")}
        mais_cara = max(marcas, key=lambda b: marcas[b]["desvio_medio"])
        texto = (f"em {cidade}, a bandeira mais cara foi {mais_cara}, "
                 f"{reais(abs(marcas[mais_cara]['desvio_medio']), 3)} "
                 f"{'acima' if marcas[mais_cara]['desvio_medio'] >= 0 else 'abaixo'} da média da semana")
        if branca:
            diferenca = marcas[mais_cara]["desvio_medio"] - branca["desvio_medio"]
            texto += (f", e os postos de bandeira branca ficaram {reais(abs(branca['desvio_medio']), 3)} "
                      f"{'abaixo' if branca['desvio_medio'] < 0 else 'acima'} dela - "
                      f"{reais(diferenca, 3)} por litro entre os dois extremos, ou "
                      f"{reais(diferenca * p3['tanque_litros'])} num tanque de {p3['tanque_litros']} litros")
        return texto

    def amplitude_bandeiras(cidade):
        valores = [v["desvio_medio"] for v in p5["cidades"][cidade].values()]
        return max(valores) - min(valores)

    bandeira_menor = all(amplitude_bandeiras(c) < p3["cidades"][c]["spread_medio"] for c in ("Brasília", "Goiânia"))
    r5 = (f"Comparando cada posto com a média da cidade na mesma semana ({mes_br(p5['meses'][0])} a "
          f"{mes_br(p5['meses'][1])}, gasolina): {resumo_bandeira('Brasília')}; {resumo_bandeira('Goiânia')}. "
          + ("A bandeira pesa no preço, mas pesa menos do que a escolha do posto: a distância entre a bandeira "
             "mais cara e a mais barata é menor que a diferença média entre o posto mais caro e o mais barato "
             "da mesma semana (pergunta 3)." if bandeira_menor else
             "A distância entre bandeiras chega a ser comparável à diferença entre o posto mais caro e o mais "
             "barato da semana (pergunta 3), então a bandeira é um critério relevante de escolha."))

    b6, g6 = p6["cidades"]["Brasília"], p6["cidades"]["Goiânia"]
    x0, x1 = b6["anos"]
    r6 = (f"Entre {x0} e {x1}, o preço médio anual da gasolina subiu {pct(b6['variacao_nominal'])} em Brasília e "
          f"{pct(g6['variacao_nominal'])} em Goiânia, em termos nominais. Descontada a inflação medida pelo IPCA "
          f"({pct(p6['ipca_acumulado'])} acumulados no período), a variação real foi de "
          f"{pct(b6['variacao_real'])} em Brasília e {pct(g6['variacao_real'])} em Goiânia. "
          + leitura_real(b6, g6) + f" Valores reais em reais de {mes_br(p6['base_real'])}.")

    conclusoes = conclusoes_do_estudo(et, ga, barata, n_et, t_et, n_ga, t_ga, d1, b3, g3, g4, p5)
    return [r1, r2, r3, r4, r5, r6], conclusoes, limitacoes_do_estudo()


def leitura_real(b6, g6):
    reais_ = (b6["variacao_real"], g6["variacao_real"])
    nominais = (b6["variacao_nominal"], g6["variacao_nominal"])
    if all(r <= 0 for r in reais_):
        return ("Descontada a inflação, o preço real da gasolina caiu nas duas capitais: toda a alta que o "
                "consumidor viu na bomba foi inflação.")
    if all(r < n / 2 for r, n in zip(reais_, nominais)):
        return ("Mais da metade da alta nominal foi inflação; a alta real existe, mas é bem menor do que a "
                "percebida na bomba, e se concentra nos choques de preço visíveis no gráfico.")
    return ("A maior parte da alta nominal foi alta real do combustível, acima da inflação geral.")


def conclusoes_do_estudo(et, ga, barata, n_et, t_et, n_ga, t_ga, d1, b3, g3, g4, p5):
    if barata(et) == barata(ga):
        onde = (f"nos últimos 12 meses, tanto o etanol quanto a gasolina saíram mais baratos em {barata(et)}")
    else:
        onde = (f"nos últimos 12 meses, o etanol saiu mais barato em {barata(et)} e a gasolina em {barata(ga)}")
    estavel = min(n_et / t_et, n_ga / t_ga) >= 0.7
    onde += (", num padrão que se repete na maior parte da série." if estavel else
             ", mas a vantagem de uma capital sobre a outra mudou ao longo dos anos, então vale "
             "acompanhar o preço em vez de assumir que uma cidade é sempre mais barata.")

    preco_bsb, preco_gyn = d1["Brasília"]["preco_medio"], d1["Goiânia"]["preco_medio"]
    renda_ratio = d1["Brasília"]["renda_per_capita"] / d1["Goiânia"]["renda_per_capita"]
    preco_dif = preco_gyn / preco_bsb - 1
    pesa = (f"o mesmo consumo de gasolina representa {pct(d1['Goiânia']['percentual'])} da renda per capita de "
            f"Goiás e {pct(d1['Brasília']['percentual'])} da do DF. O litro custa "
            f"{pct(abs(preco_dif))} {'mais' if preco_dif > 0 else 'menos'} em Goiânia, mas a renda per capita do "
            f"DF é {decimal(renda_ratio)} vezes a de Goiás: a diferença de peso vem "
            f"{'principalmente da renda' if renda_ratio - 1 > abs(preco_dif) else 'principalmente do preço'}.")

    economia = max(b3["economia_tanque"], g3["economia_tanque"])
    parcela = len(g4["meses_compensou"]) / g4["total_meses"]
    frequencia = ("na maior parte dos meses" if parcela >= 0.5 else
                  "em parte relevante dos meses" if parcela >= 0.25 else "em poucos meses")
    controla = (f"pesquisar o posto vale até {reais(economia)} por tanque de 50 litros; e em Goiânia o etanol "
                f"compensou {frequencia} da série ({len(g4['meses_compensou'])} de {g4['total_meses']}), então "
                f"fazer a conta dos 70% antes de abastecer é um hábito que vale a pena.")
    return [("Onde abastecer: ", onde), ("Quanto pesa no orçamento: ", pesa), ("O que o consumidor controla: ", controla)]


def limitacoes_do_estudo():
    return [

        "A renda é estadual: o IBGE não publica renda domiciliar per capita anual por município, então Goiânia "
        "usa a de Goiás e Brasília a do Distrito Federal. Como a capital goiana tem renda acima da média do "
        "estado, o peso do combustível em Goiânia tende a estar superestimado.",
        "A renda per capita divide a renda do domicílio por todos os moradores, inclusive quem não dirige. O "
        "percentual mede o peso relativo do combustível, não o gasto de uma família específica.",
        "A ANP coleta uma amostra semanal de postos, e em dias diferentes em cada capital; por isso a comparação "
        "entre as cidades é feita por semana e por mês, e não pelo dia da coleta.",
        "Os microdados da PNAD foram recalibrados pelo IBGE com a população do Censo 2022. Toda a série de renda "
        "usa esses pesos atuais, o que a torna comparável entre os anos, mas faz os anos anteriores a 2025 "
        "diferirem alguns por cento dos valores publicados na época.",
        "A regra dos 70% é uma referência média: o rendimento do etanol frente à gasolina varia com o motor de "
        "cada carro.",
    ]


def metodologia(ind):
    per = ind["periodo"]
    return [
        f"Preços: os arquivos semestrais da ANP de {mes_br(per['inicio'])} a {mes_br(per['fim'])} foram lidos "
        f"em fluxo e filtrados para Brasília (DF) e Goiânia (GO), o que resultou em {milhar(per['coletas'])} "
        f"coletas de gasolina comum, etanol hidratado e diesel S10 em {milhar(per['postos'])} postos.",
        "Tratamento: os valores foram convertidos para número, as datas para o calendário e as razões sociais das "
        "distribuidoras agrupadas por marca (Petrobras Distribuidora e Vibra como BR; Raízen como Shell; CBPI "
        "como Ipiranga). Como a ANP coleta as duas capitais em dias diferentes, as comparações usam a semana e o "
        "mês como unidade.",
        "Renda: renda domiciliar per capita nominal do DF e de Goiás, calculada a partir dos microdados da PNAD "
        "Contínua pela definição do IBGE (total dos rendimentos domiciliares dividido pelo total de moradores). "
        "O cálculo foi validado contra o valor oficial de 2025, que reproduz até o real (DF R$ 4.538 e GO "
        "R$ 2.407).",
        f"Inflação: os preços foram trazidos para reais de {mes_br(ind['p6']['base_real'])} com o índice "
        "acumulado do IPCA mensal, obtido na série 433 do Banco Central.",
        "Ajustes em relação ao pré-projeto: a renda prevista era a da tabela 5437 do SIDRA (rendimento do "
        "trabalho), mas o SIDRA não aceita extração automatizada; a renda domiciliar per capita, oficial e anual "
        "por estado, foi calculada dos microdados. A base de vendas da ANP não foi necessária, porque as médias "
        "usam a coleta posto a posto.",
    ]


# ---------------------------------------------------------------- montagem
def anexa_paragrafo(documento, modelo, texto, negrito_ate=None):
    """Cria um parágrafo no fim do documento copiando o estilo de `modelo`."""
    vazio = documento.add_paragraph()
    novo = copy.deepcopy(modelo._element)
    vazio._p.addprevious(novo)
    vazio._p.getparent().remove(vazio._p)
    paragrafo = _texto(Paragraph(novo, documento._body), texto)
    paragrafo.paragraph_format.keep_with_next = False
    if negrito_ate:
        corpo = paragrafo.runs[0]
        corpo.text = texto[len(negrito_ate):]
        destaque = copy.deepcopy(corpo._element)
        corpo._element.addprevious(destaque)
        paragrafo.runs[0].text = negrito_ate
        paragrafo.runs[0].bold = True
    return paragrafo


def anexa_imagem(documento, caminho, legenda, modelo_texto):
    paragrafo = documento.add_paragraph()
    paragrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragrafo.paragraph_format.keep_with_next = True
    paragrafo.paragraph_format.space_before = Pt(6)
    paragrafo.add_run().add_picture(str(caminho), width=Inches(6.3))
    rotulo = anexa_paragrafo(documento, modelo_texto, legenda)
    rotulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in rotulo.runs:
        run.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = PRETO


def main():
    ind = json.loads((DADOS / "indicadores.json").read_text(encoding="utf-8"))
    respostas, conclusoes, limitacoes = textos(ind)

    documento = Document(pre.TEMPLATE)
    formato_corpo = pre._formato(
        documento.paragraphs[pre._acha_indice(documento, "A empresa que você irá abordar") + 1].runs[0])
    pre._troca(documento.paragraphs[0], "(TÍTULO DO SEU PROJETO)", pre.TITULO)
    pre._troca(documento.paragraphs[3], "(NOME DA DISCIPLINA)", pre.DISCIPLINA)
    pre._troca(documento.paragraphs[4], "(AUTORES)", pre.AUTORES)
    pre._preenche_secao(documento, "A empresa que você irá abordar", pre.EMPRESA)
    pre._preenche_secao(documento, "Área de negócio e o tema abordado", pre.AREA_E_TEMA)

    perguntas, bases = documento.tables
    formato_tabela = pre._formato_do_cabecalho(perguntas)
    pre._ajusta_linhas(perguntas, len(pre.PERGUNTAS))
    for linha, pergunta in zip(perguntas.rows[1:], pre.PERGUNTAS):
        celula = _texto(linha.cells[0].paragraphs[0], pergunta)
        celula.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pre._aplica_formato(celula, formato_tabela)

    intro = _texto(documento.paragraphs[pre._acha_indice(documento, "Quais bases de dados") + 1],
                   "As três bases são públicas. A ANP é a base principal; a renda e a inflação "
                   "entram para medir o peso do combustível no orçamento e separar alta real de inflação.")
    intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pre._aplica_formato(intro, formato_corpo)
    formato_bases = pre._formato_do_cabecalho(bases)
    pre._ajusta_linhas(bases, len(BASES))
    pre._larguras(bases, (2.85, 3.45))
    for linha, (base, link) in zip(bases.rows[1:], BASES):
        celula = _texto(linha.cells[0].paragraphs[0], base)
        celula.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pre._aplica_formato(celula, formato_bases)
        pre._link(linha.cells[1].paragraphs[0], link, formato_bases)
    pre._limpa_fim(documento)

    # Modelos de estilo: o título de seção do template e um parágrafo de corpo já preenchido.
    titulo = documento.paragraphs[pre._acha_indice(documento, "A empresa que você irá abordar")]
    corpo = documento.paragraphs[pre._acha_indice(documento, "A empresa que você irá abordar") + 1]

    def secao(texto):
        p = anexa_paragrafo(documento, titulo, texto)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.keep_with_next = True
        return p

    secao("Metodologia e tratamento dos dados")
    for item in metodologia(ind):
        rotulo = item.split(":")[0] + ": "
        anexa_paragrafo(documento, corpo, item, negrito_ate=rotulo)

    secao("Resultados")
    for numero, (pergunta, resposta, pagina) in enumerate(zip(pre.PERGUNTAS, respostas, PAGINAS), start=1):
        p = anexa_paragrafo(documento, corpo, f"Pergunta {numero}. {pergunta}", negrito_ate=f"Pergunta {numero}. ")
        for run in p.runs:
            run.bold = True
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_before = Pt(12)
        anexa_imagem(documento, IMAGENS / pagina, f"Página {numero} do dashboard.", corpo)
        anexa_paragrafo(documento, corpo, "Resposta: " + resposta, negrito_ate="Resposta: ")

    secao("Conclusões e recomendações ao consumidor")
    for rotulo, texto in conclusoes:
        anexa_paragrafo(documento, corpo, rotulo + texto, negrito_ate=rotulo)

    secao("Limitações do estudo")
    for texto in limitacoes:
        anexa_paragrafo(documento, corpo, "• " + texto)

    SAIDA.mkdir(parents=True, exist_ok=True)
    destino_docx = SAIDA / f"{ARQUIVO}.docx"
    destino_pdf = SAIDA / f"{ARQUIVO}.pdf"
    documento.save(destino_docx)
    _para_pdf(destino_docx, destino_pdf)
    print(f"  {destino_docx.relative_to(RAIZ)}")
    print(f"  {destino_pdf.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
