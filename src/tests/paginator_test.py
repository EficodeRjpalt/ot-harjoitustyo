import unittest
from unittest import mock
from services.paginator import Paginator


class TestPaginator(unittest.TestCase):

    def setUp(self) -> None:
        self.pager = Paginator()
        self.single_endpoint = 'https://gitlab.com/example-group'
        self.two_endpoint = 'https://gitlab.com/example-group/projekti-x'
        self.params_single = {'per_page': '20', 'total': '1'}
        self.params_double = {'per_page': '20', 'total': '2'}
        self.headers = {'pat': 'gl-example-pat'}

    def mock_request(self, **kwargs):

        Object = lambda **kwargs: type("Object", (), kwargs)

        def json():
            return ['Datadata']

        response_obj1 = Object(
            headers={
                'X-Next-Page': ''
            },
            json=json
        )

        response_obj2 = Object(
            headers={
                'X-Next-Page': ''
            },
            json=json
        )

        if kwargs['params']['page'] == '1':
            print(kwargs['params']['total'])
            return response_obj1
        elif kwargs['params']['page'] == '2':
            print(kwargs)
            return response_obj2

    @mock.patch('requests.get', side_effect=mock_request)
    def test_get_paginated_results_sinlge_page(self, mock_get):

        results = self.pager.get_paginated_results(
            self.single_endpoint,
            params=self.params_single,
            headers=self.headers
        )

        self.assertListEqual(
            results,
            ['Datadata']
        )

    @mock.patch('requests.get', side_effect=mock_request)
    def test_get_paginated_results_double_page(self, mock_get):

        results = self.pager.get_paginated_results(
            self.two_endpoint,
            params=self.params_double,
            headers=self.headers
        )

        self.assertListEqual(
            results,
            ['Datadata']
        )
