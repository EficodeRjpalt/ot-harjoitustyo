import unittest
from unittest import mock
from services.paginator import Paginator

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, headers, json_data, status_code):
            self.headers = headers
            self.status_code = status_code
            self.json_data = json_data

            print(json_data)

            if json_data['Two Page'] == '3':
                self.headers ['X-Next-Page'] = ''

        def json(self):
            return self.json_data

    single_page_headers = {
        'X-Next-Page': ''
    }

    single_page_data = {
        'First Page': 'Single Page Data'
    }

    two_page_headers = {
            'X-Next-Page': '2'
    }

    two_page_data = {
        'Two Page': 'Two Page Data'
    }

    third_page_data = {
        'Third Page': 'Three Page Data'
    }

    print(args)

    if args[0] == 'https://gitlab.com/example-group':
        return MockResponse(single_page_headers, single_page_data, 200)
    elif args[0] == 'https://gitlab.com/example-group/projekti-x':
        return MockResponse(two_page_headers, two_page_data, 200)

    return MockResponse(single_page_headers, None, 404)

class TestPaginator(unittest.TestCase):

    def setUp(self) -> None:
        self.pager = Paginator()
        self.single_endpoint = 'https://gitlab.com/example-group'
        self.two_endpoint = 'https://gitlab.com/example-group/projekti-x'
        self.paramms = {'per_page': '20'}
        self.headers = {'pat': 'gl-example-pat'}

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_paginated_results_sinlge_page(self, mock_get):

        results = self.pager.get_paginated_results(
            self.single_endpoint,
            params=self.paramms,
            headers=self.headers
        )

        self.assertListEqual(
            results,
            ['First Page']
        )

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_paginated_results_double_page(self, mock_get):

        results = self.pager.get_paginated_results(
            self.two_endpoint,
            params=self.paramms,
            headers=self.headers
        )

        print(results)

        self.assertListEqual(
            results,
            ['Two Page']
        )
