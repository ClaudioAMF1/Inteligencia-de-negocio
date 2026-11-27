# Claudio da Aparecida Meireles Filho | Matrícula 2321070
# Executar na pasta com os três TXT extraídos de CAGEDMOV.
meses <- c(202601, 202602, 202603)
ler_mes <- function(mes) {
  arquivo <- sprintf("CAGEDMOV%d.txt", mes)
  con <- file(arquivo, open = "rt", encoding = "UTF-8")
  on.exit(close(con))
  nomes <- strsplit(readLines(con, n = 1), ";", fixed = TRUE)[[1]]
  nomes <- tolower(iconv(nomes, to = "ASCII//TRANSLIT"))
  campos <- c("competenciamov","municipio","saldomovimentacao","sexo","salario")
  stopifnot(all(campos %in% nomes))
  partes <- list()
  repeat {
    linhas <- readLines(con, n = 50000)
    if (!length(linhas)) break
    dados <- read.table(text = linhas, sep = ";", dec = ",", quote = "",
      comment.char = "", col.names = nomes,
      colClasses = ifelse(nomes %in% campos, "numeric", "NULL"))
    partes[[length(partes)+1L]] <- subset(dados, municipio == 530010 & competenciamov == mes)
  }
  do.call(rbind, partes)
}
dados <- do.call(rbind, lapply(meses, ler_mes))
cat("Claudio da Aparecida Meireles Filho | Matrícula 2321070\nBrasília (DF) | Novo CAGED | Janeiro a março de 2026\n")
stopifnot(all(dados$saldomovimentacao %in% c(-1,1)))
mensal <- do.call(rbind, lapply(meses, function(m) {
  x <- subset(dados, competenciamov == m)
  a <- sum(x$saldomovimentacao == 1)
  d <- sum(x$saldomovimentacao == -1)
  data.frame(mes=m, admissoes=a, desligamentos=d, saldo=a-d)
}))
print(mensal, row.names=FALSE)
cat("Saldo trimestral:", sum(mensal$saldo), "\n")
admitidos <- subset(dados, saldomovimentacao == 1 & salario > 0 & is.finite(salario))
medias <- tapply(admitidos$salario, factor(admitidos$sexo, levels=c(3,1),
  labels=c("Feminino","Masculino")), mean)
print(round(medias,2))
cat("Diferença percentual sobre a menor média:", round(100*(max(medias)/min(medias)-1),2), "%\n")
cat("Variação dos desligamentos entre meses:", diff(mensal$desligamentos), "\n")
cat("Mês com mais desligamentos:", mensal$mes[which.max(mensal$desligamentos)], "\n")
