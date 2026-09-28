#!/usr/bin/env bash
# Gera o site em dist/ a partir dos dados versionados em coleta/dados/.
# Uso: ./build.sh            (só gera)
#      ./build.sh deploy     (gera e publica no Cloudflare com o wrangler)
set -euo pipefail
cd "$(dirname "$0")"
python3 coleta/legendas.py
python3 coleta/norm.py
python3 coleta/prep.py
python3 scripts/build_proto.py
python3 scripts/build_pages.py
cp prototipo/support.js dist/support.js
echo "site gerado em dist/"
if [[ "${1:-}" == "deploy" ]]; then
  npx --yes wrangler deploy
fi
