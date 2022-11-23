"""
Class to represent a GitLab issue.
"""


class Issue():
    """
    This class represents a GitLab issue with the properties that
    have been chosen as salient.
    """

    def __init__(self, attributes: dict):

        self.attributes = attributes

    def issue_to_dict(self):
        return self.attributes

    def displaynames_to_emails(self, domain_name: str):

        self.attributes['Reporter'] = self.transform_name_to_email(
            self.attributes['Reporter'], domain_name)
        self.attributes['Assignee'] = self.transform_name_to_email(
            self.attributes['Assignee'], domain_name)

    def timestamps_to_jira(self):

        self.attributes['Created'] = self.transform_timestamp_to_jira(
            self.attributes['Created'])
        self.attributes['Due Date'] = self.transform_timestamp_to_jira(
            self.attributes['Due Date'])
        self.attributes['Closed'] = self.transform_timestamp_to_jira(
            self.attributes['Closed'])

    @classmethod
    def transform_name_to_email(cls, name: str, domain_name: str):

        if name != '':
            return name.lower().replace(' ', '.') + '@' + domain_name

        return None

    @classmethod
    def transform_timestamp_to_jira(cls, timestamp):

        if timestamp != '':

            timestamp_parts = timestamp.split(' ')
            date_parts = timestamp_parts[0].split('-')
            time_parts = timestamp_parts[1].split(':')

            jira_date = date_parts[2] + '/' + \
                date_parts[1] + '/' + date_parts[0]
            jira_time = time_parts[0] + ':' + time_parts[1]

            return jira_date + ' ' + jira_time

        return None

    def __repr__(self):
        return str(self.attributes)
