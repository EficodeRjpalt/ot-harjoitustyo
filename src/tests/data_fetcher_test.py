import unittest
from unittest.mock import MagicMock
from services.data_fetcher import DataFetcher
from copy import deepcopy


class TestDataFetcher(unittest.TestCase):

    def setUp(self) -> None:

        self.mock_pager = MagicMock()
        self.mock_pager.get_paginated_results = MagicMock(return_value=None)

        self.datafetch = DataFetcher(self.mock_pager)
        self.settings = {
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

    def test_fetch_data_with_issue(self):

        self.datafetch.fetch_data(
            self.settings,
            data_type='issue'
        )

        self.mock_pager.get_paginated_results.assert_called_once_with(
            endpoint=self.settings['endpoint']['group'],
            params={
                'state': 'all',
                'per_page': '100'
            },
            headers={
                'PRIVATE-TOKEN': 'glpat-foo-bar'
            }
        )

    def test_fetch_data_with_comment(self):

        self.datafetch.fetch_data(
            self.settings,
            comment_endpoint='https://gitlab.com/api/v4/projects/666/issues/1/notes',
            data_type='comment'
        )

        self.mock_pager.get_paginated_results.assert_called_with(
            endpoint='https://gitlab.com/api/v4/projects/666/issues/1/notes',
            params={
                'per_page': '20'
            },
            headers={
                'PRIVATE-TOKEN': 'glpat-foo-bar'
            }
        )

    def test_fetch_data_with_no_comment_endpoint(self):

        with self.assertRaises(Exception) as context:
            self.datafetch.fetch_data(
                self.settings,
                comment_endpoint='',
                data_type='comment'
            )

    def test_get_endpoint(self):

        endpoint = self.datafetch._get_endpoint(self.settings)

        self.assertEqual(
            'https://gitlab.com/api/v4/groups/666/issues',
            endpoint
        )

    def test_get_endpoint_project(self):

        settings = deepcopy(self.settings)

        settings['scope_type'] = 'project'

        endpoint = self.datafetch._get_endpoint(settings)

        self.assertEqual(
            'https://gitlab.com/api/v4/projects/666/issues',
            endpoint
        )

    def test_paginator_called_with_correct_values_group(self):

        self.datafetch.fetch_data(
            self.settings,
            data_type='issue'
        )

        self.mock_pager.get_paginated_results.assert_called_with(
            endpoint='https://gitlab.com/api/v4/groups/666/issues',
            params={
                'state': 'all',
                'per_page': '100'
            },
            headers={
                'PRIVATE-TOKEN': 'glpat-foo-bar'
            }
        )

    # Yllä oleva testi, mutta projekteilla

    def test_paginator_called_with_correct_values_project(self):

        project_settings = deepcopy(self.settings)

        project_settings['scope_type'] = 'project'

        self.datafetch.fetch_data(
            project_settings,
            data_type='issue'
        )

        self.mock_pager.get_paginated_results.assert_called_with(
            endpoint='https://gitlab.com/api/v4/projects/666/issues',
            params={
                'state': 'all',
                'per_page': '100'
            },
            headers={
                'PRIVATE-TOKEN': 'glpat-foo-bar'
            }
        )
