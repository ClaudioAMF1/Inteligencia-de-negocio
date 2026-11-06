# DataLab 9-B2 - Indicadores do mercado de trabalho
# Aluno: Claudio da Aparecida Meireles Filho
# Matrícula: 2321070
# Fonte: IBGE, PNAD Contínua, SIDRA 4093; 4º trimestre de 2025.
# Recorte: Distrito Federal; sexo total; pessoas de 14 anos ou mais.
# Estimativas expandidas em MIL PESSOAS, já ponderadas pelo IBGE.
# Dados de entrada e resposta original da API acompanham a entrega.

aluno <- "Claudio da Aparecida Meireles Filho"
matricula <- "2321070"
local <- "Distrito Federal"
dados <- c(pia = 2489, ft = 1670, ocupados = 1557,
           desocupados = 113, informais = 422)

calcular_indicadores <- function(x) {
  campos <- c("pia", "ft", "ocupados", "desocupados", "informais")
  if (!is.numeric(x) || !all(campos %in% names(x)))
    stop("Informe os cinco totais numéricos com os nomes esperados.")
  x <- x[campos]
  if (any(!is.finite(x)) || any(x < 0))
    stop("Os totais devem ser finitos e não negativos.")
  if (any(x[c("pia", "ft", "ocupados")] == 0))
    stop("Os denominadores precisam ser maiores que zero.")
  if (x["ft"] > x["pia"] || x["ocupados"] > x["ft"] ||
      x["informais"] > x["ocupados"] || x["desocupados"] > x["ft"])
    stop("Totais incompatíveis com os grupos populacionais.")
  # Tolerância de mil pessoas: arredondamento dos totais publicados.
  if (abs(x["ft"] - x["ocupados"] - x["desocupados"]) > 1)
    stop("Força de trabalho deve ser ocupados + desocupados.")
  formais <- x["ocupados"] - x["informais"]
  taxas <- c(x["ft"] / x["pia"], x["ocupados"] / x["ft"],
             x["desocupados"] / x["ft"], x["informais"] / x["ocupados"],
             formais / x["ocupados"], x["ocupados"] / x["pia"]) * 100
  data.frame(
    indicador = c("Participação na força de trabalho", "Taxa de ocupação",
                  "Taxa de desocupação", "Taxa de informalidade",
                  "Grau de formalização",
                  "Nível da ocupação (complementar)"),
    formula = c("FT / PIA", "PO / FT", "PD / FT", "PI / PO",
                "(PO - PI) / PO", "PO / PIA"),
    percentual = unname(taxas), stringsAsFactors = FALSE)
}

# Taxa de ocupação (PO/FT) difere do nível da ocupação (PO/PIA).
# Formalização: complemento da proxy de informalidade do IBGE.
# Informais: sem carteira (privado/doméstico), conta própria/empregador
# sem CNPJ e trabalhador familiar auxiliar. Não é só carteira assinada.
resultado <- calcular_indicadores(dados)
fmt <- function(x)
  formatC(x, digits = 2, format = "f", decimal.mark = ",")
cat("DATALAB 9-B2 | INDICADORES DO MERCADO DE TRABALHO\n")
cat("Aluno:", aluno, "\nMatrícula:", matricula, "\n")
cat("Recorte:", local, "| 4º trimestre de 2025 | sexo total\n")
cat("Fonte: IBGE / PNAD Contínua / SIDRA 4093\n")
cat("Ambiente:", R.version.string, "\n\n")
cat("TOTAIS DE ENTRADA (mil pessoas)\n")
for (nome in names(dados))
  cat(sprintf("  %-14s %8.0f\n", nome, dados[nome]))
cat(sprintf("  %-14s %8.0f\n", "formais*",
            dados["ocupados"] - dados["informais"]))
cat("* Formais calculados por PO - PI.\n\n")
cat("INDICADORES (fórmulas multiplicadas por 100)\n")
for (i in seq_len(nrow(resultado))) {
  cat(sprintf("%s %6s %%\n", format(resultado$indicador[i], width = 34),
              fmt(resultado$percentual[i])))
}
cat("\nChecagens: totais coerentes; denominadores positivos.\n")
cat("Ocupação + desocupação:", fmt(sum(resultado$percentual[2:3])), "%\n")
cat("Informalidade + formalização:",
    fmt(sum(resultado$percentual[4:5])), "%\n")
cat("Nota: percentuais recalculados sobre totais arredondados.\n")
cat("Taxa de ocupação usa FT; nível da ocupação usa PIA.\n")
write.csv(resultado, "resultados.csv", row.names = FALSE,
          fileEncoding = "UTF-8")
