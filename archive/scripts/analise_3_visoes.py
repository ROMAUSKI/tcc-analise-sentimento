import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, accuracy_score
import os
import re

# Configurações
SEED = 42
MAX_FEATURES = 5000

def limpar_texto(texto):
    if not isinstance(texto, str): return ""
    texto = texto.lower()
    texto = re.sub(r'[^a-zÀ-ÿ\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

def load_real_data(path, nrows=100000):
    print(f"Carregando dados reais de {path}...")
    df = pd.read_csv(path, nrows=nrows)
    
    def mapper(rating):
        if rating >= 4: return 'Positiva'
        elif rating <= 2: return 'Negativa'
        else: return 'Neutra'
    
    df['classe'] = df['rating'].apply(mapper)
    df = df[['review_text', 'classe']].dropna()
    df.columns = ['texto', 'classe']
    
    df['texto'] = df['texto'].apply(limpar_texto)
    df = df[df['texto'] != ""]
    
    counts = df['classe'].value_counts()
    print(f"Contagem real original:\n{counts}")
    min_size = counts.min()
    
    # Balanceamento manual para evitar problemas de índice
    df_pos = df[df['classe'] == 'Positiva'].sample(min_size, random_state=SEED)
    df_neg = df[df['classe'] == 'Negativa'].sample(min_size, random_state=SEED)
    df_neu = df[df['classe'] == 'Neutra'].sample(min_size, random_state=SEED)
    
    df_balanced = pd.concat([df_pos, df_neg, df_neu]).sample(frac=1, random_state=SEED).reset_index(drop=True)
    return df_balanced

def run_vision(X_train, y_train, X_test, y_test, vision_name):
    print(f"\n--- {vision_name} ---")
    results = []
    models = {
        'Naive Bayes': MultinomialNB(),
        'SVM Linear': LinearSVC(random_state=SEED, max_iter=5000),
        'Reg. Logística': LogisticRegression(random_state=SEED, max_iter=1000)
    }
    
    vectorizer = TfidfVectorizer(max_features=MAX_FEATURES, ngram_range=(1,2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    for name, model in models.items():
        model.fit(X_train_vec, y_train)
        y_pred = model.predict(X_test_vec)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        print(f"{name}: Acc={acc:.2%}, F1={f1:.2%}")
        results.append({'Modelo': name, 'Visão': vision_name, 'Acurácia': acc, 'F1-Score': f1})
    
    return results

# 1. Carregar Datasets
print("Carregando dataset sintético...")
df_sintetico = pd.read_csv('dados/processado/synthetic_dataset.csv')

path_real = 'src/dados_reais/utlc_movies.csv'
if os.path.exists(path_real):
    df_real = load_real_data(path_real)
    print(f"Dataset real balanceado: {len(df_real)} amostras ({len(df_real)//3} por classe)")

    # VISÃO 1: Real -> Real (Split 80/20 do Real)
    R_train, R_test = train_test_split(df_real, test_size=0.2, stratify=df_real['classe'], random_state=SEED)
    res_v1 = run_vision(R_train['texto'], R_train['classe'], R_test['texto'], R_test['classe'], "Visão 1: Real -> Real")

    # VISÃO 2: Sintético -> Sintético (Split 80/20 do Sintético)
    S_train, S_test = train_test_split(df_sintetico, test_size=0.2, stratify=df_sintetico['classe'], random_state=SEED)
    res_v2 = run_vision(S_train['frase_limpa'], S_train['classe'], S_test['frase_limpa'], S_test['classe'], "Visão 2: Sintético -> Sintético")

    # VISÃO 3: Sintético -> Real (Train 100% Sintético, Test 100% Real Amostrado)
    res_v3 = run_vision(df_sintetico['frase_limpa'], df_sintetico['classe'], df_real['texto'], df_real['classe'], "Visão 3: Sintético -> Real")

    # Consolidar
    df_res = pd.DataFrame(res_v1 + res_v2 + res_v3)
    df_res.to_csv('resultados/analise_3_visoes_movies.csv', index=False)
    print("\nAnálise concluída e salva em resultados/analise_3_visoes_movies.csv")
else:
    print(f"ERRO: Arquivo {path_real} não encontrado para a Visão 1 e 3.")
