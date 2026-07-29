import asyncio
from app.models.incident import Incident
from app.models.camera import Camera
from app.services.telegram_service import TelegramService

async def test_alert():
    # Mock Incident
    fake_incident = Incident(
        id=999,
        camera_id=1,
        incident_type="fire",
        severity="critical",
        confidence=0.89,
        status="detected",
        snapshot=None  # or path to test image
    )
    
    # Mock Camera
    fake_camera = Camera(
        id=1,
        name="Main Entrance Cam",
        location="Building A, Floor 1"
    )

    print("🚀 Triggering Test Telegram Alert...")
    result = await TelegramService.send_alert(fake_incident, fake_camera)
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_alert())