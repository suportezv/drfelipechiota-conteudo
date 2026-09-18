# Dr. Felipe Chiota Conteúdo Studio: FRAMEWORK

Estúdio de edição e agendamento para as redes da **Dr. Felipe Chiota**. Framework compartilhado da agência, adaptado para esta marca.

> Os blocos marcados **PENDENTE** dependem do briefing de posicionamento da marca e serão preenchidos e commitados quando confirmados.

## Persona e voz do perfil

- **PENDENTE**: persona, tom de voz e posicionamento da Dr. Felipe Chiota (definir no primeiro briefing).
- CTA padrão: **PENDENTE (CTA padrão da marca)**.
- Quando citar a criadora ou criador: credencial sempre completa, **"PENDENTE (credencial completa de quem cria, para citação em texto público)"**.

### REGRAS INEGOCIÁVEIS

1. **Nunca usar travessão em texto público.** Reescrever a frase.
2. Credencial sempre completa: **"PENDENTE (credencial completa de quem cria, para citação em texto público)"**.
3. Palavrão em vídeo **se bipa, não se corta** (sine 1000 Hz curto, voz mutada no trecho).
4. Loudness final: **-14 LUFS**.

## Pilares de conteúdo

**PENDENTE**: definir com o primeiro briefing (tratar como hipóteses iniciais e validar com desempenho).

## Assinaturas de edição

Padrão validado da agência:

- Hook verbal ou visual + título na tela nos **2 primeiros segundos**.
- Lettering condensado caps branco com sombra dura; acento colorido nas ênfases (cor da marca: **PENDENTE confirmar**, o logo vetorial está no Drive em pasta não pública, ver `CLAUDE.md`; fonte: Helvetica Neue Condensed Black no Mac; Liberation Sans Bold como fallback Linux).
- Legendas frase a frase em branco (não karaokê), terço inferior, SEMPRE por último no filter chain.
- Cortes secos; punch-ins de zoom 1.10 a 1.22x; freeze frames P&B com card para punchlines; cutaways como payoff de piada.
- Palavrão não corta: **bipa**.
- Trilha discreta (vol ~0.12 a 0.15) gerada via ElevenLabs sound-generation; SFX (whoosh, impact, riser, scratch) sincronizados aos cortes.
- Duração alvo: **20 a 60s**. Loudness final: **-14 LUFS**.

## Escolha do framework de motion: HyperFrames ou Remotion

O estúdio mantém os dois, e a escolha **não é preferência do momento**: cada peça declara o seu no `BRIEFING.md`, na primeira linha. Sem isso, quem pegar o projeto depois não sabe onde mexer.

**O que decide**: a ponte entre os dois só existe num sentido. Há a skill `remotion-to-hyperframes`; **não existe o inverso**. Então peça feita em HyperFrames é definitiva, e peça feita em Remotion ainda pode migrar. Na dúvida, Remotion é a aposta reversível.

| Use **HyperFrames** quando | Use **Remotion** quando |
|---|---|
| É peça de série recorrente, numa gramática de motion já documentada aqui (hoje: **PENDENTE**, nenhuma série definida) | A peça é exceção, fora do padrão da série |
| Você quer o fluxo pronto: brief, storyboard, registry de ~400 blocos, legendas, áudio, render em nuvem | A composição precisa de lógica de programação, dados ou parametrização |
| O visual pedido já existe no registry (scanlines, glitch, gráfico, janela de terminal) | Você vai gerar **N variações** da mesma peça mudando nome, cupom, idioma ou número |
| Ninguém vai reprocessar a peça em outro framework | Há chance real de a peça mudar de destino depois |

**Padrão declarado: HyperFrames.** Ele é o que está integrado ao fluxo do estúdio e o que tem as 20 skills. O Remotion entra por decisão consciente, não por inércia.

**Custo de manter os dois, para vigiar**: dois `node_modules`, dois caminhos de render e dois lugares onde a paleta pode divergir. O terceiro está mitigado, porque os tokens do Remotion vivem só em `remotion/src/marca.ts`, mas **se a paleta da marca mudar, atualizar os dois lados**. Hoje `marca.ts` é placeholder (paleta oficial PENDENTE). Se em alguns meses o Remotion não tiver sido usado em nada, ele vira peso morto e se corta; o inverso não vale, porque o HyperFrames é o que sustenta o fluxo.

## Fórmula da caption

1. Hook em 1 linha (dor ou cena concreta, sem travessão)
2. 2 a 3 parágrafos curtos
3. CTA: **PENDENTE (CTA padrão da marca)**
4. Pergunta de engajamento

## Fluxo por vídeo

1. Bruto (Drive público ou anexo na conversa) + briefing (pilar, mensagem central, duração, data)
2. Proxy SDR (se HLG) + transcrição Scribe (timestamps por palavra)
3. Decupagem/cortes (mapear falas de impacto e picos de áudio; com transcrição Scribe, usar `scripts/decupar.py` por âncora de texto e `scripts/relatorio_decupagem.py` para o relatório)
4. Cor (iPhone HLG: proxy SDR; Sony S-Log2: LUT de `scripts/gera_lut_slog2.py`)
5. Lettering/motion (PIL, PNGs com fade de alpha)
6. **Legendas por último**
7. Trilha + SFX (sound-generation; batidas detectadas por script)
8. Preview 720p+ para aprovação na conversa
9. Caption
10. Agendamento no Metricool como rascunho (marca deste estúdio; melhor horário: medir após conectar a marca)

## Gotchas técnicos

Ver a seção "Gotchas essenciais" do `CLAUDE.md` deste repo (herdados dos estúdios da agência, todos validados).
