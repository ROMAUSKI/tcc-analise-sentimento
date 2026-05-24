"""
Regenera a Figura 3 (comparativo Movies x Apps em F1-macro nas 5 visões),
corrigindo 2 problemas: legenda cobrindo as barras e números pequenos.

Ajustes:
  - Legenda movida para o 6º painel vazio (canto inferior direito).
  - Fonte dos valores em cima das barras aumentada.
  - ylim com folga no topo para os números não cortarem.

Fonte: resultados/metricas_consolidado_geral.csv (coluna F1-Macro)
Salva: resultados/comparativo_nichos_f1macro.png + artigo/imagens/...
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "resultados" / "metricas_consolidado_geral.csv"
OUT_RES = ROOT / "resultados" / "comparativo_nichos_f1macro.png"
OUT_ART = ROOT / "artigo" / "imagens" / "comparativo_nichos_f1macro.png"

VISOES = [
    ("V1: Sintético → Sintético", "V1: Sintético → Sintético"),
    ("V2: Real → Real", "V2: Real → Real"),
    ("V3: Sintético → Real", "V3: Sintético → Real"),
    ("V4: Real → Real (desbalanceado)", "V4: Real → Real (desbalanceado)"),
    ("V5: Sintético → Real (desbalanceado)", "V5: Sintético → Real (desbalanceado)"),
]
MODELOS_CSV = ["Naive Bayes", "Regressão Logística", "SVM Linear", "LSTM", "BERT (Bertimbau)"]
MODELOS_LBL = ["Naive Bayes", "Regressão Logística", "SVM Linear", "LSTM", "BERT"]

COR_MOVIES = "#1f77b4"
COR_APPS = "#ff7f0e"


def main():
    df = pd.read_csv(CSV)

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle("Comparativo Movies × Apps — F1-Score (macro)",
                 fontsize=14, fontweight="bold")
    axes = axes.flatten()

    x = np.arange(len(MODELOS_CSV))
    width = 0.38

    for idx, (visao_csv, titulo) in enumerate(VISOES):
        ax = axes[idx]
        mov, app = [], []
        for m in MODELOS_CSV:
            rm = df[(df["Nicho"] == "Movies") & (df["Visão"] == visao_csv) & (df["Modelo"] == m)]
            ra = df[(df["Nicho"] == "Apps") & (df["Visão"] == visao_csv) & (df["Modelo"] == m)]
            mov.append(float(rm["F1-Macro"].iloc[0]) * 100 if len(rm) else 0)
            app.append(float(ra["F1-Macro"].iloc[0]) * 100 if len(ra) else 0)

        b1 = ax.bar(x - width / 2, mov, width, label="Movies", color=COR_MOVIES)
        b2 = ax.bar(x + width / 2, app, width, label="Apps", color=COR_APPS)
        for bars in (b1, b2):
            for bar in bars:
                h = bar.get_height()
                ax.annotate(f"{h:.0f}",
                            xy=(bar.get_x() + bar.get_width() / 2, h),
                            xytext=(0, 2), textcoords="offset points",
                            ha="center", fontsize=9)

        ax.set_title(titulo, fontsize=11, fontweight="bold")
        ax.set_ylim(0, 113)
        ax.set_xticks(x)
        ax.set_xticklabels(MODELOS_LBL, rotation=22, ha="right", fontsize=9)
        ax.set_ylabel("F1-Score macro (%)", fontsize=10)
        ax.grid(axis="y", alpha=0.3)

    # 6º painel = legenda grande
    legenda_ax = axes[5]
    legenda_ax.axis("off")
    handles = [Patch(facecolor=COR_MOVIES, label="Movies (filmes e séries)"),
               Patch(facecolor=COR_APPS, label="Apps (aplicativos móveis)")]
    legenda_ax.legend(handles=handles, loc="center", fontsize=15,
                      title="Nicho", title_fontsize=15, frameon=True,
                      handlelength=2.0, borderpad=1.2, labelspacing=1.2)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(OUT_RES, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_RES}")
    OUT_ART.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_ART, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_ART}")

    # verificação rápida de alguns valores-chave
    def v(nicho, visao, modelo):
        r = df[(df["Nicho"] == nicho) & (df["Visão"] == visao) & (df["Modelo"] == modelo)]
        return float(r["F1-Macro"].iloc[0])
    print("Conferência:")
    print(f"  V4 BERT Movies={v('Movies','V4: Real → Real (desbalanceado)','BERT (Bertimbau)'):.4f} "
          f"Apps={v('Apps','V4: Real → Real (desbalanceado)','BERT (Bertimbau)'):.4f}")
    print(f"  V5 BERT Movies={v('Movies','V5: Sintético → Real (desbalanceado)','BERT (Bertimbau)'):.4f} "
          f"Apps={v('Apps','V5: Sintético → Real (desbalanceado)','BERT (Bertimbau)'):.4f}")


if __name__ == "__main__":
    main()
