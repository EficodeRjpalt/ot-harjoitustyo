import json


class JSONReader():
    """Class to provide JSON reading services.
    """

    @classmethod
    def read_json_to_dict(cls, filepath: str) -> dict:
        """Function that reads a JSON file located at the location provided
        in the arguments.

        Args:
            filepath (str): The relative path to a JSON file that is to be
            read.

        Returns:
            dict: Returns read data as a Python dict.
        """

        data = {}

        with open(filepath, encoding='UTF-8') as file:

            data = json.load(file)

            file.close()

        return data
