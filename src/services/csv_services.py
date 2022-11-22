import csv
from services.json_reader import JSONReader


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

        with open(self._export_csv_filepath, encoding='UTF-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                temp_dict = {value: row[key] for (
                    key, value) in self._header_mapping.items()}
                return_list.append(temp_dict)

        return return_list

    def write_dict_into_csv(self, issue_dict_list: dict) -> None:

        with open(self._output_filepath, 'w', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, self._header_mapping.values())
            writer.writeheader()
            for issue_dictionary in issue_dict_list:
                writer.writerow(issue_dictionary)

    def transform_export_csv_to_import_csv(self):

        self.write_dict_into_csv(
            self.read_csv_to_dict()
        )

    @classmethod
    def write_issues_to_csv(cls, issue_list, output_filepath, header_mappings: dict):

        # print(header_mappings.values())

        with open(output_filepath, 'w', encoding='UTF-8') as file:
            writer = csv.DictWriter(file, header_mappings.values())
            writer.writeheader()
            for issue in issue_list:

                writer.writerow(
                    {
                        jira_fieldname: issue.attributes[gl_fieldname]
                        for (gl_fieldname, jira_fieldname)
                        in header_mappings.items()
                    }
                )
