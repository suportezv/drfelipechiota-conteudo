# Design system — Dr. Felipe Chiota (overlays de vídeo)

Extraído dos vetores oficiais do cliente em 2026-08-20 (`Logotipo_DR_Felipe_Chiota_02CURVA.pdf` e cartão de visita, pasta "Docs enviados pelo cliente" no Drive da agência). O site drfelipechiota.com.br e o Instagram estão bloqueados pelo proxy deste ambiente; se um dia forem liberados, validar contra eles.

## Paleta (hex exatos dos vetores)

| Token | Hex | Origem no logo | Uso em vídeo |
|---|---|---|---|
| `vinho` | `#5E2947` | wordmark "Dr. Felipe Chiota" | reservado a momentos de assinatura/encerramento; não usar em texto pequeno sobre vídeo |
| `azul-profundo` | `#003751` | pontos da coluna e tagline | painel do lower third; textos escuros sobre fundo claro |
| `azul-claro` | `#8EC1CD` | pincelada do símbolo | pontos da escadinha, linha do CRM, detalhes decorativos |
| `indigo` | `#394F7E` | ícones do cartão | secundário, evitar em vídeo |
| `azul-vivo` | `#3EC8ED` | derivado do azul-claro (mesmo matiz, saturação e brilho altos) | palavra-chave dos destaques em vídeo (o azul-claro puro é morto demais como texto) |
| `off-white` | `#FCFCFB` | fundo | equivalente do branco da marca |

## Tipografia (v2, definida pelo usuário em 2026-08-26 com base nas referências)

- **Par de título**: linha principal em **sans bold pesada** (Helvetica Bold; no Linux o clone FreeSans Bold) + linha secundária em **Garamond** (Apple Garamond; substituta atual EB Garamond 600, itálica 500 para frases suaves), entrelinha apertada. Exemplo canônico da capa: "Dorflex" (bold) sobre "TODA SEMANA?" (Garamond caps). **Entrelinha quase colada nos GCs de topo** (linha 2 encosta na baseline da linha 1).
- **Corpo de legenda**: YWFT Clarify Medium, branca.
- **Destaque inline**: palavra-chave em FreeSans Bold ~1.16x do corpo, na cor `azul-vivo #3EC8ED`; o resto da frase branco em Clarify. Sem itálico de shear, **sem pincelada** (testada e reprovada pelo usuário), sem caixa alta fina.
- **Legibilidade em fundo claro** (técnica da REFERENCIA 4): faixas de gradiente escuro sutil atrás das zonas de texto (legenda ~alpha 78, topo ~alpha 112, escadinha ~alpha 70), sempre difusas. O azul claro só vira cor de texto sobre essas faixas.
- Fontes alternativas aprovadas pelo usuário (enviar arquivo quando quiser usar): Integral+Montserrat, Poppins, Faltando+Doshi, Callum+Sylvan, Scholar+Clarify, Raleway bold+Creato Display, Clarify bold+True Destiny. Poppins 400/500/600/800 e EB Garamond já baixadas via npm @fontsource (rota direta) e convertidas com fonttools.

## Kit de SFX (STANDBY: removido das edições em 2026-08-26 a pedido do usuário; não aplicar sem pedido explícito)

Sintetizado localmente (numpy) em `scratchpad/sfx/`; regenerável pelo script da sessão. Mapeamento fixo:

| SFX | Quando | Volume rel. |
|---|---|---|
| woosh | acompanha zoom/reframe (suaviza o movimento) | ~0.10 |
| click | entrada de GC, lower third, cards | ~0.12 |
| pop | degrau da escadinha, animação surgindo | ~0.10 |
| riser | 1,2 s antes do ponto-chave do roteiro | ~0.08 |
| keyboard typing | sob reveal letra a letra de destaque | ~0.09 |
| camera shutter | corte seco forte/freeze (usar raramente) | ~0.10 |

Regra de bom gosto: só onde há evento visual real; picos 10-15% da fala; poucos eventos por vídeo (edição de videomaker profissional, não carregada).

## Assets

- Fontes: `assets/fonts/` (fora do git; Clarify via usuário, Poppins/EB Garamond re-baixáveis do npm).
- Logo e cartões: Drive da agência, pasta `Dr. Felipe Chiota_Cliente/Docs enviados pelo cliente`.
