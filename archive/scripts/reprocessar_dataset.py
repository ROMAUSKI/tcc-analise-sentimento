import pandas as pd
import glob
import os
import re

print("--- Iniciando Re-unificação do Dataset (Filmes) ---")

# 1. Encontrar todos os arquivos CSV
os.chdir('dados/brutos')
arquivos_csv = glob.glob('*.csv')
for arq_ignorar in ['metadata.csv', 'dataset_completo.csv', 'synthetic_dataset.csv']:
    if arq_ignorar in arquivos_csv:
        arquivos_csv.remove(arq_ignorar)

print(f"Arquivos: {arquivos_csv}")

lista_dataframes = []

# 2. Loop para ler cada arquivo
for arquivo in arquivos_csv:
    df_temp = pd.read_csv(arquivo, header=None, names=['frase'], usecols=[0])
    df_temp = df_temp.dropna(subset=['frase'])
    df_temp['frase'] = df_temp['frase'].astype(str)
    df_temp = df_temp[df_temp['frase'].str.strip() != ""]

    nome_arquivo = arquivo.split('.')[0]
    if 'positive' in nome_arquivo: df_temp['classe'] = 'Positiva'
    elif 'negative' in nome_arquivo: df_temp['classe'] = 'Negativa'
    elif 'neutral' in nome_arquivo: df_temp['classe'] = 'Neutra'
    
    if '_gemini_' in nome_arquivo: df_temp['fonte'] = 'Gemini'
    elif '_gpt_' in nome_arquivo: df_temp['fonte'] = 'ChatGPT'
    elif '_claude_' in nome_arquivo: df_temp['fonte'] = 'Claude'

    lista_dataframes.append(df_temp)

df_final = pd.concat(lista_dataframes, ignore_index=True)
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)
df_final.to_csv('../processado/dataset_completo.csv', index=False)

print(f"Total no completo: {len(df_final)}")

# 3. Limpeza e Unicidade
def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-zÀ-ÿ\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

df_final['frase_limpa'] = df_final['frase'].apply(limpar_texto)
df_final = df_final.drop_duplicates(subset=['frase_limpa']).reset_index(drop=True)
df_final = df_final[['frase_limpa', 'classe', 'fonte', 'frase']]
df_final.to_csv('../processado/synthetic_dataset.csv', index=False)

print(f"Total no synthetic_dataset (únicas): {len(df_final)}")
print(df_final['classe'].value_counts())
print(df_final.groupby(['fonte', 'classe']).size())
