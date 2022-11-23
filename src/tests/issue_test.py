import unittest
from entities.issue import Issue


class TestIssue(unittest.TestCase):
    def setUp(self):

        self.issue_dict = {
            "Summary": "Test title",
            "Description": "This issue is meant to test the Issue class",
            "GitLab ID": 1,
            "GitLab Issue URL": "www.gitlab.com/example_project/-/1",
            "Status": "Open",
            "Reporter": "Herra Sitti-Sonniainen",
            "GitLab Username": "Pormestari",
            "Assignee": "Pormestari Kontiainen",
            "Created": "2022-07-20 03:45:02",
            "Due Date": "2022-07-26 12:00:02",
            "Closed": "2022-07-25 05:23:02",
            "Epic Link": "Epic 1",
            "Labels": "tests,mock",
            "Estimate": 0,
            "Time Spent": 5
        }

        self.no_names_issue_dict = {
            "Summary": "Test title",
            "Description": "This issue is meant to test the Issue class",
            "GitLab ID": 1,
            "GitLab Issue URL": "www.gitlab.com/example_project/-/1",
            "Status": "Open",
            "Reporter": "",
            "GitLab Username": "",
            "Assignee": "",
            "Created": "2022-07-20 03:45:02",
            "Due Date": "",
            "Closed": "",
            "Epic Link": "Epic 1",
            "Labels": "tests,mock",
            "Estimate": 0,
            "Time Spent": 5
        }

        self.issue = Issue(self.issue_dict)
        self.no_names_issue = Issue(self.no_names_issue_dict)

    def test_issue_attributes(self):

        self.assertEqual(self.issue.attributes['Summary'], 'Test title')
        self.assertEqual(self.issue.attributes['Description'],
                         'This issue is meant to test the Issue class')
        self.assertEqual(self.issue.attributes['GitLab ID'], 1)
        self.assertEqual(
            self.issue.attributes['GitLab Issue URL'], 'www.gitlab.com/example_project/-/1')
        self.assertEqual(self.issue.attributes['Status'], 'Open')
        self.assertEqual(
            self.issue.attributes['Assignee'], 'Pormestari Kontiainen')
        self.assertEqual(
            self.issue.attributes['GitLab Username'], 'Pormestari')
        self.assertEqual(
            self.issue.attributes['Reporter'], 'Herra Sitti-Sonniainen')
        self.assertEqual(
            self.issue.attributes['Created'], '2022-07-20 03:45:02')
        self.assertEqual(
            self.issue.attributes['Closed'], '2022-07-25 05:23:02')
        self.assertEqual(
            self.issue.attributes['Due Date'], '2022-07-26 12:00:02')
        self.assertEqual(self.issue.attributes['Epic Link'], 'Epic 1')
        self.assertEqual(self.issue.attributes['Labels'], 'tests,mock')
        self.assertEqual(self.issue.attributes['Estimate'], 0)
        self.assertEqual(self.issue.attributes['Time Spent'], 5)

    def test_issue_to_dict(self):

        self.assertDictEqual(self.issue_dict, self.issue.issue_to_dict())

    def test_displaynames_to_emails(self):

        self.issue.displaynames_to_emails('eficode.com')

        self.assertEqual(
            self.issue.attributes['Reporter'],
            'herra.sitti-sonniainen@eficode.com'
        )

        self.assertEqual(
            self.issue.attributes['Assignee'],
            'pormestari.kontiainen@eficode.com'
        )

    def test_displaynames_to_emails_no_names(self):

        self.no_names_issue.displaynames_to_emails('eficode.com')

        self.assertIsNone(
            self.no_names_issue.attributes['Reporter']
        )

        self.assertIsNone(
            self.no_names_issue.attributes['Assignee']
        )

    def test_timestamps_to_jira(self):

        self.issue.timestamps_to_jira()

        self.assertEqual(
            self.issue.attributes['Created'],
            '20/07/2022 03:45'
        )

        self.assertEqual(
            self.issue.attributes['Closed'],
            '25/07/2022 05:23'
        )

        self.assertEqual(
            self.issue.attributes['Due Date'],
            '26/07/2022 12:00'
        )

    def test_timestamps_to_jira_empty_fields(self):

        self.no_names_issue.timestamps_to_jira()

        self.assertEqual(
            self.no_names_issue.attributes['Created'],
            '20/07/2022 03:45'
        )

        self.assertIsNone(
            self.no_names_issue.attributes['Closed']
        )

        self.assertIsNone(
            self.no_names_issue.attributes['Due Date']
        )

# Testattava, että tulee oikeat attribuutit
# Päivitä testi-issuet oikealla datalla
# __repr__ testattava