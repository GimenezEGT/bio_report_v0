
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
import os
import base64

# Caminhos
base_path = os.path.dirname(__file__)
csv_path = os.path.join(base_path, "data", "exemplo_dados.csv")
grafico_file_path = os.path.abspath(os.path.join(base_path, "images", "grafico.png"))
grafico_url_path = "file://" + grafico_file_path.replace("\\", "/")
print("Grafico path URL:", grafico_url_path)
with open(grafico_file_path, 'rb') as img_file:
    grafico_base64 = base64.b64encode(img_file.read()).decode('utf-8')
grafico_path = f"data:images/png;base64,{grafico_base64}"
template_path = os.path.join(base_path, "templates")
output_html = os.path.join(base_path, "output", "relatorio.html")
output_pdf = os.path.join(base_path, "output", "relatorio_final.pdf")

# Leitura
df = pd.read_csv(csv_path)

# Estatísticas
resumo = df.groupby("Grupo")["Valor"].agg(["mean", "std", "count"]).reset_index()
resumo.columns = ["Grupo", "Media", "DP", "n"]
# Detecta automaticamente os grupos únicos
grupos_unicos = df["Grupo"].unique()

# Verifica se há exatamente 2 grupos para aplicar o t-test
if len(grupos_unicos) != 2:
    raise ValueError(f"Esperado exatamente 2 grupos, mas foram encontrados: {list(grupos_unicos)}")

grupo1_nome, grupo2_nome = grupos_unicos

# Separa os dados de cada grupo
grupo1 = df[df["Grupo"] == grupo1_nome]["Valor"]
grupo2 = df[df["Grupo"] == grupo2_nome]["Valor"]

# Teste t de Student
if len(grupos_unicos) != 2:
    raise ValueError(
        f"O teste t requer exatamente 2 grupos. Foram encontrados {len(grupos_unicos)}: {list(grupos_unicos)}. "
        "Por favor, verifique sua tabela CSV."
    )
else:
    _, p_valor = stats.ttest_ind(grupo1, grupo2)

# Gráfico
sns.set(style="whitegrid")
plt.figure(figsize=(6, 4))
sns.barplot(x="Grupo", y="Valor", data=df, ci="sd", capsize=.1, palette="Set2")
plt.title("Comparação entre Grupos")
plt.ylabel("Valor médio")
plt.tight_layout()
plt.savefig(grafico_file_path)
plt.close()

# Template
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
# Salva o HTML e gera o PDF
if not os.path.exists(os.path.dirname(output_html)):
    os.makedirs(os.path.dirname(output_html))
if not os.path.exists(os.path.dirname(output_pdf)):
    os.makedirs(os.path.dirname(output_pdf))
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_rendered)
if not os.path.exists(grafico_file_path):
    raise FileNotFoundError(f"Imagem não encontrada: {grafico_file_path}")
# Gera o PDF a partir do HTML
HTML(string=html_rendered, base_url=base_path).write_pdf(output_pdf)
print("Relatório gerado com sucesso em:", output_pdf)
