#!/usr/bin/env bash
# Wrapper do HyperFrames para este container: `bash scripts/hf.sh doctor`,
# `bash scripts/hf.sh render <dir>` etc.
#
# Por que existe: o `hyperframes doctor` sem estas variaveis reprova o ffmpeg
# (que funciona) e nao acha Chrome, e `hyperframes browser ensure` tenta baixar
# um browser de um host fora da allowlist. O headless_shell do Playwright ja
# esta na imagem e serve. Duravel de verdade e cadastrar as tres variaveis
# HYPERFRAMES_* nas env vars do environment (valem para sessao nova); ate la,
# este wrapper.
set -euo pipefail

export HYPERFRAMES_BROWSER_PATH="${HYPERFRAMES_BROWSER_PATH:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}"
export HYPERFRAMES_FFMPEG_PATH="${HYPERFRAMES_FFMPEG_PATH:-$(command -v ffmpeg || echo /usr/local/bin/ffmpeg)}"
export HYPERFRAMES_FFPROBE_PATH="${HYPERFRAMES_FFPROBE_PATH:-$(command -v ffprobe || echo /usr/local/bin/ffprobe)}"
# O init confere skills contra raw.githubusercontent.com (bloqueado); as skills
# ja estao registradas pelo setup.sh a partir do clone.
export HYPERFRAMES_SKIP_SKILLS="${HYPERFRAMES_SKIP_SKILLS:-1}"

# Mesma rota de rede do setup.sh: npm pelo agent proxy com o CA bundle.
if [ -n "${HTTPS_PROXY:-}" ]; then
  export no_proxy="" NO_PROXY="" HTTP_PROXY="$HTTPS_PROXY"
  export npm_config_proxy="$HTTPS_PROXY" npm_config_https_proxy="$HTTPS_PROXY"
  export npm_config_noproxy="" npm_config_cafile="${SSL_CERT_FILE:-/root/.ccr/ca-bundle.crt}"
  # O `fetch` embutido do Node NAO le HTTPS_PROXY sozinho (Node >= 22.21 precisa
  # de NODE_USE_ENV_PROXY=1) e nao confia no CA do proxy sem NODE_EXTRA_CA_CERTS.
  # Sem os dois, `hyperframes catalog` e `add` dizem "No items found in registry"
  # em silencio, porque o fetch do registry falha dentro de um try/catch.
  export NODE_USE_ENV_PROXY=1
  export NODE_EXTRA_CA_CERTS="${NODE_EXTRA_CA_CERTS:-${SSL_CERT_FILE:-/root/.ccr/ca-bundle.crt}}"
  # O Chromium do render le https_proxy/http_proxy em MINUSCULA; sem isso ele vai
  # direto ao firewall de egresso e qualquer <script src="https://cdn..."> falha.
  export https_proxy="$HTTPS_PROXY" http_proxy="$HTTPS_PROXY"
fi

exec npx --yes hyperframes "$@"
