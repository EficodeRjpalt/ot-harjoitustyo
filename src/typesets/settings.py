import re
from typing import TypedDict
from strongtyping.strong_typing import match_class_typing


@match_class_typing
class Settings(TypedDict):
    baseurl: str
    comment: dict #
    domain_name: str
    endpoint: dict
    issue: dict #
    pat: str
    scope_id: str
    scope_type: str
    watcher: dict #


@match_class_typing
class Issue(TypedDict):
    state: str
    per_page: str


@match_class_typing
class Comment(TypedDict):
    per_page: str


class SettingsValidator():

    valid_scope_types = ['group', 'project']
    valid_deconst_attributes = ['Comment']

    @classmethod
    def validate_http_settings(cls, settings: dict):

        try:
            Settings(settings)
        except Exception as exc:
            raise TypeError('Wrongly typed settings!') from exc

        try:
            Issue(settings['issue'])
        except Exception as exc:
            raise TypeError('Issue settings mistyped!') from exc

        try:
            Comment(settings['comment'])
        except Exception as exc:
            raise TypeError('Comment settings mistyped!') from exc

        if not cls.validate_url(settings['baseurl']):
            raise ValueError('Invalid baseURL provided!')

        if not cls.validate_domain_name(settings['domain_name']):
            raise ValueError('Invalid domain name provided!')

        if not cls.validate_gl_pat(settings['pat']):
            raise ValueError(
                'There is likely something wrong with your GL PAT')

        if not cls.validate_scope_type(settings['scope_type']):
            raise ValueError('Incorrect scope type provided!')

        if not cls.validate_scope_id(settings['scope_id']):
            raise ValueError('Incorrect scope ID. Must be an integer!')

    @classmethod
    def validate_url(cls, url: str):

        validation_re = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""

        pattern = re.compile(validation_re)
        return pattern.match(url)

    @classmethod
    def validate_domain_name(cls, domain_name: str):

        validation_re = r"^[a-z0-9]+\.[a-z0-9]+$"

        pattern = re.compile(validation_re)
        return pattern.match(domain_name.lower())

    @classmethod
    def validate_gl_pat(cls, gl_pat: str):

        validation_re = r"glpat-[0-9a-zA-Z\-]{20}"

        pattern = re.compile(validation_re)

        return pattern.match(gl_pat)

    @classmethod
    def validate_scope_type(cls, scope_type: str):

        return scope_type in cls.valid_scope_types

    @classmethod
    def validate_scope_id(cls, scope_id: str) -> bool:

        try:
            test_scope_id = int(scope_id)
        except ValueError:
            test_scope_id = scope_id

        if isinstance(test_scope_id, int):
            return True

        return False


test_settings = {
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


SettingsValidator.validate_http_settings(test_settings)
