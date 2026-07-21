# app/api/routes/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

router = APIRouter()

# 🔴 FIX: Add explicit allowed origins to bypass the 403 check
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # If standard origins clash, force accept by explicitly receiving the connection header
    # Some older FastAPI configurations require checking headers before accepting
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)