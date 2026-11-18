"""
DataLab 9-B2 - gera a entrega em .docx e .pdf a partir do template do aluno.

Os números citados saem da execução real de datalab9/indicadores_pnad_microdados.R
sobre os microdados da PNAD Contínua do 3º trimestre de 2026.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from entrega import RAIZ, gerar

IMAGENS = RAIZ / "datalab9" / "imagens"
SAIDA = RAIZ / "datalab9" / "entrega"

PRINTS = [
    ("Código em R (1/5) - cabeçalho com identificação e dados utilizados, pacotes, nome e matrícula "
     "na primeira linha do console e download dos microdados.", IMAGENS / "codigo_1.png"),
    ("Código em R (2/5) - posições das variáveis no arquivo do IBGE, leitura em blocos e classificação "
     "de cada pessoa (força de trabalho, ocupado, desocupado, informal e formal).", IMAGENS / "codigo_2.png"),
    ("Código em R (3/5) - plano amostral, fórmula de cada um dos cinco indicadores e taxas oficiais do "
     "SIDRA usadas na conferência.", IMAGENS / "codigo_3.png"),
    ("Código em R (4/5) - impressão dos resultados, composição dos ocupados por posição na ocupação e "
     "gravação do CSV.", IMAGENS / "codigo_4.png"),
    ("Código em R (5/5) - gráfico comparando Brasil e Distrito Federal.", IMAGENS / "codigo_5.png"),
    ("Saída do console no R: nome e matrícula na primeira linha, os cinco indicadores para o Brasil e o "
     "Distrito Federal com intervalo de confiança e a taxa publicada pelo IBGE.", IMAGENS / "console.png"),
    ("Gráfico gerado pelo script: os cinco indicadores no Brasil e no Distrito Federal, 3º trimestre "
     "de 2026.", IMAGENS / "indicadores_brasil_df.png"),
]

INTRODUCAO = (
    "O laboratório implementou em R os cinco indicadores do mercado de trabalho apresentados na "
    "aula: taxa de participação na força de trabalho, taxa de ocupação, taxa de desemprego, taxa de "
    "informalidade e grau de formalização do emprego. Em vez de usar totais prontos, o cálculo parte "
    "dos microdados da PNAD Contínua do 3º trimestre de 2026, o trimestre mais recente publicado pelo "
    "IBGE: são 533.366 pessoas entrevistadas, das quais 439.277 têm 14 anos ou mais. Os indicadores "
    "foram calculados para o Brasil e para o Distrito Federal, com os pesos amostrais da pesquisa, e "
    "conferidos contra as taxas oficiais publicadas no SIDRA."
)

OBJETIVO = [
    "Transformar as definições formais vistas em aula em código e chegar aos números oficiais do "
    "mercado de trabalho brasileiro a partir do dado bruto. Cada indicador é uma razão entre dois "
    "grupos da população: a força de trabalho e os ocupados sobre a população em idade de trabalhar "
    "(PIA), os desocupados sobre a força de trabalho, e os informais e os formais sobre os ocupados.",

    "No Brasil, no 3º trimestre de 2026: taxa de participação de 62,18%, taxa de ocupação de 58,98%, "
    "desemprego de 5,15%, informalidade de 37,46% e grau de formalização de 59,08%. No Distrito "
    "Federal: 67,98%, 64,28%, 5,45%, 26,73% e 70,27%, respectivamente.",

    "A leitura dos dois recortes: o DF tem mais gente participando do mercado e ocupada, um "
    "desemprego parecido com o do país e um emprego bem mais formal. A diferença vem principalmente "
    "do setor público: militares e servidores estatutários são 15,67% dos ocupados no DF, contra "
    "7,61% no Brasil, enquanto os trabalhadores por conta própria pesam menos (18,25% contra 25,21%).",
]

TECNICAS = [
    "Leitura dos microdados em blocos: o arquivo do trimestre tem 1,8 GB em largura fixa. O script lê "
    "100 mil linhas por vez direto do .zip, recorta só as 11 variáveis necessárias pelas posições do "
    "dicionário do IBGE (input_PNADC_trimestral.txt) e junta tudo num data.table.",

    "Classificação de cada pessoa com as variáveis derivadas do IBGE: VD4001 (força de trabalho), "
    "VD4002 (ocupado ou desocupado), VD4009 (posição na ocupação) e V4019 (negócio com CNPJ). "
    "Informal segue a definição do IBGE: empregado sem carteira no setor privado ou doméstico, "
    "empregador ou conta própria sem CNPJ e trabalhador familiar auxiliar. Formal segue a definição "
    "da aula: carteira assinada, militar ou estatutário e empregador ou conta própria com CNPJ.",

    "Plano amostral com o pacote survey: svydesign com a UPA como conglomerado, o estrato e o peso "
    "calibrado V1028. Cada indicador é estimado com svyratio, que devolve a razão e o erro-padrão; "
    "daí sai o intervalo de 95% impresso no console. Sem o peso, a média simples dos entrevistados "
    "não representaria a população.",

    "Validação: o script lê a resposta da API do SIDRA (tabela 4093) para o mesmo trimestre e imprime "
    "a taxa oficial ao lado da calculada. Os totais estimados batem exatamente com os publicados "
    "(PIA de 175.729 mil, força de trabalho de 109.266 mil, 103.638 mil ocupados, 5.628 mil "
    "desocupados e 38.819 mil informais no Brasil), e as oito taxas que o IBGE publica coincidem com "
    "as calculadas na casa decimal divulgada.",
]

APRENDIZADO = [
    "Que o denominador define o indicador. A taxa de ocupação da aula divide os ocupados pela PIA "
    "(58,98% no Brasil), e o IBGE publica esse mesmo número com o nome de nível da ocupação. Dividir "
    "os ocupados pela força de trabalho daria outra coisa: o complemento da taxa de desemprego "
    "(94,85%). Confundir os dois muda completamente a leitura.",

    "Que formalização e informalidade não somam exatamente 100%. No Brasil, 59,08% dos ocupados são "
    "formais e 37,46% são informais; os 3,46% restantes são empregados do setor público sem carteira, "
    "que o IBGE não classifica como informais, mas que também não têm carteira, estatuto ou CNPJ. No "
    "DF a conta é 70,27% + 26,73% + 3,00%.",

    "Que um recorte menor traz mais incerteza. Com 439 mil entrevistados no país, o intervalo de 95% "
    "da taxa de desemprego é de ±0,15 ponto; no DF, com uma amostra muito menor, é de ±0,75 ponto. "
    "Por isso o desemprego do DF (5,45%) e o do Brasil (5,15%) não são estatisticamente diferentes, "
    "embora a informalidade (26,73% contra 37,46%) seja.",

    "Que o peso amostral é parte do dado. Cada entrevistado representa centenas de pessoas, e o "
    "número que ele representa muda com a região e o perfil. Foi usando o peso calibrado que os "
    "totais calculados chegaram exatamente aos publicados pelo IBGE.",
]


def main():
    faltando = [str(caminho) for _, caminho in PRINTS if not Path(caminho).exists()]
    if faltando:
        raise SystemExit("rode antes o script R e o script 08; imagens ausentes: " + ", ".join(faltando))

    SAIDA.mkdir(parents=True, exist_ok=True)
    base = "IDP.INE - Atividade Avaliativa 9-B2 - Claudio da Aparecida Meireles Filho"
    gerar(
        destino_docx=SAIDA / f"{base}.docx",
        destino_pdf=SAIDA / f"{base}.pdf",
        tipo_atividade="DataLab 9-B2 - Cálculo dos principais indicadores do mercado de trabalho",
        introducao=INTRODUCAO,
        prints=PRINTS,
        objetivo=OBJETIVO,
        tecnicas=TECNICAS,
        aprendizado=APRENDIZADO,
    )


if __name__ == "__main__":
    main()
