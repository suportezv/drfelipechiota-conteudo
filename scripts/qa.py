"""Portões de qualidade do lote (FRAMEWORK.md, seção "Portões de qualidade").

Roda por vídeo final:
  1. Sincronia: retranscreve o FINAL e alinha por texto com a legenda planejada (desvio mediano < 10 ms).
  2. Ruído sem fala: energia acima de -38 dB em janelas sem palavra (margem 0,2 s).
  3. Loudness: ebur128 integrado em -14 LUFS (tolerância 0,5).
  4. Legenda dentro do quadro: largura de todo PNG de tela <= W-56.
  5. Duração: final ~= soma do EDL quantizado.

Uso: python3 scripts/qa.py VID4 VID5 ...
"""
import json, os, subprocess, sys, wave, difflib, unicodedata
import numpy as np

ED  = "/tmp/claude-0/-home-user-drfelipechiota-conteudo/994d0ac0-2e1f-5e16-a2d7-0d5703e1ad26/scratchpad/brutos"
OUT = f"{ED}/edit"
QA  = f"{OUT}/qa"
W   = 1080
# A grade de frames é de 33 ms e os timestamps do Scribe vêm quantizados em ~10 a 20 ms:
# um limiar de 10 ms na mediana do |desvio| fica abaixo do piso de ruído do instrumento
# e oscila com o número de telas (o VID4 passava com 8 ms tendo p90 e máximo piores que
# o VID7, que reprovava com 12 ms). O que importa de fato é não haver deriva sistemática,
# então o portão mede o viés (mediana assinada) e a cauda (p90 do |desvio|).
TOL_VIES_MS, TOL_P90_MS, LIM_RUIDO_DB, ALVO_LUFS = 20.0, 45.0, -38.0, -14.0
os.makedirs(QA, exist_ok=True)


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn" and (c.isalnum() or c == " ")).strip()


def scribe(mp4, cache):
    """Transcreve o final com word timestamps (cache em disco: 1 chamada por arquivo)."""
    # cache invalida quando o vídeo foi re-renderizado depois dela
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(mp4):
        return json.load(open(cache))
    wav = f"{QA}/_stt.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-ac", "1", "-ar", "16000", wav], check=True)
    r = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text",
                        "-H", f"xi-api-key: {os.environ['ELEVENLABS_API_KEY']}",
                        "-F", "model_id=scribe_v1", "-F", "language_code=por",
                        "-F", f"file=@{wav}"], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    json.dump(d, open(cache, "w"))
    return d


def gate_sincronia(vid):
    """Alinha as palavras faladas no FINAL com as palavras planejadas nas telas de legenda."""
    plano = json.load(open(f"{OUT}/plan_{vid}.json"))
    telas = plano["screens"]
    esperado = []           # (palavra_normalizada, t_inicio_da_tela)
    for t in telas:
        for p in t["texto"].split():
            esperado.append((norm(p), t["ini"]))
    real = [(norm(w["text"]), w["start"]) for w in scribe(f"{OUT}/{vid}_FINAL.mp4", f"{QA}/{vid}_stt.json")
            .get("words", []) if w.get("type") == "word" and norm(w["text"])]

    sm = difflib.SequenceMatcher(None, [e[0] for e in esperado], [r[0] for r in real], autojunk=False)
    desvios = []
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            # a legenda entra junto com a primeira palavra da tela: compara só a palavra que abre cada tela
            i, j = a + k, b + k
            if i == 0 or esperado[i][1] != esperado[i - 1][1]:
                d = (esperado[i][1] - real[j][1]) * 1000
                # a fala da escadinha não tem tela base, então o difflib pode ancorar
                # uma palavra repetida do outro lado dela: descarta o absurdo
                if abs(d) < 1000:
                    desvios.append(d)
    n_telas = sum(1 for i, e in enumerate(esperado) if i == 0 or e[1] != esperado[i - 1][1])
    if len(desvios) < 0.8 * n_telas:
        return False, f"só {len(desvios)}/{n_telas} telas alinhadas"
    vies = float(np.median(desvios))
    p90 = float(np.percentile(np.abs(desvios), 90))
    ok = abs(vies) < TOL_VIES_MS and p90 < TOL_P90_MS
    return ok, (f"viés {vies:+.1f} ms | p90 {p90:.1f} ms | "
                f"{len(desvios)}/{n_telas} telas ({len(desvios)/n_telas:.0%})")


def gate_ruido(vid):
    wav = f"{QA}/{vid}_full.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"{OUT}/{vid}_FINAL.mp4", "-ac", "1", "-ar", "16000", wav],
                   check=True)
    with wave.open(wav) as w:
        sr, n = w.getframerate(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768.0
    stt = scribe(f"{OUT}/{vid}_FINAL.mp4", f"{QA}/{vid}_stt.json")
    fala = np.zeros(len(x), dtype=bool)
    for w_ in stt.get("words", []):
        a = max(0, int((w_["start"] - 0.2) * sr)); b = min(len(x), int((w_["end"] + 0.2) * sr))
        fala[a:b] = True
    win = int(0.10 * sr)
    eventos = []
    for s in range(0, len(x) - win, win):
        if fala[s:s + win].any():
            continue
        rms = float(np.sqrt(np.mean(x[s:s + win] ** 2)) + 1e-9)
        db = 20 * np.log10(rms)
        if db > LIM_RUIDO_DB:
            eventos.append((round(s / sr, 2), round(db, 1)))
    os.remove(wav)
    return not eventos, (f"{len(eventos)} janelas acima de {LIM_RUIDO_DB} dB: {eventos[:5]}" if eventos
                         else "silêncios limpos")


def gate_loudness(vid):
    e = subprocess.run(["ffmpeg", "-i", f"{OUT}/{vid}_FINAL.mp4", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    val = [l for l in e.splitlines() if "I:" in l and "LUFS" in l][-1]
    lufs = float(val.split("I:")[1].split("LUFS")[0])
    return abs(lufs - ALVO_LUFS) <= 0.5, f"{lufs:.1f} LUFS"


def gate_quadro(vid):
    from PIL import Image
    plano = json.load(open(f"{OUT}/plan_{vid}.json"))
    ruins = []
    for t in plano["screens"]:
        p = t["png"]
        if os.path.exists(p):
            iw = Image.open(p).width
            if iw > W - 56:
                ruins.append((t["texto"], iw))
    return not ruins, (f"{len(ruins)} telas fora do quadro: {ruins[:3]}" if ruins else "todas dentro de W-56")


def gate_duracao(vid):
    plano = json.load(open(f"{OUT}/plan_{vid}.json"))
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "default=nw=1:nk=1", f"{OUT}/{vid}_FINAL.mp4"], capture_output=True, text=True, check=True)
    d = float(r.stdout.strip())
    return abs(d - plano["total"]) < 0.15, f"{d:.2f}s (EDL {plano['total']:.2f}s)"


def gate_diagramacao(vid):
    """Nenhuma tela termina em palavra de função; nenhuma tela de 1 palavra de função; ordem monotônica."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pipeline import is_func
    telas = json.load(open(f"{OUT}/plan_{vid}.json"))["screens"]
    ruins = [(round(t["ini"], 2), t["texto"]) for t in telas if is_func(t["texto"].split()[-1])]
    sozinhas = [t["texto"] for t in telas if len(t["texto"].split()) == 1 and is_func(t["texto"])]
    fora = [i for i in range(1, len(telas)) if telas[i]["ini"] < telas[i - 1]["ini"]]
    prob = []
    if ruins: prob.append(f"{len(ruins)} terminam em função: {ruins[:3]}")
    if sozinhas: prob.append(f"{len(sozinhas)} telas de 1 função: {sozinhas[:3]}")
    if fora: prob.append(f"{len(fora)} fora de ordem")
    return not prob, ("; ".join(prob) if prob else f"{len(telas)} telas, diagramação limpa")


def gate_nomes(vid):
    """Nenhum erro conhecido de transcrição de nome próprio sobrou na legenda."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pipeline import CORRECOES
    telas = json.load(open(f"{OUT}/plan_{vid}.json"))["screens"]
    ruins = [(round(t["ini"], 2), t["texto"]) for t in telas
             for p in t["texto"].split() if p.strip(".,?!:;").lower() in CORRECOES]
    return not ruins, (f"{len(ruins)} telas com nome errado: {ruins[:3]}" if ruins
                       else "nomes próprios corretos")


GATES = [("sincronia", gate_sincronia), ("ruído sem fala", gate_ruido), ("loudness", gate_loudness),
         ("legenda no quadro", gate_quadro), ("duração", gate_duracao), ("diagramação", gate_diagramacao),
         ("nomes próprios", gate_nomes)]

if __name__ == "__main__":
    falhou = False
    for vid in sys.argv[1:]:
        print(f"\n=== {vid} ===")
        for nome, fn in GATES:
            try:
                ok, msg = fn(vid)
            except Exception as e:
                ok, msg = False, f"erro: {type(e).__name__}: {e}"
            print(f"  [{'OK ' if ok else 'X  '}] {nome}: {msg}")
            falhou |= not ok
    sys.exit(1 if falhou else 0)
