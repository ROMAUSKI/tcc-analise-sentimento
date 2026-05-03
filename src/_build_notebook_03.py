"""Script temporário para gerar src/03_movies_3_visoes.ipynb a partir das células abaixo.
Após gerar, este script é deletado."""

import nbformat as nbf
import os

nb = nbf.v4.new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.10"}
}

# ============================================================
# CÉLULA 1 — Setup padrão (template idêntico a todos notebooks)
# ============================================================
cell1 = '''# ============================================================
# CÉLULA 1 — SETUP PADRÃO (idêntica em todos os notebooks)
# ============================================================
import os, sys, shutil, re, glob
import numpy as np
import pandas as pd

# Reprodutibilidade
SEED = 42
np.random.seed(SEED)

# Detecção de ambiente
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    if not os.path.exists('/content/tcc-analise-sentimento'):
        os.system('git clone https://github.com/ROMAUSKI/tcc-analise-sentimento.git /content/tcc-analise-sentimento')
    else:
        os.system('cd /content/tcc-analise-sentimento && git pull')
    BASE_DIR = '/content/tcc-analise-sentimento'
    REAL_DATA_PATH = '/content/sample_data/dataset_real_sentimentos'
else:
    BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), '..'))
    REAL_DATA_PATH = os.path.join(BASE_DIR, 'src', 'dados_reais')

# Dataset real via kagglehub (baixa só na 1ª vez)
if not os.path.exists(REAL_DATA_PATH) or not os.listdir(REAL_DATA_PATH):
    import kagglehub
    print("Baixando dataset real do Kaggle (~877 MB, só na 1ª vez)...")
    cache_path = kagglehub.dataset_download("fredericods/ptbr-sentiment-analysis-datasets")
    os.makedirs(REAL_DATA_PATH, exist_ok=True)
    for f in os.listdir(cache_path):
        shutil.copy(os.path.join(cache_path, f), os.path.join(REAL_DATA_PATH, f))
    print(f"Dataset real disponível em: {REAL_DATA_PATH}")
else:
    print(f"Dataset real já existe em: {REAL_DATA_PATH}")

# Caminhos do projeto
DADOS_BRUTOS_MOVIES = os.path.join(BASE_DIR, 'dados', 'brutos')
DADOS_BRUTOS_APPS   = os.path.join(BASE_DIR, 'dados', 'brutos_apps')
DADOS_PROCESSADO    = os.path.join(BASE_DIR, 'dados', 'processado')
RESULTADOS          = os.path.join(BASE_DIR, 'resultados')

print(f"Ambiente: {'Colab' if IN_COLAB else 'Local'}")
print(f"BASE_DIR: {BASE_DIR}")
'''

# ============================================================
# CÉLULA 2 — Markdown explicando o objetivo
# ============================================================
cell2_md = '''# Notebook 03 — Comparativo das 3 Visões (Nicho: Movies)

Executa as três visões metodológicas para o nicho de filmes (UTLC-Movies):

- **V1: Real → Real** — treina e testa em reviews reais (baseline do domínio real)
- **V2: Sintético → Sintético** — treina e testa em frases geradas por LLMs
- **V3: Sintético → Real** — treina em sintético, testa em real (*cross-domain evaluation*)

**Controle metodológico:** todas as visões usam **200 frases por classe** (600 total).
Em V1 e V3 o conjunto de teste é o mesmo, isolando a variável "fonte do treino" (real vs sintético).

**Saída final (última célula):** `metricas_3_visoes_movies.csv` + `grafico_3_visoes_movies.png`.
'''

# ============================================================
# CÉLULA 3 — Carregar sintético + função limpar
# ============================================================
cell3 = '''# ============================================================
# CÉLULA 3 — Carregar dataset sintético (Movies) e limpar
# ============================================================
def limpar_texto(texto):
    texto = str(texto).lower()
    texto = re.sub(r'[^a-zà-ÿ\\s]', '', texto)
    texto = re.sub(r'\\s+', ' ', texto).strip()
    return texto

# Lê o synthetic_dataset.csv já gerado pelo notebook 01
df_sintetico = pd.read_csv(os.path.join(DADOS_PROCESSADO, 'synthetic_dataset.csv'))
df_sintetico = df_sintetico[['frase_limpa', 'classe', 'fonte']].dropna()

# Balanceia para 200 frases por classe (controle metodológico)
N_POR_CLASSE = 200
df_sintetico_bal = (df_sintetico
                    .groupby('classe')
                    .sample(n=N_POR_CLASSE, random_state=SEED)
                    .reset_index(drop=True))

print(f"Sintético balanceado: {len(df_sintetico_bal)} frases ({N_POR_CLASSE}/classe)")
print(df_sintetico_bal['classe'].value_counts())
'''

# ============================================================
# CÉLULA 4 — Carregar real, mapear rating→classe, balancear
# ============================================================
cell4 = '''# ============================================================
# CÉLULA 4 — Carregar dataset real (Movies), mapear rating→3 classes, balancear
# ============================================================
path_real = os.path.join(REAL_DATA_PATH, 'utlc_movies.csv')

# Carrega só uma fração para evitar travamento (100k linhas é suficiente)
df_real_raw = pd.read_csv(path_real, nrows=100000)

# Mapping rating → 3 classes (essencial: dataset nativo só tem polaridade binária)
def rating_para_classe(rating):
    if rating >= 4: return 'Positiva'   # 4-5 estrelas
    elif rating <= 2: return 'Negativa' # 1-2 estrelas
    else: return 'Neutra'               # 3 estrelas

df_real_raw['classe'] = df_real_raw['rating'].apply(rating_para_classe)
df_real = df_real_raw[['review_text', 'classe']].dropna().rename(columns={'review_text': 'frase'})
df_real['frase_limpa'] = df_real['frase'].apply(limpar_texto)
df_real = df_real[df_real['frase_limpa'] != ''].reset_index(drop=True)

# Balanceia para 200 frases por classe (mesmo volume do sintético → comparação justa)
df_real_bal = (df_real
               .groupby('classe')
               .sample(n=N_POR_CLASSE, random_state=SEED)
               .reset_index(drop=True))

print(f"Real balanceado: {len(df_real_bal)} frases ({N_POR_CLASSE}/classe)")
print(df_real_bal['classe'].value_counts())
'''

# ============================================================
# CÉLULA 5 — Função run_vision (TF-IDF + 3 modelos)
# ============================================================
cell5 = '''# ============================================================
# CÉLULA 5 — Função genérica para executar uma visão
# ============================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

def run_vision(X_train, y_train, X_test, y_test, visao_nome):
    modelos = {
        'Naive Bayes': MultinomialNB(),
        'Regressão Logística': LogisticRegression(random_state=SEED, max_iter=1000),
        'SVM Linear': LinearSVC(random_state=SEED, max_iter=5000),
    }
    tfidf = TfidfVectorizer()
    X_tr = tfidf.fit_transform(X_train)
    X_te = tfidf.transform(X_test)

    rows = []
    print(f"\\n--- {visao_nome} ---")
    for nome, clf in modelos.items():
        clf.fit(X_tr, y_train)
        y_pred = clf.predict(X_te)
        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        print(f"  {nome:22s} F1={f1:.2%}  Acc={acc:.2%}")
        rows.append({'Visão': visao_nome, 'Modelo': nome,
                     'Acurácia': acc, 'Precisão': prec, 'Recall': rec, 'F1-Score': f1})
    return rows
'''

# ============================================================
# CÉLULA 6 — Executar V1, V2, V3 com test set comum entre V1 e V3
# ============================================================
cell6 = '''# ============================================================
# CÉLULA 6 — Executar as 3 visões
# ============================================================
# Splits 80/20 estratificados (comum a V1 e V2)
R_tr, R_te = train_test_split(df_real_bal, test_size=0.2, stratify=df_real_bal['classe'], random_state=SEED)
S_tr, S_te = train_test_split(df_sintetico_bal, test_size=0.2, stratify=df_sintetico_bal['classe'], random_state=SEED)

print(f"V1 treina com {len(R_tr)} reais, testa em {len(R_te)} reais")
print(f"V2 treina com {len(S_tr)} sintéticas, testa em {len(S_te)} sintéticas")
print(f"V3 treina com {len(S_tr)} sintéticas, testa nas MESMAS {len(R_te)} reais do V1")

todos_resultados = []
todos_resultados += run_vision(R_tr['frase_limpa'], R_tr['classe'],
                                R_te['frase_limpa'], R_te['classe'],
                                "V1: Real → Real")
todos_resultados += run_vision(S_tr['frase_limpa'], S_tr['classe'],
                                S_te['frase_limpa'], S_te['classe'],
                                "V2: Sintético → Sintético")
# V3 reusa o test set do V1 → comparação direta isolando a fonte do treino
todos_resultados += run_vision(S_tr['frase_limpa'], S_tr['classe'],
                                R_te['frase_limpa'], R_te['classe'],
                                "V3: Sintético → Real")
'''

# ============================================================
# CÉLULA 7 — TABELA + GRÁFICO + SALVAR (a célula que importa pro artigo)
# ============================================================
cell7 = '''# ============================================================
# CÉLULA 7 — RESULTADO FINAL: tabela + gráfico + salvar arquivos do artigo
# ============================================================
import matplotlib.pyplot as plt

df_resultados = pd.DataFrame(todos_resultados)

# Tabela pivotada (Visão × Modelo) com F1-Score — formato pronto pro artigo
pivot_f1 = df_resultados.pivot(index='Visão', columns='Modelo', values='F1-Score')
pivot_f1 = pivot_f1[['Naive Bayes', 'Regressão Logística', 'SVM Linear']]
print("\\n=== TABELA F1-SCORE (Visão × Modelo) — Nicho: Movies ===")
print((pivot_f1 * 100).round(2).to_string())

# Salva CSV completo (todas as métricas)
os.makedirs(RESULTADOS, exist_ok=True)
csv_path = os.path.join(RESULTADOS, 'metricas_3_visoes_movies.csv')
df_resultados.round(4).to_csv(csv_path, index=False)
print(f"\\n✓ CSV salvo: {csv_path}")

# Gráfico de barras agrupadas (Visão × Modelo)
fig, ax = plt.subplots(figsize=(10, 6))
pivot_f1.plot(kind='bar', ax=ax, rot=0, edgecolor='black', width=0.75)
ax.set_ylabel('F1-Score (weighted)', fontsize=12)
ax.set_xlabel('')
ax.set_title('Comparativo das 3 Visões — Nicho: Movies (UTLC-Movies)', fontsize=13)
ax.set_ylim(0, 1.0)
ax.legend(title='Modelo', loc='upper right')
ax.grid(axis='y', alpha=0.3)
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', padding=2, fontsize=9)
plt.tight_layout()

png_path = os.path.join(RESULTADOS, 'grafico_3_visoes_movies.png')
plt.savefig(png_path, dpi=150, bbox_inches='tight')
plt.show()
print(f"✓ Gráfico salvo: {png_path}")
'''

# Monta o notebook
nb.cells = [
    nbf.v4.new_code_cell(cell1),
    nbf.v4.new_markdown_cell(cell2_md),
    nbf.v4.new_code_cell(cell3),
    nbf.v4.new_code_cell(cell4),
    nbf.v4.new_code_cell(cell5),
    nbf.v4.new_code_cell(cell6),
    nbf.v4.new_code_cell(cell7),
]

out_path = os.path.join(os.path.dirname(__file__), '03_movies_3_visoes.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Notebook criado: {out_path}")
print(f"Total de células: {len(nb.cells)}")
