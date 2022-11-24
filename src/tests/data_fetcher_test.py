import unittest
from unittest.mock import MagicMock
from services.data_fetcher import DataFetcher


class TestDataFetcher(unittest.TestCase):

    def setUp(self) -> None:

        self.mock_pager = MagicMock()
        self.mock_pager.get_paginated_results = MagicMock(return_value=None)

        self.datafetch = DataFetcher(self.mock_pager)
        self.settings = {
            'pat': 'gl-test-token',
            'baseurl': 'www.gitlab.com/',
            'issue': {
                'state': 'all',
                'per_page': '100',
                'scope_id': '1000'
            },
            'comment': {
                'per_page': '20'
            }
        }

    def test_fetch_data_with_issue(self):

        self.datafetch.fetch_data(
            self.settings,
            data_type='issue'
        )

        self.mock_pager.get_paginated_results.assert_called_once_with(
            endpoint='www.gitlab.com/api/v4/groups/1000/issues',
            params={
                'state': 'all',
                'per_page': '100'
            },
            headers={
                'PRIVATE-TOKEN': 'gl-test-token'
            }
        )

    def test_fetch_data_with_comment(self):

        self.datafetch.fetch_data(
            self.settings,
            comment_endpoint='https://gitlab.com/api/v4/projects/37532450/issues/1/notes',
            data_type='comment'
        )

        self.mock_pager.get_paginated_results.assert_called_with(
            endpoint='https://gitlab.com/api/v4/projects/37532450/issues/1/notes',
            params={
                'per_page': '20'
            },
            headers={
                'PRIVATE-TOKEN': 'gl-test-token'
            }
        )

    def test_fetch_data_with_no_comment_endpoint(self):

        with self.assertRaises(Exception) as context:
            self.datafetch.fetch_data(
                self.settings,
                comment_endpoint='',
                data_type='comment'
            )
