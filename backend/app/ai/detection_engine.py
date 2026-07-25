from dataclasses import dataclass


@dataclass
class Detection:

    class_name: str

    confidence: float

    source: str



class DetectionEngine:
    """
    Converts multiple YOLO model results into
    unified Detection objects.
    """


    @staticmethod
    def parse(results) -> list[Detection]:

        detections: list[Detection] = []


        if not results:
            return detections


        for index, result in enumerate(results):

            if not result.boxes:
                continue


            # Identify model source
            if index == 0:
                source = "object_model"

            else:
                source = "fire_model"


            for box in result.boxes:

                class_id = int(
                    box.cls[0]
                )


                confidence = float(
                    box.conf[0]
                )


                class_name = result.names[
                    class_id
                ]


                detections.append(

                    Detection(
                        class_name=class_name,
                        confidence=confidence,
                        source=source
                    )

                )


        return detections