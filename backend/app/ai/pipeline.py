from app.ai.models.model_manager import ModelManager



class VisionPipeline:


    @staticmethod
    def analyze(frame):


        results = []


        object_results = (
            ModelManager.object_model(frame)
        )


        fire_results = (
            ModelManager.fire_model(frame)
        )


        weapon_results = (
            ModelManager.weapon_model(frame)
        )


        results.extend(
            object_results
        )


        results.extend(
            fire_results
        )


        results.extend(
            weapon_results
        )


        return results