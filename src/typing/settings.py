from typing import TypedDict
from strongtyping.strong_typing import match_class_typing

@match_class_typing
class Settings(TypedDict):
    pat: str
    issue: dict
    comment: dict

@match_class_typing
class Issue(TypedDict):
    state: str
    per_page: str
    scope_id: str

@match_class_typing
class Comment(TypedDict):
    per_page: str

class SettingsValidator():

    @classmethod
    def validate_settings(cls, settings: dict):

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


settings = {
    'pat': 'bleh',
    'issue': {
        'state': 'opened',
        'per_page': '100',
        'scope_id': '235236'
    },
    'comment' : {
        'per_page': '20'
    }
}

## To-do
# Assertoi, että arvot ovat oikeata tyyppiä (3xint ja opened/all/closed)

SettingsValidator.validate_settings(settings)
