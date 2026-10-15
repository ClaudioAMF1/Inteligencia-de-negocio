// DataLab 7-B2 - Inteligência de Negócio (IDP)
// Tratamento do dataset no Power Query: os mesmos passos de scripts/11_trata_dados_datalab7.py.
//
// Como usar no Power BI Desktop:
//   Página Inicial > Transformar dados > Nova Fonte > Consulta Nula
//   Exibir > Editor Avançado > cole este código > Concluído
//   Renomeie a consulta para "dados" e clique em Fechar e Aplicar.
//
// Ajuste o caminho do arquivo antes de usar.
let
    Caminho = "C:\Users\SeuUsuario\Downloads\ine_datalab7b2_dados_financeiros.xlsx",
    Fonte = Excel.Workbook(File.Contents(Caminho), null, true),
    Aba = Fonte{[Item = "DadosFinanceiros", Kind = "Sheet"]}[Data],

    // 1. A primeira linha traz Tipo, Componente e os 36 meses.
    ComCabecalho = Table.PromoteHeaders(Aba, [PromoteAllScalars = true]),

    // 2. Unpivot: cada coluna de mês vira uma linha, mantendo Tipo e Componente fixos.
    Longo = Table.UnpivotOtherColumns(ComCabecalho, {"Tipo", "Componente"}, "Data", "Valor"),

    // 3 e 4. Os valores vêm como texto "30000,00" e as datas como "01/01/2019".
    // Converter com a localidade pt-BR resolve a vírgula decimal e o dia/mês/ano.
    Tipado = Table.TransformColumnTypes(
        Longo,
        {{"Valor", type number}, {"Data", type date}},
        "pt-BR"
    ),
    ComAno = Table.AddColumn(Tipado, "Ano", each Date.Year([Data]), Int64.Type)
in
    ComAno
