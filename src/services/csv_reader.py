import csv
from services.json_reader import JSONReader
from entities.issue import Issue


class CSVReader():

    def __init__(self, filepath_headers: str,
                 filepath_export_csv: str,
                 output_filepath='src/resources/output.csv'
                 ) -> None:

        self._filepath_headers = filepath_headers
        self._header_mapping = self.get_header_mapping(
            self._filepath_headers)
        self._export_csv_filepath = filepath_export_csv
        self._output_filepath = output_filepath

    def get_header_mapping(self, filepath: str) -> dict:

        return JSONReader.read_json_to_dict(filepath)

    def read_csv_to_dict(self) -> dict:
        """
        Reads a CSV file at the path provided in arguments and
        returns the parsed file as a dictionary.

        Args:
            pathToCSV (str): absolute or relative path to the csv
            file that.

        Returns:
            List: contains the read CSV file's data as dict objects
            with each object having row-by-row
            values as values.
        """

        return_list = []

        with open(self.__export_csv_filepath, encoding='UTF-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {value: row[key] for (
                    key, value) in self.__header_mapping.items()}
                return_list.append(temp_dict)

        return return_list

    def transform_dict_items_into_issues(self, dict_list):

        issue_list = []

        for item in dict_list:
            issue_list.append(
                Issue(item)
            )

        return issue_list

    def write_dict_into_csv(self, issue_dict_list: dict) -> None:

        with open(self.__output_filepath, 'w', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, self.__header_mapping.values())
            writer.writeheader()
            for issue_dictionary in issue_dict_list:
                writer.writerow(issue_dictionary)

    def transform_export_csv_to_import_csv(self):

        self.write_dict_into_csv(
            self.read_csv_to_dict()
        )

