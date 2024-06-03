import streamlit as st
import pandas as pd
import sqlite3

# #conexao e selecao de dados no banco
conn = sqlite3.connect('../transform/quotes.db')
df = pd.read_sql_query("SELECT * FROM mercadolivre_mangas", conn)


st.title('Pesquisa de Mercado - Mangás no Mercado Livre')

st.subheader('KPIs principais do sistema')
col1, col2, col3, col4 = st.columns(4)

#total de mangás
total_items = df.shape[0]
col1.metric(label='Número total de produtos', value=total_items)

#preco medio dos mangás
preco_medio = df['preco_total'].mean()
col2.metric(label='Preço médio (R$)', value=f"{preco_medio:.2f}")
st.write(df)

#manga mais caro
titulo_preco_max = df['preco_total'].max()
col3.metric(label='Produto mais caro (R$)', value=titulo_preco_max)

titulo_preco_min = df['preco_total'].min()
col4.metric(label='Produto mais barato (R$)', value=titulo_preco_min)

# Top 50 avaliados
st.subheader('Top 100 - Satisfação por produto')
col1, col2 = st.columns([7,1])
avaliacao_filtrada = df[df['avaliacao'] > 0]
titulo_avaliado = avaliacao_filtrada.groupby('titulo')['avaliacao'].mean().sort_values(ascending=False).head(100)

col1.write(titulo_avaliado)

conn.close()


