// DataLab 4-B1 - Inteligência de Negócio (IDP)
// Consulta do Power Query que carrega a série histórica direto da API do World Bank.
//
// Indicador: IT.NET.USER.ZS - Individuals using the Internet (% of population)
// Entidades: BRA (Brasil), LCN (América Latina e Caribe), WLD (Mundo)
// Portal...: https://data.worldbank.org/indicator/IT.NET.USER.ZS?locations=BR
//
// Como usar no Power BI Desktop:
//   Página Inicial > Transformar dados > Nova Fonte > Consulta Nula
//   Exibir > Editor Avançado > cole este código > Concluído > Fechar e Aplicar
let
    Fonte = Json.Document(
        Web.Contents(
            "https://api.worldbank.org/v2",
            [
                RelativePath = "country/BRA;LCN;WLD/indicator/IT.NET.USER.ZS",
                Query = [format = "json", per_page = "20000"]
            ]
        )
    ),

    // A API devolve uma lista de dois elementos: metadados na posição 0 e os dados na 1.
    Registros = Fonte{1},
    Tabela = Table.FromList(Registros, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Expandido = Table.ExpandRecordColumn(Tabela, "Column1", {"country", "date", "value"}, {"entidade", "ano", "valor"}),

    // A coluna "country" vem como registro {id, value}; interessa só o nome.
    NomeDaEntidade = Table.TransformColumns(Expandido, {{"entidade", each [value], type text}}),
    Tipado = Table.TransformColumnTypes(NomeDaEntidade, {{"ano", Int64.Type}, {"valor", type number}}),

    // Anos ainda não publicados voltam como nulo e não devem entrar nos gráficos.
    SemVazios = Table.SelectRows(Tipado, each [valor] <> null),
    Ordenado = Table.Sort(SemVazios, {{"entidade", Order.Ascending}, {"ano", Order.Ascending}})
in
    Ordenado
