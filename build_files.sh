#!/bin/bash
echo "==> Preparing static files..."
mkdir -p staticfiles

export PATH="$HOME/.local/bin:$PATH"
export PYTHONPATH="$HOME/.local/lib/python3.12/site-packages:$HOME/.local/lib/python3.10/site-packages:$PYTHONPATH"

python3 -m pip install -r requirements.txt 2>/dev/null || true
python3 manage.py collectstatic --noinput 2>/dev/null || true

echo "==> Static files ready in staticfiles directory."
