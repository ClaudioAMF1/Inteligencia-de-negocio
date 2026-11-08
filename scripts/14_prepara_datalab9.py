"""Prepara os dados e perfis das duas versões do DataLab 9-B2."""
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
