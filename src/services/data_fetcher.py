import requests

#from paginator import Paginator


class DataFetcher():

    def __init__(self):
        pass

    @classmethod
    def fetch_data(cls, settings: dict) -> dict:

        headers = {
            'PRIVATE-TOKEN': settings['pat']
        }

        params = {
            'state': settings['state'],
            'per_page': settings['per_page']
        }

        print(headers)
        print(params)

        groupname = settings['groupname']
        projectname = settings['projectname']

        if projectname not in (None, ''):
            endpoint = settings['baseURL'] + \
                f'api/v4/groups/{groupname}/{projectname}/issues'
        else:
            endpoint = settings['baseURL'] + \
                f'api/v4/groups/{groupname}/issues'

        print(endpoint)

# 2-do
# - settings-toiminnallisuus haulle -> lue configista -> anna datan haulle dictinä
