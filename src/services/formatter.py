import unicodedata
from entities.issue import Issue
from entities.comment import Comment
from services.data_fetcher import DataFetcher


class Formatter():

    def __init__(self, datafetcher: DataFetcher):
        self.datafetch = datafetcher

    def format_response_data_to_dict(
        self,
        response_data: list,
        domain_name: str,
        user_mapping: dict
    ):

        return_issue_dict_list = []

        print('Issues to handle: ' + str(len(response_data)))

        for issue in response_data:

            try:
                milestone = issue['milestone']['title']
            except TypeError:
                milestone = 'The issue was not tied to a milestone'

            try:
                assignee = Formatter.map_username_to_email(
                    issue['assignee']['name'],
                    domain_name,
                    user_mapping
                )
            except TypeError:
                assignee = None

            try:
                author = Formatter.map_username_to_email(
                    issue['author']['name'],
                    domain_name,
                    user_mapping
                )
            except TypeError:
                author = None

            return_issue_dict_list.append(
                {
                    "Title": issue['title'],
                    "Description": issue['description'],
                    "GitLab UID": issue['id'],
                    "GitLab Issue URL": issue['web_url'],
                    "URL": issue['web_url'],
                    "State": issue['state'],
                    "Author": author,
                    "Assignee": assignee,
                    "Due Date": issue['due_date'],
                    "Created At (UTC)": issue['created_at'],
                    "Closed At (UTC)": issue['closed_at'],
                    "Labels": issue['labels'],
                    "Time Estimate": issue['time_stats']['time_estimate'],
                    "Time Spent": issue['time_stats']['total_time_spent'],
                    "Milestone": milestone,
                    "Participant EP": issue['_links']['self'] + '/participants',
                    "Comment Link": issue['_links']['notes']
                }
            )

        return return_issue_dict_list

    @classmethod
    def transform_dict_items_into_issues(cls, dict_list: list) -> list:

        issue_list = []

        for item in dict_list:
            issue_list.append(
                Issue(item)
            )

        return issue_list

    def add_comments_to_all_issues(
            self,
            issue_dict_list: list,
            settings: dict,
            user_mappings: dict) -> None:

        for issue in issue_dict_list:
            comment_list = [
                Comment(
                    comment['created_at'],
                    Formatter.map_username_to_email(
                        comment['author']['name'],
                        settings['domain_name'],
                        user_mappings
                    ),
                    comment['body']
                )
                for comment in self.datafetch.fetch_data(
                    settings,
                    issue.attributes['Comment Link'],
                    data_type='comment'
                )
            ]

            issue.attributes['Comments'] = comment_list
            issue.attributes.pop('Comment Link')

    def add_participants_to_all_issues(
        self,
        issue_dict_list: list,
        settings: dict,
        user_mappings: dict
    ) -> None:

        for issue in issue_dict_list:
            participant_list = [
                Formatter.map_username_to_email(
                    participant['name'],
                    settings['domain_name'],
                    user_mappings)
                for participant in
                self.datafetch.fetch_data(
                    settings,
                    issue.attributes['Participant EP'],
                    data_type='watcher')
            ]

            issue.attributes['Participants'] = participant_list

    @classmethod
    def fix_issue_attribute_names(cls, list_of_issues: list, header_mappings: dict):

        for issue in list_of_issues:
            new_attributes = {
                jira_fieldname: issue.attributes[gl_fieldname]
                for (gl_fieldname, jira_fieldname)
                in header_mappings.items()
            }

            issue.attributes = new_attributes

    @classmethod
    def map_username_to_email(cls, username: str, domain_name: str, user_mappings: dict) -> str:

        if username in user_mappings.keys():
            return user_mappings[username]

        print(username + ' is not in the user mappings!')

        return cls.format_username_to_email(username, domain_name)

    @classmethod
    def format_username_to_email(cls, username: str, domain_name: str) -> str:

        if len(username) > 0:
            # Remove umlauts etc. from the name and return it to UTF-8 format
            normalized_name = unicodedata.normalize(
                'NFKD', username).encode('ASCII', 'ignore').decode('UTF-8')
            name_parts = [part.lower() for part in normalized_name.split(' ')]
            return name_parts[0] + '.' + ''.join(name_parts[1:]) + '@' + domain_name

        return username

    def format_fetched_issue_data(
            self,
            retrieved_json_data: list,
            http_settings: dict,
            header_mappings: dict,
            user_mappings
    ) -> list:

        # This needs refactoring. Why should some be classmethods and soem instance?

        issue_dict_list = Formatter.transform_dict_items_into_issues(
            self.format_response_data_to_dict(
                retrieved_json_data,
                http_settings['domain_name'],
                user_mappings
            )
        )

        self.add_comments_to_all_issues(
            issue_dict_list,
            http_settings,
            user_mappings
        )

        self.add_participants_to_all_issues(
            issue_dict_list,
            http_settings,
            user_mappings
        )
        Formatter.fix_issue_attribute_names(issue_dict_list, header_mappings)

        return issue_dict_list
