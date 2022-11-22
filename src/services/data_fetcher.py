from services.paginator import Paginator


class DataFetcher():

    pager = Paginator()

    @classmethod
    def fetch_data(cls, settings: dict) -> dict:

        headers = {
            'PRIVATE-TOKEN': settings['pat']
        }

        params = {
            'state': settings['state'],
            'per_page': settings['per_page']
        }

        scope_id = settings['scope_id']

        endpoint = settings['baseURL'] + \
            f'api/v4/groups/{scope_id}/issues'

        scope_data = cls.pager.get_paginated_results(
            endpoint=endpoint,
            params=params,
            headers=headers
        )

        return scope_data
