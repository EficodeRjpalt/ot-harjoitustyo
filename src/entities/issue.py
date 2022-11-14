"""
Class to represent a GitLab issue.
"""


class Issue():
    """
    This class represents a GitLab issue with the properties that
    have been chosen as salient.
    """

    def __init__(self, attributes: dict):

        self.summary = attributes['Summary']
        self.description = attributes['Description']
        self.gitlab_id = attributes['GitLab ID']
        self.gl_url = attributes['GitLab Issue URL']
        self.status = attributes['Status']
        self.reporter = attributes['Reporter']
        self.assignee = attributes['Assignee']
        self.gl_username = attributes['GitLab Username']
        self.created = attributes['Created']
        self.closed = attributes['Closed']
        self.due_date = attributes['Due Date']
        self.labels = attributes['Labels']
        self.epic_link = attributes['Epic Link']
        self.estimate = attributes['Estimate']
        self.time_spent = attributes['Time Spent']

    def issue_to_dict(self):
        return {
            'Summary': self.summary,
            'Description': self.description,
            'GitLab ID': self.gitlab_id,
            'GitLab Issue URL': self.gl_url,
            'Status': self.status,
            'Reporter': self.reporter,
            'GitLab Username': self.gl_username,
            'Assignee': self.assignee,
            'Due Date': self.due_date,
            'Created': self.created,
            'Closed': self.closed,
            'Epic Link': self.epic_link,
            'Labels': self.labels,
            'Estimate': self.estimate,
            'Time Sent': self.time_spent
        }

    def displaynames_to_emails(self, domain_name: str):

        self.reporter = self.transform_name_to_email(self.reporter, domain_name)
        self.assignee = self.transform_name_to_email(self.assignee, domain_name)

    def timestamps_to_jira(self):

        self.created = self.transform_timestamp_to_jira(self.created)
        self.due_date = self.transform_timestamp_to_jira(self.due_date)
        self.closed = self.transform_timestamp_to_jira(self.closed)

    @classmethod
    def transform_name_to_email(cls, name: str, domain_name: str):

        return name.lower().replace(' ', '.') + '@' + domain_name

    @classmethod
    def transform_timestamp_to_jira(cls, timestamp):

        if timestamp != '':

            timestamp_parts = timestamp.split(' ')
            date_parts = timestamp_parts[0].split('-')
            time_parts = timestamp_parts[1].split(':')

            jira_date = date_parts[2] + '/' + date_parts[1] + '/' + date_parts[0]
            jira_time = time_parts[0] + ':' + time_parts[1]

            return jira_date + ' ' + jira_time

        return ''