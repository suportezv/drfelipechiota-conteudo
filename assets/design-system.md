# Design system — Dr. Felipe Chiota (overlays de vídeo)

Extraído dos vetores oficiais do cliente em 2026-08-20 (`Logotipo_DR_Felipe_Chiota_02CURVA.pdf` e cartão de visita, pasta "Docs enviados pelo cliente" no Drive da agência). O site drfelipechiota.com.br e o Instagram estão bloqueados pelo proxy deste ambiente; se um dia forem liberados, validar contra eles.

## Paleta (hex exatos dos vetores)

| Token | Hex | Origem no logo | Uso em vídeo |
|---|---|---|---|
| `vinho` | `#5E2947` | wordmark "Dr. Felipe Chiota" | reservado a momentos de assinatura/encerramento; não usar em texto pequeno sobre vídeo |
| `azul-profundo` | `#003751` | pontos da coluna e tagline | texto sobre a pincelada; painel do lower third |
| `azul-claro` | `#8EC1CD` | pincelada do símbolo | pincelada marca-texto, marcadores, linha do CRM |
| `indigo` | `#394F7E` | ícones do cartão | secundário, evitar em vídeo |
| `off-white` | `#FCFCFB` | fundo | equivalente do branco da marca |

## Linguagem dos destaques (substitui o itálico amarelo da série anterior)

- **Sem itálico e sem shear**: o logo é sans fina e elegante; a sobriedade médica pede peso por cor e tamanho, não inclinação.
- **Palavra-chave = marca-texto de pincelada**: swash horizontal em `azul-claro` atrás da palavra, com a palavra em `azul-profundo` por cima. As demais palavras da tela seguem brancas. É a pincelada do símbolo aplicada como grifo.
- Headlines (GC de capa e CTA): mesma regra; a linha de ênfase inteira pode receber a pincelada.
- Escadinha: degraus brancos com **ponto de coluna** (`azul-claro`, círculo cheio) como marcador à esquerda de cada degrau, ecoando os pontos do símbolo.
- Lower third: painel `azul-profundo` translúcido (alpha ~200), barra lateral e linha do CRM em `azul-claro`, nome em branco.
- Sombra e tipografia: iguais ao framework de legenda (YWFT Clarify Medium, sombra preta alpha 60/255, blur 22, offset 12,12).
- Contraste: `azul-claro` puro nunca vira cor de texto sobre cenário claro (não segura contraste); ele é sempre fundo de grifo, marcador ou detalhe.

## Assets

- Fonte: `assets/fonts/YWFTClarifyMedium.otf` (fora do git por licença; cópia na pasta de brutos do Drive).
- Logo e cartões: Drive da agência, pasta `Dr. Felipe Chiota_Cliente/Docs enviados pelo cliente`.
- A pincelada de grifo é gerada proceduralmente (PIL) em `azul-claro`; se o cliente fornecer o brush original em PNG, substituir.
