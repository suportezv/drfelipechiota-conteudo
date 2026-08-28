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

Lote fechado em 2026-08-28 com `scripts/pipeline.py` + `scripts/config_lote.py`, estilo aprovado no VID8.
Todos passaram nos 7 portões de `scripts/qa.py` (63 verificações, nenhuma falha).

| Vídeo | Roteiro | Duração | Telas | Escadinha | Viés sinc. | p90 | LUFS |
|---|---|---|---|---|---|---|---|
| VID4 | 1 Medo do especialista | 44,4s | 50 | 4 tratamentos | +0,0 ms | 14,0 ms | -14,1 |
| VID5 | 2 Repouso piora | 36,2s | 39 | 4 pilares | +0,0 ms | 20,0 ms | -14,1 |
| VID8 | 3 Dorflex toda semana | 33,5s | 45 | 4 etapas | 0 ms | | -14,1 |
| VID7 | 4 Quatro sinais | 33,1s | 24 | 4 sinais | -7,0 ms | 14,0 ms | -14,1 |
| VID10 | 5 Postura no trabalho | 39,8s | 30 | 3 erros | +6,0 ms | 13,1 ms | -14,1 |
| VID11 | 6 Dor pós-treino | 34,3s | 49 | não | +7,0 ms | 14,0 ms | -14,0 |
| VID13 | 7 Hérnia cervical | 33,2s | 30 | 3 condutas | +0,5 ms | 15,0 ms | -14,0 |
| VID15 | 8 Posicionamento | 35,0s | 45 | não | +1,0 ms | 20,0 ms | -14,0 |
| VID16 | 9 Dor precoce nos jovens | 35,6s | 44 | não | +1,0 ms | 20,7 ms | -14,1 |
| VID17 | 12 Volta ao esporte | 31,0s | 34 | 3 pilares | +0,0 ms | 20,0 ms | -14,0 |

Retakes e gaguejos cortados: VID4 "Esse mes-- medo"; VID7 "pre--" antes de "existem";
VID11 "Agora," pendurado; VID13 take abortado "e se você--"; VID15 take abortado + "Peraí";
VID17 "mas parar..." abortado.

**Correção de transcrição**: no VID15 o Scribe grafou "Felipe Schotta". O nome da marca passa
por dicionário de correção antes de virar legenda, com portão próprio em `qa.py`.

## Defeitos encontrados na primeira passada (todos viraram portão)

| Defeito | Onde | Correção |
|---|---|---|
| Gatilho de degrau casando com palavra igual anterior | VID7 (o "quatro" do hook) | busca sequencial por degrau |
| Fim da frase vazando como legenda base sobre a escadinha | VID7, VID10, VID13, VID17 | região vai até a pontuação final |
| Rótulo ou artigo pendurado antes da escadinha | VID4, VID5, VID10, VID13 | recuo até a pontuação anterior |
| Telas de 5 a 7 palavras | VID10, VID11, VID15, VID16 | duração virou critério do DP; fusão pós-DP removida |
| Legenda em minúscula abrindo frase | VID11, VID13 | recapitalização pós-corte |
| Nome próprio errado | VID15 | dicionário de correção |

Dois portões estavam calibrados errado e foram corrigidos: o de sincronia media a mediana do
|desvio| contra 10 ms, abaixo do piso do instrumento (grade de 33 ms, Scribe em passos de 10 a
20 ms), e o de ruído acusava o fade final desenhado. Ver `FRAMEWORK.md`.

## Próximo passo

Aguardando aprovação dos proxies para renderizar as entregas finais. Agendamento no Metricool
segue bloqueado: a marca não tem redes conectadas (networksData vazio).
