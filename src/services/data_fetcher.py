from services.paginator import Paginator


class DataFetcher():

    pager = Paginator()

    @classmethod
    def fetch_data(cls, settings: dict, comment_endpoint='', data_type='issue') -> dict:

        headers = {
            'PRIVATE-TOKEN': settings['pat']
        }


        if data_type == 'issue':
            params = {
                'state': settings['state'],
                'per_page': settings['per_page']
            }

            scope_id = settings['scope_id']

            endpoint = settings['baseURL'] + \
                f'api/v4/groups/{scope_id}/issues'
                
        elif data_type == 'comment':
            params = {
                'per_page': settings['per_page']
            }

            endpoint = comment_endpoint
            
        

        scope_data = cls.pager.get_paginated_results(
            endpoint=endpoint,
            params=params,
            headers=headers
        )

        return scope_data