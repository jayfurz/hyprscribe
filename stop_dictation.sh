#!/bin/bash
# Stop recording by sending SIGTERM to the process found in the PID file
PID_FILE="/tmp/voice_assist_dictate.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        kill -TERM $PID
    else
        # Stale PID file
        rm "$PID_FILE"
    fi
fi
