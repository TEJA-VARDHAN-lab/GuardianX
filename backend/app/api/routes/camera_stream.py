import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.camera.registry import CameraRegistry


router = APIRouter(
    prefix="/api/v1/cameras",
    tags=["Camera Streaming"]
)


async def generate(camera_id: int):

    worker = CameraRegistry.get(
        camera_id
    )


    if not worker:
        return


    while True:

        frame = worker.get_jpeg()


        if frame:

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame
                + b"\r\n"
            )


        await asyncio.sleep(
            0.03
        )



@router.get("/{camera_id}/stream")
async def camera_stream(
    camera_id:int
):

    return StreamingResponse(
        generate(camera_id),
        media_type=
        "multipart/x-mixed-replace; boundary=frame"
    )