# -*- coding: utf-8 -*-
"""Preenche e enriquece o template UTFPR com o conteudo do TCC (versao visual)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SRC = "Modelo de Apresentação para Banca de TCC.pptx"
OUT = "Apresentacao_TCC_Davi.pptx"
IMG = "artigo/imagens"
VINHO = RGBColor(0x8C, 0x23, 0x32)
VINHO2 = RGBColor(0xB0, 0x3A, 0x48)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
PRETO = RGBColor(0x22, 0x22, 0x22)
CINZA = RGBColor(0xEC, 0xEC, 0xEC)
CINZAESC = RGBColor(0x5A, 0x5A, 0x5A)

prs = Presentation(SRC)


def ph(slide, idx):
    for sh in slide.shapes:
        if sh.is_placeholder and sh.placeholder_format.idx == idx:
            return sh
    raise KeyError(idx)


def set_title(slide, text, size=None):
    tf = ph(slide, 0).text_frame
    p = tf.paragraphs[0]
    for extra in list(tf.paragraphs)[1:]:
        extra._p.getparent().remove(extra._p)
    if p.runs:
        p.runs[0].text = text
        for r in list(p.runs)[1:]:
            r._r.getparent().remove(r._r)
    else:
        p.add_run().text = text
    if size:
        p.runs[0].font.size = Pt(size)


def set_lines(shape, lines, size=None, align=None):
    tf = shape.text_frame
    tf.clear()
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = ln
        if size:
            r.font.size = Pt(size)
        if align is not None:
            p.alignment = align


def set_body(slide, items, size=None):
    tf = ph(slide, 1).text_frame
    tf.clear()
    for i, (txt, lvl) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = lvl
        r = p.add_run()
        r.text = txt
        if size:
            r.font.size = Pt(size)


def shrink_body(slide, left, top, width, height):
    sh = ph(slide, 1)
    sh.left, sh.top, sh.width, sh.height = Inches(left), Inches(top), Inches(width), Inches(height)


def add_img(slide, path, left, top, width):
    return slide.shapes.add_picture(path, Inches(left), Inches(top), width=Inches(width))


def decorate_title(slide):
    """Marcador geometrico vinho ao lado do titulo + desloca o titulo."""
    t = ph(slide, 0)
    t.left = Inches(1.18)
    t.width = Inches(11.0)
    mk = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(0.82), Inches(0.42), Inches(0.42))
    mk.fill.solid()
    mk.fill.fore_color.rgb = VINHO
    mk.line.fill.background()
    mk.shadow.inherit = False


def stat_card(slide, left, top, w, h, number, label):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(h))
    box.fill.solid()
    box.fill.fore_color.rgb = BRANCO
    box.line.color.rgb = VINHO
    box.line.width = Pt(1.5)
    box.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = Pt(4)
    tf.margin_bottom = Pt(4)
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    r1 = p1.add_run()
    r1.text = number
    r1.font.size = Pt(50)
    r1.font.bold = True
    r1.font.color.rgb = VINHO
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = label
    r2.font.size = Pt(13)
    r2.font.color.rgb = PRETO


def chevron(slide, left, top, w, h, title, sub, fill):
    ch = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(left), Inches(top), Inches(w), Inches(h))
    ch.fill.solid()
    ch.fill.fore_color.rgb = fill
    ch.line.fill.background()
    ch.shadow.inherit = False
    tf = ch.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = title
    r.font.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = BRANCO
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = sub
    r2.font.size = Pt(10)
    r2.font.color.rgb = BRANCO


# Snapshot das referencias estaveis (a reordenacao do sldIdLst nao as afeta)
(s_capa, s_sum, s_intro, s_obj, s_just, s_refteo, s_mat, s_met,
 s_r1, s_r2, s_vol, s_conc, s_refs, s_fim) = list(prs.slides)

# ---------- SLIDE 1 - CAPA ----------
set_title(s_capa, "Utilização de LLMs para Geração de Bases de Treinamento em Classificação de Sentimento: Uma Análise de Viabilidade Prática", size=28)
set_lines(ph(s_capa, 1), [
    "Trabalho de Conclusão de Curso 2",
    "Discente: Davi Romauski Meurer",
    "Orientador: Prof. Marlon Marcon",
])

# ---------- SLIDE 2 - SUMARIO ----------
decorate_title(s_sum)

# ---------- SLIDE 3 - INTRODUCAO ----------
decorate_title(s_intro)
set_body(s_intro, [
    ("Análise de sentimento: classificar opiniões em positiva, negativa ou neutra.", 0),
    ("Treinar modelos exige datasets rotulados — caros e demorados de construir.", 0),
    ("Em português brasileiro, faltam recursos anotados.", 0),
    ("LLMs podem gerar esses dados já rotulados — mas funcionam no mundo real?", 0),
])

# ---------- SLIDE 4 - OBJETIVOS ----------
decorate_title(s_obj)
set_body(s_obj, [
    ("Objetivo geral:", 0),
    ("Avaliar a viabilidade prática de treinar classificadores de sentimento com dados sintéticos de LLMs.", 1),
    ("Objetivos específicos:", 0),
    ("Medir a assertividade com treino apenas sintético.", 1),
    ("Verificar a coerência entre os LLMs geradores.", 1),
    ("Avaliar o cross-domain: treino sintético, teste real.", 1),
    ("Comparar dois nichos com subjetividade diferente.", 1),
])

# ---------- SLIDE 5 - JUSTIFICATIVA ----------
decorate_title(s_just)
set_body(s_just, [
    ("Datasets rotulados são caros, e o português tem poucos recursos.", 0),
    ("LLMs geram texto rotulado sem anotação humana.", 0),
    ("Três LLMs reduzem o viés de uma fonte única.", 0),
    ("Dois nichos e o cross-domain revelam onde a abordagem funciona.", 0),
])

# ---------- SLIDE 6 - REFERENCIAL TEORICO ----------
decorate_title(s_refteo)
set_body(s_refteo, [
    ("Análise de sentimento = classificação supervisionada de texto (Pang, 2002).", 0),
    ("TF-IDF com classificadores clássicos: Naive Bayes, Regressão Logística e SVM.", 0),
    ("Modelos neurais: LSTM e BERTimbau (BERT pré-treinado em português).", 0),
    ("Geração de dados sintéticos por LLMs: área de pesquisa recente.", 0),
    ("Métrica principal: F1-macro, justo com classes desbalanceadas.", 0),
])

# ---------- SLIDE 7 - MATERIAIS ----------
decorate_title(s_mat)
set_body(s_mat, [
    ("LLMs geradores: ChatGPT, Gemini e Claude.", 0),
    ("Classificadores: Naive Bayes, Reg. Logística, SVM, LSTM e BERTimbau.", 0),
    ("Stack: Python, scikit-learn, PyTorch e Hugging Face Transformers.", 0),
    ("Dados reais: UTLC-Movies e UTLC-Apps (Kaggle), via kagglehub.", 0),
    ("Execução dos modelos neurais em Google Colab (GPU NVIDIA T4).", 0),
])

# ---------- SLIDE 8 - METODOS (pipeline + tabela) ----------
decorate_title(s_met)
set_body(s_met, [("Pipeline em quatro etapas, avaliado sob cinco visões metodológicas:", 0)])
shrink_body(s_met, 1.18, 1.55, 11.0, 0.55)
# pipeline de chevrons
cw, cstep, ctop, ch_h = 3.25, 2.78, 2.25, 1.05
etapas = [
    ("1. Geração", "3 LLMs · 1.800 frases", VINHO),
    ("2. Pré-proc.", "limpeza · TF-IDF", CINZAESC),
    ("3. Treino", "5 classificadores", VINHO),
    ("4. Avaliação", "5 visões · F1-macro", CINZAESC),
]
for i, (tt, sub, fill) in enumerate(etapas):
    chevron(s_met, 0.55 + i * cstep, ctop, cw, ch_h, tt, sub, fill)
# tabela 5 visoes
tbl_shape = s_met.shapes.add_table(6, 4, Inches(1.85), Inches(3.7), Inches(9.6), Inches(2.7))
tbl = tbl_shape.table
tbl.columns[0].width = Inches(1.4)
tbl.columns[1].width = Inches(2.73)
tbl.columns[2].width = Inches(2.73)
tbl.columns[3].width = Inches(2.74)
dados = [
    ["Visão", "Treino", "Teste", "Volume"],
    ["V1", "Sintético", "Sintético", "Controlado"],
    ["V2", "Real", "Real", "Controlado"],
    ["V3", "Sintético", "Real", "Controlado"],
    ["V4", "Real", "Real", "Desbalanceado"],
    ["V5", "Sintético", "Real", "Desbalanceado"],
]
for ri, row in enumerate(dados):
    for ci, val in enumerate(row):
        cell = tbl.cell(ri, ci)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_top = Pt(1)
        cell.margin_bottom = Pt(1)
        tfc = cell.text_frame
        tfc.clear()
        p = tfc.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = val
        r.font.size = Pt(14)
        if ri == 0:
            r.font.bold = True
            r.font.color.rgb = BRANCO
            cell.fill.solid()
            cell.fill.fore_color.rgb = VINHO
        else:
            r.font.color.rgb = PRETO
            cell.fill.solid()
            cell.fill.fore_color.rgb = BRANCO if ri % 2 else CINZA

# ---------- SLIDE 9 - RESULTADOS (1/4): dominio sintetico e real ----------
decorate_title(s_r1)
set_title(s_r1, "Resultados (1/4): Domínio Sintético e Real")
set_body(s_r1, [
    ("No mundo sintético, a classificação é quase perfeita.", 0),
    ("Nos dados reais, o desempenho fica no esperado para a tarefa.", 0),
], size=16)
shrink_body(s_r1, 1.18, 1.62, 11.0, 1.0)
stat_card(s_r1, 1.7, 3.0, 4.2, 3.0, "97%", "Sintético → Sintético\n(V1, BERTimbau)")
stat_card(s_r1, 7.4, 3.0, 4.2, 3.0, "60–67%", "Dados reais\n(V2 e V4)")

# ---------- SLIDE 10 - RESULTADOS (2/4): cross-domain ----------
decorate_title(s_r2)
set_title(s_r2, "Resultados (2/4): Cross-domain — a Queda")
set_body(s_r2, [
    ("Treino sintético, teste real: o desempenho despenca.", 0),
    ("O modelo acerta a classe dominante e erra as minoritárias.", 0),
    ("A Neutra é confundida com Positiva e Negativa.", 0),
], size=15)
shrink_body(s_r2, 1.18, 1.6, 5.5, 1.6)
stat_card(s_r2, 1.18, 3.4, 2.55, 2.7, "43%", "Filmes e séries\n(V5)")
stat_card(s_r2, 4.0, 3.4, 2.55, 2.7, "56%", "Aplicativos\n(V5)")
add_img(s_r2, f"{IMG}/matriz_confusao_v3_svm_filmes.png", left=7.15, top=2.0, width=5.0)

# ---------- SLIDE 11 (NOVO) - RESULTADOS (3/4): reality gap ----------
layout_conteudo = s_intro.slide_layout
novo = prs.slides.add_slide(layout_conteudo)
# reordenar para a posicao 11 (apos o slide 10, index 9 -> nova posicao index 10)
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
mover = ids[-1]
sldIdLst.remove(mover)
sldIdLst.insert(10, mover)
decorate_title(novo)
set_title(novo, "Resultados (3/4): Reality Gap")
try:
    set_body(novo, [("A frase do LLM é limpa e direta; a review real tem gíria, erro e ironia.", 0)], size=16)
    shrink_body(novo, 1.18, 1.6, 11.0, 0.7)
except KeyError:
    pass
# tabela de exemplos 4x3
ex_shape = novo.shapes.add_table(4, 3, Inches(0.8), Inches(2.5), Inches(11.7), Inches(3.8))
ex = ex_shape.table
ex.columns[0].width = Inches(1.5)
ex.columns[1].width = Inches(5.1)
ex.columns[2].width = Inches(5.1)
exdata = [
    ["Classe", "Sintética (Claude)", "Real (UTLC-Movies)"],
    ["Positiva", "Nunca vi atuações tão intensas e verdadeiras; merece todos os prêmios.", "Estou sem xão sem ar sem vida PQP q filme"],
    ["Negativa", "A história é completamente previsível; adivinhei o final nos dez primeiros minutos.", "Horrivel com péssimas interpretações."],
    ["Neutra", "O filme tem duas horas e quinze minutos e estreou em março.", "é bem interesante! mais ainda sim não deixa de ser sessão da tarde"],
]
for ri, row in enumerate(exdata):
    for ci, val in enumerate(row):
        cell = ex.cell(ri, ci)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = Pt(6)
        cell.margin_right = Pt(6)
        cell.margin_top = Pt(3)
        cell.margin_bottom = Pt(3)
        tfc = cell.text_frame
        tfc.word_wrap = True
        tfc.clear()
        p = tfc.paragraphs[0]
        r = p.add_run()
        r.text = val
        if ri == 0:
            p.alignment = PP_ALIGN.CENTER
            r.font.bold = True
            r.font.size = Pt(14)
            r.font.color.rgb = BRANCO
            cell.fill.solid()
            cell.fill.fore_color.rgb = VINHO
        elif ci == 0:
            p.alignment = PP_ALIGN.CENTER
            r.font.bold = True
            r.font.size = Pt(13)
            r.font.color.rgb = VINHO
            cell.fill.solid()
            cell.fill.fore_color.rgb = CINZA
        else:
            r.font.size = Pt(12)
            r.font.color.rgb = PRETO
            cell.fill.solid()
            cell.fill.fore_color.rgb = BRANCO if ri % 2 else CINZA

# ---------- SLIDE 12 - RESULTADOS (4/4): volume e nichos ----------
decorate_title(s_vol)
set_title(s_vol, "Resultados (4/4): Volume e Nichos")
set_body(s_vol, [
    ("Triplicar o volume sintético (200 → 600 frases/classe) não fecha o gap.", 0),
    ("A limitação é estrutural (distribuição), não falta de dados.", 0),
    ("Apps supera filmes e séries no desbalanceado: vocabulário mais objetivo.", 0),
], size=16)
shrink_body(s_vol, 1.18, 1.55, 11.0, 1.5)
add_img(s_vol, f"{IMG}/comparativo_200_vs_600_movies.png", left=3.56, top=3.2, width=6.2)

# ---------- SLIDE 13 - CONCLUSAO ----------
decorate_title(s_conc)
set_body(s_conc, [
    ("Dados sintéticos de LLMs ainda não substituem dados reais para uso prático.", 0),
    ("A limitação é estrutural: o texto do LLM difere da review real.", 0),
    ("Continuam úteis para protótipo, pesquisa e cenários sem dados reais.", 0),
    ("Trabalhos futuros: adaptação de domínio (pouco dado real + muito sintético).", 0),
])

# ---------- SLIDE 14 - REFERENCIAS ----------
decorate_title(s_refs)
set_body(s_refs, [
    ("PANG, B.; LEE, L.; VAITHYANATHAN, S. Thumbs up? Sentiment classification using machine learning techniques. EMNLP, 2002.", 0),
    ("SOUZA, F.; FILHO, J. A. Sentiment analysis on Brazilian Portuguese user reviews. IEEE LA-CCI, 2022.", 0),
    ("ARAÚJO, G.; MELO, T.; FIGUEIREDO, C. M. S. Is ChatGPT an effective solver of sentiment analysis tasks in Portuguese? PROPOR, 2024.", 0),
    ("ZHANG, W. et al. Sentiment analysis in the era of large language models: a reality check. NAACL Findings, 2024.", 0),
    ("LI, Z. et al. Synthetic data generation with large language models for text classification. EMNLP, 2023.", 0),
    ("HELLWIG, N. C.; FEHLE, J.; WOLFF, C. Exploring LLMs for the generation of synthetic training samples for aspect-based sentiment analysis. Expert Systems with Applications, 2025.", 0),
], size=14)

# ---------- SLIDE 15 - ENCERRAMENTO ----------
set_title(s_fim, "Obrigado pela atenção!")
set_lines(ph(s_fim, 1), [
    "Davi Romauski Meurer",
    "davimeurer@alunos.utfpr.edu.br",
    "Orientador: Prof. Marlon Marcon",
])

prs.save(OUT)
print("Salvo:", OUT, "| total de slides:", len(prs.slides._sldIdLst))
