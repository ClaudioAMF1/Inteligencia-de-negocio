#!/usr/bin/env bash
# Passos 1 e 2: verificação read-only no macOS. Não instala nem altera nada.
set -uo pipefail

NEED_GB=90

echo "=== Sistema ==="
sw_vers 2>/dev/null || { echo "ERRO: não é macOS."; exit 1; }
echo "Arquitetura: $(uname -m)"
echo

echo "=== Passo 1: espaço livre em disco ==="
df -g /System/Volumes/Data | awk 'NR==1{print} NR==2{print}'
FREE_GB=$(df -g /System/Volumes/Data | awk 'NR==2{print $4}')
echo
echo "Livre segundo df: ${FREE_GB} GiB (inclui espaço 'purgeable')"
diskutil info /System/Volumes/Data 2>/dev/null | grep -E "Container Free Space|Volume Free Space" || true
echo
if [ "${FREE_GB:-0}" -ge "$NEED_GB" ]; then
  echo "OK: >= ${NEED_GB} GB livres."
else
  echo "FALTA: precisa de ${NEED_GB} GB, faltam ~$(( NEED_GB - FREE_GB )) GB."
  echo "PARE aqui e libere espaço antes de continuar."
fi
echo

echo "=== Passo 2: Homebrew ==="
if command -v brew >/dev/null 2>&1; then
  echo "OK: $(brew --version | head -1)"
  echo "Prefixo: $(brew --prefix)"
else
  echo "AUSENTE. Comando oficial de instalação (https://brew.sh):"
  echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  echo "PARE aqui, instale e rode este script de novo."
fi
