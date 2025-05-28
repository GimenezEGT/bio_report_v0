import streamlit as st
import pandas as pd
from main import gerar_relatorio
import tempfile
import os

st.set_page_config(page_title="Gerador de Relatório Experimental", layout="centered")

st.title("📊 Gerador de Relatório Experimental")
st.write("Envie um arquivo CSV com os dados dos grupos experimentais (colunas: 'Grupo' e 'Valor').")

uploaded_file = st.file_uploader("📁 Enviar CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Pré-visualização dos dados:")
        st.dataframe(df)

        if st.button("Gerar Relatório"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                uploaded_file.seek(0)
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                caminho_pdf = gerar_relatorio(tmp_path)
                with open(caminho_pdf, "rb") as f:
                    st.success("✅ Relatório gerado com sucesso!")
                    st.download_button("📥 Baixar Relatório PDF", f, file_name="relatorio_experimental.pdf")
            except Exception as e:
                st.error(f"❌ Erro ao gerar o relatório: {e}")
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
