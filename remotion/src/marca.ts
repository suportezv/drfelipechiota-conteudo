/**
 * Paleta e tokens da marca no Remotion.
 *
 * Os NOMES dos tokens sao os do template compartilhado da agencia: Aurora.tsx e
 * CartaoTitulo.tsx leem daqui e nao devem ser editados por estudio (e o que
 * permite portar o Remotion entre estudios trocando so este arquivo e o
 * Root.tsx). So os VALORES sao da marca.
 *
 * PENDENTE: paleta oficial da Dr. Felipe Chiota. O logo vetorial existe no Drive
 * (pasta "Docs enviados pelo cliente", Logotipo_DR_Felipe_Chiota_02CURVA.pdf),
 * mas a pasta nao e publica e o conector nao entrega o PDF para este container.
 * Os valores abaixo sao PLACEHOLDER neutro (azul-ardosia) apenas para o pipeline
 * renderizar. Trocar pelos hexes oficiais antes de qualquer peca publica.
 *
 * Mapa de uso: rosaVivo = acento (palavra em destaque e 1a mancha da aurora);
 * violeta, ciano e rosaSuave = manchas 2 a 4 da aurora; auroraBase = fundo claro;
 * tinta = texto. Os demais ficam exportados por compatibilidade com o template.
 */
export const marca = {
  rosaVivo: "#1F5FBF",
  rosa: "#174A94",
  rosaSuave: "#9DBBE8",
  violeta: "#2B6E8C",
  ciano: "#5FB3D9",
  azulNeon: "#7CC7E8",
  azulProfundo: "#1B2A44",
  fundoEscuro: "#0B1220",
  superficie: "#152238",
  auroraBase: "#F3F6FA",
  tinta: "#152238",
  /** Fonte da marca: PENDENTE. Sem rede no render, cai para a sans do sistema. */
  fonte: '"Inter Tight", "Helvetica Neue", Arial, system-ui, sans-serif',
} as const;
