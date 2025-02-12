import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


# Criar guias
titulos_guias = ['Panorama Mundial', 'Consumo de energia elétrica ', 'Tópico C']
guia1, guia2, guia3 = st.tabs(titulos_guias)
 
# Adicionar conteúdo a cada guia
with guia1:
    data = pd.read_excel('Data/1_1_principais_informacoes_por_regiao_2025-02-10_.xlsx',decimal='.')
    df = pd.DataFrame(data)
# Transformando a base para formato de série temporal
    df_pivot = df.pivot_table(index=["grupo", "tipo_de_informacao"], columns="ano", values="total")
    st.header('Panorama Mundial')
    # Criando o menu suspenso para seleção do tipo de informação
    tipo_info = st.selectbox("Selecione o tipo de informação:", df["tipo_de_informacao"].unique())

# Criando a flag para exibir valores absolutos ou percentuais
    exibir_percentual = st.checkbox(
    "Usar valores percentuais",  # Texto do checkbox
    value=False,  # Valor padrão (False = valores absolutos)
    key="usar_percentuais"  # Chave única para evitar conflitos
)

# Filtrando os dados conforme a seleção
    df_filtrado = df_pivot.loc[(slice(None), tipo_info), :]
    df_filtrado.index = df_filtrado.index.droplevel(1)  # Removendo a coluna tipo_de_informacao

# Criando a tabela com variação percentual em relação ao ano anterior
    df_percentual = df_filtrado.pct_change(axis=1) * 100

# Definindo qual tabela exibir
    if exibir_percentual:
        st.write("### Variação Percentual em Relação ao Ano Anterior (%)")
        st.write(df_percentual)
        df_plot = df_percentual.T.reset_index()
    else:
        st.write("### Valores Absolutos")
        st.write(df_filtrado)
        df_plot = df_filtrado.T.reset_index()

    # Criando o gráfico de linhas com Plotly
    #df_plot = df_filtrado.T.reset_index()  # Transforma os anos em uma coluna "ano"
    fig = px.line(df_plot, x="ano", y=df_plot.columns, title=f"Evolução de {tipo_info}", markers=True)
    st.plotly_chart(fig)
    st.write('Fonte: U.S. Energy Information Administration (EIA) - dados acessados em 19/04/2024; América do Sul: para o Brasil, Balanço Energético Nacional 2024 (EPE).')

 
with guia2:
    data = pd.read_excel('Data/1_2_consumo_energia_eletrica_10_paises_2025-02-10_.xlsx',decimal='.')
    df = pd.DataFrame(data)
    df_pivot = df.pivot(index="grupo", columns="ano", values="total")
# Exibir resultado
    st.header('Consumo de energia elétrica - 10 maiores países')
    st.write('Conteúdo do tópico B')
    #st.write(df_pivot)
    df_pivot['Total Acumulado Calculado'] = df_pivot.sum(axis=1)

# Sorting by the calculated total and getting the top 2
    top_10_calculated = df_pivot.sort_values('Total Acumulado Calculado', ascending=False).head(10)
    # Botão para selecionar entre valores absolutos e percentuais
    tipo_visualizacao = st.checkbox("Exibir valores percentuais")
# Função para calcular valores percentuais
    def calcular_percentuais(df):
        return df.pct_change(axis=1) * 100  # Converte para percentual

# Aplicar a seleção do usuário
    if tipo_visualizacao:
        df_top_10 = calcular_percentuais(top_10_calculated.drop(columns=['Total Acumulado Calculado']))
    else:
        df_top_10 = top_10_calculated.drop(columns=['Total Acumulado Calculado'])

# Exibir os dados selecionados
    st.write(df_top_10)

    # Gráfico de linhas com marcadores
    st.subheader(f'Gráfico de Linhas - Consumo de Energia por Ano ({tipo_visualizacao})')
    fig_line = px.line(df_top_10.T,
                    x=df_top_10.columns,
                    y=df_top_10.index,
                    labels={'x': 'Ano', 'value': 'Consumo de Energia'},
                    title=f'Consumo de Energia Elétrica por Ano ({tipo_visualizacao})',
                    markers=True)  # Adiciona marcadores
    st.plotly_chart(fig_line)


 
with guia3:
    st.header('Tópico C')
    st.write('Conteúdo do tópico C')