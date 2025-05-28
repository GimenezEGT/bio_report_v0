import tkinter as tk
from tkinter import filedialog, messagebox
import os
import webbrowser

# Importa a função do seu script principal
from main import gerar_relatorio


def selecionar_arquivo():
    filepath = filedialog.askopenfilename(
        title="Selecione o arquivo CSV",
        filetypes=[("Arquivos CSV", "*.csv")]
    )
    if filepath:
        entrada_csv.delete(0, tk.END)
        entrada_csv.insert(0, filepath)


def gerar():
    csv_path = entrada_csv.get()
    if not csv_path or not os.path.isfile(csv_path):
        messagebox.showerror("Erro", "Selecione um arquivo CSV válido.")
        return

    try:
        caminho_pdf = gerar_relatorio(csv_path)
        messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso em:\n{caminho_pdf}")
        # Abre o PDF gerado
        if messagebox.askyesno("Abrir PDF", "Deseja abrir o relatório agora?"):
            webbrowser.open_new(f"file://{caminho_pdf}")
    except Exception as e:
        messagebox.showerror("Erro ao gerar relatório", str(e))


# Interface
janela = tk.Tk()
janela.title("Gerador de Relatório Experimental")
janela.geometry("500x180")
janela.resizable(False, False)

# Instruções
tk.Label(janela, text="Selecione um arquivo CSV com os dados experimentais:").pack(pady=(10, 5))

# Campo e botão para seleção de arquivo
frame = tk.Frame(janela)
frame.pack(pady=5)

entrada_csv = tk.Entry(frame, width=50)
entrada_csv.pack(side=tk.LEFT, padx=(0, 5))

btn_browse = tk.Button(frame, text="Procurar", command=selecionar_arquivo)
btn_browse.pack(side=tk.LEFT)

# Botão para gerar
btn_gerar = tk.Button(janela, text="Gerar Relatório", command=gerar, bg="#4CAF50", fg="white", width=20)
btn_gerar.pack(pady=15)

# Inicia interface
janela.mainloop()
