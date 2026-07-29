class SeverityService:


    @staticmethod
    def calculate(
        confidence,
        incident_type
    ):


        if incident_type in [
            "fire",
            "weapon",
            "explosion"
        ]:

            return "critical"


        if confidence > 0.8:

            return "high"


        if confidence > 0.5:

            return "medium"


        return "low"