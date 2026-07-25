import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramService:

    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    @classmethod
    def send_telegram(cls, message: str):
        if not cls.BOT_TOKEN or not cls.CHAT_ID:
            print("⚠️ Telegram credentials missing in .env file. Skipping alert.")
            return None

        url = f"https://api.telegram.org/bot{cls.BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": cls.CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=15.0,
                proxies={"http": None, "https": None},
            )
            if response.status_code != 200:
                print(f"❌ Telegram message failed: {response.text}")
            else:
                print("✅ Telegram notification sent successfully!")
            return response
        except Exception as e:
            print(f"❌ Error sending Telegram message: {e}")
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

    @classmethod
    def send_photo(cls, photo: str, caption: str = ""):
        """Sends a photo (URL or local file path) to the Telegram channel/chat."""
        if not cls.BOT_TOKEN or not cls.CHAT_ID:
            print("⚠️ Telegram credentials missing in .env file. Skipping photo.")
            return None

        url = f"https://api.telegram.org/bot{cls.BOT_TOKEN}/sendPhoto"

        try:
            # If photo is a local file path
            if os.path.exists(photo):
                with open(photo, "rb") as image_file:
                    files = {"photo": image_file}
                    data = {"chat_id": cls.CHAT_ID, "caption": caption}
                    response = requests.post(
                        url,
                        data=data,
                        files=files,
                        timeout=15.0,
                        proxies={"http": None, "https": None},
                    )
            else:
                # If photo is a URL link
                payload = {
                    "chat_id": cls.CHAT_ID,
                    "photo": photo,
                    "caption": caption,
                }
                response = requests.post(
                    url,
                    json=payload,
                    timeout=15.0,
                    proxies={"http": None, "https": None},
                )

            if response.status_code != 200:
                print(f"❌ Telegram photo failed: {response.text}")
            else:
                print("✅ Telegram photo sent successfully!")
            return response
        except Exception as e:
            print(f"❌ Error sending photo to Telegram: {e}")
            return None