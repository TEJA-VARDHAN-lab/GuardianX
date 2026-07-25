import os
import requests
from dotenv import load_dotenv

load_dotenv()


class NotificationService:

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    @classmethod
    def send_telegram(cls, message: str):
        if not cls.BOT_TOKEN or not cls.CHAT_ID:
            print("⚠️ Telegram credentials missing. Skipping alert.")
            return None

        url = f"https://api.telegram.org/bot{cls.BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": cls.CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(url, json=payload, timeout=5.0)
            if response.status_code != 200:
                print(f"❌ Telegram notification failed: {response.text}")
            return response
        except Exception as e:
            print(f"❌ Error sending Telegram notification: {e}")
            return None

    @classmethod
    def send_alert(cls, incident, camera):
        text = f"""
🚨 *GuardianX Emergency Alert*

*Incident:* {incident.incident_type.upper()}
*Severity:* {incident.severity.upper()}

*Camera:* {camera.name}
*Location:* {camera.location_name}

*Confidence:* {incident.confidence:.1%}
*Detected:* {incident.created_at}
"""

        return cls.send_telegram(text)