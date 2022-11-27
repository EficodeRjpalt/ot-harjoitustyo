from entities.issue import Issue
from entities.comment import Comment
from services.data_fetcher import DataFetcher


class Formatter():

    def __init__(self, datafetcher: DataFetcher):
        self.datafetch = datafetcher

    def format_response_data_to_dict(self, response_data: list):

        return_issue_dict_list = []

        print('Issues to handle: ' + str(len(response_data)))

        for issue in response_data:

            try:
                milestone = issue['milestone']['title']
            except TypeError:
                milestone = 'The issue was not tied to a milestone'

            try:
                assignee = issue['assignee']['name']
            except TypeError:
                assignee = None

            return_issue_dict_list.append(
                {
                    "Title": issue['title'],
                    "Description": issue['description'],
                    "GitLab UID": issue['id'],
                    "GitLab Issue URL": issue['web_url'],
                    "URL": issue['web_url'],
                    "State": issue['state'],
                    "Author": issue['author']['name'],
                    "Assignee": assignee,
                    "Due Date": issue['due_date'],
                    "Created At (UTC)": issue['created_at'],
                    "Closed At (UTC)": issue['closed_at'],
                    "Labels": issue['labels'],
                    "Time Estimate": issue['time_stats']['time_estimate'],
                    "Time Spent": issue['time_stats']['total_time_spent'],
                    "Milestone": milestone,
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

    def add_comments_to_all_issues(self, issue_dict_list: list, settings: dict):

        for issue in issue_dict_list:
            comment_list = [
                Comment(
                    comment['created_at'],
                    comment['author']['name'],
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

    @classmethod
    def fix_issue_attribute_names(cls, list_of_issues: list, header_mappings: dict):

        for issue in list_of_issues:
            new_attributes = {
                jira_fieldname: issue.attributes[gl_fieldname]
                for (gl_fieldname, jira_fieldname)
                in header_mappings.items()
            }

            issue.attributes = new_attributes


