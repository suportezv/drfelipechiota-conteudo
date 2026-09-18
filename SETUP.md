# Setup do Dr. Felipe Chiota Conteúdo Studio

Espelho do setup dos estúdios irmãos. No cloud, basta:

```bash
bash scripts/setup.sh
bash scripts/validate.sh
```

## Environment (Claude Code cloud)

Network **Custom** com `drive.google.com`, `drive.usercontent.google.com` e `api.elevenlabs.io` na lista de domínios, mais a env var `ELEVENLABS_API_KEY` e o setup script. Configura-se no seletor de nuvem acima da caixa de mensagem em claude.ai/code (não nas Configurações gerais). **Mudanças valem para sessões novas.**

- **Setup script: usar caminho absoluto.** `bash /home/user/drfelipechiota-conteudo/scripts/setup.sh`. Com caminho relativo o boot roda no diretório pai do repo e falha com exit 127; a sessão nasce sem ffmpeg e sem `/workspace`. Versão à prova de diretório, idêntica nos estúdios irmãos:
  ```bash
  for p in ./scripts/setup.sh ./*/scripts/setup.sh; do [ -f "$p" ] && exec bash "$p"; done; p=$(find /home /workspace /repo /app /src -maxdepth 4 -type f -path "*/scripts/setup.sh" 2>/dev/null | head -1); [ -n "$p" ] && exec bash "$p"; echo "setup.sh nao encontrado no repo"; exit 1
  ```
- Hosts a liberar se as ferramentas correspondentes forem usadas: `api.openai.com` e `generativelanguage.googleapis.com` (`gera_imagem.py`), `www.googleapis.com` (`sobe_para_drive.py`). Allowlist é literal por subdomínio.
- Chaves opcionais, só como env var do environment (nunca no repo, nunca no chat): `OPENAI_API_KEY`, `GEMINI_API_KEY`.

## Conectores (cada um exige ação do usuário)

- **Google Drive**: conector oficial do Claude. Pasta de brutos **"Dr. Felipe Chiota - Brutos"** (`1K2KbBds5POHZNZfJpLmdw_Y2FkBA-4F2`), pública, download direto por curl.
- **Metricool**: conta da agência `suporte@zavi.ag`. Marca **"drfelipechiota"**, **blog_id 6741532**. Só Instagram conectado; Facebook, TikTok, YouTube, LinkedIn e Pinterest ainda não.
- **Kairogen**: conta da agência, plano **FREE, 0 créditos**. B-roll por IA indisponível até haver créditos.
- **ElevenLabs**: chave `sk_...` (51 chars) presente. Escopos e cota: conferir.

## Validação final

1. `bash scripts/validate.sh` verde: ffmpeg com `subtitles` e `zscale`, `is_portrait_source` acertando retrato, paisagem e girado, ElevenLabs no `.env`, rede, render de 1 frame no Remotion, skills registradas.
2. Metricool: `getBrandSettings` lista "drfelipechiota" com blog_id 6741532.
3. Kairogen: `get_me_context` mostra plano e créditos.
4. Memória persistente: `CLAUDE.md` deste repo.

## Pendências de marca (bloqueiam produção de texto público)

- Persona, tom de voz, pilares e CTA padrão (`FRAMEWORK.md`).
- Credencial completa para citação em texto público.
- Paleta oficial e fonte (`remotion/src/marca.ts` está placeholder; o logo vetorial está no Drive em pasta não pública).
- Voz da marca na ElevenLabs (voice_id, modelo, settings).
