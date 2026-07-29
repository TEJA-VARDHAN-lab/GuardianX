from fastapi import APIRouter
from pydantic import BaseModel

from app.services.assistant_service import AssistantService


router = APIRouter(
    prefix="/api/v1/assistant",
    tags=["AI Assistant"],
)


class AssistantRequest(BaseModel):
    message: str



@router.post("/chat")
def chat(
    request: AssistantRequest
):

    return AssistantService.answer(
        request.message
    )