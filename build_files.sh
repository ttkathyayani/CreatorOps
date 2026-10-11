#!/bin/bash
echo "==> Installing Python dependencies..."
python3 -m pip install -r requirements.txt

echo "==> Applying migrations..."
python3 manage.py migrate --noinput || true

echo "==> Collecting static assets..."
python3 manage.py collectstatic --noinput

echo "==> Build complete!"
