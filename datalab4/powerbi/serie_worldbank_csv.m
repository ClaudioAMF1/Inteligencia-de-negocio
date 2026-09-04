// DataLab 4-B1 - Inteligência de Negócio (IDP)
// Alternativa à consulta pela API: carrega o mesmo indicador a partir do pacote CSV
// baixado no portal (botão "Download" > "CSV" na página do indicador).
//
// O arquivo do World Bank vem no formato largo - uma linha por país e uma coluna por
// ano - e com quatro linhas de aviso antes do cabeçalho real. As duas correções estão
// nos passos abaixo.
//
// Ajuste o caminho do arquivo antes de usar.
let
    Caminho = "C:\Users\SeuUsuario\Downloads\API_IT.NET.USER.ZS_DS2_en_csv_v2.csv",
    Fonte = Csv.Document(File.Contents(Caminho), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),

    // Descarta as linhas de aviso e promove a linha "Country Name" a cabeçalho.
    SemAvisos = Table.Skip(Fonte, 4),
    ComCabecalho = Table.PromoteHeaders(SemAvisos, [PromoteAllScalars = true]),

    Entidades = {"BRA", "LCN", "WLD"},
    Filtrado = Table.SelectRows(ComCabecalho, each List.Contains(Entidades, [Country Code])),

    // Transposição das colunas de ano para o formato longo (ano, valor).
    Fixas = {"Country Name", "Country Code", "Indicator Name", "Indicator Code"},
    Longo = Table.UnpivotOtherColumns(Filtrado, Fixas, "ano", "valor"),

    Renomeado = Table.RenameColumns(Longo, {{"Country Name", "entidade"}}),
    Reduzido = Table.SelectColumns(Renomeado, {"entidade", "ano", "valor"}),
    Tipado = Table.TransformColumnTypes(Reduzido, {{"ano", Int64.Type}, {"valor", type number}}),
    SemVazios = Table.SelectRows(Tipado, each [valor] <> null),
    Ordenado = Table.Sort(SemVazios, {{"entidade", Order.Ascending}, {"ano", Order.Ascending}})
in
    Ordenado
