# app/core/websocket_manager.py
from fastapi import WebSocket
import logging

logger = logging.getLogger("uvicorn.error")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("📡 New client connected to WebSocket. Total active: %s", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("📡 Client disconnected from WebSocket. Total active: %s", len(self.active_connections))

    async def broadcast_json(self, message: dict):
        """Sends a JSON payload to all active clients safely."""
        for connection in self.active_connections[:]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error("❌ Failed broadcasting packet to single socket instance: %s", e)
                self.disconnect(connection)

# Singleton Instance
manager = ConnectionManager()