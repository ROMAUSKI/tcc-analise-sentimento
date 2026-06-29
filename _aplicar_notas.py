# -*- coding: utf-8 -*-
"""Reescreve as notas (speaker notes) dos 20 slides em estilo FLASHCARD:
objetivo, pra bater o olho e lembrar o significado/porque. Nao e roteiro de
leitura. Regenera tambem o Roteiro_Apresentacao.md. Backup antes."""
import glob, os, shutil, datetime
from pptx import Presentation

BASE = r"C:\Users\Davi\Documentos\tcc-analise-sentimento"
PPTX = glob.glob(os.path.join(BASE, "Apresenta*", "Apresentacao_TCC_Davi.pptx"))[0]
ROTEIRO = glob.glob(os.path.join(BASE, "Apresenta*", "Roteiro_Apresentacao.md"))
ROTEIRO = ROTEIRO[0] if ROTEIRO else os.path.join(os.path.dirname(PPTX), "Roteiro_Apresentacao.md")

NOTAS = {
 0: "ABERTURA — nome, orientador (Prof. Marlon), tema.\n"
    "Pitch (1 frase): testar se LLMs servem pra gerar base de treino JA ROTULADA pra analise de sentimento em pt-BR — e se funciona em reviews reais.\n"
    "Respirar, olhar a banca, nao correr.",
 1: "Roteiro da fala: Contexto -> Metodo -> Resultados -> Conclusao.\n"
    "So situar a banca; NAO ler item por item.",
 2: "Analise de sentimento = classificar opiniao em positiva / negativa / neutra.\n"
    "- Treinar exige base rotulada: cara e lenta; pt-BR tem pouco.\n"
    "- Ideia: o LLM gera o dado JA rotulado.\n"
    "Pergunta central (pipeline): gera -> treina -> testa no REAL -> funciona?",
 3: "Geral: avaliar a viabilidade pratica de treinar com dados sinteticos.\n"
    "3 perguntas: (1) assertividade do sintetico; (2) coerencia ENTRE os LLMs; (3) cross-domain = treino sintetico, teste real.\n"
    "A 3a (cross-domain) e a estrela — foi sugestao do Marlon.",
 4: "Por que importa: anotacao humana e cara/lenta; pt-BR escasso.\n"
    "- LLM rotula sem anotacao manual.\n"
    "- 3 LLMs reduzem vies de fonte unica.\n"
    "- 2 nichos + cross-domain mostram ONDE funciona.",
 5: "Base teorica: analise de sentimento = classificacao supervisionada (Pang, 2002).\n"
    "- Classicos: TF-IDF + NB / LR / SVM.\n"
    "- Neurais: LSTM e BERTimbau (BERT pre-treinado em pt-BR).\n"
    "- Metrica: F1-macro (justo com classes desbalanceadas).",
 6: "O que usei: 3 LLMs geradores, 5 classificadores, 2 datasets reais (UTLC-Movies/Apps, via kagglehub).\n"
    "Stack: Python, scikit-learn, PyTorch, HuggingFace. Neurais rodaram no Colab (GPU T4).",
 7: "NUMERO-CHAVE: 200 frases POR LLM por classe -> 3 LLMs = 600/classe -> 1.800/nicho.\n"
    "- 2 nichos (filmes/series e apps).\n"
    "- Real: ~100k reviews/nicho; nota 1-5 -> 3 classes (>=4 pos, <=2 neg, =3 neu).\n"
    "Pipeline: geracao -> pre-proc (TF-IDF) -> treino -> avaliacao.",
 8: "Prompt ISOMORFO: mesmo pros 3 LLMs, so muda a classe (comparacao justa).\n"
    "- Pede 200 frases, max 30 palavras, saida em CSV.\n"
    "- CSV: frase | classe | fonte (qual LLM gerou).\n"
    "LEMBRAR: o '200' e POR LLM -> 3x200 = 600 por classe.",
 9: "Estilo de geracao (comprimento): ChatGPT ~50 (curto/regular); Claude ~95 em filmes (longo); Gemini ~60.\n"
    "- Em apps (texto tecnico) os 3 se aproximam.\n"
    "Por que importa: frase longa/elaborada se afasta da review real -> ajuda a explicar o gap e a diferenca entre nichos.",
 10: "5 visoes = FONTE do treino (sint/real) x TESTE (controlado/natural).\n"
     "- V1 = baseline sintetico; V5 = cross-domain realista (a que importa).\n"
     "- Pares: V2 vs V3 e V4 vs V5 isolam a fonte; V1 vs V5 = reality gap.\n"
     "Metrica principal: F1-macro.",
 11: "V1 (sint->sint) = 97% com BERTimbau — sintetico e otimo 'em casa'.\n"
     "Real (V2/V4) = 60-67% — patamar normal da tarefa.\n"
     "ARMADILHA: 97% NAO significa sucesso; e so dentro do mundo sintetico.",
 12: "V5 (sint->real natural) DESPENCA: 43% filmes / 56% apps -> inviavel pra uso pratico.\n"
     "- Matriz (V3-SVM): a classe Neutra e a mais sacrificada.\n"
     "Mensagem: o modelo treinado em sintetico NAO generaliza pro real.",
 13: "Por que cai: frase sintetica e limpa e direta; review real tem giria, erro, ironia.\n"
     "- Exemplos reais: 'PQP q filme', 'interesante', 'mais' (em vez de mas).\n"
     "Causa = diferenca de DISTRIBUICAO entre os textos.",
 14: "Teste de volume: triplicar o sintetico (600 -> 1.800 no nicho) NAO fecha o gap em V3.\n"
     "- Logo: limitacao e ESTRUTURAL, nao falta de dados (argumento central!).\n"
     "- Apps > filmes no desbalanceado (vocabulario mais objetivo).\n"
     "Legenda: Reduzido = 600/nicho; Completo = 1.800/nicho. Reducao = amostra aleatoria por classe (seed 42).",
 15: "Objetivo ATENDIDO: avaliamos a viabilidade.\n"
     "- 97% no sintetico, MAS 43-56% no cross-domain real -> inviavel pra producao.\n"
     "- Limitacao e estrutural (distribuicao), nao falta de dados.",
 16: "- Geracao manual: ~3-4h por nicho (interface web).\n"
     "- BERT estourou a RAM do Colab -> subamostra estratificada de 100k (distribuicao preservada).\n"
     "- Paradoxo: calibrar o sintetico exige dado real.\n"
     "- TF-IDF nao pega negacao/ironia -> por isso testei LSTM e BERT.",
 17: "- Adaptacao de dominio (pouco real + muito sintetico).\n"
     "- Outros nichos; prompts mais elaborados.\n"
     "- Gerar via API (controle de temperatura) e mais LLMs.",
 18: "Citar de passagem; nao ler.\n"
     "Principais: Pang 2002 (base); Souza 2022 (sentimento pt-BR); Li 2023 / Hellwig 2025 (LLM gerando dado sintetico).",
 19: "Agradecer e abrir pra perguntas.\n"
     "Mensagem final (1 frase): dado sintetico de LLM serve pra prototipo/pesquisa, mas ainda NAO substitui dado real em producao.",
}


def titulo(slide):
    for sh in slide.shapes:
        if sh.is_placeholder and sh.placeholder_format.idx == 0 and sh.has_text_frame and sh.text_frame.text.strip():
            return sh.text_frame.text.strip()
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            return sh.text_frame.text.strip()[:50]
    return "(sem titulo)"


def main():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(os.path.dirname(PPTX), "_backups")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy2(PPTX, os.path.join(bdir, f"Apresentacao_TCC_Davi_backup_{ts}.pptx"))

    prs = Presentation(PPTX)
    titulos = []
    for idx, slide in enumerate(prs.slides):
        titulos.append(titulo(slide))
        if idx in NOTAS:
            slide.notes_slide.notes_text_frame.text = NOTAS[idx]
    prs.save(PPTX)
    print(f"[ok] notas aplicadas em {len(NOTAS)} slides")

    with open(ROTEIRO, "w", encoding="utf-8") as f:
        f.write("# Notas de fixação — Apresentação TCC (flashcards)\n\n")
        f.write("> Bater o olho e lembrar. Não é roteiro de leitura.\n\n")
        for idx in range(len(titulos)):
            f.write(f"## Slide {idx+1} — {titulos[idx]}\n\n")
            f.write(NOTAS.get(idx, "") + "\n\n")
    print(f"[ok] roteiro regenerado: {ROTEIRO}")


if __name__ == "__main__":
    main()
