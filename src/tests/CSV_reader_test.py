import unittest
import os
import csv
from pathlib import Path
import pandas as pd
from entities.issue import Issue
from services.csv_services import CSVTool
from services.json_reader import JSONReader


class TestCSVReader(unittest.TestCase):
    def setUp(self):

        # Remove possible test_output.csv if left from failed tests
        try:
            for path in Path('./').glob("TEST_CSV*.csv"):
                os.remove(path)
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

        self.sample_issue_attributes = {
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
            'Comments': ["2022-07-24T03:28:38.348Z; Rasmus Paltschik; assigned to @rjpalt"],
            'Watchers': ['Rasmus Paltschik']
        }

        self.issue_list = [
            Issue(
                self.sample_issue_attributes
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
                'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/30',
            ]
        ]

        self.deconstr_attrs = [
            'Labels',
            'Comments',
            'Watchers'
        ]

        self.reformatted_issue_attributes = {
            'Assignee': None,
            'Closed': None,
            'Comments1': 'It was done',
            'Created': '2022-11-22T13:27:56.554Z',
            'Description': 'issue numero yksi sisältö ja liite '
            '[liite8.txt](/uploads/05a314ad019c8b3592733a5802f6c36a/liite8.txt)',
            'Due Date': None,
            'Epic Link': 'The issue was not tied to a milestone',
            'Estimate': 0,
            'GitLab Issue URL': 'https://gitlab.com/rasse-posse/scripting-testing-subgroup/second-scripting-testing-subgroup/scripting-testing-project-in-subgroup/-/issues/1',
            'GitLab UID': 119188120,
            'Labels1': 'To_do',
            'Labels2': 'Undone',
            'Reporter': 'Ilkka Väisänen',
            'Status': 'opened',
            'Summary': 'issue numero yksi',
            'Time Spent': 0,
            'Watchers1': 'Ilkka Väisänen',
            'Watchers2': 'Rasmus Paltschik'
        }

        self.reformatted_columns = [
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
            'Comments1',
            'Labels1',
            'Labels2',
            'Watchers1',
            'Watchers2'
        ]

        self.test_settings = {
            'project_key': 'TEST_CSV'
        }

    def test_write_issues_to_csv(self):

        # Check that the temp file does not exist already
        for path in Path('./').glob("TEST_CSV*.csv"):
            self.assertIsNone(path)

        # Test the method
        return_filename = self.csv.write_issues_to_csv(
            self.issue_list,
            self.header_mappings,
            self.deconstr_attrs,
            self.test_settings
        )

        # Ascertain that the expectedfile was created
        self.assertTrue(os.path.isfile('./' + return_filename))

        # Test CSV output line-by-line
        with open('./' + return_filename, 'r', encoding='UTF-8', newline='') as test_csv:
            reader = csv.reader(test_csv, dialect='excel')
            self.assertEqual(next(reader), self.target_rows[0])
            self.assertEqual(next(reader), self.target_rows[1])

        # Remove the temp csv
        os.remove('./' + return_filename)

        # Ascertain the file was removed
        self.assertFalse(os.path.isfile('./' + return_filename))

    def test_issue_with_false_attributes(self):

        fake_deconstr_attrs = [
            'Branches'
        ]

        # Check that the temp file does not exist already
        for path in Path('./').glob("TEST_CSV*.csv"):
            self.assertIsNone(path)

        with self.assertRaises(KeyError):
            self.csv.write_issues_to_csv(
                self.issue_list,
                self.header_mappings,
                fake_deconstr_attrs,
                self.test_settings
            )

    def test_reformat_deconstructed_headers(self):

        data = [self.reformatted_issue_attributes]

        dataf = pd.DataFrame(data=data, columns=self.reformatted_columns)

        reformed_dataf = self.csv.reformat_deconstructed_headers(
            self.deconstr_attrs,
            dataf
        )

        target_list = [
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
            'Comments',
            'Labels',
            'Labels',
            'Watchers',
            'Watchers'
        ]

        self.assertListEqual(
            target_list,
            list(reformed_dataf.columns)
        )

    def test_add_removable_elements_to_rename_dict(self):

        data = [self.reformatted_issue_attributes]

        dataf = pd.DataFrame(data=data, columns=self.reformatted_columns)

        rename_dict = {}

        for attribute in self.deconstr_attrs:
            CSVTool.add_removable_elements_to_rename_dict(
                rename_dict, dataf, attribute
            )

        target_dict = {
            'Comments1': 'Comments',
            'Labels1': 'Labels',
            'Labels2': 'Labels',
            'Watchers1': 'Watchers',
            'Watchers2': 'Watchers'
        }

        self.assertDictEqual = (
            target_dict,
            rename_dict
        )
