"""
Class to represent a GitLab issue.
"""


class Issue():
    """
    This class represents a GitLab issue with the properties that
    have been chosen as salient.
    """

    def __init__(self, attributes: dict):

        self.title = attributes['title']
        self.description = attributes['description']
        self.state = attributes['state']
        self.author = attributes['author']
        self.assignee = attributes['assignee']
        self.created = attributes['created']
        self.closed = attributes['closed']
        self.labels = attributes['labels']
