import unittest
import configparser
from services.json_reader import JSONReader


class TestCSVReader(unittest.TestCase):
    def setUp(self):
        self.csv = JSONReader()

        config = configparser.ConfigParser()
        config.read('src/config.cfg')

        self.mapping_filepath = config['FILEPATHS']['mapping']

    def test_read_json_to_dict(self):

        target_dict = {
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

        return_dict = JSONReader.read_json_to_dict(self.mapping_filepath)

        self.assertTrue(isinstance(return_dict, dict))

        self.assertDictEqual(target_dict, return_dict)
