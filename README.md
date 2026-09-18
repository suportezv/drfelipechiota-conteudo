# Dr. Felipe Chiota Conteúdo Studio

Estúdio de edição e agendamento de conteúdo para as redes da marca **Dr. Felipe Chiota**. Infraestrutura compartilhada da agência; posicionamento desta marca.

- **`FRAMEWORK.md`**: persona, regras, pilares, assinaturas de edição, escolha HyperFrames vs Remotion e fluxo por vídeo.
- **`CLAUDE.md`**: memória persistente do projeto (IDs, contas, rede, gotchas).
- **`SETUP.md`**: environment, conectores e validação.
- **`projects/`**: um subdiretório por vídeo (briefing, transcrição, scripts de edição, caption).
- **`scripts/`**: setup e validação do ambiente (Linux/cloud) e os scripts genéricos de produção (decupagem por âncora, LUT S-Log2, ZIP remoto, imagem por IA, upload para o Drive).
- **`remotion/`**: composições Remotion (React/TS). Paleta em `src/marca.ts`, rodapé em `src/Root.tsx`.

## Primeiro uso (cloud)

```bash
bash scripts/setup.sh
bash scripts/validate.sh
```

Depois: coloque o bruto no Drive (pasta pública) ou anexe na conversa, escreva o briefing em `projects/<nome>/` e peça a edição.

| Serviço | Uso | Configuração |
|---|---|---|
| Google Drive | Brutos | Pasta "Dr. Felipe Chiota - Brutos" (pública) + domínios liberados no environment |
| Metricool | Agendamento | Marca "drfelipechiota", blog_id 6741532, só Instagram conectado |
| ElevenLabs | Transcrição, trilha, SFX, TTS | Chave `sk_...` na env var e no `.env` do video-use |
| Kairogen | B-roll por IA | Conta da agência (FREE, sem créditos) |
| OpenAI / Gemini | Imagem por IA | Chaves ausentes e hosts bloqueados; ver `CLAUDE.md` |

> Este repositório é **público** de propósito: o agendamento no Metricool depende de servir o render por `raw.githubusercontent.com`. Nunca commitar chaves aqui.
