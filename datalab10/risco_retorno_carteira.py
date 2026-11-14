# Autor: Claudio da Aparecida Meireles Filho - matrícula 2321070
# Objetivo: DataLab 10-B2 - análise da relação risco versus retorno em uma
#           carteira de investimentos em Python
# Disciplina: Inteligência de Negócio (INE) - Prof. Bruno Miranda - 2026.2S
#
# DADOS UTILIZADOS
#   Ativos   : PETR4 (Petrobras PN, petróleo e gás), VALE3 (Vale ON, mineração)
#              e ITUB4 (Itaú Unibanco PN, bancos)
#   Período  : 30 pregões, de 01/10/2026 a 13/11/2026
#   Preço    : fechamento do dia (PREULT), mercado à vista, lote padrão, em R$,
#              sem ajuste por proventos
#   Fonte    : B3 - Séries Históricas de Cotações (arquivos COTAHIST diários)
#              https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_DDDMMAAAA.ZIP
#              coletados com datalab10/coleta_cotacoes_b3.py
#
# Instalação dos pacotes usados:
#     !pip install numpy pandas matplotlib

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ALUNO = "Claudio da Aparecida Meireles Filho"
MATRICULA = "2321070"

# nome dos ativos da carteira
vetor_ativos_analisados = ['PETR4', 'VALE3', 'ITUB4']  # ativos escolhidos na B3

# datas dos 30 pregões coletados
datas = pd.to_datetime([
    '2026-10-01', '2026-10-02', '2026-10-05', '2026-10-06', '2026-10-07', '2026-10-08',
    '2026-10-09', '2026-10-13', '2026-10-14', '2026-10-15', '2026-10-16', '2026-10-19',
    '2026-10-20', '2026-10-21', '2026-10-22', '2026-10-23', '2026-10-26', '2026-10-27',
    '2026-10-28', '2026-10-29', '2026-10-30', '2026-11-03', '2026-11-04', '2026-11-05',
    '2026-11-06', '2026-11-09', '2026-11-10', '2026-11-11', '2026-11-12', '2026-11-13'])

# preço de fechamento de cada ativo (R$), na mesma ordem das datas
PETR4 = np.array([49.77, 51.17, 55.36, 53.82, 54.33, 55.48, 56.00, 56.85, 58.11, 57.36,
                  59.68, 58.00, 58.21, 57.75, 57.83, 58.68, 53.88, 52.79, 52.51, 52.20,
                  52.71, 50.71, 47.12, 45.95, 45.36, 45.19, 44.95, 43.55, 44.70, 45.30])
VALE3 = np.array([70.30, 72.10, 71.40, 70.37, 68.75, 67.64, 67.90, 67.16, 66.72, 66.42,
                  66.21, 66.36, 65.44, 64.03, 61.49, 61.90, 64.38, 63.00, 61.38, 60.05,
                  62.02, 60.25, 62.35, 62.67, 64.04, 66.11, 64.80, 64.43, 63.95, 63.50])
ITUB4 = np.array([44.15, 44.83, 49.48, 50.45, 49.11, 49.35, 50.47, 49.68, 48.98, 48.35,
                  48.09, 47.90, 48.80, 48.90, 48.00, 48.30, 41.70, 41.19, 39.78, 39.54,
                  38.69, 38.49, 39.71, 39.97, 40.53, 41.72, 41.20, 41.72, 41.68, 42.27])

# pesos da carteira: o mesmo valor investido em cada ativo
pesos = np.array([1 / 3, 1 / 3, 1 / 3])

GRAFICO = Path(__file__).resolve().parent / "imagens" / "risco_retorno.png"
pd.set_option("display.width", 120)
pd.set_option("display.float_format", lambda v: f"{v:.6f}")


def titulo(texto):
    print(f"\n### {texto} ###")


# identificação do aluno: primeira linha do console
print(f"Aluno: {ALUNO} | Matrícula: {MATRICULA}")
print("DataLab 10-B2 - Relação risco versus retorno em carteiras de investimento")
print(f"Carteira: {', '.join(vetor_ativos_analisados)} | {len(datas)} pregões, "
      f"{datas[0]:%d/%m/%Y} a {datas[-1]:%d/%m/%Y} | Fonte: B3 (COTAHIST)")

# utilizando Pandas para criar o dataframe dos ativos analisados
df = pd.DataFrame([PETR4, VALE3, ITUB4], index=vetor_ativos_analisados, columns=datas)
df_precos_ativos = df.T
df_precos_ativos.index = df_precos_ativos.index.strftime("%d/%m/%Y")
titulo("Preço de fechamento dos ativos (R$)")
print(df_precos_ativos.to_string(float_format=lambda v: f"{v:.2f}"))

# retorno diário: variação percentual do preço de um pregão para o seguinte
df_retornos = df_precos_ativos.pct_change()
titulo("Valor retorno investimento (retorno diário)")
print(df_retornos)

# retorno médio e risco (desvio-padrão dos retornos) de cada ativo
retorno_medio = df_retornos.mean()
risco = df_retornos.std()
titulo("Valor retorno médio diário")
print(retorno_medio)
titulo("Risco: desvio-padrão do retorno diário")
print(risco)

# matrizes de covariância e de correlação dos retornos
matriz_covariancia = df_retornos.cov()
titulo("Matriz de Covariância da Carteira de Investimentos")
print(matriz_covariancia)
titulo("Matriz de Correlação da Carteira de Investimentos")
print(df_retornos.corr())

# relação risco versus retorno de cada ativo
quadro = pd.DataFrame({
    "retorno_medio": retorno_medio,
    "risco": risco,
    "retorno_no_periodo": df_precos_ativos.iloc[-1] / df_precos_ativos.iloc[0] - 1,
})
titulo("Relação risco versus retorno por ativo")
print(quadro)

# carteira com pesos iguais: retorno = w . media ; risco = raiz(w' . COV . w)
retorno_carteira = float(pesos @ retorno_medio.values)
risco_carteira = float(np.sqrt(pesos @ matriz_covariancia.values @ pesos))
risco_medio_ponderado = float(pesos @ risco.values)
titulo("Carteira com pesos iguais (1/3 em cada ativo)")
print(f"Retorno médio diário da carteira : {retorno_carteira:.6f}")
print(f"Risco (desvio-padrão) da carteira: {risco_carteira:.6f}")
print(f"Média ponderada do risco dos ativos: {risco_medio_ponderado:.6f}")
print(f"Redução de risco pela diversificação: {1 - risco_carteira / risco_medio_ponderado:.2%}")

# simulação de 10.000 carteiras com pesos aleatórios para ver a fronteira risco x retorno
gerador = np.random.default_rng(2321070)
simulados = gerador.dirichlet(np.ones(len(vetor_ativos_analisados)), size=10_000)
retornos_sim = simulados @ retorno_medio.values
riscos_sim = np.sqrt(np.einsum("ij,jk,ik->i", simulados, matriz_covariancia.values, simulados))
menor_risco = riscos_sim.argmin()
maior_retorno = retornos_sim.argmax()
titulo("Simulação de 10.000 carteiras")
for nome, i in (("Carteira de menor risco", menor_risco),
                ("Carteira de maior retorno", maior_retorno)):
    composicao = ", ".join(f"{a} {p:.1%}" for a, p in zip(vetor_ativos_analisados, simulados[i]))
    print(f"{nome}: {composicao} | retorno {retornos_sim[i]:.6f} | risco {riscos_sim[i]:.6f}")

# gráfico da relação risco versus retorno
figura, eixo = plt.subplots(figsize=(10, 6.2), dpi=150)
eixo.scatter(riscos_sim * 100, retornos_sim * 100, s=6, alpha=0.35, color="#7F8C8D",
             label="10.000 carteiras simuladas")
for ativo in vetor_ativos_analisados:
    eixo.scatter(risco[ativo] * 100, retorno_medio[ativo] * 100, s=90, color="#C0392B", zorder=3)
    eixo.annotate(ativo, (risco[ativo] * 100, retorno_medio[ativo] * 100),
                  xytext=(8, 4), textcoords="offset points", fontsize=11, fontweight="bold")
eixo.scatter(risco_carteira * 100, retorno_carteira * 100, marker="*", s=260, color="#1F4E9E",
             zorder=4, label="carteira com pesos iguais")
eixo.scatter(riscos_sim[menor_risco] * 100, retornos_sim[menor_risco] * 100, marker="D", s=70,
             color="#E67E22", zorder=4, label="carteira de menor risco")
eixo.axhline(0, color="#7F8C8D", linewidth=0.8)
eixo.set_xlabel("Risco: desvio-padrão do retorno diário (%)")
eixo.set_ylabel("Retorno médio diário (%)")
eixo.set_title("Risco versus retorno - PETR4, VALE3 e ITUB4 (01/10 a 13/11/2026)")
eixo.legend(loc="lower right")
eixo.grid(alpha=0.3)
figura.text(0.01, 0.01, f"{ALUNO} - {MATRICULA} | Fonte: B3, preços de fechamento", fontsize=8,
            color="#555555")
figura.tight_layout()
GRAFICO.parent.mkdir(parents=True, exist_ok=True)
figura.savefig(GRAFICO, facecolor="white")
print(f"\nGráfico salvo em: imagens/{GRAFICO.name}")
