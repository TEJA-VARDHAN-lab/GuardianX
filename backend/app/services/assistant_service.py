import logging

from app.services.system_context_service import (
    SystemContextService
)


logger = logging.getLogger("uvicorn.error")


class AssistantService:


    KNOWLEDGE = {

        "fire":
        "Move away from the fire source. Avoid elevators. Contact fire emergency services.",


        "flood":
        "Move to higher ground. Avoid electrical equipment and flowing water.",


        "earthquake":
        "Drop, cover, and hold. Stay away from windows and heavy objects.",


        "accident":
        "Move to a safe location. Contact police and ambulance services.",


        "weapon":
        "Avoid confrontation. Move away and notify police immediately.",

    }



    @classmethod
    def answer(
        cls,
        query: str
    ):


        text = query.lower()


        # Live GuardianX status questions

        status_keywords = [
            "status",
            "what is happening",
            "current",
            "active incident",
            "latest alert",
            "system"
        ]


        if any(
            keyword in text
            for keyword in status_keywords
        ):

            context = (
                SystemContextService
                .get_context()
            )


            latest = context.get(
                "latest_incident"
            )


            if latest:

                answer = f"""
GuardianX Live Status:

Active Incidents:
{context['active_incidents']}


Latest Incident:

Type:
{latest['type']}


Severity:
{latest['severity']}


Confidence:
{latest['confidence'] * 100:.1f}%


Camera:
{latest['camera']}


Location:
{latest['location']}


Emergency response routing initiated.
"""

            else:

                answer = """
GuardianX Live Status:

No active incidents detected.
All monitored sectors are operating normally.
"""


            return {

                "mode": "live",

                "answer":
                answer.strip()

            }



        # Emergency safety questions

        for keyword, response in cls.KNOWLEDGE.items():

            if keyword in text:

                return {

                    "mode":
                    "offline",

                    "answer":
                    response

                }



        return {

            "mode":
            "offline",

            "answer":
            (
                "Stay calm and move to a safe location. "
                "Contact local emergency services if required."
            )

        }