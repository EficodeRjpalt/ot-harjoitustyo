import unittest
import configparser
from services.csv_reader import CSVReader


class TestCSVReader(unittest.TestCase):
    def setUp(self):

        config = configparser.ConfigParser()
        config.read('src/config.cfg')

        input_filepath = config['FILEPATHS']['input']
        mapping_filepath = config['FILEPATHS']['mapping']

        self.csv = CSVReader(mapping_filepath, input_filepath)

    def test_init_method(self):

        header_mapping = {
            "Title": "Summary",
            "Description": "Description",
            "Issue ID": "GitLab ID",
            "URL": "GitLab Issue URL",
            "State": "Status",
            "Author": "Reporter",
            "Author Username": "GitLab Username",
            "Assignee": "Assignee",
            "Due Date": "Due Date",
            "Created At (UTC)": "Created",
            "Closed At (UTC)": "Closed",
            "Milestone": "Epic Link",
            "Labels": "Labels",
            "Time Estimate": "Estimate",
            "Time Spent": "Time Spent"
        }

        self.assertEqual(
            self.csv._filepath_headers,
            'src/resources/mapping.json'
        )

        self.assertEqual(
            self.csv._header_mapping,
            header_mapping
        )
