"""
JARVIS PRIME - Core Daemon (FastAPI)
The central nervous system of the JARVIS architecture.
"""
import json
import logging
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import config
from memory.memory_manager import memory
from engine.intent_detector import intent_detector
from engine.system_actions import system_actions

# Suppress Uvicorn access logs for clean console
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

app = FastAPI(title="JARVIS PRIME Core", version="3.0.0")

# Allow CORS for external Web UI dev modes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[PRIME:Daemon] Client connected: {websocket.client.host}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("[PRIME:Daemon] Client disconnected.")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                command = payload.get("command", "").strip()
                if command:
                    print(f"[PRIME:Daemon] Vector Received: {command}")
                    response_payload = process_command(command)
                    await manager.send_personal_message(json.dumps(response_payload), websocket)
            except json.JSONDecodeError:
                await manager.send_personal_message(json.dumps({
                    "status": "error", "response": "Invalid JSON format."
                }), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[PRIME:Daemon] Socket Error: {e}")
        manager.disconnect(websocket)

def process_command(command: str) -> dict:
    """Route the command through the intelligence engine."""
    intent, action_type, confidence = intent_detector.process(command)
    response_text = "Command unrecognized by core."
    status = "failed"
    
    # Intercepts
    low = command.lower()
    if "system status" in low:
        response_text = system_actions.system_status()
        intent = "system_status"
        status = "success"
    elif intent and intent.startswith("open_"):
        app_name = intent.replace("open_", "")
        ok, msg = system_actions.open_application(app_name)
        response_text = msg
        status = "success" if ok else "error"
    elif intent:
        response_text = f"Intent '{intent}' identified. Plugin processing pending."
        status = "pending"

    # Log Execution
    memory.log_execution(command, intent or "unknown", status, response_text)
    
    return {
        "status": status,
        "response": response_text,
        "intent": intent,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat()
    }

# Entry Point to boot the server
if __name__ == "__main__":
    import uvicorn
    print(f"==================================================")
    print(f"  JARVIS PRIME DAEMON ONLINE")
    print(f"  Listening at ws://{config.DAEMON_HOST}:{config.DAEMON_PORT}/ws")
    print(f"==================================================")
    uvicorn.run("core.daemon:app", host=config.DAEMON_HOST, port=config.DAEMON_PORT, log_level="warning")
