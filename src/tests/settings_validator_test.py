import unittest
from copy import deepcopy
from typesets.settings import SettingsValidator


class TestSettignsValidator(unittest.TestCase):

    def setUp(self):

        self.test_settings = {
            'baseurl': 'https://gitlab.com/',
            'comment': {'per_page': '20'},
            'domain_name': 'eficode.com',
            'endpoint': {'group': 'https://gitlab.com/api/v4/groups/55156717/issues',
                         'project': 'https://gitlab.com/api/v4/projects/55156717/issues'},
            'issue': {'per_page': '100', 'state': 'all'},
            'pat': 'glpat--9sdj-GWwGvAeSFXxWDP',
            'scope_id': '55156717',
            'scope_type': 'project',
            'watcher': {'per_page': '20'}
        }

        self.validator = SettingsValidator()

    def test_validate_scope_id_correct_input(self):

        validation = self.validator.validate_scope_id('123456')

        self.assertTrue(
            validation
        )

    def test_validate_scope_id_character(self):

        validation = self.validator.validate_scope_id('12345d')

        self.assertFalse(
            validation
        )

    def test_validate_scope_id_characters(self):

        validation = self.validator.validate_scope_id('projektin-nimi')

        self.assertFalse(
            validation
        )

    def test_validate_scope_id_float(self):

        validation = self.validator.validate_scope_id('514.41')

        self.assertFalse(
            validation
        )

    def test_validate_scope_id_trailing_whitespace(self):

        validation = self.validator.validate_scope_id('9823598 ')

        self.assertTrue(
            validation
        )

    def test_validate_scope_type_project(self):

        self.assertTrue(
            self.validator.validate_scope_type('project')
        )

    def test_validate_scope_type_group(self):

        self.assertTrue(
            self.validator.validate_scope_type('group')
        )

    def test_validate_scope_type_false_input(self):

        self.assertFalse(
            self.validator.validate_scope_type('groups')
        )

    def test_validate_scope_type_case_sensitive(self):

        self.assertFalse(
            self.validator.validate_scope_type('Group')
        )

    def test_validate_scope_type_trailing_ws(self):

        self.assertFalse(
            self.validator.validate_scope_type('project ')
        )

    def test_validate_gl_pat(self):

        self.assertTrue(
            self.validator.validate_gl_pat(self.test_settings['pat'])
        )

    def test_validate_gl_pat_short(self):

        test_pat = 'glpat--9sdj-GWwGvAeSFXxWD'

        self.assertFalse(
            self.validator.validate_gl_pat(test_pat)
        )

    def test_validate_gl_pat_long(self):

        test_pat = 'glpat--9sdj-GWwGvAeSFXxWDPPASD9klsadkjklasdlksakdsa9lasn,ajfna,jsfn,'

        self.assertFalse(
            self.validator.validate_gl_pat(test_pat)
        )

    def test_validate_domain_name_correct_inputs(self):

        self.assertTrue(
            self.validator.validate_domain_name('eficode.com')
        )

        self.assertTrue(
            self.validator.validate_domain_name('smartly.io')
        )

        self.assertTrue(
            self.validator.validate_domain_name('digital14.com')
        )

        self.assertTrue(
            self.validator.validate_domain_name('team.magenta')
        )

    def test_validate_domain_name_correct_inputs_capitals(self):

        self.assertTrue(
            self.validator.validate_domain_name('Eficode.com')
        )

        self.assertTrue(
            self.validator.validate_domain_name('eficode.Com')
        )

        self.assertTrue(
            self.validator.validate_domain_name('EFCICODE.COM')
        )

    def test_validate_domain_name_correct_inputs_trailing_ws(self):

        self.assertTrue(
            self.validator.validate_domain_name('eficode.com ')
        )

        self.assertTrue(
            self.validator.validate_domain_name('Eficode.com ')
        )

        self.assertTrue(
            self.validator.validate_domain_name('EFCICODE.COM ')
        )

    def test_validate_domain_name_incorrect_input(self):

        self.assertFalse(
            self.validator.validate_domain_name('eficode,com ')
        )

        self.assertFalse(
            self.validator.validate_domain_name('Eficodecom ')
        )

        self.assertFalse(
            self.validator.validate_domain_name('EFCICODECOM ')
        )

    def test_validate_url_correct_inputs(self):

        self.assertTrue(
            self.validator.validate_url(
                self.test_settings['baseurl']
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'http://gitlab.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'https://gitlab.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'www.gitlab.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'www.my.domain.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'https://my.domain.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'https://test-test.domain.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'https://my.test-domain.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'www.my.test-domain-test.com/'
            )
        )

        self.assertTrue(
            self.validator.validate_url(
                'www.my.portal.com/'
            )
        )


    def test_validate_url_incorrect_input(self):

        self.assertFalse(
            self.validator.validate_url(
                'https://gitlab.com'
            )
        )

        self.assertFalse(
            self.validator.validate_url(
                'wwwgitlab.com'
            )
        )

        self.assertFalse(
            self.validator.validate_url(
                'https://gitlabcom/'
            )
        )

        self.assertFalse(
            self.validator.validate_url(
                'https:/gitlab.com/'
            )
        )

    def test_settings_input_validation_correct_settings(self):

        self.assertTrue(
            self.validator.settings_input_validation(
                self.test_settings
            )
        )

    def test_settings_input_validation_incorrect_url(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['baseurl'] = 'www.gitlab.com'

        with self.assertRaises(ValueError):
            self.validator.settings_input_validation(
                tmp_settings
            )

    def test_settings_input_validation_incorrect_domain_name(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['domain_name'] = ''

        with self.assertRaises(ValueError):
            self.validator.settings_input_validation(
                tmp_settings
            )

    def test_settings_input_validation_incorrect_pat(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['pat'] = 'glat-foo-bar-biz'

        with self.assertRaises(ValueError):
            self.validator.settings_input_validation(
                tmp_settings
            )

    def test_settings_input_validation_incorrect_scope_type(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['scope_type'] = 'organization'

        with self.assertRaises(ValueError):
            self.validator.settings_input_validation(
                tmp_settings
            )

    def test_settings_input_validation_incorrect_scope_id(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['scope_id'] = '1234abc'

        with self.assertRaises(ValueError):
            self.validator.settings_input_validation(
                tmp_settings
            )

    def test_settings_input_validation_incorrect_issue_state(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['issue']['state'] = 'done'

        with self.assertRaises(ValueError):
            self.validator.settings_input_validation(
                tmp_settings
            )

    def test_settings_type_validation(self):

        self.assertTrue(
            self.validator.settings_type_validation(self.test_settings)
        )

    def test_settings_type_validation_mistype_scope_id(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['scope_id'] = 12498

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settings_type_validation_missing_issue(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings.pop('issue')

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settings_type_validation_missing_comment(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings.pop('comment')

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settings_type_validation_missing_watcer(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings.pop('watcher')

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settigs_type_validation_malformatted_issue(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['issue']['per_page'] = 20

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settigs_type_validation_malformatted_issue_no_state(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['issue'].pop('state')

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settigs_type_validation_malformatted_comment(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['comment']['per_page'] = 20

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_settigs_type_validation_malformatted_comment_no_per_page(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['comment'].pop('per_page')

        with self.assertRaises(TypeError):
            self.validator.settings_type_validation(
                tmp_settings
            )

    def test_validate_issue_state_correct_values(self):

        self.assertTrue(
            self.validator.validate_issue_state('opened')
        )

        self.assertTrue(
            self.validator.validate_issue_state('closed')
        )

        self.assertTrue(
            self.validator.validate_issue_state('all')
        )

    def test_validate_issue_state_malformatted(self):

        self.assertFalse(
            self.validator.validate_issue_state('')
        )

        self.assertFalse(
            self.validator.validate_issue_state('opned')
        )

        self.assertFalse(
            self.validator.validate_issue_state('done')
        )

        self.assertFalse(
            self.validator.validate_issue_state('opened ')
        )

        self.assertFalse(
            self.validator.validate_issue_state('CLOSED')
        )

    def test_validate_http_settings_correct_values(self):

        self.assertTrue(
            self.validator.validate_http_settings(
                self.test_settings
            )
        )

    def test_validate_http_settings_validation_incorrect_typing(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['issue'].pop('state')

        with self.assertRaises(TypeError):
            self.validator.validate_http_settings(
                tmp_settings
            )

    def test_validate_http_settings_validation_incorrect_values(self):

        tmp_settings = deepcopy(self.test_settings)
        tmp_settings['scope_type'] = 'organization'

        with self.assertRaises(ValueError):
            self.validator.validate_http_settings(
                tmp_settings
            )

    def test_validate_deconstruction_attributes(self):

        test_lists = [
            ['Comments'],
            ['Labels', 'Watchers'],
            ['Watchers', 'Comments'],
            ['Watchers', 'Labels', 'Comments'],
            []
        ]

        for test_list in test_lists:
            self.assertTrue(
                SettingsValidator.validate_deconstruction_attributes(test_list)
            )

    def test_validate_deconstruction_attributes_invalid(self):

        test_lists = [
            ['Labels', 'Badgers'],
            ['Comments', 'Watchers', 'Foxes'],
            ['Foxes', 'Badgers'],
        ]

        for test_list in test_lists:
            self.assertFalse(
                SettingsValidator.validate_deconstruction_attributes(test_list)
            )
