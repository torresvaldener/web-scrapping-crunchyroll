import pandas as pd
import sqlite3 
from datetime import datetime

df = pd.read_json('data.jsonl', lines=True)

# print(df)
# pd.options.display.max_columns = None
df['_source'] = 'https://lista.mercadolivre.com.br/mang%C3%A1-livro'
df['_data_coleta'] = datetime.now()

# #tratando as strings para float
df['preco'] = df['preco'].fillna(0).astype(float)
df['preco_centavos'] = df['preco_centavos'].fillna(0).astype(float)
df['avaliacao'] = df['avaliacao'].fillna(0).astype(float)

# #regex para retirar as avaliacoes entre parenteses
df['avaliacao_quantidade'] = df['avaliacao_quantidade'].str.replace(r'\(|\)', '', regex=True)
df['avaliacao_quantidade'] = df['avaliacao_quantidade'].fillna(0).astype(int)


df['preco_total'] = df['preco'] + df['preco_centavos'] / 100

# #conexao banco de dados sqlite
conn = sqlite3.connect('quotes.db')
df.to_sql('mercadolivre_mangas', conn, if_exists='replace', index=False)
conn.close()