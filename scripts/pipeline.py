"""Pipeline de edição do lote Chiota. Estilo aprovado no VID8 (v7).
Corte respirado + zoom narrativo cúbico + cor + legendas Clarify + escadinha + trilha com ducking.
Sem SFX, sem GCs de topo. Legendas SEMPRE por último. -14 LUFS."""
import json, os, subprocess, shutil, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ED   = "/tmp/claude-0/-home-user-drfelipechiota-conteudo/994d0ac0-2e1f-5e16-a2d7-0d5703e1ad26/scratchpad/brutos"
OUT  = f"{ED}/edit"
AF   = "/home/user/drfelipechiota-conteudo/assets/fonts"
F_CORPO = f"{AF}/YWFTClarifyMedium.otf"
F_BOLD  = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
W, H, FPS = 1080, 1920, 30
BRANCO, AZUL_VIVO, AZUL_CLARO = (255,255,255,255), (62,200,237,255), (142,193,205,255)
TRACK, Y_BLOCO = -4, 1140
SH_A, SH_BLUR, SH_OFF = 60, 22, (12,12)
GRADE = "colorcorrect=analyze=average,colortemperature=temperature=7000:mix=0.3,eq=contrast=1.07:saturation=1.06:brightness=0.012"
# FUNC: palavra de função de verdade (artigo, preposição, conjunção, pronome). Tela nunca termina nelas.
FUNC = {"a","o","as","os","um","uma","de","do","da","dos","das","em","no","na","nos","nas","por","pra",
        "pro","para","com","sem","que","e","ou","se","ao","aos","à","às","meu","minha","seu","sua",
        "esse","essa","aquela","aquele","ele","ela","isso"}
# FRACO: advérbio/quantificador que fecha mal uma tela mas carrega sentido. Só encarece o DP.
FRACO = FUNC | {"mais","menos","já","só","cada","muito","bem","tão"}
Q = lambda t: round(t*FPS)/FPS
def _n(t): return t.lower().strip(".,?!:;")
def is_func(t): return _n(t) in FUNC and _n(t) not in {"é","dá"}
def is_fraco(t): return _n(t) in FRACO and _n(t) not in {"é","dá"}
def _adv(d, ch, f, tam, track=TRACK):
    return max(d.textlength(" ", font=f), tam*0.30) if ch==" " else d.textlength(ch, font=f)+track

# ---------- 1. CORTES (respiração) ----------
def planear_cortes(words, excluir):
    keep = [w for w in words if not any(a <= w["start"] < b or a < w["end"] <= b for a,b in excluir)]
    segs, ini, prev = [], Q(max(0, keep[0]["start"]-0.15)), keep[0]
    for w in keep[1:]:
        gap = w["start"] - prev["end"]
        salto = any(prev["end"] <= a and b <= w["start"] for a,b in excluir)
        if gap >= 0.5 or salto:
            segs.append((ini, Q(prev["end"]+0.15))); ini = Q(max(0, w["start"]-0.15))
        prev = w
    segs.append((ini, Q(prev["end"]+0.35)))
    return [s for s in segs if s[1]-s[0] > 0.25], keep

# ---------- 2. ZOOM NARRATIVO ----------
def ease(p, tipo): return f"({p})*({p})*(3-2*({p}))" if tipo=="io" else f"(1-pow(1-({p}),3))"
def zoom_expr(nf, z0, z1, tipo="io"):
    return f"({z0}+({z1}-{z0})*{ease(f'clip(on/{max(nf-1,1)},0,1)', tipo)})"
def plano_zoom(i, n, aberto):
    if aberto:            return (1.04, 1.07, "io")     # escadinha precisa de espaço
    if i == 0:            return (1.06, 1.14, "io")     # hook
    if i == n-1:          return (1.20, 1.12, "out")    # CTA relaxa
    return (1.17, 1.25, "io") if i % 2 else (1.24, 1.09, "out")

# ---------- 3. RENDER DE TEXTO ----------
def com_sombra(img):
    sh = Image.new("RGBA", img.size, (0,0,0,0)); sh.putalpha(img.split()[3].point(lambda a:int(a*SH_A/255)))
    sh = sh.filter(ImageFilter.GaussianBlur(SH_BLUR))
    out = Image.new("RGBA",(img.width+60,img.height+60),(0,0,0,0))
    out.alpha_composite(sh,(30+SH_OFF[0],30+SH_OFF[1])); out.alpha_composite(img,(30,30)); return out

def render_linha(palavras, tam, chaves, letra_t=None):
    fb, fk = ImageFont.truetype(F_CORPO,tam), ImageFont.truetype(F_BOLD,int(tam*1.16))
    pr = ImageDraw.Draw(Image.new("RGBA",(4,4))); seq, x = [], 0.0
    ch_norm = {c.strip(",.?!:;").lower() for c in chaves}
    for wi,t in enumerate(palavras):
        key = t.strip(",.?!:;").lower() in ch_norm
        f, tm = (fk, int(tam*1.16)) if key else (fb, tam)
        for c in t: seq.append((c,x,key,f,tm)); x += _adv(pr,c,f,tm)
        if wi < len(palavras)-1: seq.append((" ",x,False,fb,tam)); x += _adv(pr," ",fb,tam)
    asc = max(fk.getmetrics()[0], fb.getmetrics()[0]); desc = max(fk.getmetrics()[1], fb.getmetrics()[1])
    img = Image.new("RGBA",(int(x)+52, asc+desc+60),(0,0,0,0)); d = ImageDraw.Draw(img); li=0
    for c,cx,key,f,tm in seq:
        if c==" ": continue
        alpha, dy = (255,0.0) if letra_t is None else letra_t(li); li+=1
        if alpha<=0: continue
        col = AZUL_VIVO if key else BRANCO
        d.text((26+cx, 26+(asc-f.getmetrics()[0])+4+dy), c, font=f, fill=(col[0],col[1],col[2],int(alpha)))
    return img

def encolhe(img, maxw):
    return img.resize((maxw,int(img.height*maxw/img.width)), Image.LANCZOS) if img.width>maxw else img

def faixa(h_px, amax, path):
    img = Image.new("RGBA",(W,h_px),(0,0,0,0)); d=ImageDraw.Draw(img)
    for y in range(h_px):
        p=y/h_px; d.line([(0,y),(W,y)], fill=(0,0,0,int(amax*(1-abs(2*p-1))**1.4)))
    img.save(path)

# ---------- 4. DIAGRAMAÇÃO ----------
MIN_TELA, CONF_TELA, MAX_TELA = 0.30, 0.45, 2.4

def dp_chunk(cl, words):
    """Partição ótima em telas de 1 a 3 palavras.

    O custo pesa três coisas ao mesmo tempo: quantas palavras a tela tem, em que
    palavra ela termina e quanto tempo ela fica no ar. A duração entra aqui porque
    fundir telas curtas depois do DP produzia telas de 5 a 7 palavras
    ("irradia ou tira força, isso é"), que é pior do que a tela rápida que a fusão
    tentava evitar."""
    n=len(cl); best=[1e9]*(n+1); best[0]=0; prev=[0]*(n+1)
    for j in range(1,n+1):
        for k in (1,2,3):
            i=j-k
            if i<0: continue
            c = 0 if k>1 else (100 if is_fraco(words[cl[i]]["text"]) else 8)
            if j<n:
                u = words[cl[j-1]]["text"]
                # terminar em função é proibido na prática; em advérbio fraco, só evitado
                c += 90 if is_func(u) else (30 if is_fraco(u) else 0)
            d = words[cl[j-1]]["end"] - words[cl[i]]["start"]
            if   d < MIN_TELA:  c += 120     # pisca e some
            elif d < CONF_TELA: c += 25
            if d > MAX_TELA:    c += 40      # fica parada tempo demais
            # pausa longa dentro da tela deixa a legenda pendurada no silêncio
            c += 35*sum(1 for m in range(i+1, j)
                        if words[cl[m]]["start"] - words[cl[m-1]]["end"] > 0.45)
            if best[i]+c < best[j]: best[j]=best[i]+c; prev[j]=i
    out,j=[],n
    while j>0: out.append(cl[prev[j]:j]); j=prev[j]
    return list(reversed(out))

def telas_base(idxs, words, dest_idx):
    runs, cur = [], []
    for i in idxs:
        if cur and i != cur[-1]+1: runs.append(cur); cur=[]
        cur.append(i)
    if cur: runs.append(cur)
    telas=[]
    for run in runs:
        cl=[]
        for i in run:
            cl.append(i)
            if words[i]["text"].rstrip()[-1:] in ".,?!:;": telas += [{"idx":c,"dest":False} for c in dp_chunk(cl,words)]; cl=[]
        if cl: telas += [{"idx":c,"dest":False} for c in dp_chunk(cl,words)]
    return telas

# ---------- 5. PIPELINE POR VÍDEO ----------
def editar(vid, cfg):
    src = f"{ED}/{vid}.mp4"; wk = f"{OUT}/{vid}"; shutil.rmtree(wk, ignore_errors=True); os.makedirs(wk)
    words = [w for w in json.load(open(f"{OUT}/transcripts/{vid}.json"))["words"] if w.get("type")=="word"]
    segs, keep = planear_cortes(words, cfg["excluir"])
    idx_de = {id(w): i for i, w in enumerate(words)}
    # o corte pode remover a palavra que abria a frase ("Agora, dor localizada" no VID11),
    # deixando a legenda começar em minúscula. Recapitaliza na timeline de saída.
    for k in range(1, len(keep)):
        if keep[k-1]["text"].rstrip().endswith((".", "?", "!")) and keep[k]["text"][:1].islower():
            keep[k]["text"] = keep[k]["text"][0].upper() + keep[k]["text"][1:]

    # localizar escadinha
    esc = None
    if cfg["escada"]:
        alvos, cur = [], 0
        for txt, gatilho in cfg["escada"]:
            g = gatilho.lower().strip(",.?!:;")
            # busca sequencial: o gatilho de um degrau vem sempre depois do anterior.
            # ("quatro" abre o hook do VID7 e reaparece como quarto degrau aos 16 s)
            achou = next((k for k in range(cur, len(keep))
                          if keep[k]["text"].lower().strip(",.?!:;")==g), None)
            if achou is None: break
            alvos.append((txt, keep[achou])); cur = achou+1
        if len(alvos)==len(cfg["escada"]): esc = alvos

    esc_fim_w = None
    if esc:
        pos = {id(w): k for k, w in enumerate(keep)}
        kf = pos[id(alvos[-1][1])]
        while kf+1 < len(keep) and not keep[kf]["text"].rstrip().endswith((".","?","!")):
            kf += 1
        esc_fim_w = keep[kf]
    esc_span = (alvos[0][1]["start"]-0.15, esc_fim_w["end"]+0.6) if esc else None
    def seg_aberto(a,b): return esc_span and not (b <= esc_span[0] or a >= esc_span[1])

    # 5.1 vídeo: segmentos frame-exatos com zoom
    lines, offs, t = [], [], 0.0
    durs=[]
    for i,(a,b) in enumerate(segs):
        nf = round((b-a)*FPS); durs.append(nf)
        z0,z1,tp = plano_zoom(i, len(segs), seg_aberto(a,b))
        vf = (f"scale=2160:3840:flags=lanczos,{GRADE},zoompan=z='{zoom_expr(nf,z0,z1,tp)}':"
              f"x='1000*(1-1/zoom)':y='1600*(1-1/zoom)':d=1:s={W}x{H}:fps={FPS}")
        subprocess.run(["ffmpeg","-y","-v","error","-ss",f"{a:.4f}","-i",src,"-vf",vf,
                        "-frames:v",str(nf),"-an","-c:v","libx264","-crf","18","-preset","medium",
                        "-pix_fmt","yuv420p",f"{wk}/s{i}.mp4"], check=True)
        lines.append(f"file 's{i}.mp4'"); offs.append(round(t,4)); t += nf/FPS
    TOTAL = round(t,4)
    open(f"{wk}/cat.txt","w").write("\n".join(lines)+"\n")
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",f"{wk}/cat.txt",
                    "-c","copy",f"{wk}/base.mp4"], check=True)

    # 5.2 voz: passada única, fades 30ms, cauda mata a expiração
    ult = keep[-1]["end"]
    ch, pt = [], []
    for i,((a,b),nf) in enumerate(zip(segs,durs)):
        d = nf/FPS; fim = a+d
        if i==len(segs)-1 and ult+0.03 < fim:
            st = ult+0.03-a; fo = f"afade=t=out:st={st:.4f}:d={d-st:.4f}"
        else:
            fo = f"afade=t=out:st={d-0.03:.4f}:d=0.03"
        ch.append(f"[0:a]atrim={a:.4f}:{fim:.4f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03,{fo}[a{i}]")
        pt.append(f"[a{i}]")
    fc = ";".join(ch)+";"+"".join(pt)+f"concat=n={len(segs)}:v=0:a=1[v]"
    subprocess.run(["ffmpeg","-y","-v","error","-i",src,"-filter_complex",fc,"-map","[v]",
                    "-ar","48000","-c:a","pcm_s16le",f"{wk}/voz.wav"], check=True)

    def out_t(s):
        for (a,b),nf,o in zip(segs,durs,offs):
            if a-0.08 <= s <= a+nf/FPS+0.08: return max(0.0, min(s, a+nf/FPS)-a)+o
        return None

    # 5.3 telas de legenda
    esc_idx = set()
    if esc:
        ini_i = idx_de[id(alvos[0][1])]
        fim_w = esc_fim_w
        # a escadinha começa no início da oração do primeiro degrau, não na palavra-gatilho:
        # recua até a pontuação anterior. Senão sobra pendurado no fim da última tela base
        # o rótulo da enumeração ("Erro", VID10) ou o artigo do primeiro item ("o", VID5).
        passos = 0
        while (ini_i > 0 and passos < 4 and words[ini_i-1] in keep
               and not words[ini_i-1]["text"].rstrip().endswith((",", ".", ";", ":", "?", "!"))
               and words[ini_i]["start"] - words[ini_i-1]["end"] < 0.6):
            ini_i -= 1; passos += 1
        esc_idx = {i for i in range(ini_i, idx_de[id(fim_w)]+1)}
    dest_map, cur_d = {}, 0
    for frase, chaves in cfg["destaques"]:
        alvo = frase.split()[-1].lower().strip(",.?!:;")
        achou = next((k for k in range(cur_d, len(keep))
                      if keep[k]["text"].lower().strip(",.?!:;")==alvo), None)
        if achou is None: continue
        dest_map[idx_de[id(keep[achou])]] = chaves; cur_d = achou+1
    vis = [i for i,w in enumerate(words) if w in keep and i not in esc_idx]
    telas = telas_base(vis, words, set())
    for t_ in telas:
        t_["dest"] = any(i in dest_map for i in t_["idx"])
        t_["chaves"] = set().union(*[dest_map[i] for i in t_["idx"] if i in dest_map]) if t_["dest"] else set()
    return wk, segs, durs, offs, TOTAL, telas, esc, alvos if esc else None, esc_fim_w, out_t, words, keep

# ---------- 6. RENDER FINAL ----------
def montar(vid, cfg):
    wk, segs, durs, offs, TOTAL, telas, esc, alvos, esc_fim_w, out_t, words, keep = editar(vid, cfg)
    NF_TOT = sum(durs)

    # 6.1 assets de legenda
    faixa(340, 78, f"{wk}/band_leg.png"); faixa(620, 70, f"{wk}/band_esc.png")
    man=[]
    for k,s in enumerate(telas):
        pal=[words[i]["text"] for i in s["idx"]]
        tam = 96 if s["dest"] else 92
        img = encolhe(com_sombra(render_linha(pal, tam, s["chaves"])), W-56)
        p=f"{wk}/t{k:02d}.png"; img.save(p)
        ini, fim = out_t(words[s["idx"][0]]["start"]), out_t(words[s["idx"][-1]]["end"])
        if ini is None or fim is None: continue
        m={"png":p,"ini":round(ini,3),"fim":fim,"x":(W-img.width)//2,"y":Y_BLOCO-img.height//2,
           "dest":s["dest"],"txt":" ".join(pal)}
        if s["dest"]:
            nletras=sum(1 for c in m["txt"] if c!=" ")
            nf=max(2,int(((nletras-1)*0.032+0.27)*FPS)+1)
            tmp=f"{wk}/rev{k}"; os.makedirs(tmp, exist_ok=True)
            for fr in range(nf):
                tt=fr/FPS
                def lt(li, tt=tt):
                    st=0.06+li*0.032; pp=max(0.0,min(1.0,(tt-st)/0.15)); e=1-(1-pp)**3
                    return int(255*e),(1-e)*16
                com_sombra(render_linha(pal,tam,s["chaves"],letra_t=lt)).save(f"{tmp}/f_{fr:03d}.png")
            subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{tmp}/f_%03d.png",
                            "-c:v","qtrle",f"{wk}/d{k:02d}.mov"], check=True)
            ex=Image.open(f"{tmp}/f_000.png"); fat=min(1.0,(W-56)/ex.width)
            m.update({"mov":f"{wk}/d{k:02d}.mov","mdur":round(min(nf/FPS, m["fim"]-m["ini"]),3),
                      "mw":int(ex.width*fat),"mh":int(ex.height*fat)})
            m["mx"]=(W-m["mw"])//2; m["my"]=Y_BLOCO-m["mh"]//2
        man.append(m)
    for k,m in enumerate(man):
        f = m["fim"]+0.18
        if k+1 < len(man): f = min(f, man[k+1]["ini"]-0.02)
        m["fim"]=round(min(f,TOTAL),3)

    # 6.2 escadinha
    esc_info=None
    if esc:
        E_INI = out_t(alvos[0][1]["start"])-0.15
        E_FIM = min(TOTAL, (out_t(esc_fim_w["end"]) or TOTAL)+0.9)
        f66=ImageFont.truetype(F_CORPO,66); pr=ImageDraw.Draw(Image.new("RGBA",(4,4)))
        REG_H, STEP = 560, 112
        XOFF = [-150,-50,50,150][:len(alvos)] if len(alvos)==4 else [-120,0,120][:len(alvos)]
        degs=[]
        for di,(txt,w0) in enumerate(alvos):
            wt=sum(_adv(pr,c,f66,66) for c in txt)
            x=max(64,min((W-wt)/2+XOFF[di], W-40-wt))
            degs.append({"txt":txt,"t0":out_t(w0["start"])-E_INI,"x":x,"y":40+di*STEP})
        tmp=f"{wk}/esc"; os.makedirs(tmp, exist_ok=True)
        if E_FIM <= E_INI:
            raise RuntimeError(f"{vid}: escadinha com span invertido "
                               f"(ini {E_INI:.2f} > fim {E_FIM:.2f}); confira os gatilhos em config_lote")
        nf=int((E_FIM-E_INI)*FPS)+1
        for fr in range(nf):
            tt=fr/FPS; img=Image.new("RGBA",(W,REG_H),(0,0,0,0)); d=ImageDraw.Draw(img)
            for dg in degs:
                pd=max(0.0,min(1.0,(tt-dg["t0"])/0.25)); ed=1-(1-pd)**3
                if pd>0:
                    r=11*ed; cy=dg["y"]+40
                    d.ellipse([dg["x"]-38-r,cy-r,dg["x"]-38+r,cy+r], fill=(142,193,205,int(255*ed)))
                li,x=0,dg["x"]
                for c in dg["txt"]:
                    if c!=" ":
                        st=dg["t0"]+li*0.032; pp=max(0.0,min(1.0,(tt-st)/0.15)); e=1-(1-pp)**3
                        if pp>0: d.text((x,dg["y"]+(1-e)*16),c,font=f66,fill=(255,255,255,int(255*e)))
                        li+=1
                    x+=_adv(pr,c,f66,66)
            com_sombra(img).save(f"{tmp}/f_{fr:04d}.png")
        subprocess.run(["ffmpeg","-y","-v","error","-framerate","30","-i",f"{tmp}/f_%04d.png",
                        "-c:v","qtrle",f"{wk}/esc.mov"], check=True)
        esc_info={"mov":f"{wk}/esc.mov","ini":round(E_INI,3),"fim":round(E_FIM,3),
                  "y":Y_BLOCO-(REG_H+60)//2}

    # 6.3 lower third
    lt=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(lt)
    bx,by,bw,bh=48,1500,690,186
    d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=18,fill=(0,55,81,200))
    d.rectangle([bx,by+8,bx+10,by+bh-8],fill=AZUL_CLARO)
    d.text((bx+32,by+20),"Dr. Felipe Chiota",font=ImageFont.truetype(F_CORPO,48),fill=BRANCO)
    d.text((bx+32,by+86),"Ortopedista especialista em coluna",font=ImageFont.truetype(F_CORPO,31),fill=(225,232,235,255))
    d.text((bx+32,by+130),"CRM 162427 | RQE 73780",font=ImageFont.truetype(F_CORPO,31),fill=AZUL_CLARO)
    lt.save(f"{wk}/lt.png")

    # 6.4 composição (legendas por último)
    inp=["-i",f"{wk}/base.mp4","-loop","1","-t","3.2","-i",f"{wk}/lt.png",
         "-loop","1","-t",f"{TOTAL:.3f}","-i",f"{wk}/band_leg.png"]
    fc=["[2:v]format=rgba[bl]"]
    if esc_info:
        inp += ["-i",esc_info["mov"],"-loop","1","-t",f"{esc_info['fim']-esc_info['ini']:.3f}","-i",f"{wk}/band_esc.png"]
        fc += [f"[4:v]format=rgba,setpts=PTS-STARTPTS+{esc_info['ini']}/TB[be]",
               f"[0:v][bl]overlay=0:970:enable='lt(t,{esc_info['ini']})+gt(t,{esc_info['fim']})'[g1]",
               f"[g1][be]overlay=0:830:enable='between(t,{esc_info['ini']},{esc_info['fim']})'[g2]",
               f"[3:v]setpts=PTS-STARTPTS+{esc_info['ini']}/TB[esc]"]
        base_lbl, n = "g2", 5
    else:
        fc += ["[0:v][bl]overlay=0:970[g2]"]; base_lbl, n = "g2", 3
    fc += ["[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st=2.95:d=0.25:alpha=1,setpts=PTS-STARTPTS+1.0/TB[ltv]",
           f"[{base_lbl}][ltv]overlay=0:0:enable='between(t,1.0,4.2)'[v1]"]
    prev="v1"
    if esc_info:
        fc.append(f"[v1][esc]overlay=x=-30:y={esc_info['y']-30}:enable='between(t,{esc_info['ini']},{esc_info['fim']})'[v2]")
        prev="v2"
    for k,m in enumerate(man):
        dur=m["fim"]-m["ini"]
        if dur<=0.05: continue
        if m.get("mov"):
            inp+=["-i",m["mov"]]; md=min(m["mdur"],dur)
            fc.append(f"[{n}:v]scale={m['mw']}:{m['mh']},setpts=PTS-STARTPTS+{m['ini']}/TB[m{k}]")
            fc.append(f"[{prev}][m{k}]overlay={m['mx']}:{m['my']}:enable='between(t,{m['ini']},{m['ini']+md:.3f})'[p{k}a]"); n+=1
            inp+=["-loop","1","-t",f"{max(dur-md,0.02):.3f}","-i",m["png"]]
            fc.append(f"[{n}:v]format=rgba,setpts=PTS-STARTPTS+{m['ini']+md:.3f}/TB[q{k}]")
            fc.append(f"[p{k}a][q{k}]overlay={m['x']}:{m['y']}:enable='between(t,{m['ini']+md:.3f},{m['fim']})'[p{k}]"); n+=1
        else:
            inp+=["-loop","1","-t",f"{dur:.3f}","-i",m["png"]]
            fc.append(f"[{n}:v]format=rgba,fade=t=in:st=0:d=0.05:alpha=1,fade=t=out:st={max(dur-0.05,0):.3f}:d=0.05:alpha=1,setpts=PTS-STARTPTS+{m['ini']}/TB[b{k}]")
            fc.append(f"[{prev}][b{k}]overlay={m['x']}:{m['y']}:enable='between(t,{m['ini']},{m['fim']})'[p{k}]"); n+=1
        prev=f"p{k}"
    subprocess.run(["ffmpeg","-y","-v","error"]+inp+["-filter_complex",";".join(fc),"-map",f"[{prev}]",
                   "-an","-frames:v",str(NF_TOT),"-c:v","libx264","-crf","18","-preset","medium",
                   "-pix_fmt","yuv420p",f"{wk}/video.mp4"], check=True)

    # 6.5 áudio: voz + trilha com ducking, -14 LUFS
    bed=f"{OUT}/trilha_bed.mp3"
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"{wk}/voz.wav","-i",bed,"-i",bed,"-i",bed,
      "-filter_complex",
      f"[1:a][2:a]acrossfade=d=2[b1];[b1][3:a]acrossfade=d=2[bl];"
      f"[bl]volume=0.09,atrim=0:{TOTAL:.3f},afade=t=in:st=0:d=0.6,afade=t=out:st={max(TOTAL-1.25,0):.3f}:d=1.25[bed];"
      f"[0:a]asplit[v1][v2];[bed][v2]sidechaincompress=threshold=0.015:ratio=10:attack=15:release=500:makeup=1[bd];"
      f"[v1][bd]amix=inputs=2:duration=first:normalize=0[mix]",
      "-map","[mix]","-ar","48000","-c:a","pcm_s16le",f"{wk}/premix.wav"], check=True)
    m=subprocess.run(["ffmpeg","-i",f"{wk}/premix.wav","-af",
        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json","-f","null","-"],
        capture_output=True, text=True).stderr
    j=json.loads(m[m.rfind("{"):m.rfind("}")+1])
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"{wk}/video.mp4","-i",f"{wk}/premix.wav","-af",
        f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
        f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
        "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k",
        "-movflags","+faststart",f"{OUT}/{vid}_FINAL.mp4"], check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"{OUT}/{vid}_FINAL.mp4","-vf","scale=720:1280",
        "-c:v","libx264","-crf","23","-preset","medium","-pix_fmt","yuv420p","-c:a","copy",
        f"{OUT}/{vid}_proxy.mp4"], check=True)
    # 6.6 plano para os portões de qualidade (scripts/qa.py)
    json.dump({"total": TOTAL, "segs": segs, "escada": bool(esc_info),
               "screens": [{"texto": m["txt"], "ini": m["ini"], "fim": m["fim"],
                            "png": m["png"], "dest": m["dest"]} for m in man]},
              open(f"{OUT}/plan_{vid}.json", "w"), ensure_ascii=False, indent=1)

    return {"vid":vid,"dur":TOTAL,"segs":len(segs),"telas":len(man),
            "dest":sum(1 for m in man if m.get("mov")),"escada":bool(esc_info)}

if __name__ == "__main__":
    sys.path.insert(0,"/home/user/drfelipechiota-conteudo/scripts")
    from config_lote import CONFIG
    falhas = []
    for v in sys.argv[1:]:
        try:
            r = montar(v, CONFIG[v])
        except Exception as e:                 # um vídeo quebrado não derruba o lote
            falhas.append((v, f"{type(e).__name__}: {e}"))
            print(f"FALHA {v}: {type(e).__name__}: {e}", flush=True)
            continue
        print(f"OK {r['vid']}: {r['dur']}s | {r['segs']} segs | {r['telas']} telas | "
              f"{r['dest']} destaques | escadinha={r['escada']}", flush=True)
    for v, e in falhas:
        print(f"PENDENTE {v}: {e}", flush=True)
    sys.exit(1 if falhas else 0)
