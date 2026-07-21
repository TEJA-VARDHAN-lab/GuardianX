from fastapi import APIRouter

from app.websocket.manager import manager

router = APIRouter(
    prefix="/api/v1/debug",
    tags=["Debug"],
)


@router.post("/broadcast")
async def broadcast():

    await manager.broadcast(
        {
            "type": "test",
            "message": "GuardianX WebSocket Working"
        }
    )

    return {
        "status": "sent"
    }