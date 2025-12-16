#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VENV_DIR=".venv"
PYTHON_BIN=""
PIP_BIN=""
MKDOCS_BIN=""

usage(){
  cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -a, --all        Crear venv, instalar dependencias y construir (default)
  -c, --create     Crear el virtualenv (if not exists)
  -i, --install    Instalar dependencias desde requirements.txt
  -b, --build      Ejecutar 'mkdocs build'
  -s, --serve      Ejecutar 'mkdocs serve' (bloqueante)
  -f, --force      Forzar recreación del virtualenv
  -h, --help       Mostrar esta ayuda

Examples:
  $(basename "$0") -a        # crear venv, instalar y build
  $(basename "$0") -s        # servir (asume venv y deps instaladas)
EOF
}

# Default behaviour
DO_CREATE=false
DO_INSTALL=false
DO_BUILD=false
DO_SERVE=false
FORCE=false

if [[ $# -eq 0 ]]; then
  DO_CREATE=true
  DO_INSTALL=true
  DO_BUILD=true
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    -a|--all)
      DO_CREATE=true; DO_INSTALL=true; DO_BUILD=true; shift;;
    -c|--create)
      DO_CREATE=true; shift;;
    -i|--install)
      DO_INSTALL=true; shift;;
    -b|--build)
      DO_BUILD=true; shift;;
    -s|--serve)
      DO_SERVE=true; shift;;
    -f|--force)
      FORCE=true; shift;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown option: $1"; usage; exit 2;;
  esac
done

# Determine python to create venv
if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=python
else
  echo "No Python interpreter found in PATH." >&2
  exit 1
fi

if $DO_CREATE; then
  if [[ -d "$VENV_DIR" && "$FORCE" != "true" ]]; then
    echo "Virtualenv already exists at $VENV_DIR. Use --force to recreate. Skipping create."
  else
    if [[ -d "$VENV_DIR" && "$FORCE" == "true" ]]; then
      echo "Removing existing virtualenv..."
      rm -rf "$VENV_DIR"
    fi
    echo "Creating virtualenv in $VENV_DIR using $PYTHON_CMD..."
    $PYTHON_CMD -m venv "$VENV_DIR"
  fi
fi

PIP_BIN="$VENV_DIR/bin/pip"
PYTHON_BIN="$VENV_DIR/bin/python"
MKDOCS_BIN="$VENV_DIR/bin/mkdocs"

if $DO_INSTALL; then
  if [[ ! -x "$PIP_BIN" ]]; then
    echo "Pip not found in $VENV_DIR. Ensure virtualenv is created." >&2
    exit 1
  fi
  echo "Upgrading pip and installing requirements.txt..."
  "$PIP_BIN" install --upgrade pip
  if [[ -f "requirements.txt" ]]; then
    "$PIP_BIN" install -r requirements.txt
  else
    echo "requirements.txt not found in $ROOT_DIR" >&2
    exit 1
  fi
fi

if $DO_BUILD; then
  if [[ ! -x "$MKDOCS_BIN" ]]; then
    echo "mkdocs not found in virtualenv. Did installation succeed?" >&2
    exit 1
  fi
  echo "Building site with mkdocs..."
  "$MKDOCS_BIN" build
fi

if $DO_SERVE; then
  if [[ ! -x "$MKDOCS_BIN" ]]; then
    echo "mkdocs not found in virtualenv. Did installation succeed?" >&2
    exit 1
  fi
  echo "Serving site with mkdocs (press Ctrl+C to stop)..."
  exec "$MKDOCS_BIN" serve
fi

echo "Done."
