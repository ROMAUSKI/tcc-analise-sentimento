"""
Regenera o gráfico comparativo 200 vs 600 frases sintéticas por classe (nicho
filmes e séries) usando F1-MACRO no eixo (antes era F1-Score weighted).

Lê: resultados/comparativo_200_vs_600_movies.csv (já tem coluna F1-Macro)
Salva: resultados/comparativo_200_vs_600_movies.png  (sobrescreve)
       artigo/imagens/comparativo_200_vs_600_movies.png
Layout: 2x3 (V1/V2/V3 na 1a linha; V4/V5 na 2a; 6o painel oculto).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "resultados" / "comparativo_200_vs_600_movies.csv"
OUT_RES = ROOT / "resultados" / "comparativo_200_vs_600_movies.png"
OUT_ART = ROOT / "artigo" / "imagens" / "comparativo_200_vs_600_movies.png"

VISOES = [
    "V1: Sintético → Sintético",
    "V2: Real → Real",
    "V3: Sintético → Real",
    "V4: Real → Real (desbalanceado)",
    "V5: Sintético → Real (desbalanceado)",
]
MODELOS = ["Naive Bayes", "Regressão Logística", "SVM Linear"]
MODELOS_CURTO = ["Naive Bayes", "Regressão Logística", "SVM Linear"]


def vol_label(v):
    return "200/classe" if v.startswith("200") else "600/classe"


def main():
    df = pd.read_csv(CSV)
    df["vol"] = df["Volume"].apply(vol_label)

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle(
        "Comparação 200 vs 600 frases sintéticas por classe — Filmes e séries (F1-macro)\n"
        "(volume não fecha o gap em V3)",
        fontsize=12, fontweight="bold",
    )
    axes = axes.flatten()

    x = np.arange(len(MODELOS))
    width = 0.38

    for i, visao in enumerate(VISOES):
        ax = axes[i]
        sub = df[df["Visão"] == visao]
        vals200, vals600 = [], []
        for m in MODELOS:
            r200 = sub[(sub["Modelo"] == m) & (sub["vol"] == "200/classe")]
            r600 = sub[(sub["Modelo"] == m) & (sub["vol"] == "600/classe")]
            vals200.append(float(r200["F1-Macro"].iloc[0]) * 100 if len(r200) else 0)
            vals600.append(float(r600["F1-Macro"].iloc[0]) * 100 if len(r600) else 0)

        b1 = ax.bar(x - width / 2, vals200, width, label="200/classe (600 total)", color="#9aa0a6")
        b2 = ax.bar(x + width / 2, vals600, width, label="600/classe (1800 total — sintético inteiro)", color="#1f77b4")
        for bars in (b1, b2):
            for bar in bars:
                h = bar.get_height()
                ax.annotate(f"{h:.0f}".replace(".", ","), xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 2), textcoords="offset points", ha="center", fontsize=7)
        ax.set_title(visao, fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_xticks(x)
        ax.set_xticklabels(MODELOS_CURTO, rotation=20, ha="right", fontsize=8)
        ax.set_ylabel("F1-Score (macro)", fontsize=9)
        if i == 0:
            ax.legend(fontsize=7, loc="upper right", title="Volume sintético", title_fontsize=7)

    # 6o painel oculto
    axes[5].axis("off")

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(OUT_RES, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_RES}")
    OUT_ART.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_ART, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_ART}")


if __name__ == "__main__":
    main()
