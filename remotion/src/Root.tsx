import React from "react";
import { Composition } from "remotion";
import { CartaoTitulo } from "./CartaoTitulo";

// Os defaultProps sao so o exemplo que o Studio e o `remotion still` mostram.
// O titulo vem de um carrossel do briefing de julho/2026 da marca; o rodape e o
// handle verificado no Metricool.
const exemplo = {
  titulo: "Sua coluna já está avisando",
  destaque: "avisando",
  rodape: "@drfelipechiota",
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="CartaoTituloVertical"
      component={CartaoTitulo}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={exemplo}
    />
    <Composition
      id="CartaoTituloQuadrado"
      component={CartaoTitulo}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={exemplo}
    />
  </>
);
