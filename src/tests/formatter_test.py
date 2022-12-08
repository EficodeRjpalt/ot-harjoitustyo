import unittest
from unittest.mock import patch
import configparser
from services.formatter import Formatter
from services.settings_getter import SettingsGetter
from services.data_fetcher import DataFetcher
from services.paginator import Paginator
from entities.issue import Issue
from resources.sample_responses import sample_response
from resources.sample_responses import target_dict
from resources.sample_responses import comment_sample_response
from resources.sample_responses import participants_sample_response
from resources.sample_responses import sample_issue_before_header_formatting


class TestFormatter(unittest.TestCase):

    def setUp(self) -> None:

        self.formatter = Formatter(
            DataFetcher(
                Paginator()
            )
        )

        self.sett_gett = SettingsGetter(
            'src/resources/test_config.cfg',
            configparser.ConfigParser()
        )

        self.user_mappings = self.sett_gett.get_user_mappings()

        self.response_dict = self.formatter.format_response_data_to_dict(
            sample_response,
            'test.com',
            self.user_mappings
        )

        self.header_mappings = self.sett_gett.get_header_mappings()

    def test_format_response_data_to_dict(self):

        self.assertTrue(
            target_dict,
            self.response_dict
        )

    def test_transform_dict_items_into_issues(self):

        issue_list = Formatter.transform_dict_items_into_issues(
            self.response_dict
        )

        self.assertTrue(
            len(issue_list) == 5
        )

        self.assertIsInstance(
            issue_list[0],
            Issue
        )

        self.assertDictEqual(
            issue_list[0].attributes,
            {
                'Assignee': None,
                'Author': 'ilkka.vaisanen@test.com',
                'Closed At (UTC)': None,
                'Comment Link': 'https://gitlab.com/api/v4/projects/41272516/issues/1/notes',
                'Created At (UTC)': '22/11/2022 13:27',
                'Description': 'issue numero yksi sisältö ja liite '
                                '[liite8.txt](/uploads/05a314ad019c8b3592733a5802f6c36a/liite8.txt)',
                'Due Date': None,
                'GitLab Issue URL': 'https://gitlab.com/rasse-posse/scripting-testing-subgroup/second-scripting-testing-subgroup/scripting-testing-project-in-subgroup/-/issues/1',
                'GitLab UID': 119188120,
                'Labels': [],
                'Milestone': 'The issue was not tied to a milestone',
                'Participant EP': 'https://gitlab.com/api/v4/projects/41272516/issues/1/participants',
                'State': 'opened',
                'Time Estimate': 0,
                'Time Spent': 0,
                'Title': 'issue numero yksi',
                'URL': 'https://gitlab.com/rasse-posse/scripting-testing-subgroup/second-scripting-testing-subgroup/scripting-testing-project-in-subgroup/-/issues/1'
            }
        )

    @patch('services.data_fetcher.DataFetcher.fetch_data')
    def test_add_comments_to_all_issues(self, mock_fetch_data):

        def side_effect(*args, **kwargs):
            return comment_sample_response

        mock_fetch_data.side_effect = side_effect

        http_settings = self.sett_gett.get_http_request_settings()

        test_issue_list = [
            Issue(self.response_dict[0])
        ]

        self.formatter.add_comments_to_all_issues(
            test_issue_list,
            http_settings,
            self.user_mappings
        )

        self.assertEqual(
            1,
            len(test_issue_list[0].attributes['Comments']),
        )

        self.assertEqual(
            '11/07/2022 09:40; rasmus.paltschik@eficode.com; MAGNIFICENT TEST COMMENT',
            str(test_issue_list[0].attributes['Comments'][-1])
        )

    @patch('services.data_fetcher.DataFetcher.fetch_data')
    def test_add_participants_to_all_issues(self, mock_fetch_data):

        def side_effect(*args, **kwargs):
            return participants_sample_response

        mock_fetch_data.side_effect = side_effect

        test_issue_list = [
            Issue(self.response_dict[0])
        ]

        http_settings = self.sett_gett.get_http_request_settings()

        self.formatter.add_participants_to_all_issues(
            test_issue_list,
            http_settings,
            self.user_mappings
        )

        self.assertEqual(
            1,
            len(test_issue_list[0].attributes['Participants']),
        )

        self.assertEqual(
            'testy.testersson@test.com',
            test_issue_list[0].attributes['Participants'][-1],
        )

    def test_fix_issue_attribute_names(self):

        test_issue_list = [
            Issue(sample_issue_before_header_formatting)
        ]

        self.formatter.fix_issue_attribute_names(
            test_issue_list,
            self.header_mappings
        )

        self.assertListEqual(
            list(test_issue_list[0].attributes.keys()),
            list(self.header_mappings.values())
        )

    def test_format_username_to_email_valids(self):

        testable_usernames = [
            ('Källe Kökkö', 'kalle.kokko@test.com'),
            ('Åke Öylätti', 'ake.oylatti@test.com'),
            ('Kelju K. Kojootti', 'kelju.k.kojootti@test.com'),
            ('Pekka-Liisa Kahlander', 'pekka-liisa.kahlander@test.com'),
            ('Wunder van der Wahlen', 'wunder.vanderwahlen@test.com'),
            ('Un  Lucky', 'un.lucky@test.com'),
            (' Miss Typed', 'miss.typed@test.com'),
            ('Peppeli', 'peppeli@test.com')
        ]

        for user in testable_usernames:
            formatted_usern = Formatter.format_username_to_email(
                user[0],
                'test.com'
            )

            self.assertEqual(
                user[1],
                formatted_usern
            )

    def test_format_invalid_usernames(self):

        testable_usernames = [
            ('', '')
        ]

        for user in testable_usernames:
            formatted_usern = Formatter.format_username_to_email(
                user[0],
                'test.com'
            )

            self.assertEqual(
                user[1],
                formatted_usern
            )
    def test_timestamps_to_jira(self):

        return_date = Formatter.transform_timestamp_to_jira(
            '2022-06-25T13:37:13.345Z'
        )

        self.assertEqual(
            '25/06/2022 13:37',
            return_date
        )

        return_date = Formatter.transform_timestamp_to_jira(
            '2022-06-25'
        )

        self.assertEqual(
            '25/06/2022 00:00',
            return_date
        )


    def test_timestamps_to_jira_empty_fields(self):

        return_date_empty_str = Formatter.transform_timestamp_to_jira(
            ''
        )

        self.assertEqual(
            None,
            return_date_empty_str
        )

    def test_timestamp_to_jira_invalid_values(self):

        return_date_invalid = Formatter.transform_timestamp_to_jira(
            '1998-6-13T13:37:45.456Z'
        )

        self.assertEqual(
            None,
            return_date_invalid
        )

        return_date_invalid = Formatter.transform_timestamp_to_jira(
            '1998-06-13T13:37:45:456'
        )

        self.assertEqual(
            '13/06/1998 00:00',
            return_date_invalid
        )