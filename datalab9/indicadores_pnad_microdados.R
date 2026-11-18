# Autor: Claudio da Aparecida Meireles Filho - matrícula 2321070
# Objetivo: DataLab 9-B2 - cálculo dos principais indicadores do mercado
#           de trabalho em R, com os microdados da PNAD Contínua
# Disciplina: Inteligência de Negócio (INE) - Prof. Bruno Miranda - 2026.2S
#
# DADOS UTILIZADOS
#   Fonte    : IBGE - PNAD Contínua trimestral, microdados do 3º trimestre de 2026
#              ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_
#              Amostra_de_Domicilios_continua/Trimestral/Microdados/2026/PNADC_032026.zip
#   Recorte  : Brasil e Distrito Federal; pessoas de 14 anos ou mais (PIA)
#   Peso     : V1028 (peso com calibração); plano amostral com UPA e Estrato
#   Variáveis: VD4001 força de trabalho, VD4002 ocupação, VD4009 posição na
#              ocupação, V4019 CNPJ, V2009 idade, UF
#   Conferência: taxas oficiais do SIDRA, tabela 4093 (dados/sidra_*.json)
#
# Pacotes:  install.packages(c("survey", "data.table", "jsonlite"))

suppressPackageStartupMessages({
  library(data.table)
  library(survey)
  library(jsonlite)
})
milhar <- function(x) formatC(round(x), format = "d", big.mark = ".", decimal.mark = ",")
decimal <- function(x, casas = 2) formatC(x, format = "f", digits = casas, decimal.mark = ",")

aluno <- "Claudio da Aparecida Meireles Filho"
matricula <- "2321070"
cat("Aluno:", aluno, "| Matrícula:", matricula, "\n")
cat("DataLab 9-B2 - Indicadores do mercado de trabalho | PNAD Contínua 3º tri 2026\n\n")

arquivo_zip <- "dados/microdados/PNADC_032026.zip"
if (!file.exists(arquivo_zip)) {
  dir.create(dirname(arquivo_zip), recursive = TRUE, showWarnings = FALSE)
  download.file(paste0("https://ftp.ibge.gov.br/Trabalho_e_Rendimento/",
    "Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/",
    "Microdados/2026/PNADC_032026.zip"), arquivo_zip, mode = "wb")
}

# posição inicial e tamanho de cada variável (input_PNADC_trimestral.txt)
layout <- list(Ano = c(1, 4), Trimestre = c(5, 1), UF = c(6, 2), UPA = c(12, 9),
               Estrato = c(21, 7), V1028 = c(50, 15), V2009 = c(104, 3),
               V4019 = c(186, 1), VD4001 = c(409, 1), VD4002 = c(410, 1),
               VD4009 = c(417, 2))

# leitura em blocos: o arquivo tem 1,8 GB e só 11 colunas interessam
conexao <- unz(arquivo_zip, "PNADC_032026.txt")
open(conexao)
blocos <- list()
repeat {
  linhas <- readLines(conexao, n = 100000)
  if (length(linhas) == 0) break
  blocos[[length(blocos) + 1]] <- as.data.table(lapply(layout, function(p)
    trimws(substr(linhas, p[1], p[1] + p[2] - 1))))
}
close(conexao)
pnad <- rbindlist(blocos)
rm(blocos, linhas)
stopifnot(all(pnad$Ano == "2026"), all(pnad$Trimestre == "3"))
pnad[, `:=`(V1028 = as.numeric(V1028), V2009 = as.integer(V2009))]

# classificação de cada pessoa em idade de trabalhar (14 anos ou mais)
pnad[, pia := as.integer(V2009 >= 14)]
pnad[, forca_trabalho := as.integer(VD4001 == "1")]
pnad[, ocupado := as.integer(VD4002 == "1")]
pnad[, desocupado := as.integer(VD4002 == "2")]
# informal (definição do IBGE): sem carteira no setor privado ou doméstico,
# empregador ou conta própria sem CNPJ e trabalhador familiar auxiliar
pnad[, informal := as.integer(ocupado == 1 & (VD4009 %in% c("02", "04", "10") |
       (VD4009 %in% c("08", "09") & V4019 == "2")))]
# formal (definição da aula): carteira assinada, militar ou estatutário,
# empregador ou conta própria com CNPJ
pnad[, formal := as.integer(ocupado == 1 & (VD4009 %in% c("01", "03", "05", "07") |
       (VD4009 %in% c("08", "09") & V4019 == "1")))]
cat("Registros lidos:", milhar(nrow(pnad)), "pessoas |",
    milhar(sum(pnad$pia)), "com 14 anos ou mais\n")

# plano amostral da PNAD Contínua, restrito à população em idade de trabalhar
options(survey.lonely.psu = "adjust")
plano <- svydesign(ids = ~UPA, strata = ~Estrato, weights = ~V1028,
                   data = pnad[pia == 1], nest = TRUE)

indicadores <- list(
  "1. Taxa de participação na força de trabalho" = c("forca_trabalho", "pia"),
  "2. Taxa de ocupação (ou emprego)"             = c("ocupado", "pia"),
  "3. Taxa de desemprego (ou desocupação)"       = c("desocupado", "forca_trabalho"),
  "4. Taxa de informalidade"                     = c("informal", "ocupado"),
  "5. Grau de formalização do emprego"           = c("formal", "ocupado"))

calcula <- function(desenho) {
  t(sapply(indicadores, function(v) {
    r <- svyratio(as.formula(paste0("~", v[1])), as.formula(paste0("~", v[2])), desenho)
    c(taxa = 100 * unname(coef(r)), ep = 100 * unname(SE(r)))
  }))
}
recortes <- list(Brasil = plano, "Distrito Federal" = subset(plano, UF == "53"))

# taxas publicadas pelo IBGE para conferência (SIDRA 4093)
sidra <- fromJSON("dados/sidra_4093_032026_brasil_df.json")[-1, ]
oficial <- function(local, variavel) as.numeric(sidra$V[sidra$D1N == local & sidra$D2C == variavel])
codigo_oficial <- c("4096", "4097", "4099", "12466", NA)

resultados <- list()
for (local in names(recortes)) {
  tabela <- calcula(recortes[[local]])
  totais <- svytotal(~forca_trabalho + ocupado + desocupado + informal + formal,
                     recortes[[local]]) / 1000
  cat("\n### ", local, " ###\n", sep = "")
  cat(sprintf("Totais estimados (mil pessoas): PIA %s | força de trabalho %s | ocupados %s\n",
      milhar(sum(weights(recortes[[local]])) / 1000),
      milhar(totais[["forca_trabalho"]]),
      milhar(totais[["ocupado"]])))
  cat(sprintf("                                desocupados %s | informais %s | formais %s\n",
      milhar(totais[["desocupado"]]),
      milhar(totais[["informal"]]),
      milhar(totais[["formal"]])))
  cat(format("Indicador", width = 46), format("Taxa (%)", width = 9, justify = "right"),
      format("IC 95%", width = 8, justify = "right"), format("IBGE (%)", width = 9, justify = "right"), "\n")
  for (i in seq_len(nrow(tabela))) {
    ref <- if (is.na(codigo_oficial[i])) "-" else decimal(oficial(local, codigo_oficial[i]), 1)
    cat(format(rownames(tabela)[i], width = 46),
        format(decimal(tabela[i, "taxa"]), width = 9, justify = "right"),
        format(paste0("±", decimal(1.96 * tabela[i, "ep"])), width = 8, justify = "right"),
        format(ref, width = 9, justify = "right"), "\n")
  }
  resultados[[local]] <- data.frame(local = local, indicador = rownames(tabela),
    taxa = round(tabela[, "taxa"], 4), erro_padrao = round(tabela[, "ep"], 4),
    ibge = sapply(codigo_oficial, function(cod) if (is.na(cod)) NA else oficial(local, cod)))
}

# composição dos ocupados pela posição na ocupação (diagrama da aula)
posicao <- c("01" = "Assalariado com carteira", "02" = "Assalariado sem carteira",
             "03" = "Assalariado com carteira", "04" = "Assalariado sem carteira",
             "05" = "Assalariado com carteira", "06" = "Setor público sem carteira",
             "07" = "Militar ou estatutário", "08" = "Empregador",
             "09" = "Autônomo (conta própria)", "10" = "Trabalhador familiar auxiliar")
plano_ocupados <- subset(plano, ocupado == 1)
plano_ocupados <- update(plano_ocupados, posicao = factor(posicao[VD4009]))
cat("\n### Composição dos ocupados por posição na ocupação (%) ###\n")
composicao <- cbind(
  Brasil = 100 * coef(svymean(~posicao, plano_ocupados)),
  DF = 100 * coef(svymean(~posicao, subset(plano_ocupados, UF == "53"))))
rownames(composicao) <- sub("^posicao", "", rownames(composicao))
composicao <- composicao[order(-composicao[, "Brasil"]), ]
cat(format("Posição na ocupação", width = 32), format("Brasil", width = 8, justify = "right"),
    format("DF", width = 8, justify = "right"), "\n")
for (i in seq_len(nrow(composicao)))
  cat(format(rownames(composicao)[i], width = 32), format(decimal(composicao[i, 1]), width = 8, justify = "right"),
      format(decimal(composicao[i, 2]), width = 8, justify = "right"), "\n")

dir.create("resultados", showWarnings = FALSE)
write.csv(do.call(rbind, resultados), "resultados/indicadores_032026.csv",
          row.names = FALSE, fileEncoding = "UTF-8")

# gráfico Brasil x Distrito Federal
taxas <- rbind(Brasil = resultados$Brasil$taxa, DF = resultados[["Distrito Federal"]]$taxa)
colnames(taxas) <- c("Participação", "Ocupação", "Desemprego", "Informalidade", "Formalização")
png("resultados/indicadores_brasil_df.png", width = 1500, height = 900, res = 150, type = "cairo")
par(mar = c(4, 4, 4, 1))
posicoes <- barplot(taxas, beside = TRUE, col = c("#1F4E9E", "#E67E22"), ylim = c(0, 100),
                    ylab = "%", main = "Indicadores do mercado de trabalho - 3º trimestre de 2026",
                    legend.text = c("Brasil", "Distrito Federal"),
                    args.legend = list(x = "topright", bty = "n"))
text(posicoes, taxas + 3, decimal(taxas, 1), cex = 0.85)
mtext(paste(aluno, "-", matricula, "| Fonte: IBGE, PNAD Contínua (microdados)"),
      side = 1, line = 2.8, cex = 0.7, col = "gray30")
invisible(dev.off())
cat("\nResultados gravados em resultados/indicadores_032026.csv e resultados/indicadores_brasil_df.png\n")
