import streamlit as st
import pandas as pd

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
data = pd.read_excel('Data/1_1_principais_informacoes_por_regiao_2025-02-10_.xlsx',decimal='.')

df = pd.DataFrame(data)

# Transformando a base para formato de série temporal
df_pivot = df.pivot_table(index=["grupo", "tipo_de_informacao"], columns="ano", values="total")

# Criando o menu suspenso para seleção do tipo de informação
tipo_info = st.selectbox("Selecione o tipo de informação:", df["tipo_de_informacao"].unique())

# Filtrando os dados conforme a seleção
df_filtrado = df_pivot.loc[(slice(None), tipo_info), :]
df_filtrado.index = df_filtrado.index.droplevel(1)  # Removendo a coluna tipo_de_informacao
# Exibindo a tabela filtrada
st.write(df_filtrado)