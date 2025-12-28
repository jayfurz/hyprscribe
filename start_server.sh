#!/bin/bash
cd /home/justin/code/local_voice_assistant

VENV_PYTHON="/home/justin/code/local_voice_assistant/venv/bin/python"

if [ -f "$VENV_PYTHON" ]; then
    "$VENV_PYTHON" server.py
else
    uv run server.py
fi
