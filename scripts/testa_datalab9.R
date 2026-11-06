# Valida o cálculo dos indicadores e os recortes de DF e SC.
# Execute da raiz: Rscript scripts/testa_datalab9.R
raiz <- normalizePath(".")
temporario <- tempfile("teste_datalab9_")
dir.create(temporario)
setwd(temporario)
casos <- 0L
confere <- function(condicao) {
  stopifnot(condicao)
  casos <<- casos + 1L
}
falha <- function(expr) inherits(tryCatch(expr, error = identity), "error")
for (pasta in c("datalab9", "datalab9_lucas")) {
  ambiente <- new.env()
  invisible(capture.output(sys.source(
    file.path(raiz, pasta, "indicadores_mercado_trabalho.R"), ambiente)))
  calc <- ambiente$calcular_indicadores
  exemplo <- c(pia=1000, ft=600, ocupados=540, desocupados=60, informais=180)
  esperado <- c(60, 90, 10, 100/3, 200/3, 54)
  confere(max(abs(calc(exemplo)$percentual - esperado)) < 1e-10)
  for (campo in c("pia", "ft", "ocupados")) {
    x <- exemplo; x[campo] <- 0
    confere(falha(calc(x)))
  }
  for (valor in c(NA, Inf, -1)) {
    x <- exemplo; x["informais"] <- valor
    confere(falha(calc(x)))
  }
  confere(falha(calc(exemplo[-1])))
  confere(falha(calc(as.character(exemplo))))
  x <- exemplo; x["informais"] <- 541
  confere(falha(calc(x)))
  x <- exemplo; x["pia"] <- 599
  confere(falha(calc(x)))
  x <- exemplo; x["desocupados"] <- 62
  confere(falha(calc(x)))
  x["desocupados"] <- 61
  confere(all(is.finite(calc(x)$percentual)))
  x <- exemplo; x["informais"] <- 0
  confere(identical(calc(x)$percentual[4:5], c(0, 100)))
  x["informais"] <- x["ocupados"]
  confere(identical(calc(x)$percentual[4:5], c(100, 0)))
  entrada <- read.csv(file.path(raiz, pasta, "dados_pnad.csv"))
  confere(identical(unname(ambiente$dados),
                   as.numeric(entrada[1, names(ambiente$dados)])))
  r <- ambiente$resultado$percentual
  referencia <- if (pasta == "datalab9") c(67.1, 62.5, 6.8, 27.1)
                else c(67.9, 66.4, 2.2, 25.7)
  # Contagens em mil pessoas são arredondadas; taxas oficiais têm 1 casa.
  confere(max(abs(r[c(1,6,3,4)] - referencia)) < 0.1)
  confere(abs(sum(r[2:3]) - 100) < 1e-10)
  confere(abs(sum(r[4:5]) - 100) < 1e-10)
  cat(pasta, ": cálculos, limites e dados oficiais conferidos.\n")
}
setwd(raiz)
unlink(temporario, recursive = TRUE)
cat(casos, "checagens aprovadas.\n")
