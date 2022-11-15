import json


class JSONReader():

    def __init__(self):
        pass

    @classmethod
    def read_json_to_dict(cls, filepath: str) -> dict:
        """Reads a JSON file located in the filepath passed as an argument
        nd returns it as a python dict.

        Returns:
           _type_: dict
        """

        data = {}

        with open(filepath, encoding='UTF-8') as file:

            data = json.load(file)

            file.close()

        return data
