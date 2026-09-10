"""Gera as entregas finais a partir dos masters de scripts/pipeline.py.

O master sai em CRF 18 (40 a 50 MB), acima do que o chat aceita e acima do que
Reels precisa. A entrega usa o mesmo padrão aprovado no VID8: CRF 21 com teto de
6 Mbps, faststart e áudio AAC 192k em 48 kHz.

O loudnorm entrega 96 kHz quando a taxa não é fixada, o que não é padrão de
plataforma; aqui o áudio é reamostrado para 48 kHz e o loudness é reconferido
depois (reamostragem não muda loudness, mas o portão confirma).

Uso: python3 scripts/entregar.py
"""
import json, os, subprocess, sys

ED  = "/tmp/claude-0/-home-user-drfelipechiota-conteudo/994d0ac0-2e1f-5e16-a2d7-0d5703e1ad26/scratchpad/brutos"
OUT = f"{ED}/edit"
ENT = f"{OUT}/entregas"
ALVO_LUFS, TOL = -14.0, 0.5

# bruto -> (número do roteiro no DOCX, slug do nome de arquivo)
NOMES = {
    "VID4":  ("01", "Medo_do_Especialista"),
    "VID5":  ("02", "Repouso_Piora"),
    "VID7":  ("04", "Quatro_Sinais"),
    "VID10": ("05", "Postura_no_Trabalho"),
    "VID11": ("06", "Dor_Pos_Treino"),
    "VID13": ("07", "Hernia_Cervical"),
    "VID15": ("08", "Posicionamento"),
    "VID16": ("09", "Dor_Precoce_Jovens"),
    "VID17": ("12", "Volta_ao_Esporte"),
}


def lufs(path):
    e = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    linha = [l for l in e.splitlines() if "I:" in l and "LUFS" in l][-1]
    return float(linha.split("I:")[1].split("LUFS")[0])


def probe(path, campos):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", campos,
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True, check=True)
    return r.stdout.split()


ORCAMENTO_MB = 27.5     # abaixo do limite de anexo do chat, com folga de container


def entregar(vid):
    src = f"{OUT}/{vid}_FINAL.mp4"
    num, slug = NOMES[vid]
    dst = f"{ENT}/Chiota_{num}_{slug}_ENTREGA.mp4"
    d_src = float(probe(src, "format=duration")[0])
    # o teto sai da duração, não de um número fixo: a 6 Mbps o VID4 (44,5 s) deu
    # 29,8 MB, em cima do limite. Vídeo curto continua no teto de qualidade.
    teto = min(6_000_000, int(ORCAMENTO_MB * 1024 * 1024 * 8 / d_src) - 192_000)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src,
                    "-c:v", "libx264", "-crf", "21", "-preset", "slow", "-profile:v", "high",
                    "-maxrate", str(teto), "-bufsize", str(teto * 2), "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", dst], check=True)
    d_dst = float(probe(dst, "format=duration")[0])
    sr = int(probe(dst, "stream=sample_rate")[0])
    mb = os.path.getsize(dst) / 1048576
    li = lufs(dst)
    ok = abs(li - ALVO_LUFS) <= TOL and abs(d_dst - d_src) < 0.10 and sr == 48000 and mb < 29
    return ok, dst, f"{mb:5.1f} MB | {d_dst:5.2f}s | {li:+.1f} LUFS | {sr} Hz | teto {teto/1e6:.2f} Mbps"


if __name__ == "__main__":
    os.makedirs(ENT, exist_ok=True)
    alvos = sys.argv[1:] or list(NOMES)
    falhou = False
    for vid in alvos:
        ok, dst, msg = entregar(vid)
        print(f"[{'OK ' if ok else 'X  '}] {vid} -> {os.path.basename(dst)}: {msg}", flush=True)
        falhou |= not ok
    sys.exit(1 if falhou else 0)
