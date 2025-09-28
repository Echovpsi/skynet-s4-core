#!/usr/bin/env bash
# Start original app (assumed Docker) and the sidecar exporter in one go (docker-compose alternative without modifying existing files)
set -euo pipefail
python3 tools/state_exporter.py &
echo "State exporter started on :9108"
echo "Now start your app container or python app/main.py in another terminal."
wait
