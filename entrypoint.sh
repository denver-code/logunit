#!/bin/sh

if [ ! -f "private.pem" ]; then
    echo "Generating private key..."
    poetry run python3 genrsa.py
else
    echo "Private key already exists, skipping generation..."
fi
echo "Starting server..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000