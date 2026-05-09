# -*- coding: utf-8 -*-
"""Adiciona V4 e V5 (desbalanceadas) ao notebook 03_movies_3_visoes.ipynb."""
import nbformat as nbf
import io

nb_path = 'src/03_movies_3_visoes.ipynb'
with io.open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# --- Atualiza markdown do título (índice 1) ---
nb.cells[1].source = (
    "# Notebook 03 — Comparativo das 5 Visões (Nicho: Movies)\n\n"
    "Executa as cinco visões metodológicas para o nicho de filmes (UTLC-Movies):\n\n"
    "**Volume controlado (200 frases/classe):**\n"
    "- **V1: Sintético → Sintético** — baseline sintético isolado\n"
    "- **V2: Real → Real** — baseline real com volume comparável\n"
    "- **V3: Sintético → Real** — *cross-domain controlado* (mesmo test set do V2)\n\n"
    "**Volume natural (todos os dados reais):**\n"
    "- **V4: Real → Real (desbalanceado)** — limite superior do real com dado abundante\n"
    "- **V5: Sintético → Real (desbalanceado)** — *cross-domain \"vida real\"* (mesmo test set do V4)\n\n"
    "**Pareamentos:** V2↔V3 isola fonte com volume controlado; V4↔V5 isola fonte com volume natural; V2↔V4 mostra ganho de volume.\n\n"
    "**Métricas reportadas:** Acurácia, Precisão, Recall, F1 weighted, **F1 macro** (importante para V4/V5 desbalanceadas).\n\n"
    "**Saída final (última célula):** `metricas_5_visoes_movies.csv` + gráficos em `resultados/`."
)

# --- Atualiza função run_vision (índice 7) para incluir F1 macro ---
nb.cells[7].source = (
    "# ============================================================\n"
    "# Função genérica para executar uma visão (com F1 macro)\n"
    "# ============================================================\n"
    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
    "from sklearn.linear_model import LogisticRegression\n"
    "from sklearn.naive_bayes import MultinomialNB\n"
    "from sklearn.svm import LinearSVC\n"
    "from sklearn.metrics import accuracy_score, precision_recall_fscore_support, f1_score\n"
    "from sklearn.model_selection import train_test_split\n"
    "\n"
    "def run_vision(X_train, y_train, X_test, y_test, visao_nome):\n"
    "    modelos = {\n"
    "        'Naive Bayes': MultinomialNB(),\n"
    "        'Regressão Logística': LogisticRegression(random_state=SEED, max_iter=1000),\n"
    "        'SVM Linear': LinearSVC(random_state=SEED, max_iter=5000),\n"
    "    }\n"
    "    # max_features=5000 para conter memória/tempo nas visões desbalanceadas (~80k frases)\n"
    "    tfidf = TfidfVectorizer(max_features=5000)\n"
    "    X_tr = tfidf.fit_transform(X_train)\n"
    "    X_te = tfidf.transform(X_test)\n"
    "\n"
    "    rows = []\n"
    "    print(f'\\n--- {visao_nome} ---')\n"
    "    for nome, clf in modelos.items():\n"
    "        clf.fit(X_tr, y_train)\n"
    "        y_pred = clf.predict(X_te)\n"
    "        acc = accuracy_score(y_test, y_pred)\n"
    "        prec, rec, f1w, _ = precision_recall_fscore_support(\n"
    "            y_test, y_pred, average='weighted', zero_division=0)\n"
    "        f1m = f1_score(y_test, y_pred, average='macro', zero_division=0)\n"
    "        print(f'  {nome:22s} F1w={f1w:.2%}  F1macro={f1m:.2%}  Acc={acc:.2%}')\n"
    "        rows.append({'Visão': visao_nome, 'Modelo': nome,\n"
    "                     'Acurácia': acc, 'Precisão': prec, 'Recall': rec,\n"
    "                     'F1-Score': f1w, 'F1-Macro': f1m})\n"
    "    return rows\n"
)

# --- Insere markdown + code para "Carregar real desbalanceado" entre cells 5 e 6 ---
md_real_desbal = nbf.v4.new_markdown_cell(
    "## 2b. Carregar dataset real DESBALANCEADO (todos os dados, distribuição natural)"
)
code_real_desbal = nbf.v4.new_code_cell(
    "# ============================================================\n"
    "# Carregar dataset real SEM balancear (V4 e V5 usam este)\n"
    "# ============================================================\n"
    "# Reusa df_real (já carregado na célula 4 com mapping rating->classe e limpeza)\n"
    "# A diferença para df_real_bal é que NÃO sub-amostramos para 200/classe\n"
    "df_real_desbal = df_real.copy().reset_index(drop=True)\n"
    "\n"
    "print(f'Real desbalanceado: {len(df_real_desbal)} frases')\n"
    "print('Distribuição natural das classes:')\n"
    "print(df_real_desbal['classe'].value_counts())\n"
    "print('Proporção (%):')\n"
    "print((df_real_desbal['classe'].value_counts(normalize=True) * 100).round(2))\n"
)

# --- Atualiza markdown da seção 4 (executar V1/V2/V3) ---
nb.cells[8].source = "## 4. Executar V1, V2, V3 (volume controlado — 200/classe)"

# --- Insere markdown + code para V4 e V5 entre cells 9 e 10 ---
md_v4_v5 = nbf.v4.new_markdown_cell(
    "## 4b. Executar V4 e V5 (volume natural — todos os reais)\n\n"
    "V4: Real desbalanceado → Real desbalanceado (split 80/20 estratificado)  \n"
    "V5: Sintético (200/classe, mesmo treino do V3) → **mesmo test set do V4** (~20k frases reais)\n\n"
    "*Atenção: pode levar 1-2 min por causa do volume.*"
)
code_v4_v5 = nbf.v4.new_code_cell(
    "# ============================================================\n"
    "# Executar V4 e V5 — desbalanceadas, volume natural\n"
    "# ============================================================\n"
    "# Split 80/20 estratificado no real desbalanceado\n"
    "RD_tr, RD_te = train_test_split(\n"
    "    df_real_desbal, test_size=0.2, stratify=df_real_desbal['classe'], random_state=SEED)\n"
    "\n"
    "print(f'V4 treina com {len(RD_tr)} reais, testa em {len(RD_te)} reais (desbalanceado)')\n"
    "print(f'V5 treina com {len(S_tr)} sintéticas (mesmo treino do V3), testa nas MESMAS {len(RD_te)} reais do V4')\n"
    "\n"
    "todos_resultados += run_vision(RD_tr['frase_limpa'], RD_tr['classe'],\n"
    "                                RD_te['frase_limpa'], RD_te['classe'],\n"
    "                                'V4: Real → Real (desbalanceado)')\n"
    "\n"
    "todos_resultados += run_vision(S_tr['frase_limpa'], S_tr['classe'],\n"
    "                                RD_te['frase_limpa'], RD_te['classe'],\n"
    "                                'V5: Sintético → Real (desbalanceado)')\n"
)

# --- Atualiza markdown da seção 5 (resultado final) ---
# (será reposicionado após inserções)
md_resultado_idx_old = 10  # antes das inserções
nb.cells[md_resultado_idx_old].source = "## 5. Resultado final → tabela + gráfico (5 visões × 4 métricas) salvos para o artigo"

# --- Reescreve a célula 11 (resultado final) para suportar 5 visões + F1 macro ---
nb.cells[11].source = (
    "# ============================================================\n"
    "# RESULTADO FINAL: tabela + gráficos (5 visões × 5 métricas)\n"
    "# ============================================================\n"
    "import matplotlib.pyplot as plt\n"
    "\n"
    "df_resultados = pd.DataFrame(todos_resultados)\n"
    "\n"
    "# Ordem fixa das visões na tabela e nos gráficos\n"
    "ordem_visoes = [\n"
    "    'V1: Sintético → Sintético',\n"
    "    'V2: Real → Real',\n"
    "    'V3: Sintético → Real',\n"
    "    'V4: Real → Real (desbalanceado)',\n"
    "    'V5: Sintético → Real (desbalanceado)',\n"
    "]\n"
    "df_resultados['Visão'] = pd.Categorical(df_resultados['Visão'], categories=ordem_visoes, ordered=True)\n"
    "df_resultados = df_resultados.sort_values(['Visão', 'Modelo']).reset_index(drop=True)\n"
    "\n"
    "ordem_modelos = ['Naive Bayes', 'Regressão Logística', 'SVM Linear']\n"
    "metricas = ['Acurácia', 'Precisão', 'Recall', 'F1-Score', 'F1-Macro']\n"
    "\n"
    "# Tabela completa\n"
    "print('\\n=== MÉTRICAS COMPLETAS — Nicho: Movies (5 visões) ===')\n"
    "print((df_resultados.set_index(['Visão', 'Modelo'])[metricas] * 100).round(2).to_string())\n"
    "\n"
    "# Salva CSV\n"
    "os.makedirs(RESULTADOS, exist_ok=True)\n"
    "csv_path = os.path.join(RESULTADOS, 'metricas_5_visoes_movies.csv')\n"
    "df_resultados.round(4).to_csv(csv_path, index=False)\n"
    "print(f'\\nCSV salvo: {csv_path}')\n"
    "\n"
    "# Mantém também o nome antigo para compatibilidade\n"
    "df_resultados.round(4).to_csv(os.path.join(RESULTADOS, 'metricas_3_visoes_movies.csv'), index=False)\n"
    "\n"
    "# --- Gráfico principal: F1-Score (weighted) com 5 colunas ---\n"
    "pivot_f1 = df_resultados.pivot(index='Visão', columns='Modelo', values='F1-Score')[ordem_modelos]\n"
    "fig, ax = plt.subplots(figsize=(13, 6))\n"
    "pivot_f1.plot(kind='bar', ax=ax, rot=15, edgecolor='black', width=0.75)\n"
    "ax.set_ylabel('F1-Score (weighted)', fontsize=12)\n"
    "ax.set_xlabel('')\n"
    "ax.set_title('Comparativo das 5 Visões — Nicho: Movies (UTLC-Movies)', fontsize=13)\n"
    "ax.set_ylim(0, 1.0)\n"
    "ax.legend(title='Modelo', loc='upper right')\n"
    "ax.grid(axis='y', alpha=0.3)\n"
    "for container in ax.containers:\n"
    "    ax.bar_label(container, fmt='%.2f', padding=2, fontsize=8)\n"
    "plt.tight_layout()\n"
    "png_path = os.path.join(RESULTADOS, 'grafico_5_visoes_movies.png')\n"
    "plt.savefig(png_path, dpi=150, bbox_inches='tight')\n"
    "plt.savefig(os.path.join(RESULTADOS, 'grafico_3_visoes_movies.png'), dpi=150, bbox_inches='tight')  # compat\n"
    "plt.show()\n"
    "print(f'Gráfico principal salvo: {png_path}')\n"
    "\n"
    "# --- Painel 2x3 com as 5 métricas ---\n"
    "fig, axes = plt.subplots(2, 3, figsize=(20, 11))\n"
    "axes = axes.flatten()\n"
    "for i, metrica in enumerate(metricas):\n"
    "    pivot = df_resultados.pivot(index='Visão', columns='Modelo', values=metrica)[ordem_modelos]\n"
    "    pivot.plot(kind='bar', ax=axes[i], rot=20, edgecolor='black', width=0.75, legend=(i==0))\n"
    "    axes[i].set_title(metrica, fontsize=13, fontweight='bold')\n"
    "    axes[i].set_xlabel('')\n"
    "    axes[i].set_ylim(0, 1.0)\n"
    "    axes[i].grid(axis='y', alpha=0.3)\n"
    "    for container in axes[i].containers:\n"
    "        axes[i].bar_label(container, fmt='%.2f', padding=2, fontsize=7)\n"
    "    if i == 0:\n"
    "        axes[i].legend(title='Modelo', loc='upper right', fontsize=8)\n"
    "axes[5].set_visible(False)  # Esconde o 6º slot (vazio)\n"
    "fig.suptitle('Comparativo das 5 Visões — 5 Métricas — Movies (UTLC-Movies)',\n"
    "             fontsize=14, fontweight='bold', y=1.00)\n"
    "plt.tight_layout()\n"
    "png_painel = os.path.join(RESULTADOS, 'grafico_5_visoes_movies_5metricas.png')\n"
    "plt.savefig(png_painel, dpi=150, bbox_inches='tight')\n"
    "plt.savefig(os.path.join(RESULTADOS, 'grafico_3_visoes_movies_4metricas.png'), dpi=150, bbox_inches='tight')  # compat\n"
    "plt.show()\n"
    "print(f'Painel 2x3 salvo: {png_painel}')\n"
    "\n"
    "# --- Gráficos individuais por métrica ---\n"
    "for metrica in metricas:\n"
    "    pivot = df_resultados.pivot(index='Visão', columns='Modelo', values=metrica)[ordem_modelos]\n"
    "    fig, ax = plt.subplots(figsize=(13, 6))\n"
    "    pivot.plot(kind='bar', ax=ax, rot=15, edgecolor='black', width=0.75)\n"
    "    ax.set_ylabel(metrica + ' (weighted)' if metrica == 'F1-Score' else metrica, fontsize=12)\n"
    "    ax.set_xlabel('')\n"
    "    ax.set_title(f'{metrica} — 5 Visões — Movies (UTLC-Movies)', fontsize=13)\n"
    "    ax.set_ylim(0, 1.0)\n"
    "    ax.legend(title='Modelo', loc='upper right')\n"
    "    ax.grid(axis='y', alpha=0.3)\n"
    "    for container in ax.containers:\n"
    "        ax.bar_label(container, fmt='%.2f', padding=2, fontsize=8)\n"
    "    plt.tight_layout()\n"
    "    slug = (metrica.lower()\n"
    "            .replace('á','a').replace('í','i').replace('ã','a').replace('-','').replace(' ',''))\n"
    "    pi = os.path.join(RESULTADOS, f'grafico_5_visoes_movies_{slug}.png')\n"
    "    plt.savefig(pi, dpi=150, bbox_inches='tight')\n"
    "    plt.close()\n"
    "    print(f'  - {pi}')\n"
)

# --- Inserções (de trás pra frente para não bagunçar índices) ---
# Após cell 9 (executar V1/V2/V3) -> insere md_v4_v5 e code_v4_v5
nb.cells.insert(10, code_v4_v5)
nb.cells.insert(10, md_v4_v5)
# Após cell 5 (real balanceado) -> insere md_real_desbal e code_real_desbal
nb.cells.insert(6, code_real_desbal)
nb.cells.insert(6, md_real_desbal)

with io.open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f'Notebook atualizado. Total de células: {len(nb.cells)}')
for i, c in enumerate(nb.cells):
    head = ''.join(c.source).split('\n')[0][:90]
    print(f'  [{i:2d}] {c.cell_type:8s} | {head}')
