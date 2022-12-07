from copy import deepcopy
import requests
from pprint import pprint


class Paginator():

    def __init__(self):
        pass

    @classmethod
    def get_paginated_results(cls, endpoint: str, params: dict, headers: dict):

        aggregate_response_data = []

        next_page = True

        # Take a copy of original parameters and add key-value
        # pair to indicate which page is paginated
        pagination_params = deepcopy(params)
        pagination_params['page'] = '1'

        while next_page:
            response = requests.get(
                endpoint,
                params=pagination_params,
                headers=headers,
                timeout=60
            )

            if response.headers['X-Next-Page'] == '':
                aggregate_response_data += response.json()
                next_page = False
            else:
                pagination_params['page'] = str(
                    int(pagination_params['page']) + 1)
                aggregate_response_data += response.json()

        return aggregate_response_data


pagery = Paginator()
