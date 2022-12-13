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

    def __repr__(self):
        return str(self.attributes)
