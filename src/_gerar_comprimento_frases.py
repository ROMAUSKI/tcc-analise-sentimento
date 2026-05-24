"""
Regenera o boxplot de comprimento das frases sintéticas por LLM (Figura 1),
com 3 ajustes pedidos:
  1. Sem outliers (showfliers=False) — remove as "bolinhas".
  2. Rótulos de média com fonte maior.
  3. Rótulos reposicionados com folga no topo + fundo branco (não fundem com
     a borda nem com os bigodes).

Fonte dos dados: dados/processado/synthetic_dataset.csv (Movies)
                 dados/processado/synthetic_dataset_apps.csv (Apps)
Salva: resultados/comprimento_frases_por_llm.png + artigo/imagens/...
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
MOV = ROOT / "dados" / "processado" / "synthetic_dataset.csv"
APP = ROOT / "dados" / "processado" / "synthetic_dataset_apps.csv"
OUT_RES = ROOT / "resultados" / "comprimento_frases_por_llm.png"
OUT_ART = ROOT / "artigo" / "imagens" / "comprimento_frases_por_llm.png"

LLMS = ["ChatGPT", "Claude", "Gemini"]
CORES = {"ChatGPT": "#2ca58d", "Claude": "#d98c5f", "Gemini": "#5b8fd6"}


def carregar(path):
    df = pd.read_csv(path)
    # coluna de texto: usar 'frase' (original, com pontuação)
    col = "frase" if "frase" in df.columns else df.columns[-1]
    df["len"] = df[col].astype(str).str.len()
    return df


def main():
    mov = carregar(MOV)
    app = carregar(APP)

    print("Fontes Movies:", sorted(mov["fonte"].unique()))
    print("Fontes Apps:  ", sorted(app["fonte"].unique()))
    for nome, df in [("Movies", mov), ("Apps", app)]:
        for llm in LLMS:
            sub = df[df["fonte"] == llm]["len"]
            print(f"  {nome} {llm}: n={len(sub)} média={sub.mean():.1f}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Comprimento das frases sintéticas por LLM gerador",
                 fontsize=13, fontweight="bold")

    for ax, (nome_plot, nome_real, df) in zip(
        axes, [("Nicho: Filmes e séries", "Movies", mov), ("Nicho: Apps", "Apps", app)]
    ):
        dados = [df[df["fonte"] == llm]["len"].dropna().values for llm in LLMS]
        bp = ax.boxplot(
            dados, labels=LLMS, showfliers=False, patch_artist=True,
            medianprops=dict(color="black", linewidth=1.3),
            widths=0.5,
        )
        for patch, llm in zip(bp["boxes"], LLMS):
            patch.set_facecolor(CORES[llm])
            patch.set_alpha(0.85)

        # limite superior com folga p/ os rótulos não colarem
        max_whisker = max(max(w.get_ydata()) for w in bp["whiskers"])
        ymax = max_whisker * 1.22
        ax.set_ylim(top=ymax)

        # rótulos de média — fonte maior, fundo branco, na faixa superior livre
        y_label = max_whisker * 1.12
        for i, d in enumerate(dados):
            media = d.mean()
            ax.text(
                i + 1, y_label, f"média: {media:.0f}",
                ha="center", va="center", fontsize=12, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor="0.7", linewidth=0.6),
            )

        ax.set_title(nome_plot, fontsize=11, fontweight="bold")
        ax.set_ylabel("Comprimento (caracteres)", fontsize=10)
        ax.grid(axis="y", alpha=0.3)
        ax.tick_params(axis="x", labelsize=10)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(OUT_RES, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_RES}")
    OUT_ART.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT_ART, dpi=160, bbox_inches="tight")
    print(f"[salvo] {OUT_ART}")


if __name__ == "__main__":
    main()
