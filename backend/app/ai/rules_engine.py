import logging

from app.ai.detection_engine import Detection


logger = logging.getLogger("uvicorn.error")


class RulesEngine:


    MIN_CONFIDENCE = 0.30


    FIRE_EVENTS = {
        "fire",
        "smoke",
        "flame",
    }


    WEAPON_EVENTS = {
        "gun",
        "pistol",
        "rifle",
        "knife",
        "weapon",
    }



    @staticmethod
    def evaluate(
        detections: list[Detection]
    ):


        if not detections:
            return None



        for detection in detections:


            if (
                detection.confidence
                < RulesEngine.MIN_CONFIDENCE
            ):
                continue



            label = (
                detection.class_name
                .lower()
            )



            # =========================
            # FIRE AI MODEL
            # =========================

            if (
                detection.source == "fire_model"
                and
                label in RulesEngine.FIRE_EVENTS
            ):

                logger.warning(
                    "🔥 FIRE ACCEPTED %s %.2f",
                    label,
                    detection.confidence,
                )


                return {

                    "incident_type":
                    "fire",

                    "severity":
                    "high",

                    "confidence":
                    detection.confidence,

                }



            # =========================
            # WEAPON AI MODEL
            # =========================

            if (
                detection.source == "weapon_model"
                and
                label in RulesEngine.WEAPON_EVENTS
            ):


                logger.warning(
                    "🚨 WEAPON ACCEPTED %s %.2f",
                    label,
                    detection.confidence,
                )


                return {

                    "incident_type":
                    "weapon",

                    "severity":
                    "critical",

                    "confidence":
                    detection.confidence,

                }



            logger.info(
                "Object ignored: %s %.2f (%s)",
                label,
                detection.confidence,
                detection.source,
            )



        return None