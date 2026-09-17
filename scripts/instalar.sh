#!/usr/bin/env bash
# Entrada sencilla; el motor verificado y el generador utilizan Python 3.10+.
set -euo pipefail
main() {
  printf '\nBottifact · instalar o actualizar\n\n'
  printf 'Se preparará una biblioteca compartida para:\n  • Codex\n  • Claude Code\n  • Hermes\n\n'
  printf 'ChatGPT: importa el ZIP desde Plugins → Skills si tu cuenta lo permite.\n'
  printf 'Las instalaciones existentes se respaldan. Tu token no cambia.\n\n'
  if ! command -v curl >/dev/null 2>&1; then
    printf 'Falta curl. Instálalo con el gestor de paquetes de tu sistema.\n' >&2; return 1
  fi
  local bottifact_python='' candidate bottifact_tmp
  for candidate in python3 /opt/homebrew/bin/python3 /usr/local/bin/python3 python3.13 python3.12 python3.11 python3.10; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3,10))' >/dev/null 2>&1; then
      bottifact_python="$candidate"; break
    fi
  done
  if [ -z "$bottifact_python" ]; then
    printf 'El generador necesita Python 3.10+.\n' >&2
    if command -v brew >/dev/null 2>&1; then printf 'Ejecuta: brew install python\n' >&2
    else printf 'Instala Python desde https://www.python.org/downloads/ y repite este comando.\n' >&2; fi
    return 1
  fi
  bottifact_tmp="$(mktemp -d "${TMPDIR:-/tmp}/bottifact-install.XXXXXX")"
  trap "rm -rf -- $(printf '%q' "$bottifact_tmp")" EXIT
  printf 'Descargando y verificando la versión publicada…\n'
  curl --proto '=https' --tlsv1.2 -fsS --max-time 60 https://artifacts.botto.is/install.py -o "$bottifact_tmp/install.py"
  "$bottifact_python" "$bottifact_tmp/install.py" "$@"
  rm -rf -- "$bottifact_tmp"
  trap - EXIT
  printf '\nPara futuras actualizaciones: bottifact actualizar\n'
  printf 'ChatGPT: https://artifacts.botto.is/downloads/bottifact-portable.zip\n'
  printf 'Abre una conversación nueva y pide: «Usa el skill bottifact».\n'
}
main "$@"
