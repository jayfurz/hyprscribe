#!/bin/bash
# Start recording in hold mode
cd /home/justin/code/local_voice_assistant

# Define the explicit venv path provided by the user
VENV_PYTHON="/home/justin/code/local_voice_assistant/venv/bin/python"

if [ -f "$VENV_PYTHON" ]; then
    # If the specific venv exists, use it directly
    "$VENV_PYTHON" dictate_client.py --hold
else
    # Fallback to uv run (looks for .venv or manages its own environment)
    # We specify --with-requirements to ensure packages are available if uv is creating an ephemeral env
    # But preferably it uses the existing project env.
    uv run dictate_client.py --hold
fi
