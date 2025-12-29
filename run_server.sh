#!/bin/bash
# Script to run the Rafeeq API server

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
if [ -d "$DIR/venv" ]; then
    source "$DIR/venv/bin/activate"
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv "$DIR/venv"
    source "$DIR/venv/bin/activate"
    pip install -r "$DIR/backend/requirements.txt"
    pip install httpx
fi

# Run the server
echo "Starting Rafeeq API..."
cd "$DIR/backend"
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
