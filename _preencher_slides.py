# -*- coding: utf-8 -*-
"""Preenche o template institucional UTFPR com o conteudo do TCC, preservando o design."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

SRC = "Modelo de Apresentação para Banca de TCC.pptx"
OUT = "Apresentacao_TCC_Davi.pptx"
IMG = "artigo/imagens"
VINHO = RGBColor(0x8C, 0x23, 0x32)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
PRETO = RGBColor(0x22, 0x22, 0x22)
CINZA = RGBColor(0xEC, 0xEC, 0xEC)

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


S = prs.slides

# ---------- SLIDE 1 - CAPA ----------
set_title(S[0], "Utilização de LLMs para Geração de Bases de Treinamento em Classificação de Sentimento: Uma Análise de Viabilidade Prática", size=28)
set_lines(ph(S[0], 1), [
    "Trabalho de Conclusão de Curso 2",
    "Discente: Davi Romauski Meurer",
    "Orientador: Prof. Marlon Marcon",
])

# ---------- SLIDE 2 - SUMARIO (mantem) ----------

# ---------- SLIDE 3 - INTRODUCAO ----------
set_body(S[2], [
    ("A análise de sentimento identifica a polaridade — positiva, negativa ou neutra — de uma opinião expressa em texto.", 0),
    ("Treinar classificadores para essa tarefa depende de datasets rotulados, cuja construção manual é cara e demorada.", 0),
    ("Em português brasileiro, a disponibilidade de recursos anotados é bem menor do que em inglês.", 0),
    ("LLMs como ChatGPT, Gemini e Claude surgem como possível fonte de dados sintéticos já rotulados.", 0),
    ("Este trabalho investiga se esses dados sintéticos servem para treinar classificadores usados em um cenário real.", 0),
])

# ---------- SLIDE 4 - OBJETIVOS ----------
set_body(S[3], [
    ("Objetivo geral:", 0),
    ("Avaliar a viabilidade prática de treinar classificadores de sentimento em português usando dados sintéticos gerados por LLMs.", 1),
    ("Objetivos específicos:", 0),
    ("Medir a assertividade de classificadores treinados apenas com dados sintéticos.", 1),
    ("Verificar a coerência entre os dados gerados por diferentes LLMs.", 1),
    ("Avaliar o desempenho cross-domain (treino sintético, teste em dados reais).", 1),
    ("Comparar dois nichos com graus diferentes de subjetividade.", 1),
])

# ---------- SLIDE 5 - JUSTIFICATIVA ----------
set_body(S[4], [
    ("A construção manual de datasets rotulados é cara e demorada, e o português brasileiro tem poucos recursos anotados.", 0),
    ("LLMs conseguem gerar texto rotulado sem anotação humana, o que poderia reduzir esse custo.", 0),
    ("Usar três LLMs distintos reduz o viés associado a uma única fonte de geração.", 0),
    ("Avaliar dois nichos e o cenário cross-domain mostra em quais contextos a abordagem realmente funciona.", 0),
])

# ---------- SLIDE 6 - REFERENCIAL TEORICO ----------
set_body(S[5], [
    ("Análise de sentimento tratada como classificação supervisionada de texto (Pang et al., 2002).", 0),
    ("Vetorização TF-IDF com classificadores clássicos: Naive Bayes, Regressão Logística e SVM Linear.", 0),
    ("Modelos neurais: LSTM e BERTimbau, um BERT pré-treinado em português brasileiro.", 0),
    ("Dados sintéticos gerados por LLMs: área recente, promissora em cenários de poucos recursos.", 0),
    ("Avaliação por F1-macro, mais informativo que a acurácia quando as classes estão desbalanceadas.", 0),
])

# ---------- SLIDE 7 - MATERIAIS ----------
set_body(S[6], [
    ("LLMs geradores: ChatGPT (OpenAI), Gemini (Google) e Claude (Anthropic).", 0),
    ("Classificadores: Naive Bayes, Regressão Logística, SVM Linear, LSTM e BERTimbau.", 0),
    ("Bibliotecas: Python, scikit-learn, PyTorch e Hugging Face Transformers.", 0),
    ("Dados reais: UTLC-Movies e UTLC-Apps (Kaggle), carregados via kagglehub.", 0),
    ("Execução dos modelos neurais em Google Colab com GPU NVIDIA T4.", 0),
])

# ---------- SLIDE 8 - METODOS (texto + tabela das 5 visoes) ----------
set_body(S[7], [
    ("Geração de 1.800 frases sintéticas por nicho (3 LLMs × 3 classes × 200 frases), em dois nichos: filmes e séries e aplicativos móveis.", 0),
    ("Dados reais: cerca de 100 mil reviews por nicho, com a nota mapeada para as três classes.", 0),
    ("Pré-processamento, vetorização TF-IDF e treino com semente fixa (42); avaliação nas cinco visões abaixo.", 0),
])
shrink_body(S[7], 0.59, 1.7, 12.16, 1.9)
rows, cols = 6, 4
tbl_shape = S[7].shapes.add_table(rows, cols, Inches(1.7), Inches(3.75), Inches(9.9), Inches(2.9))
tbl = tbl_shape.table
tbl.columns[0].width = Inches(1.5)
tbl.columns[1].width = Inches(2.8)
tbl.columns[2].width = Inches(2.8)
tbl.columns[3].width = Inches(2.8)
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
        cell.margin_top = Pt(2)
        cell.margin_bottom = Pt(2)
        tfc = cell.text_frame
        tfc.clear()
        p = tfc.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = val
        r.font.size = Pt(15)
        if ri == 0:
            r.font.bold = True
            r.font.color.rgb = BRANCO
            cell.fill.solid()
            cell.fill.fore_color.rgb = VINHO
        else:
            r.font.color.rgb = PRETO
            cell.fill.solid()
            cell.fill.fore_color.rgb = BRANCO if ri % 2 else CINZA

# ---------- SLIDE 9 - RESULTADOS (1/3) ----------
set_title(S[8], "Resultados (1/3): Domínio Sintético e Real")
set_body(S[8], [
    ("V1 (sintético → sintético): BERTimbau atinge 97% de F1-macro — dados internamente coerentes.", 0),
    ("V2 e V4 (dados reais): desempenho entre 60% e 67%, dentro do esperado para a tarefa.", 0),
], size=16)
shrink_body(S[8], 0.59, 1.65, 12.16, 1.15)
add_img(S[8], f"{IMG}/comparativo_nichos_f1macro.png", left=3.46, top=2.95, width=6.4)

# ---------- SLIDE 10 - RESULTADOS (2/3) ----------
set_title(S[9], "Resultados (2/3): Cross-domain — a Queda")
set_body(S[9], [
    ("No cenário mais realista (V5, desbalanceado), o F1-macro cai para 43% em filmes e séries e 56% em aplicativos.", 0),
    ("O modelo treinado em sintético acerta a classe dominante, mas erra as minoritárias (viés de classe majoritária).", 0),
    ("A matriz de confusão mostra a classe Neutra sendo confundida com Positiva e Negativa.", 0),
    ("Reality gap: a frase sintética é mais limpa e direta do que a review escrita por um usuário real.", 0),
])
shrink_body(S[9], 0.59, 2.0, 6.3, 4.6)
add_img(S[9], f"{IMG}/matriz_confusao_v3_svm_filmes.png", left=7.5, top=2.2, width=4.76)

# ---------- SLIDE 11 - RESULTADOS (3/3) ----------
set_title(S[10], "Resultados (3/3): Volume e Nichos")
set_body(S[10], [
    ("Triplicar o volume sintético (200 → 600 frases/classe) não fecha o gap no cross-domain.", 0),
    ("A limitação é estrutural (diferença de distribuição), não falta de dados.", 0),
    ("Apps supera filmes e séries no desbalanceado: vocabulário mais regular e objetivo.", 0),
], size=16)
shrink_body(S[10], 0.59, 1.55, 12.16, 1.5)
add_img(S[10], f"{IMG}/comparativo_200_vs_600_movies.png", left=3.56, top=3.2, width=6.2)

# ---------- SLIDE 12 - CONCLUSAO ----------
set_body(S[11], [
    ("Dados sintéticos gerados por LLMs ainda não são uma alternativa viável para treinar classificadores de uso prático.", 0),
    ("A limitação vem da diferença estrutural entre o texto do LLM e a review real, e não da quantidade de dados.", 0),
    ("A abordagem mantém valor em prototipagem, pesquisa exploratória e cenários sem dados reais disponíveis.", 0),
    ("Trabalhos futuros: técnicas de adaptação de domínio, combinando pouco dado real com bastante dado sintético.", 0),
])

# ---------- SLIDE 13 - REFERENCIAS ----------
set_body(S[12], [
    ("PANG, B.; LEE, L.; VAITHYANATHAN, S. Thumbs up? Sentiment classification using machine learning techniques. EMNLP, 2002.", 0),
    ("SOUZA, F.; FILHO, J. A. Sentiment analysis on Brazilian Portuguese user reviews. IEEE LA-CCI, 2022.", 0),
    ("ARAÚJO, G.; MELO, T.; FIGUEIREDO, C. M. S. Is ChatGPT an effective solver of sentiment analysis tasks in Portuguese? PROPOR, 2024.", 0),
    ("ZHANG, W. et al. Sentiment analysis in the era of large language models: a reality check. NAACL Findings, 2024.", 0),
    ("LI, Z. et al. Synthetic data generation with large language models for text classification. EMNLP, 2023.", 0),
    ("HELLWIG, N. C.; FEHLE, J.; WOLFF, C. Exploring LLMs for the generation of synthetic training samples for aspect-based sentiment analysis. Expert Systems with Applications, 2025.", 0),
], size=14)

# ---------- SLIDE 14 - ENCERRAMENTO ----------
set_title(S[13], "Obrigado pela atenção!")
set_lines(ph(S[13], 1), [
    "Davi Romauski Meurer",
    "davimeurer@alunos.utfpr.edu.br",
    "Orientador: Prof. Marlon Marcon",
])

prs.save(OUT)
print("Salvo:", OUT)
