from services.paginator import Paginator


class DataFetcher():
    """A Class to abstract the fetching of issue data via HTTP requests
    to GitLab's API. Calls on an instsance of Paginator class to handle
    the pagination of results and the actual HTTP requests.
    """

    def __init__(self, pager: Paginator):
        """Constructor of the DataFetcher class.

        Args:
            pager (Paginator): an instance of Paginator class to handle
            pagination and to make the actual HTTP requests.
        """
        self.pager = pager

    def fetch_data(self, settings: dict, comment_endpoint='', data_type='issue') -> list:
        """Function to handle the formatting of params, endpoints and headers
        that are provided to the Paginator instance that will then do the
        http requests.
        Collects the received aggregated data and forwards it back to main
        program.

        Args:
            settings (dict): contains the HTTP requests settings as a dict object.
            parsed from config.cfg.
            comment_endpoint (str, optional): Comment endpoint can and MUST be
            provided when calling teh function to get full comments of an issue.
            Defaults to ''.
            data_type (str, optional): Data type that is being fetched. Possible values:
            'issue', 'comment' or 'watcher'. Defaults to 'issue'.

        Raises:
            Exception: raises ValueError if the issue type is not an 'issue' and
            the comment endpoint is ''.

        Returns:
            list: returns all the collected items from the paginated HTTP rquests.
        """

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
                raise ValueError('No comment endpoint provided!')

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

    def _get_endpoint(self, settings: dict) -> str:
        """Helper function to extract the endpoint from the settings
        dict.

        Args:
            settings (dict): Dictionary containing the settigns for HTTP requests.

        Returns:
            str: Returns the correct endpoint as a str.
        """

        if settings['scope_type'] == 'group':
            return settings['endpoint']['group']

        return settings['endpoint']['project']
