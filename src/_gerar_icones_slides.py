"""
Gera icones de LINHA (estilo flat, monocromaticos na cor vinho do template)
para tirar a monotonia dos slides so-texto. Fundo transparente, quadrados.

Saida: resultados/icones_slides/<nome>.png
Uso no deck: um icone tematico por slide, canto inferior direito.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrow, Polygon, FancyBboxPatch, Arc
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "resultados" / "icones_slides"
OUT.mkdir(parents=True, exist_ok=True)

VINHO = "#8C2332"
LW = 9
DPI = 200


def _canvas():
    fig, ax = plt.subplots(figsize=(2.4, 2.4))
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _save(fig, nome):
    out = OUT / f"{nome}.png"
    fig.savefig(out, dpi=DPI, transparent=True, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"[salvo] {out}")


def target():  # Objetivos
    fig, ax = _canvas()
    for r in (1.05, 0.66, 0.28):
        ax.add_patch(Circle((0, 0), r, fill=False, lw=LW, edgecolor=VINHO))
    ax.add_patch(Circle((0, 0), 0.06, fill=True, color=VINHO))
    _save(fig, "target")


def check():  # Objetivo atendido
    fig, ax = _canvas()
    ax.add_patch(Circle((0, 0), 1.05, fill=False, lw=LW, edgecolor=VINHO))
    ax.plot([-0.48, -0.10, 0.55], [0.02, -0.40, 0.48],
            lw=LW, color=VINHO, solid_capstyle="round", solid_joinstyle="round")
    _save(fig, "check")


if __name__ == "__main__":
    target()
    check()
