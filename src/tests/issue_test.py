import unittest
from issue import Issue


class TestIssue(unittest.TestCase):
    def setUp(self):

        issue_dict = {
            'title': 'Test title',
            'description': 'This issue is meant to test the Issue class',
            'state': 'Open',
            'author': 'Herra Sitti-Sonniainen',
            'assignee': 'Pormestari Kontiainen',
            'created': '[2022-07-20T03:45:02Z]',
            'closed': '[2022-07-25T05:23:02Z]',
            'labels': ['tests', 'mock']
        }

        self.issue = Issue(issue_dict)

    def test_issue_attributes(self):

        self.assertEqual(self.issue.title, 'Test title')
        self.assertEqual(self.issue.description,
                         'This issue is meant to test the Issue class')
        self.assertEqual(self.issue.state, 'Open')
        self.assertEqual(self.issue.assignee, 'Pormestari Kontiainen')
        self.assertEqual(self.issue.author, 'Herra Sitti-Sonniainen')
        self.assertEqual(self.issue.created, '[2022-07-20T03:45:02Z]')
        self.assertEqual(self.issue.closed, '[2022-07-25T05:23:02Z]')
        self.assertListEqual(self.issue.labels, ['tests', 'mock'])

