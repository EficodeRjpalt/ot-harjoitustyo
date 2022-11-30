import unittest
from services.reconstructor import Reconstructor
from services.json_reader import JSONReader
from entities.issue import Issue
from pprint import pprint
from copy import deepcopy


class TestComment(unittest.TestCase):

    def setUp(self):

        self.header_mappings = JSONReader.read_json_to_dict(
            'src/tests/test_mapping.json')

        self.deconst_list = [
            'Labels',
            'Comments'
        ]

        self.test_issue1 = Issue(
            attributes={
                'Assignee': 'Evgenii Smirnov',
                'Closed': '2022-07-13T10:07:08.236Z',
                'Comments': ['2022-07-13T10:07:07.955Z; Evgenii Smirnov; mentioned in commit 5561ce985f6dc93b476478ca6911436f0205316f',
                             '2022-07-13T09:53:21.014Z; Evgenii Smirnov; mentioned in merge request !3',
                             '2022-07-13T09:53:03.939Z; Evgenii Smirnov; created branch [`1-parempi-odotus-iframen-latautumiselle-2`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...1-parempi-odotus-iframen-latautumiselle-2) to address this issue',
                             '2022-07-13T09:37:45.384Z; Evgenii Smirnov; mentioned in merge request !2',
                             '2022-07-11T12:09:01.867Z; Evgenii Smirnov; created branch [`1-parempi-odotus-iframen-latautumiselle`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...1-parempi-odotus-iframen-latautumiselle) to address this issue',
                             '2022-07-11T09:39:30.854Z; Rasmus Paltschik; assigned to @jevgenix and unassigned @anuvirtane',
                             '2022-07-11T09:39:27.794Z; Rasmus Paltschik; assigned to @anuvirtane and unassigned @jevgenix',
                             '2022-07-11T09:39:20.552Z; Rasmus Paltschik; assigned to @jevgenix and unassigned @anuvirtane',
                             '2022-07-10T17:57:38.314Z; Rasmus Paltschik; changed the description',
                             '2022-07-10T17:57:12.380Z; Rasmus Paltschik; assigned to @anuvirtane]'
                             ],
                'Created': '2022-07-10T17:57:12.278Z',
                'Description': 'Tällä hetkellä main.py rivien 29 - 32 koodi on vähän kökkö; '
                'time.sleep() ei ole oikeasti järkevä tapa ratkaista '
                'odotusongelmaa, mutta yritykset fiksummalla tavalla meni '
                'multa puihin eikä toiminu.\n'
                '\n'
                'Koodi näyttää tältä:\n'
                '\n'
                '```\n'
                'time.sleep(10)\n'
                '\n'
                'driver.switch_to.frame(driver.find_element(By.XPATH, '
                "'//iFrame'))\n"
                "table_elem = driver.find_element(By.CLASS_NAME, 'patFunc')\n"
                '```\n'
                '\n'
                'Switch tarttee tehdä, mutta lataus olis fiksu tehdä '
                'odottamalla, että elementti on lautautunut.',
                'Due Date': None,
                'Epic Link': 'The issue was not tied to a milestone',
                'Estimate': 0,
                'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/1',
                'GitLab UID': 111421942,
                'Labels': ['To Do'],
                'Reporter': 'Rasmus Paltschik',
                'Status': 'closed',
                'Summary': 'Parempi odotus iFramen latautumiselle',
                'Time Spent': 0
            }
        )

        self.test_issue2 = Issue(
            attributes={
                'Assignee': 'Rasmus Paltschik',
                'Closed': '2022-07-20T03:29:08.781Z',
                'Comments': ['2022-07-13T04:30:38.627Z; Rasmus Paltschik; mentioned in merge request !1',
                             '2022-07-13T04:30:08.486Z; Rasmus Paltschik; created branch [`4-moduuli-gmailin-lahettamista-varten`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...4-moduuli-gmailin-lahettamista-varten) to address this issue',
                             '2022-07-13T04:29:55.603Z; Rasmus Paltschik; assigned to @rjpalt'
                             ],
                'Created': '2022-07-13T04:29:55.465Z',
                'Description': 'Oma moduuli, joka lähettää epäonnistuneista lainoista '
                'tiedotteen sähköpostitse',
                'Due Date': None,
                'Epic Link': 'The issue was not tied to a milestone',
                'Estimate': 0,
                'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/4',
                'GitLab UID': 111548645,
                'Labels': ['In Progress'],
                'Reporter': 'Rasmus Paltschik',
                'Status': 'closed',
                'Summary': 'Moduuli Gmailin lähettämistä varten',
                'Time Spent': 0
            }
        )

        self.test_issue3 = Issue(
            attributes={
                'Assignee': None,
                'Closed': None,
                'Comments': [
                    """2022-11-03T03:53:14.310Z; Rasmus Paltschik; # This one has a table #

                | Päivä | Työtunnit | Kumulatiiviset tunnit |
                |-------|:---------:|:---------------------:|
                |3.11.  | 2         | 2                     |
                |       |           |                       |""",
                    '2022-07-23T04:29:38.465Z; Rasmus Paltschik; changed the description'
                ],
                'Created': '2022-07-23T04:28:56.772Z',
                'Description': 'Object tests atm have dependencies on other objects. Refactor '
                'object modules to use mock objects.',
                'Due Date': None,
                'Epic Link': 'Major Milestone 1',
                'Estimate': 0,
                'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/28',
                'GitLab UID': 112074082,
                'Labels': ['pipeline review', 'status::needs_review', 'unittest'],
                'Reporter': 'Rasmus Paltschik',
                'Status': 'opened',
                'Summary': 'Refactor object tests using mock-objects',
                'Time Spent': 0
            }
        )

        self.test_issue4 = Issue(
            attributes={
                'Assignee': None,
                'Closed': None,
                'Comments': [
                    """2022-11-03T03:53:14.310Z; Rasmus Paltschik; # This one has a table #

                | Päivä | Työtunnit | Kumulatiiviset tunnit |
                |-------|:---------:|:---------------------:|
                |3.11.  | 2         | 2                     |
                |       |           |                       |""",
                    '2022-07-23T04:29:38.465Z; Rasmus Paltschik; changed the description'
                ],
                'Created': '2022-07-23T04:28:56.772Z',
                'Description': 'Object tests atm have dependencies on other objects. Refactor '
                'object modules to use mock objects.',
                'Due Date': None,
                'Epic Link': 'Major Milestone 1',
                'Estimate': 0,
                'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/28',
                'GitLab UID': 112074082,
                'Labels': [],
                'Reporter': 'Rasmus Paltschik',
                'Status': 'opened',
                'Summary': 'Refactor object tests using mock-objects',
                'Time Spent': 0
            }
        )

    def test_reformat_tmp_issue_labels(self):

        target_issue = deepcopy(self.test_issue1)

        test_issue = deepcopy(self.test_issue1)

        target_issue.attributes['Labels1'] = 'To_Do'

        Reconstructor.reformat_tmp_issue(
            test_issue, deconst_attribute='Labels')

        self.assertDictEqual(
            test_issue.attributes,
            target_issue.attributes
        )

    def test_reformat_tmp_issue_comments(self):

        target_issue = deepcopy(self.test_issue2)

        test_issue = deepcopy(self.test_issue2)

        target_issue.attributes['Comments1'] = '2022-07-13T04:30:38.627Z; Rasmus Paltschik; mentioned in merge request !1'
        target_issue.attributes['Comments2'] = '2022-07-13T04:30:08.486Z; Rasmus Paltschik; created branch [`4-moduuli-gmailin-lahettamista-varten`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...4-moduuli-gmailin-lahettamista-varten) to address this issue'
        target_issue.attributes['Comments3'] = '2022-07-13T04:29:55.603Z; Rasmus Paltschik; assigned to @rjpalt'

        Reconstructor.reformat_tmp_issue(
            test_issue, deconst_attribute='Comments')

        self.assertDictEqual(
            test_issue.attributes,
            target_issue.attributes
        )

    def test_reformat_tmp_issue_comments_wrong_attr(self):

        test_issue = deepcopy(self.test_issue4)
        target_issue = deepcopy(self.test_issue4)

        Reconstructor.reformat_tmp_issue(
            test_issue, deconst_attribute='Labels')

        self.assertDictEqual(
            target_issue.attributes,
            test_issue.attributes
        )

    def test_max_count_labels(self):

        issue_list = [
            self.test_issue1,
            self.test_issue2,
            self.test_issue3
        ]

        max_count = Reconstructor.get_max_count(issue_list, 'Labels')

        self.assertEqual(
            3,
            max_count
        )

    def test_max_count_comments(self):

        issue_list = [
            self.test_issue1,
            self.test_issue2,
            self.test_issue3
        ]

        max_count = Reconstructor.get_max_count(issue_list, 'Comments')

        self.assertEqual(
            10,
            max_count
        )

    def test_generate_list_appendix_labels(self):

        return_list = Reconstructor.generate_list_appendix(3, 'Labels')

        target_list = ['Labels1', 'Labels2', 'Labels3']

        self.assertListEqual(
            target_list,
            return_list
        )

    def test_generate_list_appendix_comments(self):

        return_list = Reconstructor.generate_list_appendix(2, 'Comments')

        target_list = ['Comments1', 'Comments2']

        self.assertListEqual(
            target_list,
            return_list
        )

    def test_generate_list_appendix_zero_value(self):

        return_list = Reconstructor.generate_list_appendix(0, 'Comments')

        target_list = []

        self.assertListEqual(
            target_list,
            return_list
        )

    def test_generate_list_appendix_negative_value(self):

        return_list = Reconstructor.generate_list_appendix(-1, 'Comments')

        target_list = []

        self.assertListEqual(
            target_list,
            return_list
        )

    def test_generate_list_appendix_wrong_type(self):

        return_list = Reconstructor.generate_list_appendix('Bla', 'Comments')

        target_list = []

        self.assertListEqual(
            target_list,
            return_list
        )

    def test_check_spaces_from_attr_labels(self):

        test_label1 = 'Needs review'
        test_label2 = 'To  do'
        test_label3 = 'Is_done'

        return_str1 = Reconstructor.check_spaces_from_attr(
            'Labels', test_label1)
        return_str2 = Reconstructor.check_spaces_from_attr(
            'Labels', test_label2)
        return_str3 = Reconstructor.check_spaces_from_attr(
            'Labels', test_label3)

        self.assertEqual(
            'Needs_review',
            return_str1
        )

        self.assertEqual(
            'To_do',
            return_str2
        )

        self.assertEqual(
            'Is_done',
            return_str3
        )

    def test_check_spaces_from_attr_comments(self):

        return_str = Reconstructor.check_spaces_from_attr(
            'Comments', 'This is my comment!')

        self.assertEqual(
            'This is my comment!',
            return_str
        )

    def test_update_headers(self):

        header_mappings = deepcopy(self.header_mappings)
        target_headers_dict = deepcopy(self.header_mappings)

        target_headers_dict['Header1'] = 'Header1'
        target_headers_dict['Header2'] = 'Header2'

        dummy_appendix_list = ['Header1', 'Header2']

        Reconstructor.update_headers(
            header_mappings,
            dummy_appendix_list
        )

        self.assertEqual(
            'Header1',
            header_mappings['Header1']
        )

        self.assertEqual(
            'Header2',
            header_mappings['Header2']
        )

        with self.assertRaises(KeyError) as context:
            print(header_mappings['Header3'])

        self.assertDictEqual(
            target_headers_dict,
            header_mappings
        )

    def test_reconstruct_all_issue_dict_attributes(self):

        reconstruct_list = [
            deepcopy(self.test_issue1),
            deepcopy(self.test_issue2),
            deepcopy(self.test_issue3),
            deepcopy(self.test_issue4)
        ]

        header_mappings = deepcopy(self.header_mappings)

        returned_issues = Reconstructor.reconstruct_all_issue_dict_attributes(
            header_mappings,
            reconstruct_list,
            self.deconst_list
        )

        self.assertEqual(
            4,
            len(returned_issues)
        )

        target_dict = deepcopy(self.header_mappings)

        target_dict['Comments1'] = 'Comments1'
        target_dict['Comments2'] = 'Comments2'
        target_dict['Comments3'] = 'Comments3'
        target_dict['Comments4'] = 'Comments4'
        target_dict['Comments5'] = 'Comments5'
        target_dict['Comments6'] = 'Comments6'
        target_dict['Comments7'] = 'Comments7'
        target_dict['Comments8'] = 'Comments8'
        target_dict['Comments9'] = 'Comments9'
        target_dict['Comments10'] = 'Comments10'

        target_dict['Labels1'] = 'Labels1'
        target_dict['Labels2'] = 'Labels2'
        target_dict['Labels3'] = 'Labels3'

        self.assertDictEqual(
            target_dict,
            header_mappings
        )

        target_attrs1 = {
            'Assignee': 'Evgenii Smirnov',
            'Closed': '2022-07-13T10:07:08.236Z',
            'Comments': ['2022-07-13T10:07:07.955Z; Evgenii Smirnov; mentioned in commit '
                        '5561ce985f6dc93b476478ca6911436f0205316f',
                        '2022-07-13T09:53:21.014Z; Evgenii Smirnov; mentioned in merge '
                        'request !3',
                        '2022-07-13T09:53:03.939Z; Evgenii Smirnov; created branch '
                        '[`1-parempi-odotus-iframen-latautumiselle-2`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...1-parempi-odotus-iframen-latautumiselle-2) '
                        'to address this issue',
                        '2022-07-13T09:37:45.384Z; Evgenii Smirnov; mentioned in merge '
                        'request !2',
                        '2022-07-11T12:09:01.867Z; Evgenii Smirnov; created branch '
                        '[`1-parempi-odotus-iframen-latautumiselle`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...1-parempi-odotus-iframen-latautumiselle) '
                        'to address this issue',
                        '2022-07-11T09:39:30.854Z; Rasmus Paltschik; assigned to '
                        '@jevgenix and unassigned @anuvirtane',
                        '2022-07-11T09:39:27.794Z; Rasmus Paltschik; assigned to '
                        '@anuvirtane and unassigned @jevgenix',
                        '2022-07-11T09:39:20.552Z; Rasmus Paltschik; assigned to '
                        '@jevgenix and unassigned @anuvirtane',
                        '2022-07-10T17:57:38.314Z; Rasmus Paltschik; changed the '
                        'description',
                        '2022-07-10T17:57:12.380Z; Rasmus Paltschik; assigned to '
                        '@anuvirtane]'],
            'Comments1': '2022-07-13T10:07:07.955Z; Evgenii Smirnov; mentioned in commit '
                        '5561ce985f6dc93b476478ca6911436f0205316f',
            'Comments10': '2022-07-10T17:57:12.380Z; Rasmus Paltschik; assigned to '
                        '@anuvirtane]',
            'Comments2': '2022-07-13T09:53:21.014Z; Evgenii Smirnov; mentioned in merge '
                        'request !3',
            'Comments3': '2022-07-13T09:53:03.939Z; Evgenii Smirnov; created branch '
                        '[`1-parempi-odotus-iframen-latautumiselle-2`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...1-parempi-odotus-iframen-latautumiselle-2) '
                        'to address this issue',
            'Comments4': '2022-07-13T09:37:45.384Z; Evgenii Smirnov; mentioned in merge '
                        'request !2',
            'Comments5': '2022-07-11T12:09:01.867Z; Evgenii Smirnov; created branch '
                        '[`1-parempi-odotus-iframen-latautumiselle`](/rasse-posse/helmet-lainojen-uusija/-/compare/master...1-parempi-odotus-iframen-latautumiselle) '
                        'to address this issue',
            'Comments6': '2022-07-11T09:39:30.854Z; Rasmus Paltschik; assigned to '
                        '@jevgenix and unassigned @anuvirtane',
            'Comments7': '2022-07-11T09:39:27.794Z; Rasmus Paltschik; assigned to '
                        '@anuvirtane and unassigned @jevgenix',
            'Comments8': '2022-07-11T09:39:20.552Z; Rasmus Paltschik; assigned to '
                        '@jevgenix and unassigned @anuvirtane',
            'Comments9': '2022-07-10T17:57:38.314Z; Rasmus Paltschik; changed the '
                        'description',
            'Created': '2022-07-10T17:57:12.278Z',
            'Description': 'Tällä hetkellä main.py rivien 29 - 32 koodi on vähän kökkö; '
                            'time.sleep() ei ole oikeasti järkevä tapa ratkaista '
                            'odotusongelmaa, mutta yritykset fiksummalla tavalla meni '
                            'multa puihin eikä toiminu.\n'
                            '\n'
                            'Koodi näyttää tältä:\n'
                            '\n'
                            '```\n'
                            'time.sleep(10)\n'
                            '\n'
                            'driver.switch_to.frame(driver.find_element(By.XPATH, '
                            "'//iFrame'))\n"
                            "table_elem = driver.find_element(By.CLASS_NAME, 'patFunc')\n"
                            '```\n'
                            '\n'
                            'Switch tarttee tehdä, mutta lataus olis fiksu tehdä '
                            'odottamalla, että elementti on lautautunut.',
            'Due Date': None,
            'Epic Link': 'The issue was not tied to a milestone',
            'Estimate': 0,
            'GitLab Issue URL': 'https://gitlab.com/rasse-posse/helmet-lainojen-uusija/-/issues/1',
            'GitLab UID': 111421942,
            'Labels': ['To Do'],
            'Labels1': 'To_Do',
            'Reporter': 'Rasmus Paltschik',
            'Status': 'closed',
            'Summary': 'Parempi odotus iFramen latautumiselle',
            'Time Spent': 0
        }
        

        self.assertDictEqual(
            target_attrs1,
            returned_issues[0].attributes
        )