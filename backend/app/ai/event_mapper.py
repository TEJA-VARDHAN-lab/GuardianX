class EventMapper:


    MAP = {


        "fire":
        "fire",


        "smoke":
        "fire",


        "knife":
        "weapon",


        "gun":
        "weapon",


        "flood":
        "flood",


        "landslide":
        "landslide",


        "person":
        "human_detection"

    }



    @classmethod
    def normalize(cls,label):

        return cls.MAP.get(
            label.lower(),
            None
        )