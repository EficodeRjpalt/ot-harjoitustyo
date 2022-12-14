import os
import unittest
import configparser
from copy import deepcopy
from unittest import mock
from services.settings_getter import SettingsGetter


class TestComment(unittest.TestCase):

    def setUp(self):

        self.sett_get = SettingsGetter(
            'src/resources/test_config.cfg',
            configparser.ConfigParser()
        )

    def test_init(self):

        self.assertEqual(
            str(type(self.sett_get.config)),
            "<class 'configparser.ConfigParser'>"
        )

    @mock.patch.dict(os.environ, {"GL_PAT": "glpat-foo-bar"})
    def test_get_http_equest_settings(self):

        target_dict = {
            'baseurl': 'https://gitlab.com/',
            'comment': {'per_page': '20'},
            'domain_name': 'test.com',
            'endpoint': {'group': 'https://gitlab.com/api/v4/groups/666/issues',
                         'project': 'https://gitlab.com/api/v4/projects/666/issues'},
            'issue': {'per_page': '100', 'state': 'all'},
            'pat': 'glpat-foo-bar',
            'scope_id': '666',
            'scope_type': 'group',
            'watcher': {'per_page': '20'}
        }

        http_settings = self.sett_get.get_http_request_settings()

        self.assertDictEqual(
            target_dict,
            http_settings
        )

    def test_get_header_mappings(self):

        returned_mappings = self.sett_get.get_header_mappings()

        target_dict = {
            'Assignee': 'Assignee',
            'Author': 'Reporter',
            'Closed At (UTC)': 'Closed',
            'Comments': 'Comments',
            'Created At (UTC)': 'Created',
            'Description': 'Description',
            'Due Date': 'Due Date',
            'GitLab Issue URL': 'GitLab Issue URL',
            'GitLab UID': 'GitLab UID',
            'Labels': 'Labels',
            'Milestone': 'Epic Link',
            'Participants': 'Watchers',
            'State': 'Status',
            'Time Estimate': 'Estimate',
            'Time Spent': 'Time Spent',
            'Title': 'Summary',
        }

        self.assertDictEqual(
            target_dict,
            returned_mappings
        )

    def test_create_endpoint_project(self):

        return_endpoint = self.sett_get.create_endpoint('project')

        target_endpoint = 'https://gitlab.com/api/v4/projects/666/issues'

        self.assertEqual(
            target_endpoint,
            return_endpoint
        )

    def test_create_endpoint_group(self):

        return_endpoint = self.sett_get.create_endpoint('group')

        target_endpoint = 'https://gitlab.com/api/v4/groups/666/issues'

        self.assertEqual(
            target_endpoint,
            return_endpoint
        )

    def test_get_deconstruction_attributes(self):

        returned_attrs = self.sett_get.get_deconstruction_attributes()

        target_list = [
            'Comments',
            'Labels',
            'Watchers'
        ]

        self.assertListEqual(
            target_list,
            returned_attrs
        )

    def test_get_csv_settings(self):

        target_dict = {
            'project_key': 'TEST_CSV'
        }

        self.assertEqual(
            target_dict,
            self.sett_get.get_csv_settings()
        )

    def test_get_user_mappings(self):

        target_mappings = {
            'Pormestari Kontiainen': 'pormestari.kontiainen@kontiala.kon',
            'Rasmus Paltschik': 'rasmus.paltschik@eficode.com',
            'Herra Sitti-Sonniainen': 'herra.sitti-sonniainen@kontiala.kon'
        }

        user_mappings = self.sett_get.get_user_mappings()

        self.assertDictEqual(
            target_mappings,
            user_mappings
        )

    def test_sanitize_input(self):

        inputs = [
            (' faulty string', 'faulty string'),
            ('another faulty string    ', 'another faulty string'),
            ('correct string', 'correct string')
        ]

        for input in inputs:
            self.assertEqual(
                input[1],
                self.sett_get.sanitize_input(input[0])
            )

    def test_get_label_configs(self):

        target_dict = {
            'headers': {
                'Issue Type': 'Task', 'Priority': 'Normal', 'Status': ''
            },
            'labels': {
                'Prio_1': {
                    'field': 'Priority',
                    'value': 'Highest'
                },
                'Prio_3': {
                    'field': 'Priority',
                    'value': 'Medium'
                },
                'status::in_progress': {
                    'field': 'Status',
                    'value': 'In Progress'
                },
                'status::needs_review': {
                    'field': 'Status',
                    'value': 'Review'
                },
                'unittest': {
                    'field': 'Issue Type',
                    'value': 'Test'
                }
            }
        }

        label_configs = self.sett_get.get_label_configs()

        self.assertDictEqual(
            target_dict,
            label_configs
        )

    def test_get_deconstruction_attributes_wrong_attribute(self):

        self.sett_get.config['DECONSTRUCT']['allowed'] += ',Badgers'

        with self.assertRaises(ValueError):
            self.sett_get.get_deconstruction_attributes()
