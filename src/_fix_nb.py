# -*- coding: utf-8 -*-
"""Corrige o notebook 03_movies_3_visoes.ipynb com a ordem invertida das visões."""
import nbformat as nbf
import io

nb_path = 'src/03_movies_3_visoes.ipynb'
with io.open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# CÉLULA 1 (índice 1) — Markdown do título
nb.cells[1].source = (
    "# Notebook 03 — Comparativo das 3 Visões (Nicho: Movies)\n\n"
    "Executa as três visões metodológicas para o nicho de filmes (UTLC-Movies):\n\n"
    "- **V1: Sintético → Sintético** — treina e testa em frases geradas por LLMs\n"
    "- **V2: Real → Real** — treina e testa em reviews reais (baseline do domínio real)\n"
    "- **V3: Sintético → Real** — treina em sintético, testa em real (*cross-domain evaluation*)\n\n"
    "**Controle metodológico:** todas as visões usam **200 frases por classe** (600 total).\n"
    "Em V2 e V3 o conjunto de teste é o mesmo, isolando a variável \"fonte do treino\" (real vs sintético).\n\n"
    "**Saída final (última célula):** `metricas_3_visoes_movies.csv` + `grafico_3_visoes_movies.png`."
)

# CÉLULA 8 (índice 8) — Markdown da seção 4
nb.cells[8].source = "## 4. Executar V1, V2, V3 — V3 reusa o test set do V2 (comparação justa)"

# CÉLULA 9 (índice 9) — Código que executa as 3 visões (NOVA ORDEM)
nb.cells[9].source = (
    "# ============================================================\n"
    "# Executar as 3 visões (V1=Sintético, V2=Real, V3=Cross)\n"
    "# ============================================================\n"
    "# Splits 80/20 estratificados\n"
    "S_tr, S_te = train_test_split(df_sintetico_bal, test_size=0.2, "
    "stratify=df_sintetico_bal['classe'], random_state=SEED)\n"
    "R_tr, R_te = train_test_split(df_real_bal,      test_size=0.2, "
    "stratify=df_real_bal['classe'],      random_state=SEED)\n"
    "\n"
    "print(f'V1 treina com {len(S_tr)} sinteticas, testa em {len(S_te)} sinteticas')\n"
    "print(f'V2 treina com {len(R_tr)} reais, testa em {len(R_te)} reais')\n"
    "print(f'V3 treina com {len(S_tr)} sinteticas, testa nas MESMAS {len(R_te)} reais do V2')\n"
    "\n"
    "todos_resultados = []\n"
    "todos_resultados += run_vision(S_tr['frase_limpa'], S_tr['classe'],\n"
    "                                S_te['frase_limpa'], S_te['classe'],\n"
    "                                'V1: Sintético → Sintético')\n"
    "todos_resultados += run_vision(R_tr['frase_limpa'], R_tr['classe'],\n"
    "                                R_te['frase_limpa'], R_te['classe'],\n"
    "                                'V2: Real → Real')\n"
    "# V3 reusa o test set do V2 — comparação direta isolando a fonte do treino\n"
    "todos_resultados += run_vision(S_tr['frase_limpa'], S_tr['classe'],\n"
    "                                R_te['frase_limpa'], R_te['classe'],\n"
    "                                'V3: Sintético → Real')\n"
)

# CÉLULA 11 (índice 11) — Resultado final (com ordem fixa V1, V2, V3)
nb.cells[11].source = (
    "# ============================================================\n"
    "# RESULTADO FINAL: tabela + gráfico + salvar arquivos do artigo\n"
    "# ============================================================\n"
    "import matplotlib.pyplot as plt\n"
    "\n"
    "df_resultados = pd.DataFrame(todos_resultados)\n"
    "\n"
    "# Ordem fixa das visões na tabela e no gráfico\n"
    "ordem_visoes = ['V1: Sintético → Sintético', 'V2: Real → Real', 'V3: Sintético → Real']\n"
    "df_resultados['Visão'] = pd.Categorical(df_resultados['Visão'], "
    "categories=ordem_visoes, ordered=True)\n"
    "df_resultados = df_resultados.sort_values(['Visão', 'Modelo']).reset_index(drop=True)\n"
    "\n"
    "# Tabela pivotada (Visão × Modelo) com F1-Score\n"
    "pivot_f1 = df_resultados.pivot(index='Visão', columns='Modelo', values='F1-Score')\n"
    "pivot_f1 = pivot_f1[['Naive Bayes', 'Regressão Logística', 'SVM Linear']]\n"
    "print('\\n=== TABELA F1-SCORE (Visão x Modelo) — Nicho: Movies ===')\n"
    "print((pivot_f1 * 100).round(2).to_string())\n"
    "\n"
    "# Salva CSV\n"
    "os.makedirs(RESULTADOS, exist_ok=True)\n"
    "csv_path = os.path.join(RESULTADOS, 'metricas_3_visoes_movies.csv')\n"
    "df_resultados.round(4).to_csv(csv_path, index=False)\n"
    "print(f'CSV salvo: {csv_path}')\n"
    "\n"
    "# Gráfico\n"
    "fig, ax = plt.subplots(figsize=(10, 6))\n"
    "pivot_f1.plot(kind='bar', ax=ax, rot=0, edgecolor='black', width=0.75)\n"
    "ax.set_ylabel('F1-Score (weighted)', fontsize=12)\n"
    "ax.set_xlabel('')\n"
    "ax.set_title('Comparativo das 3 Visões — Nicho: Movies (UTLC-Movies)', fontsize=13)\n"
    "ax.set_ylim(0, 1.0)\n"
    "ax.legend(title='Modelo', loc='upper right')\n"
    "ax.grid(axis='y', alpha=0.3)\n"
    "for container in ax.containers:\n"
    "    ax.bar_label(container, fmt='%.2f', padding=2, fontsize=9)\n"
    "plt.tight_layout()\n"
    "\n"
    "png_path = os.path.join(RESULTADOS, 'grafico_3_visoes_movies.png')\n"
    "plt.savefig(png_path, dpi=150, bbox_inches='tight')\n"
    "plt.show()\n"
    "print(f'Gráfico salvo: {png_path}')\n"
)

with io.open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print('Notebook reescrito com sucesso.')
