from app.assistant.knowledge import (
    EMERGENCY_KNOWLEDGE
)



class GuardianAssistant:


    @staticmethod
    def answer(question:str):

        text = question.lower()


        for key,data in EMERGENCY_KNOWLEDGE.items():


            if key in text:


                return {

                    "type":"emergency",

                    "response":data

                }



        return {


            "type":"general",

            "response":{

                "message":
                "Please describe the emergency type clearly."

            }


        }