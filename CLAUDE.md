# Dr. Felipe Chiota Conteúdo Studio (memória persistente do projeto)

Este repositório é o **Dr. Felipe Chiota Conteúdo Studio**: edição e agendamento de conteúdo para as redes da **Dr. Felipe Chiota**. Estúdio da agência com infraestrutura compartilhada; o posicionamento é o desta marca.

**Antes de editar qualquer vídeo ou escrever qualquer caption, leia `FRAMEWORK.md`** (posicionamento, regras inegociáveis, formatos, assinaturas de edição e todos os gotchas técnicos).

> Marca, persona, voz, CTA e credencial são próprios desta marca e ainda estão **PENDENTE**: perguntar, nunca inventar nem herdar de estúdio irmão. O material de briefing do cliente existe no Drive (ver "Ativos da marca no Drive") e é a fonte para preencher, mas nada ali vira regra sem confirmação.

## Regras que valem em qualquer resposta pública

- Nunca usar travessão em texto público (caption, lettering, legenda): reescrever a frase.
- Quando citar a criadora ou criador: sempre a credencial completa **"PENDENTE (credencial completa de quem cria, para citação em texto público)"**.
- Palavrão em vídeo **se bipa, não se corta**.
- Loudness final: **-14 LUFS**.

## Working dirs

- Estúdio: este repo (symlink `~/drfelipechiota-conteudo` aponta para cá). Projetos em `projects/<nome>/`.
- Ferramentas: `video-use` e `hyperframes` clonados em `/workspace/browser-use/` e `/workspace/heygen-com/` (Linux/cloud) ou `~/video-editor/` (Mac). Skills registradas em `~/.claude/skills/` (video-use + 20 do hyperframes).
- **Remotion**: composições versionadas em `remotion/` (React/TS); `node_modules` fora do git, instalado pelo `setup.sh`. `npm run studio` abre o editor, `npx remotion render src/index.ts <Composicao> saida.mp4` renderiza. Componentes prontos: `Aurora` (fundo) e `CartaoTitulo`; a paleta vive só em `remotion/src/marca.ts` (hoje placeholder, ver PENDENTE lá) e o rodapé em `Root.tsx`.
- **Scripts genéricos** (portados do `profissioai-conteudo` em 18/set/2026 seguindo o `PORTAR.md` daquele repo; zero referência de marca, conferido por grep):
  - `scripts/decupar.py`: decupa por **âncoras de texto** ("de tal frase até tal frase") casadas contra a transcrição Scribe com timestamp por palavra; junta trechos, gira, aplica LUT, normaliza áudio.
  - `scripts/relatorio_decupagem.py`: retranscreve as peças finais e relata o que ficou e o que caiu.
  - `scripts/gera_lut_slog2.py`: LUT 3D S-Log2/S-Gamut para Rec.709 via `colour-science`.
  - `scripts/zip_index_remoto.py`: lista e extrai arquivos de um ZIP gigante no Drive por range request, sem baixar o ZIP.
  - `scripts/gera_imagem.py`: imagem pela OpenAI ou pelo Gemini, chaves só por env var (**hoje sem chave e sem rede aqui**, ver IDs e Rede).
  - `scripts/sobe_para_drive.py`: upload para pasta do Drive com token (**hoje sem rede**: `www.googleapis.com` bloqueado).
- Ambiente novo (container limpo): rode `bash scripts/setup.sh` e depois `bash scripts/validate.sh`. **Em sessão nova, conferir `ls /workspace` antes de contar com video-use ou hyperframes**: em 18/set/2026 a sessão nasceu sem ffmpeg e com `/workspace` vazio, ou seja, o gatilho de boot do environment não rodou o setup. Causa conhecida nos estúdios irmãos: o campo de setup script usa caminho relativo e o boot roda no diretório pai do repo. Corrigir no environment para `bash /home/user/drfelipechiota-conteudo/scripts/setup.sh` (caminho absoluto); até lá, rodar à mão.

## IDs e contas (verificados em 18/set/2026)

- Instagram da marca: **@drfelipechiota** (única rede conectada no Metricool).
- **Metricool**: conta da agência (`suporte@zavi.ag`). Marca **"drfelipechiota"**, **blog_id 6741532**, timezone America/Sao_Paulo, marca criada em 18/ago/2026.
  - Redes conectadas: **só Instagram** (`instagramData: drfelipechiota`). Sem Facebook, TikTok, YouTube, LinkedIn ou Pinterest. A regra de agendamento abaixo ("todos os canais conectados") hoje significa **Instagram REEL apenas**; conectar as demais no painel antes de esperar multi-rede.
  - Melhor horário de publicação: medir com `getBestTimeToPostByNetwork` (marca nova, pouco histórico).
- **Regra de agendamento (todas as marcas da agência)**: sempre incluir TODOS os canais conectados da marca no post, exceto YouTube horizontal. YouTube entra como **Short** (`youtubeData: {type: "short", title, madeForKids: false}`); Instagram como REEL; Facebook como REEL; TikTok, LinkedIn e Pinterest com networkData padrão. Nunca publicar vídeo vertical como YouTube horizontal comum.
- **Kairogen**: conta da agência (`suporte@zavi.ag`), plano **FREE, 0 créditos**, 1 geração concorrente. **B-roll por IA indisponível** até haver créditos.
- **ElevenLabs**: chave `sk_` (51 chars) presente em `ELEVENLABS_API_KEY` do environment; o `setup.sh` grava em `.env` na raiz do video-use. Escopos necessários: TTS, STT Scribe, sound-generation, voices_read (conferir sem gastar: endpoint com parâmetro inválido, `401 missing_permissions` = escopo ausente). Plano e cota: **PENDENTE conferir**. Voz da marca para narração: **PENDENTE (voice_id, modelo e settings)**.
- **OpenAI e Gemini (imagem)**: `OPENAI_API_KEY` e `GEMINI_API_KEY` **ausentes** neste environment, e `api.openai.com` e `generativelanguage.googleapis.com` **bloqueados** na allowlist. `gera_imagem.py` só funciona depois de cadastrar chave (env var do environment, sessão nova) e liberar os hosts.
- **Drive (brutos)**: pasta **"Dr. Felipe Chiota - Brutos"**, id `1K2KbBds5POHZNZfJpLmdw_Y2FkBA-4F2`, dona `suporte@zavi.ag`, **pública (qualquer pessoa com o link: leitor)**, então download direto por curl funciona. Conteúdo em 18/set/2026: `VID1.mp4` a `VID18.mp4` (67 a 188 MB, gravados em 20/ago/2026, mais `VID3 CONTATO VISUAL.mp4`), `REFERENCIA 1` a `4` (mov/MP4), `Roteiros - Felipe Chiota.pdf` e `Chiota_Reels_JulAgo_Roteiros_de_Gravacao.docx`.

## Ativos da marca no Drive (localizados em 18/set/2026)

- Pasta do cliente **"Dr. Felipe Chiota_Cliente"** (`1zV2ZOtTWjt1oC9zVBNJYKQS4KbPqWaEy`), subpastas: Conteúdo, Briefing, Planilha, Material Blog, Docs enviados pelo cliente.
- **Logo vetorial**: `Logotipo_DR_Felipe_Chiota_02CURVA.pdf` (`1XUU2gqtPlCFDtQ2i56_t7EE5AbYIfU8S`, 3,2 MB) em "Docs enviados pelo cliente" (`1nzS-gP9jIwy1bUnK6UDhe3C5rmw5S7Xb`), com papel de carta e cartões. **A pasta não é pública**: curl falha e o conector devolve base64 na conversa (inviável). Para extrair a paleta: tornar a pasta pública ou passar os hexes.
- **Briefings mensais** (Google Docs) na subpasta Briefing (`1XX_yFneFfybbNE3CugLiE49P_a9e1UfL`), março a setembro de 2026. Tema dominante: coluna (dor, hérnia de disco, cirurgia, relaxantes musculares, medicina regenerativa). CTA que se repete nos carrosséis de julho: "Vamos avaliar o seu caso? Link na bio" (observado, **não confirmado como CTA padrão**).
- Ficha do cliente (doc `14MP1NtZwIY1wNq9h1ox-ea3Pdu5-tx3B1Sqj3aVkKaY`): links para fotos profissionais (Dropbox), análise do Instagram e posts modelo.
- Planilhas: "Felipe Chiota- Planejamento de Conteúdo" e "@drfelipechiota [awareness e leads]".

## Rede do environment (verificado em 18/set/2026)

Diagnóstico de qualquer host: `curl -sv https://host/ 2>&1 | grep CONNECT`. `HTTP/1.1 403` no CONNECT = fora da allowlist; qualquer outra resposta = rede passou, o problema é outro (chave, quota, rota). A allowlist é literal por subdomínio: `www.googleapis.com` não cobre `generativelanguage.googleapis.com`; para um site inteiro usar `*.dominio.com` junto do apex.

| Host | Status | Observação |
|---|---|---|
| `api.elevenlabs.io` | OK | TTS, STT, SFX |
| `drive.google.com`, `drive.usercontent.google.com` | OK | brutos por curl |
| `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org` | OK | pip, uv e npm funcionam; o `setup.sh` ainda força a rota pelo proxy (gotcha herdado, inofensivo) |
| `api.github.com`, `github.com`, `objects.githubusercontent.com` | OK | clones e ffmpeg estático dos Releases |
| `raw.githubusercontent.com` | **403** | não precisa liberar: skills do hyperframes vêm do clone local |
| `api.openai.com` | **403** | liberar se `gera_imagem.py openai` for usado |
| `generativelanguage.googleapis.com` | **403** | liberar se `gera_imagem.py gemini` for usado |
| `www.googleapis.com` | **403** | `sobe_para_drive.py` indisponível |
| `static.metricool.com` | bloqueado | logo da marca no Metricool não baixa daqui |
| `archive.ubuntu.com` | 403 | apt indisponível; ffmpeg vem estático (BtbN, ~151 MB) |

## Gotchas essenciais (herdados dos estúdios da agência, todos validados)

- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez antes de editar (filtro `colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc`).
- **Brutos de Sony em S-Log2 (A7 III): converter, não "filtrar".** O XML lateral de cada clipe (`C00xxM01.XML`) declara `CaptureGammaEquation` e `CaptureColorPrimaries`; quando diz `s-log2`/`s-gamut`, a imagem chega chapada e precisa de conversão para Rec.709. `scripts/gera_lut_slog2.py` gera a LUT (log, linear, primárias, ombro, gama). Dois cuidados: **`--exposicao -0.5` e `--joelho 0.65`** (os defaults são 0 e 0,80), senão o branco estoura; e conferir que o ffmpeg aplica a `lut3d` **em RGB, não em YUV** (verificar com `-v verbose`). Saída sempre com `out_range=tv` e `-color_range tv`.
- **Câmera pode gravar na vertical sem gravar a flag de rotação.** O arquivo vem 3840x2160 deitado e o ffprobe não mostra rotação; só olhando um frame se descobre. Corrigir com `transpose=1` antes de escalar. Checar um frame de qualquer lote novo antes de planejar o corte.
- **Decupagem por âncora de texto, não por timecode.** `scripts/decupar.py` recebe um `edl.json` onde cada trecho é "de tal frase até tal frase" e resolve os tempos contra a transcrição Scribe. Revisar um corte vira editar uma frase. O campo `apos` empurra o cursor quando a mesma frase aparece antes.
- **Upload de vídeo para o Drive não é possível deste container.** `www.googleapis.com` está fora da allowlist e o conector MCP só aceita `base64Content` na própria chamada. Criar pasta funciona. Entrega de vídeo sai por commit na branch ou pelo envio do arquivo na conversa.
- **Processo em background com `nohup`/`setsid` é recolhido quando a tool call retorna.** Usar `run_in_background: true` da própria ferramenta Bash, que o harness rastreia. Em lote longo, `flock` num arquivo de lock evita dois loops escrevendo o mesmo arquivo.
- **Remotion renderiza com o `headless_shell`, não com o Chromium do Playwright.** O `chromium-1194` removeu o headless antigo e o launch morre com "Old Headless mode has been removed". O binário certo é `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, fixado em `remotion/remotion.config.ts`. Baixar o browser próprio do Remotion está fora da allowlist.
- **Licença do Remotion não é MIT.** Grátis para indivíduo, organização sem fins lucrativos, empresa de até 3 funcionários e avaliação; acima disso exige Company License (remotion.pro). **Confirmar o enquadramento antes de usar em produção.**
- **Sem rede de fontes no render.** Google Fonts está fora da allowlist; a fonte da marca precisa entrar como asset local.
- **O patch `video-use-is-portrait-source` foi aposentado (18/set/2026).** O upstream lê o `rotation` do side data. O `validate.sh` testa **comportamento** (retrato, paisagem e paisagem com matriz de rotação 90) em vez de procurar patch no código.
- **A URL do ffmpeg estático tem uma forma certa.** `releases/download/latest/…` serve o arquivo; `releases/latest/download/…` devolve 404. O `setup.sh` tenta as duas em ordem e confere a assinatura XZ antes de extrair.
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG sequence + qtrle (ou PNG estático com fade de alpha).
- Zoom animado com `zoompan`, não `crop` (crop não aceita `t` em w/h).
- Metricool MCP: sem delete (cancelar = update `draft:true`; update devolve id novo); mídia por URL pública (o Metricool copia para o CDN dele na hora).
- **Metricool, rascunho com data vencida não publica e não avisa.** Um post `draft:true` cuja data passa continua no calendário como se agendado, mas nunca dispara. Regra: **quem agenda tira do rascunho na mesma sessão e confirma com `getScheduledPosts`**. Tirar do rascunho com a data no passado também não resolve; é preciso data nova.
- **Ler o índice de um ZIP gigante no Drive sem baixar o arquivo.** `drive.usercontent.google.com` aceita `Range`; `scripts/zip_index_remoto.py` acha o EOCD (e o ZIP64 em arquivo >4 GB), lista o central directory e extrai entradas `stored` por outro `Range`.
- Mac: usar ffmpeg-full keg-only com PATH explícito. Linux: apt bloqueado no cloud, o `setup.sh` instala o build estático.
- Cloud, brutos do Drive: environment com network Custom e `drive.google.com` + `drive.usercontent.google.com` + `api.elevenlabs.io` liberados. Download direto de arquivo público, qualquer tamanho: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`. Arquivo em pasta **não pública** redireciona para login e o curl devolve `000`. O conector MCP do Drive serve para busca e metadados; download por ele só até ~4 MB. Fallback para arquivo público pequeno: Kairogen `download_audio_from_url`.
- Cloud, mídia pública para o Metricool: commit temporário do render na branch (repo público, `raw.githubusercontent.com` é lido pelo servidor do Metricool, não por este container), agendar e remover o arquivo em seguida. Exige `git add -f` (o `.gitignore` barra mídia) com autorização do usuário. **Por isso este repo deve ser público** (confirmado: visibility public).
- Trilhas/SFX: ElevenLabs sound-generation (`/v1/sound-generation`, máx ~22s, `duration_seconds` entre 0.5 e 30) gera beds e SFX ótimos; para trilha maior, gerar build+drop e costurar com `acrossfade`. Detecção de BPM/batidas: script próprio com numpy (fluxo de energia + autocorrelação).
- **Skills do hyperframes sem rede**: `npx hyperframes skills update` falha com `raw.githubusercontent.com` bloqueado; o `setup.sh` registra as 20 skills direto do clone.
- **Chave de API entra na criação do container.** Cadastrar env var no environment com a sessão aberta não faz a sessão enxergar: precisa de sessão nova. Conferir com `printenv | grep -c API_KEY` antes de acusar o script.
- **Instagram exige login, mesmo liberado na rede.** Ler perfil ou post anonimamente não funciona (302 para login, 401 na API). Para analisar feed: prints do usuário, o conector do Metricool (contas conectadas à marca) ou a Graph API da Meta com token.

## Histórico de decisões

- 18/set/2026: bootstrap do estúdio; PR #1 consertou o `setup.sh` (ffmpeg estático, rede pelo proxy, nenhum passo derruba o boot).
- 18/set/2026: port do cinto de ferramentas do `profissioai-conteudo` (branch `claude/reels-automaticos-profissio-d0qk2d`, guia `PORTAR.md`): 6 scripts genéricos, `remotion/`, `validate.sh` por comportamento, `colour-science` no setup, patch do video-use aposentado. Paleta do Remotion ficou placeholder até a marca entregar os hexes.
