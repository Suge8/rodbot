#!/bin/bash
# Hot restart rodbot: start new instance, wait, kill old one
# This script runs independently of the current process

LOG="/tmp/rodbot_restart.log"
OLD_PIDS="60687 60688"
WORKDIR="/Users/sugeh/Documents/Project/rodbot"

echo "[$(date)] Starting hot restart..." > "$LOG"

# 1. Start new instance in background
cd "$WORKDIR"
nohup uv run rodbot gateway >> /tmp/rodbot_new.log 2>&1 &
NEW_PID=$!
echo "[$(date)] New instance started, PID=$NEW_PID" >> "$LOG"

# 2. Wait for new instance to initialize
sleep 8
echo "[$(date)] Wait complete, checking new process..." >> "$LOG"

# 3. Verify new instance is alive
if kill -0 $NEW_PID 2>/dev/null; then
    echo "[$(date)] New instance (PID=$NEW_PID) is alive. Killing old processes..." >> "$LOG"
    for pid in $OLD_PIDS; do
        kill $pid 2>/dev/null && echo "[$(date)] Killed old PID $pid" >> "$LOG"
    done
    echo "[$(date)] Hot restart complete!" >> "$LOG"
else
    echo "[$(date)] ERROR: New instance failed to start! Old processes NOT killed." >> "$LOG"
    echo "[$(date)] Manual intervention required." >> "$LOG"
fi
