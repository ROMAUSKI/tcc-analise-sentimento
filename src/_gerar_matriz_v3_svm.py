"""
Gera matriz de confusão para SVM Linear em V3 (Sintético → Real, controlado)
no nicho de filmes/séries. Usado no artigo (Tarefa G).

Saída:
- resultados/matriz_confusao_v3_svm_filmes.png
- resultados/matriz_confusao_v3_svm_filmes.csv
"""
import re
import unicodedata
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

SEED = 42
np.random.seed(SEED)

ROOT = Path(__file__).resolve().parent.parent
SYNTH = ROOT / "dados" / "processado" / "synthetic_dataset.csv"
REAL = ROOT / "src" / "dados_reais" / "utlc_movies.csv"
OUT_PNG = ROOT / "resultados" / "matriz_confusao_v3_svm_filmes.png"
OUT_CSV = ROOT / "resultados" / "matriz_confusao_v3_svm_filmes.csv"

CLASSES = ["Negativa", "Neutra", "Positiva"]


def limpar(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def rating_para_classe(r):
    if r in (4, 5):
        return "Positiva"
    if r in (1, 2):
        return "Negativa"
    if r == 3:
        return "Neutra"
    return None


def main():
    print("Carregando dataset sintético (filmes)...")
    syn = pd.read_csv(SYNTH)
    print(f"  → {len(syn)} frases sintéticas")

    print("Carregando dataset real (utlc_movies)...")
    real = pd.read_csv(REAL, usecols=["review_text", "rating"], nrows=100_000)
    real["classe"] = real["rating"].map(rating_para_classe)
    real = real.dropna(subset=["classe", "review_text"])
    print(f"  → {len(real)} reviews reais carregadas")

    # Mesma estratégia de V3 do notebook 03: real controlado em 600/classe
    samples_per_class = 600
    pieces = []
    for c in CLASSES:
        sub = real[real["classe"] == c]
        pieces.append(sub.sample(samples_per_class, random_state=SEED))
    real_balanced = pd.concat(pieces).sample(frac=1, random_state=SEED).reset_index(drop=True)
    print(f"  → test real balanceado: {len(real_balanced)} frases (600/classe)")

    # Limpeza
    X_train_raw = syn["frase"].astype(str).tolist()
    y_train = syn["classe"].tolist()
    X_test_raw = real_balanced["review_text"].astype(str).tolist()
    y_test = real_balanced["classe"].tolist()

    X_train_clean = [limpar(t) for t in X_train_raw]
    X_test_clean = [limpar(t) for t in X_test_raw]

    # TF-IDF + SVM
    print("Vetorizando TF-IDF e treinando SVM Linear...")
    vec = TfidfVectorizer()
    X_tr = vec.fit_transform(X_train_clean)
    X_te = vec.transform(X_test_clean)
    clf = LinearSVC(max_iter=5000, random_state=SEED)
    clf.fit(X_tr, y_train)
    y_pred = clf.predict(X_te)

    print()
    print("Classification report:")
    print(classification_report(y_test, y_pred, labels=CLASSES, digits=3))

    # Matriz de confusão (ordem fixa: Negativa, Neutra, Positiva)
    cm = confusion_matrix(y_test, y_pred, labels=CLASSES)
    print("Matriz de confusão (linhas=verdadeiro, colunas=predito):")
    print(pd.DataFrame(cm, index=CLASSES, columns=CLASSES))

    # Salvar CSV
    pd.DataFrame(cm, index=CLASSES, columns=CLASSES).to_csv(OUT_CSV)
    print(f"\n[salvo] {OUT_CSV}")

    # Plot
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASSES,
        yticklabels=CLASSES,
        cbar=True,
        ax=ax,
        annot_kws={"size": 13},
    )
    ax.set_xlabel("Predito", fontsize=11)
    ax.set_ylabel("Verdadeiro", fontsize=11)
    ax.set_title("Matriz de confusão — SVM Linear, V3 (Sintético → Real)\nNicho: filmes e séries", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_PNG}")


if __name__ == "__main__":
    main()
