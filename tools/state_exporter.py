"""State exporter sidecar.
Connects to the Socket.IO endpoint exposed by the UI server (without modifying app/),
and re-exports state as Prometheus metrics on a separate HTTP server.
"""
import socketio, time, threading
from prometheus_client import Gauge, start_http_server

MH_M = Gauge("mhksi_m_value", "M scalar value from agent")
MH_MODE = Gauge("mhksi_mode_index", "Enumerated mode: conserve=0, steady=1, explore=2")
PSI_RHO = Gauge("psi_rho", "Psi-field rho") 
AFFECT_CHI = Gauge("affect_chi", "Affect chi (engagement)")

MODE_MAP = {"conserve": 0, "steady": 1, "explore": 2}

def run_export(socketio_url: str):
    sio = socketio.Client()

    @sio.on("state")
    def on_state(data):
        # Expect keys: m, mode, psi_rho, chi — tolerant to missing keys
        m = data.get("m")
        if m is not None:
            MH_M.set(float(m))
        mode = data.get("mode")
        if mode is not None:
            MH_MODE.set(MODE_MAP.get(mode, -1))
        rho = data.get("psi_rho") or data.get("rho")
        if rho is not None:
            PSI_RHO.set(float(rho))
        chi = data.get("chi")
        if chi is not None:
            AFFECT_CHI.set(float(chi))

    sio.connect(socketio_url)
    sio.wait()

if __name__ == "__main__":
    import os
    socketio_url = os.getenv("STATE_WS_URL", "http://localhost:8080")
    metrics_port = int(os.getenv("EXPORTER_PORT", "9108"))
    start_http_server(metrics_port)
    run_export(socketio_url)
