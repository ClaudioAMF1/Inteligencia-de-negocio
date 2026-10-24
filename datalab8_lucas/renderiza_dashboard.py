"""Gera cinco páginas do dashboard APINFO e a evidência do dataset tratado."""
import base64
import csv
import html
import json
import textwrap
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

RAIZ = Path(__file__).resolve().parent.parent
LAB = RAIZ / "datalab8_lucas"
IMAGENS = LAB / "imagens"
ENTREGA = LAB / "entrega"
DADOS = LAB / "dados"
AZUL, NAVY, ROXO, LARANJA = "#118DFF", "#09124f", "#6B007B", "#E66C37"
CINZA = "#565e69"
ALUNO = "Lucas Fiche Ungarelli Borges | RA 2021068"
PAGINAS = ["01_media_brasil", "02_cargo_destaque", "03_clt_pj", "04_extremos", "05_comparativo_estados"]


def numero(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def reais(valor, casas=2):
    return "R$ " + numero(valor, casas)


def le_csv(nome):
    with (DADOS / nome).open(encoding="utf-8-sig") as arquivo:
        return list(csv.DictReader(arquivo))


def texto(fig, x, y, conteudo, tamanho=17, cor=CINZA, negrito=False, **kwargs):
    return fig.text(x, y, conteudo, fontsize=tamanho, color=cor,
                    fontweight="bold" if negrito else "normal", va="top", parse_math=False, **kwargs)


def moldura(titulo, subtitulo, pagina):
    fig = plt.figure(figsize=(16, 9), dpi=150, facecolor="white")
    texto(fig, .05, .958, "DataLab 8-B2 | Mercado de trabalho em TI", 14, CINZA)
    texto(fig, .05, .906, titulo, 29, NAVY, True)
    texto(fig, .05, .841, subtitulo, 15)
    pacote = RAIZ / "datalab3" / "idp_ine_datalab3.pbix"
    with zipfile.ZipFile(pacote) as arq:
        with arq.open("Report/StaticResources/RegisteredResources/Logomarca_pequena_IDP4803064698123293.jpg") as img:
            logo = mpimg.imread(img, format="jpg")
    ax = fig.add_axes([.879, .847, .071, .12]); ax.imshow(logo); ax.axis("off")
    texto(fig, .05, .054, "Fonte: APINFO 2025 | Tabelas salariais | Consulta: 24/10/2026", 11)
    texto(fig, .05, .027, ALUNO, 11)
    texto(fig, .95, .027, f"{pagina}/5", 11, ha="right")
    return fig


def cartao(fig, x, valor, rotulo, detalhe, largura=.28, cor=ROXO):
    fig.add_artist(Rectangle((x, .606), largura, .17, transform=fig.transFigure,
                            facecolor="#F8FAFD", edgecolor="#DEE4ED", linewidth=1))
    texto(fig, x+.015, .754, rotulo, 15, CINZA)
    texto(fig, x+.015, .711, valor, 30, cor, True)
    texto(fig, x+.015, .644, detalhe, 12)


def estiliza(ax, horizontal=False):
    for lado in ["top", "right", "left"]: ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color("#DDE3EB")
    ax.tick_params(colors=CINZA, labelsize=13, length=0, pad=8)
    ax.grid(axis="x" if horizontal else "y", color="#E9EDF3")
    ax.set_axisbelow(True)


def pagina1(s, registros):
    fig = moldura("A. Salário médio na base nacional", "Média simples das referências publicadas por perfil e vínculo | Valores mensais nominais", 1)
    cartao(fig, .05, reais(s["media_referencias_brasil"]), "MÉDIA DAS REFERÊNCIAS", "164 valores válidos | Brasil")
    cartao(fig, .36, reais(s["media_clt_coluna_fonte"]), "COLUNA CLT DA APINFO", "83 valores | inclui uma bolsa de estágio", cor=AZUL)
    cartao(fig, .67, reais(s["media_pj"]), "COLUNA PJ DA APINFO", "81 valores | dois não publicados", cor=LARANJA)
    ax = fig.add_axes([.105,.229,.40,.29])
    ufs=["BR","PR","RS","SC"]
    valores=[]
    for uf in ufs:
        publicados=[float(r["salario_mensal_brl"]) for r in registros if r["uf"]==uf and r["salario_mensal_brl"]]
        valores.append(sum(publicados)/len(publicados))
    barras=ax.barh(range(4),valores,color=[NAVY,AZUL,AZUL,AZUL],height=.58)
    ax.set_yticks(range(4),["Brasil","PR","RS","SC"]);ax.invert_yaxis()
    ax.set_xlim(0,max(valores)*1.32)
    for i,v in enumerate(valores):ax.text(v+100,i,numero(v),va="center",fontsize=14,color=NAVY)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:numero(v/1000,0)))
    ax.set_xlabel("Média simples por tabela (R$ mil)",fontsize=14,color=CINZA,labelpad=10)
    estiliza(ax,True)
    texto(fig,.59,.535,"O que este número representa",20,NAVY,True)
    texto(fig,.59,.481,"83 perfis profissionais e 164 valores.\nCada valor publicado tem o mesmo peso.\nOs dois campos vazios de PJ não viram zero.",17,linespacing=1.6)
    texto(fig,.59,.323,"Sem a bolsa de estágio",17,NAVY,True)
    texto(fig,.59,.28,reais(s["media_sem_bolsa_estagio"]),25,ROXO,True)
    texto(fig,.59,.226,"Média de 163 referências remuneratórias.",14)
    texto(fig,.05,.132,"A APINFO não divulga contagens por perfil/vínculo nesta tabela. Portanto, este valor não é uma média\nponderada dos trabalhadores brasileiros ou dos 26.174 participantes da pesquisa.",14,linespacing=1.4)
    return fig


def pagina2(s):
    fig=moldura("B. Cargo com maior remuneração", "Ranking nacional pela média simples entre CLT e PJ do mesmo perfil",2)
    lider=s["lider"]
    cartao(fig,.05,reais(lider["media_perfil_brl"],0),"GERENTE DE TI","Maior média entre as duas modalidades")
    cartao(fig,.36,reais(lider["CLT"],0),"GERENTE DE TI | CLT","Maior referência nacional CLT",cor=AZUL)
    cartao(fig,.67,reais(lider["PJ"],0),"GERENTE DE TI | PJ","Maior referência nacional PJ",cor=LARANJA)
    top=s["top10"][:8][::-1]; y=np.arange(len(top))
    ax=fig.add_axes([.28,.193,.63,.345])
    ax.barh(y-.17,[r["CLT"] for r in top],height=.32,color=AZUL,label="CLT")
    ax.barh(y+.17,[r["PJ"] for r in top],height=.32,color=LARANJA,label="PJ")
    ax.set_yticks(y,[r["perfil"] for r in top]); ax.set_xlim(0,24000)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_:numero(x/1000,0)))
    ax.set_xlabel("Rendimento mensal (R$ mil)",fontsize=14,color=CINZA)
    ax.legend(loc="lower right",frameon=False,fontsize=14)
    estiliza(ax,True)
    texto(fig,.05,.117,"Gerente de TI lidera nos dois vínculos. O ranking compara 81 perfis com CLT e PJ publicados;\na média entre vínculos dá peso igual a cada modalidade e não mede o salário médio de todos os gerentes.",14,linespacing=1.35)
    return fig


def pagina3(s):
    fig=moldura("C. Diferença percentual entre CLT e PJ", "Comparação pareada: mesmo perfil profissional e abrangência Brasil",3)
    cartao(fig,.05,"+"+numero(s["ganho_pj_medio_pct"])+"%","GANHO PERCENTUAL MÉDIO PJ","Média dos percentuais de 81 pares")
    cartao(fig,.36,reais(s["media_clt_pares"]),"MÉDIA CLT DOS PARES","Apenas perfis com ambos os valores",cor=AZUL)
    cartao(fig,.67,reais(s["media_pj_pares"]),"MÉDIA PJ DOS PARES","Mesmos 81 perfis profissionais",cor=LARANJA)
    texto(fig,.05,.543,"Como calculei",20,NAVY,True)
    texto(fig,.05,.484,"Ganho por perfil = (PJ / CLT - 1) × 100",17,NAVY)
    texto(fig,.05,.426,"Depois, tirei a média dos 81 percentuais.\nAssistente de Informática e Estagiário\nficaram fora, pois não têm PJ publicado.",16,linespacing=1.55)
    texto(fig,.05,.287,"Outra medida, outro resultado",17,NAVY,True)
    texto(fig,.05,.24,f"Ganho entre as médias dos pares: +{numero(s['razao_das_medias_pares_pct'])}%.\nEle não é a média dos percentuais por perfil.",15,linespacing=1.5)
    selecionados={"Arquiteto de Sistemas","Desenvolvedor Full-Stack","Desenvolvedor Front-End","Desenvolvedor Back-End"}
    pares=le_csv("comparativo_clt_pj.csv")
    top=sorted([r for r in pares if r["perfil"] in selecionados],key=lambda r:float(r["ganho_pj_pct"]))
    ax=fig.add_axes([.68,.22,.255,.28]); vals=[float(r["ganho_pj_pct"]) for r in top]
    ax.barh(range(len(top)),vals,color=LARANJA,height=.6)
    ax.set_yticks(range(len(top)),[textwrap.fill(r["perfil"],22) for r in top])
    for i,v in enumerate(vals):ax.text(v+.6,i,numero(v,1)+"%",va="center",fontsize=14,color=NAVY)
    ax.set_xlim(0,max(vals)*1.2);ax.set_xlabel("PJ acima do CLT (%)",fontsize=14,color=CINZA)
    estiliza(ax,True)
    texto(fig,.53,.553,"Ganho PJ nos quatro cargos escolhidos",17,NAVY,True)
    texto(fig,.05,.118,"A diferença é nominal e descritiva. Não representa vantagem líquida do PJ: benefícios, impostos,\nférias e demais componentes da remuneração não foram convertidos em valores equivalentes.",14,linespacing=1.35)
    return fig


def pagina4(s,registros):
    fig=moldura("D. Extremos nacionais e nos estados do Sul", "Referências mensais publicadas | A bolsa de estágio é identificada separadamente do salário",4)
    cartao(fig,.05,reais(s["maior_referencia"]["salario_mensal_brl"],0),"MAIOR VALOR NO BRASIL","Gerente de TI | PJ",cor=LARANJA)
    cartao(fig,.36,reais(s["menor_referencia"]["salario_mensal_brl"],0),"MENOR VALOR NO BRASIL","Estagiário | bolsa na coluna CLT")
    cartao(fig,.67,reais(s["menor_sem_bolsa"]["salario_mensal_brl"],0),"MENOR SALÁRIO NO BRASIL","Assistente de Informática | CLT",cor=AZUL)
    ufs=["BR","PR","RS","SC"]
    extremos=[]
    for uf in ufs:
        linhas=[r for r in registros if r["uf"]==uf and r["salario_mensal_brl"]]
        extremos.append((min(linhas,key=lambda r:float(r["salario_mensal_brl"])),max(linhas,key=lambda r:float(r["salario_mensal_brl"]))))
    for x,pos,titulo,cor,xmax in [(.12,0,"Menores valores por localidade",AZUL,2500),(.62,1,"Maiores valores por localidade",LARANJA,26000)]:
        ax=fig.add_axes([x,.262,.31,.252])
        itens=[r[pos] for r in extremos];valores=[float(r["salario_mensal_brl"]) for r in itens]
        ax.barh(range(4),valores,height=.56,color=cor)
        ax.set_yticks(range(4),["Brasil","PR","RS","SC"]);ax.invert_yaxis()
        for i,v in enumerate(valores):ax.text(v+xmax*.025,i,numero(v,0),va="center",fontsize=14,color=NAVY)
        ax.set_xlim(0,xmax);ax.set_xticks([0,1000,2000] if pos==0 else [0,10000,20000])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:numero(v/1000,0)))
        ax.set_xlabel("R$ mil por mês",fontsize=14,color=CINZA);estiliza(ax,True)
        texto(fig,x-.05,.556,titulo,18,NAVY,True)
    texto(fig,.05,.19,"Os menores valores são bolsas de Estagiário. Os maiores são de Gerente de TI PJ nas quatro tabelas.",14)
    texto(fig,.05,.145,f"Base completa (BR, PR, RS, SC): máximo de {reais(s['maior_base_coletada']['salario_mensal_brl'],0)} na tabela Brasil e mínimo de {reais(s['menor_base_coletada']['salario_mensal_brl'],0)} no Paraná.\nEssas referências agregadas não são os maiores e menores pagamentos individuais do país.",14,NAVY,linespacing=1.4)
    return fig


def pagina5(s,comparativo):
    fig=moldura("E. Três estados comparados ao Brasil", "Quatro cargos presentes nas três tabelas | Referência nacional do mesmo cargo e vínculo",5)
    cargos=["Arquiteto de Sistemas","Desenvolvedor Full-Stack","Desenvolvedor Front-End","Desenvolvedor Back-End"]
    lookup={(r["cargo"],r["vinculo"],r["uf"]):r for r in comparativo}
    linhas=[];deltas=[]
    for cargo in cargos:
        for vinculo in ["CLT","PJ"]:
            br=float(lookup[(cargo,vinculo,"PR")]["referencia_brasil_brl"])
            linha=[cargo,vinculo,numero(br,0)]; ds=[]
            for uf in ["PR","RS","SC"]:
                r=lookup[(cargo,vinculo,uf)];pct=float(r["diferenca_pct"])
                linha.append(numero(float(r["salario_estado_brl"]),0)+"\n"+("+" if pct>=0 else "")+numero(pct,1)+"%")
                ds.append(pct)
            linhas.append(linha);deltas.append(ds)
    ax=fig.add_axes([.05,.25,.90,.51]);ax.axis("off")
    tab=ax.table(cellText=linhas,colLabels=["Cargo","Vínculo","Brasil (R$)","Paraná (R$)","Rio Grande do Sul (R$)","Santa Catarina (R$)"],
                 colWidths=[.27,.08,.13,.17,.18,.17],cellLoc="center",bbox=[0,0,1,1])
    tab.auto_set_font_size(False);tab.set_fontsize(14)
    for (r,c),cel in tab.get_celld().items():
        cel.set_edgecolor("#DDE3EB");cel.set_linewidth(.7)
        if r==0:cel.set_facecolor(NAVY);cel.set_text_props(color="white",weight="bold",fontsize=13)
        else:
            cel.set_facecolor("#F4F7FB" if (r-1)//2%2==0 else "white")
            if c==0:cel.set_text_props(ha="left",fontsize=14)
            if c>=3:
                d=deltas[r-1][c-3]
                cel.set_facecolor("#EAF3FD" if d>=0 else "#FCEFEA")
                cel.set_text_props(color=NAVY if d>=0 else "#9B421B")
    texto(fig,.05,.204,"Cada célula estadual mostra o valor mensal e a diferença percentual para o Brasil, no mesmo vínculo.",14)
    texto(fig,.05,.156,"As 24 referências estaduais selecionadas ficam abaixo do Brasil para o mesmo cargo e vínculo.\nSC apresenta o maior valor regional em seis dos oito pares; RS lidera em dois. O recorte não representa todo o estado.",15,NAVY,linespacing=1.4)
    return fig


def evidencia(registros,validacao):
    fig=plt.figure(figsize=(10,7.3),dpi=180,facecolor="white")
    texto(fig,.04,.96,"Construção e tratamento do dataset",23,NAVY,True)
    texto(fig,.04,.89,"APINFO 2025 | Brasil, Paraná, Rio Grande do Sul e Santa Catarina",13)
    br=[r for r in registros if r["uf"]=="PR"]
    perfis=["Arquiteto de Sistemas","Programador - Python","Estagiário"]
    bruto=[]
    for perfil in perfis:
        par=[r for r in br if r["perfil"]==perfil]
        bruto.append([par[0]["cargo"],par[0]["especialidade_original"] or "-",par[0]["valor_original"],par[1]["valor_original"] or "(vazio)"])
    texto(fig,.04,.816,"1. Recorte dos valores originais da tabela Paraná",16,NAVY,True)
    ax=fig.add_axes([.04,.586,.92,.18]);ax.axis("off")
    t=ax.table(cellText=bruto,colLabels=["Cargo","Especialidade","CLT","PJ"],colWidths=[.42,.25,.165,.165],cellLoc="left",bbox=[0,0,1,1])
    formatar_tabela(t,12)
    texto(fig,.04,.55,"2. Recorte do CSV longo após o tratamento",16,NAVY,True)
    tratado=[]
    for perfil in perfis:
        for r in br:
            if r["perfil"]==perfil:
                tratado.append([r["uf"],r["perfil"],r["vinculo_fonte"],r["salario_mensal_brl"] or "(nulo)","bolsa" if r["natureza"]=="bolsa_estagio" else "remuneração"])
    ax=fig.add_axes([.04,.237,.92,.26]);ax.axis("off")
    t=ax.table(cellText=tratado,colLabels=["UF","Perfil","Vínculo","Valor BRL","Natureza"],colWidths=[.06,.43,.10,.16,.25],cellLoc="left",bbox=[0,0,1,1]);formatar_tabela(t,11)
    texto(fig,.04,.197,"Conversões: 10.847 → 10847.0; Phyton → Python; vazio → nulo.\nA coluna CLT da linha Estagiário foi preservada e marcada como bolsa.",13,linespacing=1.5)
    texto(fig,.04,.107,f"{validacao['linhas']} linhas | {validacao['valores_validos']} valores válidos | {validacao['valores_ausentes']} ausentes | 0 chaves duplicadas",15,NAVY,True)
    texto(fig,.04,.049,"Evidência gerada a partir dos HTMLs e do CSV efetivamente processados por prepara_dados.py.",11)
    fig.savefig(IMAGENS/"00_tratamento_dataset.png",dpi=180);plt.close(fig)


def formatar_tabela(t,tamanho):
    t.auto_set_font_size(False);t.set_fontsize(tamanho)
    for (r,c),cel in t.get_celld().items():
        cel.set_edgecolor("#D9D9D9")
        if r==0:cel.set_facecolor(NAVY);cel.set_text_props(color="white",weight="bold")
        else:cel.set_facecolor("#F4F7FB" if r%2 else "white")


def exportar_html():
    titulos=["A. Média nacional","B. Cargo destaque","C. CLT e PJ","D. Extremos","E. Estados"]
    botoes="".join(f'<button role="tab" id="tab{i}" aria-controls="pagina{i}" aria-selected="{str(i==0).lower()}" onclick="mostrar({i})">{html.escape(t)}</button>' for i,t in enumerate(titulos))
    paineis="".join(f'<section id="pagina{i}" role="tabpanel" aria-labelledby="tab{i}" {"hidden" if i else ""}><img alt="{html.escape(titulos[i])}. Gráfico e resultados do DataLab 8." src="data:image/png;base64,{base64.b64encode((IMAGENS/(nome+".png")).read_bytes()).decode()}"></section>' for i,nome in enumerate(PAGINAS))
    conteudo='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DataLab 8-B2 — Lucas Fiche Ungarelli Borges</title>
<style>body{margin:0;font-family:Arial,sans-serif;background:#eef2f8;color:#09124f}header{max-width:1280px;margin:auto;padding:20px 16px 10px}h1{font-size:22px;margin:0 0 8px}p{font-size:14px;margin:8px 0}nav{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 12px}button{border:1px solid #c4cddd;border-radius:5px;padding:11px 16px;background:white;color:#09124f;font-size:14px;cursor:pointer}button[aria-selected=true]{background:#09124f;color:white}button:focus-visible{outline:3px solid #118dff;outline-offset:3px}main{max-width:1280px;margin:0 auto 24px;background:white;box-shadow:0 2px 14px #cdd4de}img{width:100%;height:auto;display:block}@media print{header{display:none}main{box-shadow:none}section[hidden]{display:block}section{break-after:page}@page{size:landscape;margin:0}}</style>
<header><h1>DataLab 8-B2 — Mercado de trabalho em TI no Brasil</h1><p>Lucas Fiche Ungarelli Borges · RA 2021068 · APINFO 2025</p><p>Use as abas ou as teclas de seta para navegar pelas cinco páginas. Valores estáticos do recorte de 24/10/2026.</p><nav role="tablist" aria-label="Perguntas do DataLab">BOTOES</nav></header><main>PAINEIS</main>
<script>let atual=0;function mostrar(n){atual=(n+5)%5;for(let i=0;i<5;i++){document.getElementById('pagina'+i).hidden=i!==atual;document.getElementById('tab'+i).setAttribute('aria-selected',String(i===atual));document.getElementById('tab'+i).tabIndex=i===atual?0:-1}}document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();mostrar(atual+(e.key==='ArrowRight'?1:-1));document.getElementById('tab'+atual).focus()}});mostrar(0);</script></html>'''.replace("BOTOES",botoes).replace("PAINEIS",paineis)
    (ENTREGA/"dashboard_datalab8.html").write_text(conteudo,encoding="utf-8")


def main():
    IMAGENS.mkdir(parents=True,exist_ok=True);ENTREGA.mkdir(parents=True,exist_ok=True)
    s=json.loads((DADOS/"indicadores.json").read_text())
    registros=le_csv("apinfo_2025.csv");comparativo=le_csv("comparativo_estados.csv")
    validacao=json.loads((DADOS/"validacao.json").read_text())
    plt.rcParams.update({"font.family":"DejaVu Sans","pdf.fonttype":42})
    with PdfPages(ENTREGA/"dashboard_datalab8.pdf",metadata={"Title":"DataLab 8-B2 - Mercado de trabalho em TI","Author":"Lucas Fiche Ungarelli Borges"}) as pdf:
        for nome,fig in zip(PAGINAS,[pagina1(s,registros),pagina2(s),pagina3(s),pagina4(s,registros),pagina5(s,comparativo)]):
            fig.savefig(IMAGENS/(nome+".png"),dpi=150,facecolor="white")
            pdf.savefig(fig,facecolor="white");plt.close(fig)
            print("Página gerada:",nome)
    evidencia(registros,validacao)
    exportar_html()
    print("Dashboard PDF, HTML navegável e evidência do dataset gerados.")


if __name__=="__main__":
    main()
