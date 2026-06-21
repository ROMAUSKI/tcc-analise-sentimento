# -*- coding: utf-8 -*-
"""
Adiciona ELEMENTOS VISUAIS ricos (mesmo estilo dos slides 8-13: chevrons,
cards) aos slides so-texto, SEM regenerar o deck e SEM alterar o texto.
Idempotente: remove o que ele mesmo adicionou (name ELEM_AUTO*) antes de
readicionar. Faz backup. Nao toca em outras imagens/shapes.
"""
import glob, os, shutil, datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE = r"C:\Users\Davi\Documentos\tcc-analise-sentimento"
PPTX = glob.glob(os.path.join(BASE, "Apresenta*", "Apresentacao_TCC_Davi.pptx"))[0]
VINHO = RGBColor(0x8C, 0x23, 0x32)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
PRETO = RGBColor(0x22, 0x22, 0x22)
CINZA = RGBColor(0xEC, 0xEC, 0xEC)
CINZAESC = RGBColor(0x5A, 0x5A, 0x5A)
TAG = "ELEM_AUTO"


def _tag(sh, n):
    sh.name = f"{TAG}_{n}"


def chevron(slide, left, top, w, h, title, sub, fill, n):
    ch = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(left), Inches(top), Inches(w), Inches(h))
    ch.fill.solid(); ch.fill.fore_color.rgb = fill
    ch.line.fill.background(); ch.shadow.inherit = False
    tf = ch.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = title; r.font.bold = True; r.font.size = Pt(13); r.font.color.rgb = BRANCO
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = sub; r2.font.size = Pt(9.5); r2.font.color.rgb = BRANCO
    _tag(ch, n)


def _body(slide):
    # o corpo e o placeholder de maior altura (titulo e n. do slide sao menores)
    cands = [sh for sh in slide.shapes if sh.is_placeholder and sh.height]
    return max(cands, key=lambda s: s.height) if cands else None


def mover_texto(slide, top, height):
    sh = _body(slide)
    if sh is not None:
        sh.top = Inches(top)
        sh.height = Inches(height)


def conceito_intro(slide):
    """Pipeline conceitual do trabalho (slide 3): elemento no topo, texto desce."""
    mover_texto(slide, 2.85, 3.85)
    etapas = [
        ("LLMs geram", "frases rotuladas", VINHO),
        ("Treina", "classificador", CINZAESC),
        ("Testa", "reviews reais", VINHO),
        ("Funciona?", "cross-domain", CINZAESC),
    ]
    cw, cstep, h, top = 3.25, 2.78, 0.95, 1.62
    for i, (tt, sub, fill) in enumerate(etapas):
        chevron(slide, 0.55 + i * cstep, top, cw, h, tt, sub, fill, f"intro{i}")


def limpar(slide):
    for sh in list(slide.shapes):
        if sh.name.startswith(TAG):
            sh._element.getparent().remove(sh._element)


# idx 0-based -> funcao construtora.  DEMO: so o slide 3.
MAPA = {2: conceito_intro}


def main():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(os.path.dirname(PPTX), "_backups")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy2(PPTX, os.path.join(bdir, f"Apresentacao_TCC_Davi_backup_{ts}.pptx"))
    prs = Presentation(PPTX)
    for idx, fn in MAPA.items():
        slide = prs.slides[idx]
        limpar(slide)
        fn(slide)
        print(f"[elem] slide {idx+1}: {fn.__name__}")
    prs.save(PPTX)
    print(f"[salvo] {PPTX}")


if __name__ == "__main__":
    main()
