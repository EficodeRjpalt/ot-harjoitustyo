import json

class JSONReader():

    def __init__(self):
        pass

    @classmethod
    def read_JSON_to_dict(cls, filepath: str) -> dict:
        """Reads a JSON file located in the filepath passed as an argument
        nd returns it as a python dict.

        Returns:
           _type_: dict
        """

        file = open(filepath, encoding='UTF-8')
       
        data = json.load(file)

        file.close()

        return data