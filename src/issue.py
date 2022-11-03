"""
Class to represent a GitLab issue.
"""

class Issue():
    """
    This class represents a GitLab issue with the properties that
    have been chosen as salient.
    """
    def __init__(
            self,
            title: str,
            description: str,
            state: str,
            author: str,
            assignee: str,
            created: str,
            closed: str,
            labels: list,
            comments=[]
        ):

        self.title = title
        self.description = description
        self.state = state
        self.author = author
        self.assignee = assignee
        self.created = created
        self.closed = closed
        self.labels = labels
        self.comments = comments