"""
DataLab 10-B2 - gera a entrega em .docx e .pdf a partir do template do aluno.

Os números citados saem da execução real de datalab10/risco_retorno_carteira.py
sobre os preços de fechamento coletados na B3 (01/10 a 13/11/2026).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from entrega import RAIZ, gerar

IMAGENS = RAIZ / "datalab10" / "imagens"
SAIDA = RAIZ / "datalab10" / "entrega"

PRINTS = [
    ("Código (1/4) - cabeçalho com a identificação e os dados utilizados (ativos, período e fonte) "
     "e a lista das datas dos pregões.", IMAGENS / "codigo_1.png"),
    ("Código (2/4) - preços de fechamento dos 30 pregões, pesos da carteira e criação do "
     "dataframe com Pandas.", IMAGENS / "codigo_2.png"),
    ("Código (3/4) - retorno diário, retorno médio, risco, matrizes de covariância e correlação "
     "e o risco da carteira.", IMAGENS / "codigo_3.png"),
    ("Código (4/4) - simulação de 10.000 carteiras e gráfico de risco versus retorno.",
     IMAGENS / "codigo_4.png"),
    ("Saída do console (1/2) - nome e matrícula na primeira linha, preços de fechamento e "
     "retornos diários.", IMAGENS / "console_1.png"),
    ("Saída do console (2/2) - retorno médio, risco, matrizes de covariância e correlação, "
     "carteira com pesos iguais e carteiras simuladas.", IMAGENS / "console_2.png"),
    ("Gráfico de risco versus retorno: os três ativos, as 10.000 carteiras simuladas, a carteira "
     "com pesos iguais e a de menor risco.", IMAGENS / "risco_retorno.png"),
]

INTRODUCAO = (
    "O laboratório aplicou o algoritmo de risco versus retorno visto em aula a uma carteira "
    "real da B3. Escolhi três ações de setores diferentes, PETR4 (Petrobras, petróleo e gás), "
    "VALE3 (Vale, mineração) e ITUB4 (Itaú Unibanco, bancos), e coletei o preço de fechamento "
    "dos 30 pregões entre 01/10/2026 e 13/11/2026 nos arquivos oficiais de Séries Históricas "
    "da B3 (COTAHIST). Com esses preços, o algoritmo calcula o retorno diário, o retorno médio, "
    "o risco de cada ativo, a matriz de covariância e o risco da carteira."
)

OBJETIVO = [
    "Medir, com dados reais, quanto cada ativo rendeu e quanto oscilou, e ver como a "
    "combinação dos três numa carteira muda essa relação. O retorno é a média das variações "
    "diárias de preço; o risco é o desvio-padrão dessas variações.",

    "O período foi de queda para os três papéis: em 30 pregões, PETR4 caiu 8,98%, VALE3 caiu "
    "9,67% e ITUB4 caiu 4,26%. Os retornos médios diários foram de -0,27%, -0,33% e -0,08%, e "
    "o risco diário de 3,20%, 2,10% e 3,64%, respectivamente.",

    "A relação entre risco e retorno apareceu de forma clara: o ativo que perdeu menos (ITUB4) "
    "foi também o mais arriscado, e o mais estável (VALE3) foi o que mais perdeu. Na carteira "
    "com um terço em cada ativo, o risco caiu para 1,97% ao dia, contra 2,98% da média "
    "ponderada do risco dos ativos: uma redução de 33,76% só pela diversificação.",
]

TECNICAS = [
    "Coleta na fonte oficial: o script coleta_cotacoes_b3.py baixa os arquivos diários "
    "COTAHIST da B3 e lê o preço de fechamento (campo PREULT) no mercado à vista, lote padrão. "
    "Os 30 preços de cada ativo foram colocados no cabeçalho do algoritmo, como pede o "
    "enunciado, e conferidos contra o arquivo coletado.",

    "Estrutura do modelo da aula: vetor com os nomes dos ativos, um np.array de preços por "
    "ativo, o DataFrame do Pandas transposto (df.T) para ter uma coluna por ativo, e "
    "pct_change() para o retorno de cada pregão em relação ao anterior. O primeiro pregão fica "
    "NaN, porque não há preço anterior.",

    "Estatística da carteira: mean() para o retorno médio, std() para o risco, cov() para a "
    "matriz de covariância e corr() para a de correlação. O retorno da carteira é a média "
    "ponderada pelos pesos (w · μ) e o risco é a raiz de wᵀ · Σ · w, que leva em conta como os "
    "ativos se movem juntos.",

    "Simulação e visualização: 10.000 carteiras com pesos aleatórios (distribuição de "
    "Dirichlet, semente fixa na matrícula para o resultado ser reproduzível) desenham a região "
    "de combinações possíveis no gráfico de risco versus retorno feito com matplotlib.",
]

APRENDIZADO = [
    "Que risco maior não garante retorno maior, mas costuma vir junto com a chance dele. No "
    "período, a carteira de maior retorno da simulação foi praticamente 100% ITUB4 (-0,08% ao "
    "dia), que é também a de maior risco (3,63%). A carteira de menor risco (28,5% PETR4, "
    "64,4% VALE3 e 7,1% ITUB4) baixou o risco para 1,50% ao dia, mas com retorno de -0,30%.",

    "Que a diversificação depende da correlação. PETR4 e ITUB4 se moveram juntos (correlação "
    "de 0,51), enquanto VALE3 andou em sentido contrário a PETR4 (-0,26) e quase independente "
    "de ITUB4 (-0,09). É por isso que o risco da carteira ficou bem abaixo da média do risco "
    "dos ativos: as quedas de um eram em parte compensadas pelas altas de outro.",

    "Que 30 pregões são uma janela curta e sensível a eventos. Os maiores movimentos "
    "aconteceram em 05/10 (PETR4 +8,2% e ITUB4 +10,4%) e 26/10 (PETR4 -8,2% e ITUB4 -13,7%), "
    "os pregões seguintes ao primeiro e ao segundo turno das eleições de 2026. Poucos dias "
    "assim mudam o retorno médio e o risco do período inteiro.",

    "Que o dado precisa ser lido com cuidado: o preço de fechamento da B3 não é ajustado por "
    "proventos (o ITUB4 negociou ex-juros sobre capital próprio em 02/10, por exemplo), e o "
    "retorno médio diário de um mês não é previsão do mês seguinte. A análise mostra como a "
    "carteira se comportou, não como vai se comportar.",
]


def main():
    faltando = [str(caminho) for _, caminho in PRINTS if not Path(caminho).exists()]
    if faltando:
        raise SystemExit("rode antes o exercício e o script 08; imagens ausentes: "
                         + ", ".join(faltando))

    SAIDA.mkdir(parents=True, exist_ok=True)
    base = "IDP.INE - Atividade Avaliativa 10-B2 - Claudio da Aparecida Meireles Filho"
    gerar(
        destino_docx=SAIDA / f"{base}.docx",
        destino_pdf=SAIDA / f"{base}.pdf",
        tipo_atividade="DataLab 10-B2 - Relação risco versus retorno em carteiras de investimento",
        introducao=INTRODUCAO,
        prints=PRINTS,
        objetivo=OBJETIVO,
        tecnicas=TECNICAS,
        aprendizado=APRENDIZADO,
    )


if __name__ == "__main__":
    main()
