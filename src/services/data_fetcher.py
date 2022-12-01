from services.paginator import Paginator


class DataFetcher():

    def __init__(self, pager: Paginator):
        self.pager = pager

    def fetch_data(self, settings: dict, comment_endpoint='', data_type='issue') -> dict:

        headers = {
            'PRIVATE-TOKEN': settings['pat']
        }

        if data_type == 'issue':
            params = {
                'state': settings['issue']['state'],
                'per_page': settings['issue']['per_page']
            }

            endpoint = self._get_endpoint(settings)

        else:

            if comment_endpoint == '':
                raise Exception('No comment end point provided!')

            params = {
                'per_page': settings['watcher']['per_page']
            }

            endpoint = comment_endpoint

        scope_data = self.pager.get_paginated_results(
            endpoint=endpoint,
            params=params,
            headers=headers
        )

        return scope_data

    def _get_endpoint(self, settings: dict):

        if settings['scope_type'] == 'group':
            return settings['endpoint']['group']

        return settings['endpoint']['project']
