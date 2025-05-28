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
grafico_path = os.path.join(base_path, "images", "grafico.png")
template_path = os.path.join(base_path, "templates")
output_html = os.path.join(base_path, "output", "relatorio.html")
output_pdf = os.path.join(base_path, "output", "relatorio.pdf")

# Cria pastas se necessário
os.makedirs(os.path.dirname(output_html), exist_ok=True)
os.makedirs(os.path.dirname(grafico_path), exist_ok=True)

# Leitura de dados
df = pd.read_csv(csv_path)

# Estatísticas descritivas
resumo = df.groupby("Grupo")["Valor"].agg(["mean", "std", "count"]).reset_index()
resumo.columns = ["Grupo", "Media", "DP", "n"]

# Verifica grupos únicos
grupos_unicos = df["Grupo"].unique()
if len(grupos_unicos) != 2:
    raise ValueError(f"Esperado exatamente 2 grupos, mas encontrados: {list(grupos_unicos)}")

grupo1_nome, grupo2_nome = grupos_unicos
grupo1 = df[df["Grupo"] == grupo1_nome]["Valor"]
grupo2 = df[df["Grupo"] == grupo2_nome]["Valor"]

# Teste t de Student
stat, p_valor = stats.ttest_ind(grupo1, grupo2)

# Geração do gráfico
sns.set(style="whitegrid")
plt.figure(figsize=(6, 4))
sns.barplot(x="Grupo", y="Valor", data=df, ci="sd", capsize=.1, palette="Set2")
plt.title("Comparação entre Grupos")
plt.ylabel("Valor médio")
plt.tight_layout()
plt.savefig(grafico_path)
plt.close()

# Converte imagem para base64
with open(grafico_path, "rb") as img_file:
    grafico_base64 = base64.b64encode(img_file.read()).decode('utf-8')
grafico_embutido = f"data:image/png;base64,{grafico_base64}"

# Renderização do template
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
    grafico_path=grafico_embutido
)

# Salva HTML
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_rendered)

# Gera PDF
HTML(string=html_rendered, base_url=base_path).write_pdf(output_pdf)

print("Relatório gerado com sucesso:")
print("HTML:", output_html)
print("PDF:", output_pdf)
