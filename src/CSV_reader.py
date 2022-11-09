import csv


class CSVReader():

    def __init__(self) -> None:
        pass

    def readCSVToDict(self, pathToCSV: str) -> dict:
        """
        Reads a CSV file at the path provided in arguments and
        returns the parsed file as a dictionary.

        Args:
            pathToCSV (str): absolute or relative path to the csv
            file that.

        Returns:
            dict: contains the read CSV file's data as dict objects
            with each object having column as key and row-by-row
            values as values.
        """

        return_dict = {}

        try:
            with open(pathToCSV, newline='', encoding='UTF-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    print(row['Issue ID'])
        except FileNotFoundError as error:
            print(error)

        return return_dict


cssv = CSVReader()
cssv.readCSVToDict('./test/sample.csv')
