# DataLab 9-B2 | Lucas Fiche Ungarelli Borges | RA 2021068
# Santa Catarina, PNAD Contínua, quarto trimestre de 2025.
# Fonte: SIDRA 4093. Totais em mil pessoas, já expandidos.

base <- read.csv("dados_pnad.csv", check.names = FALSE)

montar_taxas <- function(base) {
  campos <- c("pia", "ft", "ocupados", "desocupados", "informais")
  if (!is.data.frame(base) || nrow(base) != 1 ||
      !all(campos %in% names(base)))
    stop("A entrada deve conter uma linha com os cinco totais.")
  if (!all(vapply(base[campos], is.numeric, logical(1))))
    stop("As contagens devem ser numéricas.")
  v <- unlist(base[campos], use.names = TRUE)
  if (anyNA(v) || any(!is.finite(v)) || any(v < 0))
    stop("Há contagens ausentes, negativas ou não finitas.")
  with(base, {
    if (min(pia, ft, ocupados) <= 0 || ft > pia ||
        ocupados > ft || desocupados > ft || informais > ocupados)
      stop("Os grupos ou os denominadores são incompatíveis.")
    if (abs(ft - ocupados - desocupados) > 1)
      stop("A força de trabalho não confere com seus componentes.")
    quadro <- data.frame(
      indicador = c("Participação", "Ocupação", "Desocupação",
                    "Informalidade", "Formalização", "Nível de ocupação"),
      formula = c("FT / PIA", "PO / FT", "PD / FT", "PI / PO",
                  "(PO - PI) / PO", "PO / PIA"),
      numerador = c(ft, ocupados, desocupados, informais,
                    ocupados - informais, ocupados),
      denominador = c(pia, ft, ft, ocupados, ocupados, pia))
    quadro$percentual <- 100 * quadro$numerador / quadro$denominador
    quadro
  })
}

resultado <- montar_taxas(base)
exibicao <- transform(resultado, percentual = paste0(
  formatC(percentual, format = "f", digits = 2, decimal.mark = ","), "%"))

cat("DATALAB 9-B2 - SANTA CATARINA\n")
cat("Lucas Fiche Ungarelli Borges | RA 2021068\n")
cat("PNAD Contínua | 4º trimestre de 2025 | 14 anos ou mais\n\n")
cat("INDICADOR               NUMERADOR / BASE       TAXA\n")
for (i in seq_len(nrow(exibicao))) {
  linha <- exibicao[i, ]
  cat(sprintf("%-21s %7.0f / %-7.0f %8s\n", linha$indicador,
              linha$numerador, linha$denominador, linha$percentual))
}
cat("\nContagens em mil pessoas. Fonte: IBGE, SIDRA 4093.\n")
cat("Formais = ocupados - informais:",
    base$ocupados - base$informais, "mil pessoas.\n")
cat("Fora da força de trabalho:", base$pia - base$ft, "mil pessoas.\n")
cat("Ocupação e desocupação somam",
    sum(resultado$percentual[2:3]), "%.\n")
cat("Informalidade e formalização somam",
    sum(resultado$percentual[4:5]), "%.\n")
cat("O nível de ocupação usa PIA; a taxa de ocupação usa FT.\n")
write.csv(resultado, "resultados.csv", row.names = FALSE,
          fileEncoding = "UTF-8")
