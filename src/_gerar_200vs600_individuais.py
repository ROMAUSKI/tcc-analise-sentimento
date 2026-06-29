"""
Gera as 5 visoes do comparativo 200 vs 600 frases sinteticas (nicho filmes e
series, F1-macro) como FIGURAS INDIVIDUAIS, em vez do painel 2x3 unico.

Motivo: no slide 13 o painel unico parecia recorte do artigo. Separando em 5
figuras + 1 legenda, da pra posicionar cada uma livremente no PowerPoint.

Le:   resultados/comparativo_200_vs_600_movies.csv  (coluna F1-Macro)
Salva: resultados/slide13_visoes/v1.png ... v5.png + legenda.png
Aspecto fixo (sem bbox tight) para posicionamento previsivel no pptx.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "resultados" / "comparativo_200_vs_600_movies.csv"
OUT = ROOT / "resultados" / "slide13_visoes"
OUT.mkdir(parents=True, exist_ok=True)

VISOES = [
    ("v1", "V1: Sintético → Sintético"),
    ("v2", "V2: Real → Real"),
    ("v3", "V3: Sintético → Real"),
    ("v4", "V4: Real → Real (desbalanceado)"),
    ("v5", "V5: Sintético → Real (desbalanceado)"),
]
MODELOS = ["Naive Bayes", "Regressão Logística", "SVM Linear"]
MODELOS_LABEL = ["Naive\nBayes", "Regressão\nLogística", "SVM\nLinear"]

COR_200 = "#9aa0a6"
COR_600 = "#1f77b4"
LAB_200 = "Reduzido — 600 frases no nicho"
LAB_600 = "Completo — 1.800 frases no nicho"
FIGSIZE = (5.0, 3.2)   # aspecto fixo 0.64 (altura/largura)
DPI = 160


def vol_label(v):
    return "200/classe" if v.startswith("200") else "600/classe"


def main():
    df = pd.read_csv(CSV)
    df["vol"] = df["Volume"].apply(vol_label)
    x = np.arange(len(MODELOS))
    width = 0.38

    for slug, visao in VISOES:
        sub = df[df["Visão"] == visao]
        vals200, vals600 = [], []
        for m in MODELOS:
            r200 = sub[(sub["Modelo"] == m) & (sub["vol"] == "200/classe")]
            r600 = sub[(sub["Modelo"] == m) & (sub["vol"] == "600/classe")]
            vals200.append(float(r200["F1-Macro"].iloc[0]) * 100 if len(r200) else 0)
            vals600.append(float(r600["F1-Macro"].iloc[0]) * 100 if len(r600) else 0)

        fig, ax = plt.subplots(figsize=FIGSIZE)
        b1 = ax.bar(x - width / 2, vals200, width, color=COR_200)
        b2 = ax.bar(x + width / 2, vals600, width, color=COR_600)
        for bars in (b1, b2):
            for bar in bars:
                h = bar.get_height()
                ax.annotate(f"{h:.0f}", xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 2), textcoords="offset points",
                            ha="center", fontsize=12, fontweight="bold")
        ax.set_title(visao, fontsize=13, fontweight="bold")
        ax.set_ylim(0, 113)
        ax.set_xticks(x)
        ax.set_xticklabels(MODELOS_LABEL, fontsize=10)
        ax.set_ylabel("F1-macro (%)", fontsize=11)
        ax.tick_params(axis="y", labelsize=9)
        fig.tight_layout()
        out = OUT / f"{slug}.png"
        fig.savefig(out, dpi=DPI)
        plt.close(fig)
        print(f"[salvo] {out}")

    # legenda separada (mesmo aspecto, encaixa como 6a figura no grid)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.axis("off")
    handles = [Patch(facecolor=COR_200, label=LAB_200),
               Patch(facecolor=COR_600, label=LAB_600)]
    ax.legend(handles=handles, loc="center", fontsize=12,
              title="Volume sintético", title_fontsize=13, frameon=True,
              handlelength=2.0, borderpad=1.2, labelspacing=1.4)
    fig.tight_layout()
    out = OUT / "legenda.png"
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"[salvo] {out}")


if __name__ == "__main__":
    main()
