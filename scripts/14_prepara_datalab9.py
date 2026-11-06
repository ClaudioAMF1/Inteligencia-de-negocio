"""Prepara os recortes oficiais e os scripts R das duas versões do DataLab 9-B2."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "datalab9/fontes"
PROFILES = [
    ("datalab9", "Claudio da Aparecida Meireles Filho", "2321070", "53", "DF"),
    ("datalab9_lucas", "Lucas Fiche Ungarelli Borges", "2021068", "42", "SC"),
]
VARIABLES = {"pia": "1641", "ft": "4088", "ocupados": "4090",
             "desocupados": "4092", "informais": "4723"}

R_CODE = '''# DataLab 9-B2 - Indicadores do mercado de trabalho
# Aluno: @NAME@
# Matrícula: @RA@
# Fonte: IBGE, PNAD Contínua, SIDRA 4093; 4º trimestre de 2025.
# Recorte: @STATE@; sexo total; pessoas de 14 anos ou mais.
# Estimativas expandidas em MIL PESSOAS, já ponderadas pelo IBGE.
# Dados de entrada e resposta original da API acompanham a entrega.

aluno <- "@NAME@"
matricula <- "@RA@"
local <- "@STATE@"
dados <- c(pia = @PIA@, ft = @FT@, ocupados = @OCUPADOS@,
           desocupados = @DESOCUPADOS@, informais = @INFORMAIS@)

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
cat("DATALAB 9-B2 | INDICADORES DO MERCADO DE TRABALHO\\n")
cat("Aluno:", aluno, "\\nMatrícula:", matricula, "\\n")
cat("Recorte:", local, "| 4º trimestre de 2025 | sexo total\\n")
cat("Fonte: IBGE / PNAD Contínua / SIDRA 4093\\n")
cat("Ambiente:", R.version.string, "\\n\\n")
cat("TOTAIS DE ENTRADA (mil pessoas)\\n")
for (nome in names(dados))
  cat(sprintf("  %-14s %8.0f\\n", nome, dados[nome]))
cat(sprintf("  %-14s %8.0f\\n", "formais*",
            dados["ocupados"] - dados["informais"]))
cat("* Formais calculados por PO - PI.\\n\\n")
cat("INDICADORES (fórmulas multiplicadas por 100)\\n")
for (i in seq_len(nrow(resultado))) {
  cat(sprintf("%s %6s %%\\n", format(resultado$indicador[i], width = 34),
              fmt(resultado$percentual[i])))
}
cat("\\nChecagens: totais coerentes; denominadores positivos.\\n")
cat("Ocupação + desocupação:", fmt(sum(resultado$percentual[2:3])), "%\\n")
cat("Informalidade + formalização:",
    fmt(sum(resultado$percentual[4:5])), "%\\n")
cat("Nota: percentuais recalculados sobre totais arredondados.\\n")
cat("Taxa de ocupação usa FT; nível da ocupação usa PIA.\\n")
write.csv(resultado, "resultados.csv", row.names = FALSE,
          fileEncoding = "UTF-8")
'''


def main():
    source_path = SOURCE / "sidra_4093_2025t4_df_sc.json"
    raw = json.loads(source_path.read_text(encoding="utf-8"))[1:]
    for folder, name, ra, uf, initials in PROFILES:
        rows = [r for r in raw if r["D1C"] == uf]
        assert len(rows) == 10
        assert all(r["D4C"] == "6794" and r["D3C"] == "202504" for r in rows)
        by_id = {r["D2C"]: r for r in rows}
        state = rows[0]["D1N"]
        vals = {key: int(by_id[code]["V"]) for key, code in VARIABLES.items()}
        assert all(by_id[code]["MN"] == "Mil pessoas" for code in VARIABLES.values())
        dest = ROOT / folder
        dest.mkdir(exist_ok=True)
        with (dest / "dados_pnad.csv").open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["uf", "periodo", "sexo", "unidade", *VARIABLES])
            writer.writerow([state, "2025T4", "Total", "Mil pessoas", *vals.values()])
        code = R_CODE.replace("@NAME@", name).replace("@RA@", ra).replace("@STATE@", state)
        for key, value in vals.items():
            code = code.replace(f"@{key.upper()}@", str(value))
        (dest / "indicadores_mercado_trabalho.R").write_text(code, encoding="utf-8")
        profile = dict(nome=name, matricula=ra, uf=uf, sigla=initials, estado=state,
                       periodo="4º trimestre de 2025", totais=vals,
                       referencia_ibge={"participacao": float(by_id["4096"]["V"]),
                                        "nivel_ocupacao": float(by_id["4097"]["V"]),
                                        "desocupacao": float(by_id["4099"]["V"]),
                                        "informalidade": float(by_id["12466"]["V"])})
        (dest / "perfil.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2)+"\n")
        print(folder, state, vals)
    metadata = dict(fonte="IBGE / PNAD Contínua trimestral / SIDRA 4093",
                    consulta=(SOURCE / "consulta_url.txt").read_text().strip(),
                    data_acesso="2026-11-06", periodo="202504", sexo="6794 (Total)",
                    unidade_contagens="Mil pessoas", variaveis=VARIABLES,
                    sha256_resposta=hashlib.sha256(source_path.read_bytes()).hexdigest(),
                    notas="Estimativas já expandidas. Não aplicar pesos novamente. "
                          "Os totais publicados são arredondados; as taxas recalculadas "
                          "podem diferir na última casa das taxas divulgadas pelo IBGE.")
    (SOURCE / "proveniencia.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n")


if __name__ == "__main__":
    main()
