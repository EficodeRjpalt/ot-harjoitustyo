import unittest
import os
import csv

from entities.issue import Issue
from services.csv_services import CSVTool
from services.json_reader import JSONReader


class TestCSVReader(unittest.TestCase):
    def setUp(self):

        # Remove possible test_output.csv if left from failed tests
        try:
            os.remove('./src/tests/test_output.csv')
        except FileNotFoundError:
            pass

        self.csv = CSVTool()

        self.tmp_output_filepath = './src/tests/test_output.csv'

        self.header_mappings = JSONReader.read_json_to_dict(
            'src/resources/mapping.json')

        self.target_dict = {
            'Summary': 'Update renewal analyzer to handle more multiple exception cases',
            'Description': "At the moment the renewal_analyzer.py only handles 'VARATTU' exceptions. Other exception cases can occur and should be handled.",
            'GitLab UID': '16',
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

        sample_issue_attributes = {
            'Title': 'Refactor pipeline',
            'Description': "Pipeline should be in three stages.",
            'GitLab UID': 112096571,
            'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/30',
            'URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/30',
            'State': 'closed',
            'Author': 'Rasmus Paltschik',
            'Assignee': 'Rasmus Paltschik',
            'Due Date': None,
            'Created At (UTC)':
            '2022-07-24T03:28:38.280Z',
            'Closed At (UTC)': '2022-07-27T12:47:35.930Z',
            'Labels': ["Test"],
            'Time Estimate': 0,
            'Time Spent': 0,
            'Milestone': 'The issue was not tied to a milestone',
            'Comments': ["2022-07-24T03:28:38.348Z; Rasmus Paltschik; assigned to @rjpalt"]
        }

        self.issue_list = [
            Issue(
                sample_issue_attributes
            )
        ]

        self.target_rows = [
            [
                'Summary',
                'Description',
                'GitLab Issue URL',
                'Status',
                'Reporter',
                'Assignee',
                'Due Date',
                'Created',
                'Closed',
                'Epic Link',
                'Estimate',
                'Time Spent',
                'GitLab UID',
                'GitLab Issue URL',
            ],
            [
                '',
                'Pipeline should be in three stages.',
                'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/30',
                '',
                '',
                'Rasmus Paltschik',
                '',
                '',
                '',
                '',
                '',
                '0',
                '112096571',
                'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/30']
        ]

        self.deconstr_attrs = [
            'Labels',
            'Comments',
        ]

    def test_write_issues_to_csv(self):


        # Check that the temp file does not exist already
        self.assertFalse(os.path.isfile('./src/tests/test_output.csv'))

        # Test the method
        self.csv.write_issues_to_csv(
            self.issue_list,
            self.tmp_output_filepath,
            self.header_mappings,
            self.deconstr_attrs
        )

        # Ascertain that the expectedfile was created
        self.assertTrue(os.path.isfile('./src/tests/test_output.csv'))

        # Test CSV outpt line-by-line
        with open('./src/tests/test_output.csv', 'r', encoding='UTF-8', newline='') as test_csv:
            reader = csv.reader(test_csv, dialect='excel')
            self.assertEqual(next(reader), self.target_rows[0])
            self.assertEqual(next(reader), self.target_rows[1])

        # Remove the temp csv
        os.remove('./src/tests/test_output.csv')

        # Ascertain the file was removed
        self.assertFalse(os.path.isfile('./src/tests/test_output.csv'))

    def test_issue_with_false_attributes(self):

        fake_deconstr_attrs = [
            'Branches'
        ]

        # Check that the temp file does not exist already
        self.assertFalse(os.path.isfile('./src/tests/test_output.csv'))

        with self.assertRaises(KeyError) as context:
            self.csv.write_issues_to_csv(
                self.issue_list,
                self.tmp_output_filepath,
                self.header_mappings,
                fake_deconstr_attrs
            )