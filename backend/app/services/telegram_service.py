import logging
import os

import httpx

from app.core.config import settings

logger = logging.getLogger("uvicorn.error")


class TelegramService:
    @staticmethod
    async def send_alert(incident, camera=None) -> bool:
        try:
            bot_token = settings.TELEGRAM_BOT_TOKEN
            chat_id = settings.TELEGRAM_CHAT_ID

            if not bot_token or not chat_id:
                logger.warning("Telegram configuration missing")
                return False

            api_url = f"https://api.telegram.org/bot{bot_token}"

            camera_name = getattr(camera, "name", f"Camera #{incident.camera_id}")
            location = getattr(camera, "location", "Unknown Location")

            message = (
                f"🚨 *GUARDIAN EMERGENCY ALERT*\n\n"
                f"🔥 *Incident:* {incident.incident_type.upper()}\n"
                f"📍 *Location:* {location} ({camera_name})\n"
                f"⚠️ *Severity:* {incident.severity.upper()}\n"
                f"📊 *Status:* {incident.status.upper()}\n"
                f"🆔 *Incident ID:* #{incident.id}"
            )

            snapshot_path = getattr(incident, "snapshot", None)
            has_valid_image = bool(snapshot_path and os.path.exists(snapshot_path))

            async with httpx.AsyncClient(timeout=15.0) as client:
                if has_valid_image:
                    with open(snapshot_path, "rb") as image:
                        response = await client.post(
                            f"{api_url}/sendPhoto",
                            data={
                                "chat_id": chat_id,
                                "caption": message,
                                "parse_mode": "Markdown",
                            },
                            files={"photo": image},
                        )
                else:
                    response = await client.post(
                        f"{api_url}/sendMessage",
                        data={
                            "chat_id": chat_id,
                            "text": message,
                            "parse_mode": "Markdown",
                        },
                    )

            response.raise_for_status()
            logger.info("✅ Telegram alert sent successfully")
            return True

        except Exception as e:
            logger.exception("❌ Telegram alert failed: %s", e)
            return False