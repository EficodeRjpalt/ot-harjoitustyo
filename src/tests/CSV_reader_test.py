import configparser
import unittest

from entities.issue import Issue
from services.csv_reader import CSVReader


class TestCSVReader(unittest.TestCase):
    def setUp(self):

        config = configparser.ConfigParser()
        config.read('src/config.cfg')

        # Using short version of CSV (only 1 entry)
        input_filepath = config['FILEPATHS']['input_short']
        mapping_filepath = config['FILEPATHS']['mapping']

        self.csv = CSVReader(mapping_filepath, input_filepath)

        self.target_dict = {
            'Summary': 'Update renewal analyzer to handle more multiple exception cases',
            'Description': "At the moment the renewal_analyzer.py only handles 'VARATTU' exceptions. Other exception cases can occur and should be handled.",
            'GitLab ID': '16',
            'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/16',
            'Status': 'Open',
            'Reporter': 'Rasmus Paltschik',
            'GitLab Username': 'rjpalt',
            'Assignee': 'Rasmus Paltschik',
            'Due Date': '',
            'Created': '2022-07-20 03:37:45',
            'Closed': '',
            'Epic Link': '',
            'Labels': '',
            'Estimate': '0',
            'Time Spent': '0'
        }

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

    def test_csv_to_dict(self):

        return_list = self.csv.read_csv_to_dict()

        self.assertIsInstance(
            return_list, list
        )

        self.assertTrue(
            len(return_list) == 1
        )

        issue_dict = return_list[0]

        self.assertDictEqual(
            issue_dict,
            self.target_dict
        )

    def test_transform_dict_items_into_issues(self):

        issue_list = [
            self.target_dict
        ]

        return_list = self.csv.transform_dict_items_into_issues(
            issue_list
        )

        self.assertIsInstance(
            return_list, list
        )

        self.assertTrue(
            len(return_list) == 1
        )

        self.assertIsInstance(
            return_list[0],
            Issue
        )

        self.assertDictEqual(
            return_list[0].attributes,
            self.target_dict
        )
