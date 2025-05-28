import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa
from datetime import datetime
import os
import base64

def salvar_pdf(html_string, output_path):
    with open(output_path, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(html_string, dest=result_file)
    return not pisa_status.err

def gerar_relatorio(csv_path, base_path=None):
    """Gera relatório (HTML e PDF) a partir de um arquivo CSV"""
    if base_path is None:
        base_path = os.path.dirname(__file__)

    # Caminhos
    grafico_file_path = os.path.abspath(os.path.join(base_path, "images", "grafico.png"))
    template_path = os.path.join(base_path, "templates")
    output_html = os.path.join(base_path, "output", "relatorio.html")
    output_pdf = os.path.join(base_path, "output", "relatorio_final.pdf")

    # Leitura
    df = pd.read_csv(csv_path)

    # Estatísticas
    resumo = df.groupby("Grupo")["Valor"].agg(["mean", "std", "count"]).reset_index()
    resumo.columns = ["Grupo", "Media", "DP", "n"]

    grupos_unicos = df["Grupo"].unique()
    if len(grupos_unicos) != 2:
        raise ValueError(f"Esperado exatamente 2 grupos, mas foram encontrados: {list(grupos_unicos)}")

    grupo1_nome, grupo2_nome = grupos_unicos
    grupo1 = df[df["Grupo"] == grupo1_nome]["Valor"]
    grupo2 = df[df["Grupo"] == grupo2_nome]["Valor"]
    _, p_valor = stats.ttest_ind(grupo1, grupo2)

    # Geração do gráfico
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    sns.barplot(x="Grupo", y="Valor", data=df, ci="sd", capsize=.1, palette="Set2")
    plt.title("Comparação entre Grupos")
    plt.ylabel("Valor médio")
    plt.tight_layout()
    plt.savefig(grafico_file_path)
    plt.close()

    # Codificação em base64 da imagem
    with open(grafico_file_path, 'rb') as img_file:
        grafico_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    grafico_path = f"data:image/png;base64,{grafico_base64}"

    # Template Jinja2
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template("relatorio.html")
    grupo_mais_alto = resumo.loc[resumo["Media"].idxmax(), "Grupo"]
    grupo_mais_baixo = resumo.loc[resumo["Media"].idxmin(), "Grupo"]
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    html_rendered = template.render(
        data=data_hoje,
        resumo=resumo.to_dict(orient="records"),
        p_valor=f"{p_valor:.4f}",
        p_float=p_valor,
        grupo_mais_alto=grupo_mais_alto,
        grupo_mais_baixo=grupo_mais_baixo,
        grafico_path=grafico_path
    )

    # Salva arquivos
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_rendered)

    if not os.path.exists(grafico_file_path):
        raise FileNotFoundError(f"Imagem não encontrada: {grafico_file_path}")

    # Gera o PDF
    salvar_pdf(html_rendered, output_pdf)
    return output_pdf


# Execução direta pelo terminal
if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    csv_path = os.path.join(base_path, "data", "exemplo_dados.csv")

    try:
        caminho_pdf = gerar_relatorio(csv_path, base_path=base_path)
        print("Relatório gerado com sucesso em:", caminho_pdf)
    except Exception as e:
        print("Erro ao gerar relatório:", e)
