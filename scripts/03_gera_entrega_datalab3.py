"""
DataLab 3-B1 - gera a entrega em .docx e .pdf a partir do template do aluno.

Os números citados na descrição técnica saem do próprio dataset
(ine_dataset_correcoes_avaliacoes.xlsx, 46 alunos) e podem ser reconferidos com
o script scripts/02_renderiza_paginas_datalab3.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrega import RAIZ, gerar

IMAGENS = RAIZ / "datalab3" / "imagens"
SAIDA = RAIZ / "datalab3" / "entrega"

PRINTS = [
    ("Análise 1 - Indicadores de desempenho: cartões de id, nota_final e total_faltas.",
     IMAGENS / "analise1_indicadores.png"),
    ("Análise 2 - Correlação: dispersão de total_faltas (X) por nota_final (Y).",
     IMAGENS / "analise2_correlacao.png"),
    ("Análise 3 - Distribuição das notas: colunas clusterizadas por nr_matricula com linha de média.",
     IMAGENS / "analise3_distribuicao.png"),
    ("Análise 4 - Evolução das notas: gráfico de área com nota_prova_p1, p2 e p3 por nr_matricula.",
     IMAGENS / "analise4_evolucao.png"),
]

INTRODUCAO = (
    "O laboratório trabalhou a exploração visual de uma base de correções e avaliações "
    "acadêmicas (46 alunos, 13 variáveis) no Power BI Desktop. A partir do arquivo "
    "ine_dataset_correcoes_avaliacoes.xlsx foram construídas quatro páginas de relatório, "
    "cada uma respondendo a uma das análises pedidas no enunciado: indicadores agregados, "
    "correlação entre faltas e nota, distribuição das notas e evolução das notas das provas."
)

OBJETIVO = [
    "Sair do dado bruto em planilha e chegar a um relatório que responda perguntas sobre o "
    "desempenho da turma. Em vez de ler 46 linhas de notas, o relatório mostra em quatro "
    "páginas quantos alunos existem, qual é a nota média, qual é a média de faltas, se faltar "
    "tem relação com nota baixa, como as notas se distribuem em torno da média e como o "
    "rendimento se comporta da P1 para a P2 e a P3.",
    "Os resultados encontrados na base: 46 alunos, nota final média de 5,80 e média de 6,46 "
    "faltas por aluno. 25 alunos (54,3%) fecharam com nota maior ou igual a 6,0, 11 ficaram "
    "entre 5,0 e 6,0 e 10 ficaram abaixo de 5,0.",
]

TECNICAS = [
    "Conexão e transformação: importação da planilha pelo conector de Excel, promoção da "
    "primeira linha a cabeçalho e tipagem das colunas no Power Query, deixando nr_matricula "
    "como texto (é identificador, não número a ser somado) e as notas e faltas como numéricas.",
    "Modelagem e agregação: uso das agregações nativas do Power BI sobre a tabela dados - "
    "Contagem para id, Média para nota_final, total_faltas e para as notas das provas, e "
    "Máximo de nota_final na distribuição por matrícula.",
    "Visualizações: cartão (card) para os três indicadores da Análise 1; gráfico de dispersão "
    "com total_faltas no eixo X e nota_final no eixo Y na Análise 2; gráfico de colunas "
    "clusterizadas por nr_matricula com linha de referência de média na Análise 3; e gráfico "
    "de área com as três séries de provas (nota_prova_p1, nota_prova_p2 e nota_prova_p3) na "
    "Análise 4.",
    "Formatação e leitura: título em caixa de texto e logomarca da instituição em todas as "
    "páginas, títulos de eixo renomeados para linguagem de negócio (\"Quantidade de Faltas\", "
    "\"Nota Final\"), ordenação decrescente das séries e uso do tema padrão do relatório para "
    "manter a mesma identidade visual nas quatro páginas.",
]

APRENDIZADO = [
    "Que a escolha do visual é parte da análise. O cartão responde \"quanto\", a dispersão "
    "responde \"tem relação?\", as colunas com linha de média respondem \"quem está acima ou "
    "abaixo do padrão\" e a área responde \"como evoluiu\". Trocar o visual sem trocar o dado "
    "muda completamente a pergunta que o relatório consegue responder.",
    "Que a dispersão da Análise 2 mostrou uma relação negativa clara entre faltas e nota "
    "final: o coeficiente de correlação de Pearson entre total_faltas e nota_final é de -0,67. "
    "Na prática, quem teve até 4 faltas fechou com média 6,35, enquanto quem teve 10 faltas ou "
    "mais fechou com média 4,23. A frequência é, nessa turma, um indicador antecedente do "
    "resultado final.",
    "Que a linha de média da Análise 3 é o que transforma um gráfico de colunas em um "
    "instrumento de decisão: sem ela vê-se só o ranking, com ela identifica-se imediatamente o "
    "grupo abaixo da média de 5,80 que precisaria de acompanhamento.",
    "Que detalhes de modelagem mudam o resultado: deixar nr_matricula como número faria o "
    "Power BI somar matrículas no eixo, e escolher a agregação errada (Soma em vez de Média) "
    "distorceria os cartões. A Análise 4 também deixou visível que a P3 só existe para os 7 "
    "alunos que foram para a prova substitutiva, o que explica a série ficar zerada na maior "
    "parte do eixo.",
]


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    faltando = [str(caminho) for _, caminho in PRINTS if not Path(caminho).exists()]
    if faltando:
        raise SystemExit("rode antes o script 02; imagens ausentes: " + ", ".join(faltando))

    base = "IDP.INE - Atividade Avaliativa 3-B1 - Claudio da Aparecida Meireles Filho"
    gerar(
        destino_docx=SAIDA / f"{base}.docx",
        destino_pdf=SAIDA / f"{base}.pdf",
        tipo_atividade="DataLab 3-B1 - Explorando dados com o Power BI",
        introducao=INTRODUCAO,
        prints=PRINTS,
        objetivo=OBJETIVO,
        tecnicas=TECNICAS,
        aprendizado=APRENDIZADO,
    )


if __name__ == "__main__":
    main()
