import unittest
from issue import Issue


class TestIssue(unittest.TestCase):
    def setUp(self):
        self.issue = Issue(
            'Test title',
            'This issue is meant to test the Issue class',
            'Open',
            'Herra Sitti-Sonniainen',
            'Pormestari Kontiainen',
            '[2022-07-20T03:45:02Z]',
            '[2022-07-25T05:23:02Z]',
            ['tests', 'mock']
        )

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
