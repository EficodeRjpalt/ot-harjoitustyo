import unittest
from issue import Issue

class TestIssue(unittest.TestCase):
    def setUp(self):
        issue = Issue(
            'Test title',
            'This issue is meant to test the Issue class',
            'Open',
            'Herra Sitti-Sonniainen',
            'Pormestari Kontiainen',
            '[2022-07-20T03:45:02Z]',
            '[2022-07-25T05:23:02Z]',
            ['tests', 'mock']
        )