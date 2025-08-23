#!/usr/bin/env bash

# Determine venv dir
VENV_DIR=".venv"

# Create .venv if missing
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# Activate it
source "$VENV_DIR/bin/activate"

# Install deps
if [ -f "pyproject.toml" ]; then
  if grep -q '\[tool.poetry\]' pyproject.toml && command -v poetry &>/dev/null; then
    poetry install
  else
    pip install -U pip build setuptools wheel
    pip install -e . || true  # fallback if PEP 621 style
  fi
elif [ -f "Pipfile" ]; then
  pip install pipenv
  pipenv install --dev
elif [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
fi
