import logging
from fastapi import WebSocket

logger = logging.getLogger("uvicorn.error")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"➕ Connection added. Total active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"➖ Connection removed. Total active connections: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except Exception:
            self.disconnect(websocket)

    async def broadcast_text(self, message: str):
        # Using a slice copy [:] ensures we don't hit iteration errors if a socket drops mid-loop
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except Exception:
                logger.warning("⚠️ Failed to send text to a connection. Cleaning up.")
                self.disconnect(connection)

    async def broadcast_json(self, data: dict):
        # Fixed: Indented everything here by 8 spaces to fit inside the method block
        logger.info(f"📡 Broadcasting message to {len(self.active_connections)} clients")
        logger.info(f"📦 Payload: {data}")

        for connection in self.active_connections[:]:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.warning(f"⚠️ Failed to send JSON: {e}")
                self.disconnect(connection)

manager = ConnectionManager()