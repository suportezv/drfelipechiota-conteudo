# Reels jul/ago 2026: mapeamento dos brutos

Pasta Drive: "Dr. Felipe Chiota - Brutos" (`1K2KbBds5POHZNZfJpLmdw_Y2FkBA-4F2`), download público por curl OK (conferido 2026-08-20).

Docs de referência na mesma pasta:

- `Roteiros - Felipe Chiota.pdf` (`14VIvOdkj-60prGECx8QMM4vAgXiQ-gzh`): os 12 roteiros originais.
- `Chiota_Reels_JulAgo_Roteiros_de_Gravacao.docx` (`1fwHq-JKuOzc3AuifI6SGrT4oPEyeZv-G`): **fonte da verdade da edição**. Roteiros reescritos take a take com GC de capa, lower third, objetivo/CTA por vídeo, setups, b-roll e compliance CFM.

Brutos: 19 arquivos, todos 1080x1920 SDR bt709 8-bit 30 fps (não HLG; sem proxy). Identificação por transcrição Scribe dos 12 s iniciais (2026-08-20).

## Versões novas (roteiro do DOCX, usar estas na edição)

| Bruto | Roteiro DOCX | Duração bruto | Alvo | Objetivo |
|---|---|---|---|---|
| VID4 | 1 Medo do especialista | 49s | 35s | Conversão |
| VID5 | 2 Repouso piora | 38s | 32s | Conversão |
| VID8 | 3 Dorflex toda semana | 35s | 35s | Distribuição (share) |
| VID7 | 4 Quatro sinais de alerta | 36s | 40s | Conversão + save |
| VID10 | 5 Postura no trabalho (3 erros) | 42s | 40s | Distribuição (save/marcar) |
| VID11 | 6 Dor pós-treino | 37s | 35s | Conversão |
| VID13 | 7 Hérnia cervical | 41s | 35s | Conversão |
| VID15 | 8 Posicionamento | 57s | 35s | Conta (seguir) |
| VID16 | 9 Dor precoce nos jovens | 40s | 33s | Conversão |
| VID17 | 12 Volta ao esporte | 45s | 35s | Conversão |

## Takes antigos (roteiro original do PDF, com intro falada; usar só como material alternativo)

| Bruto | Roteiro original | Duração |
|---|---|---|
| VID1 | 1 Medo do especialista | 53s |
| VID2 | 2 Repouso | 75s |
| VID3 | 3 Remédio toda semana | 45s |
| VID3CV | 3 Remédio toda semana (take "contato visual") | 40s |
| VID6 | 4 Sinais de alerta | 99s |
| VID9 | 5 Postura e trabalho | 47s |
| VID12 | 7 Hérnia cervical | 60s |
| VID14 | 8 Apresentação | 51s |
| VID18 | 12 Esporte e emocional | 51s |

## Lacunas e confirmações

- **Não gravados em nenhuma versão**: vídeo 10 (Escoliose no adolescente) e vídeo 11 (Coluna travada de manhã, o roteiro de melhor nota do lote).
- Pergunta em aberto do DOCX sobre o vídeo 8 **respondida pelo próprio bruto**: no VID15 o Dr. fala "Sou especialista em cirurgia de coluna", então o hook original do roteiro vale.
- VID2 tem ruído de claquete verbal no início ("Exato. Vamo lá."); VID3 idem ("Posso? Pode."). Cortar na edição se esses takes forem usados.

## Status de produção

| Vídeo | Roteiro | Status |
|---|---|---|
| VID8 | 3 Dorflex | **Final aprovada e renderizada** (1080x1920, 33,5 s, -14.1 LUFS) |
| VID4, VID5, VID7, VID10, VID11, VID13, VID15, VID16, VID17 | demais | Bloqueados: sem rota de transcrição word-level (ver abaixo) |

## Bloqueio de transcrição (2026-08-26)

O estilo aprovado depende de timestamps por palavra. As três rotas testadas:

- **ElevenLabs Scribe**: cota do plano free esgotada (10000/10000), reset só em **2026-09-18**.
- **Whisper local** (`hyperframes transcribe`, whisper.cpp): funciona e dá word-level, mas o download do modelo falha porque `huggingface.co` e CDNs (`cdn-lfs.huggingface.co`, `cas-bridge.xethub.hf.co`) estão fora do allowlist do environment.
- **Descript** (conector ativo, drive da própria agência): bloqueado pelo classificador de permissões por enviar footage do cliente a serviço externo; depende de autorização explícita do usuário.

**Solução recomendada**: liberar `huggingface.co` + `cdn-lfs.huggingface.co` + `cas-bridge.xethub.hf.co` no environment. Isso torna a transcrição local, gratuita, offline e sem enviar material do cliente para terceiros.
