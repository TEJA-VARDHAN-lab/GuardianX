import logging


logger = logging.getLogger("uvicorn.error")


class AccidentRules:


    @staticmethod
    def evaluate(
        detections
    ):

        persons = [
            d for d in detections
            if d.class_name.lower() == "person"
        ]


        vehicles = [
            d for d in detections
            if d.class_name.lower()
            in {
                "car",
                "truck",
                "bus",
                "motorcycle"
            }
        ]


        if (
            len(persons) > 0
            and len(vehicles) > 0
        ):

            logger.info(
                "🚗 Possible accident scene detected"
            )

            return {
                "incident_type": "accident",
                "severity": "critical",
                "confidence": 0.70,
            }


        return None