import streamlit as st
import pandas as pd

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
data = pd.read_excel('Data/1_1_principais_informacoes_por_regiao_2025-02-10_.xlsx')

df = pd.DataFrame(data)

# Transformando a base para formato de série temporal
df_pivot = df.pivot_table(index=["ano"], columns=["grupo", "tipo_de_informacao"], values="total")

# Exibir o resultado
print(df_pivot)
