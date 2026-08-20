# Dr. Felipe Chiota Conteúdo Studio: FRAMEWORK

Estúdio de edição e agendamento para as redes da **Dr. Felipe Chiota**. Framework compartilhado da agência, adaptado para esta marca.

> Os blocos marcados **PENDENTE** dependem do briefing de posicionamento da marca e serão preenchidos e commitados quando confirmados.

## Persona e voz do perfil

Fonte: docs de roteiro do lote jul/ago 2026 (avaliação Zavi + roteiros de gravação; IDs no CLAUDE.md).

- Dr. Felipe Chiota, ortopedista especialista em coluna. Apresenta-se como especialista em cirurgia de coluna (confirmado em vídeo gravado, VID15). Atua com Medicina da Dor, técnicas minimamente invasivas e medicina regenerativa.
- Posicionamento: **o especialista que evita cirurgia**. Conservador primeiro; cirurgia é exceção e último recurso. O paradoxo (cirurgião que evita cirurgia) é o gancho da marca.
- Tom: conversa, não palestra. Frases curtas, uma ideia por vídeo. A régua de tom é o roteiro "Coluna travada de manhã" (vídeo 11 do lote).
- Identidade em vídeo: **nunca por intro falada**. Entra por lower third (nome, especialidade, CRM) do segundo 1 ao 4, e pela legenda.
- CTA padrão (conversão): **"Toca no link na bio e agende sua avaliação."** Funil por objetivo do vídeo: distribuição fecha em compartilhar ou salvar e marcar; conta fecha em seguir. Agendamento sempre presente na legenda do post, mesmo quando a fala fecha em share/save/follow.

### REGRAS INEGOCIÁVEIS

1. **Nunca usar travessão em texto público.** Reescrever a frase.
2. Credencial sempre completa quando citar o criador: **"Dr. Felipe Chiota, ortopedista especialista em coluna, CRM 162427 | RQE 73780"**.
3. Palavrão em vídeo **se bipa, não se corta** (sine 1000 Hz curto, voz mutada no trecho).
4. Loudness final: **-14 LUFS**.
5. **Compliance CFM (Resolução 2.336/23)**: sem promessa ou insinuação de resultado, sem estatística sem fonte (usar linguagem qualitativa: "maioria", "minoria"), sem sensacionalismo ou alarmismo. Exames em tela só genéricos ou anonimizados (LGPD e sigilo médico). Medicina regenerativa pode ser citada como opção quando bem indicada, sem prometer regeneração nem resultado.

## Pilares de conteúdo

Do lote jul/ago 2026 (validar com desempenho): mitos e medos (cirurgia, repouso), automedicação e dor recorrente, sinais de alerta, postura e ergonomia no trabalho, hérnia cervical e de disco, dor precoce em jovens, escoliose em adolescentes, retorno ao esporte e impacto emocional, posicionamento pessoal.

## Assinaturas de edição

**Base: framework de série vertical de talking head da agência (docs do usuário, 2026-08-20), com adaptações do Chiota por cima. Aprovado pelo usuário: legendas seguem o padrão validado da série anterior; trilha com ducking se mantém; destaques inline na paleta do cliente, sem fonte manuscrita.**

### Cortes (respiração)

- Transcrição word-level obrigatória, com cache por arquivo. Varredura de retakes ANTES do plano de corte: n-gramas repetidos (2-5 palavras) em janela de 15 s, protegendo retórica intencional; falsos inícios saem.
- Silêncios ≥ 0,5 s são cortados **mantendo 0,15 s de folga em cada borda** (pausa nunca zera, senão fica sem fôlego). Silêncio < 0,5 s fica.
- Cabeça: aparar até a primeira palavra. Cauda: última palavra + 0,35 s de vídeo, com fade de áudio começando em última palavra + 0,03 s (mata a expiração final).
- Nunca cortar dentro de palavra; fade de áudio de 30 ms em cada borda de corte real.
- **Grade de frames**: todo limite de corte em `round(t*fps)/fps`; áudio PCM nos intermediários; um único encode AAC no concat; offsets por soma das durações quantizadas (validado aqui: sem isso o desvio chega a ~0,25 s em 7 segmentos).

### Zoom narrativo

- Movimento guiado pelo roteiro, não por alternância geométrica. Easing **sempre cúbico**; trajetória **contínua** entre divisões de beat (refazer o movimento a cada corte = gagueira visual); divisão de beat não leva fade de áudio (não é corte real).
- Escada adaptada para **bruto 1080p** (a base 1.20 do doc original pressupõe 4K): base 1.06-1.10; ênfase 1.16-1.24; pico ~1.26-1.28; alívio/solução volta a ~1.08 em ~2 s e segura; CTA punch ~1.20 relaxando no fim. Punch de corte = salto de +0.04 a +0.08 entre segmentos.
- Anti-jitter: upscale 2x antes do zoompan. Âncora no rosto medido do take (não usar valores fixos de outro cliente).

### Cor (3 camadas)

1. Por vídeo, na extração: `colorcorrect=analyze=average, colortemperature=temperature=7000:mix=0.3, eq=contrast=1.07:saturation=1.06:brightness=0.012`.
2. Série completa: medir tom de pele (máscara YCbCr) de todos os masters, alvo = mediana, corrigir matiz por colorbalance e luminância por gamma (0.80-1.25). **Só rodar com a série inteira masterizada.**
3. O ajuste da camada 2 entra no mesmo re-encode das legendas (2 gerações de compressão no total).

### Legendas (padrão aprovado, fonte YWFT Clarify Medium em `assets/fonts/`)

| Papel | Tamanho @1080x1920 | Cor | Extras |
|---|---|---|---|
| Base | 98 px | branca | espaçamento -4 px, fade simples 50 ms |
| Destaque | 118 px | palavra-chave com pincelada #8EC1CD e texto #003751, resto branco | sem itálico, reveal letra a letra (ver assets/design-system.md) |
| Destaque forte | 134 px | idem | idem, 1 a 3 por vídeo (conceito central) |
| Escadinha | 66 px | branca | 1 linha por degrau, offsets -120/0/+120 (4 degraus: -150..+150) |

- Sombra: preta alpha 60/255, blur gaussiano 22 px, offset (12,12). Posição: centro do bloco em y=1140 (~40% da altura). Entrelinhas 1.08 em.
- Diagramação: 2-3 palavras por tela; **nenhuma tela termina em palavra de função** (partição ótima, não gulosa; cuidado "é"≠"e", "dá"≠"da"); hífen nunca quebra; função pendurada em pausa atravessa a pausa com a próxima palavra; frase larga quebra progressiva com trava de largura (≤ W-56).
- Reveal letra a letra (~32 ms/letra, deslize vertical + fade, ease-out, ~0,5 s) **só** em destaques e escadinha.
- Escadinha quando a fala enumera 3-4 itens ou constrói clímax em etapas; texto condensado à essência; o trecho inteiro é da escadinha (sem legenda base simultânea). Procurar ativamente nos roteiros.
- Render via PIL + overlay (reproduz a sombra difusa real); legendas SEMPRE por último no filter chain.
- Timing na timeline de saída; verificação de sincronia obrigatória: retranscrever o vídeo final e alinhar por texto (difflib), desvio mediano < 10 ms.
- Fonte licenciada: **nunca commitar no repo público**; manter cópia na pasta de brutos do Drive.

### GCs e identidade (específico do Chiota)

- GC de capa de 3 a 5 palavras no frame 1, sem fade, alto contraste; lower third com credencial completa (CRM 162427 | RQE 73780) do segundo 1 ao 4; GCs de apoio nos momentos do roteiro. Tipografia: Clarify, destaque na paleta do cliente (paleta **PENDENTE**; provisório azul petróleo #22B8CF).
- Palavrão não corta: **bipa**.
- Trilha discreta via ElevenLabs sound-generation (~vol 0.09) com **sidechain ducking sob a voz**; SFX só com parcimônia e aprovação (whoosh genérico foi reprovado).
- Duração alvo: **20 a 60s**. Loudness final: **-14 LUFS** (duas passadas de loudnorm, verificar com ebur128).

### Portões de qualidade (rodar todos antes de mostrar)

1. Sincronia: retranscrever o final, alinhar por texto, desvio mediano < 10 ms.
2. Ruído sem fala: som acima de -38 dB em janelas sem palavra (margem 0,2 s). Tosse não é silêncio.
3. Voz alheia: volume ~10 dB abaixo + f0 sustentada fora do padrão do locutor (cuidado com vocal fry).
4. Legenda dentro do quadro (largura ≤ W-56, escadinha considerando o offset lateral).
5. Dry-run da diagramação: ordem monotônica, zero telas de 1 palavra de função, zero telas terminando em função.
6. Ajuste pontual = diff antes/depois contendo exatamente o pedido, e nada mais.
7. Duração ≈ soma do EDL; filmstrip nos cortes novos; frames dos destaques e escadinha completos.

## Fórmula da caption

1. Hook em 1 linha (dor ou cena concreta, sem travessão)
2. 2 a 3 parágrafos curtos, com ângulo complementar ao do vídeo (não repetir a fala)
3. CTA: "Toca no link na bio e agende sua avaliação." (agendamento sempre na legenda, mesmo em vídeo de distribuição)
4. Pergunta de engajamento
5. Bloco de assinatura fixo: **PENDENTE (texto exato do bloco; o doc de roteiros o cita sem definir)**

## Fluxo por vídeo

1. Bruto (Drive público ou anexo na conversa) + briefing (pilar, mensagem central, duração, data)
2. Proxy SDR (se HLG) + transcrição Scribe (timestamps por palavra)
3. Decupagem/cortes (mapear falas de impacto e picos de áudio)
4. Cor
5. Lettering/motion (PIL, PNGs com fade de alpha)
6. **Legendas por último**
7. Trilha + SFX (sound-generation; batidas detectadas por script)
8. Preview 720p+ para aprovação na conversa
9. Caption
10. Agendamento no Metricool como rascunho (marca deste estúdio; melhor horário: medir após conectar a marca)

## Gotchas técnicos

Ver a seção "Gotchas essenciais" do `CLAUDE.md` deste repo (herdados dos estúdios da agência, todos validados).
