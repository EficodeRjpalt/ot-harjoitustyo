import re
from typing import TypedDict
from strongtyping.strong_typing import match_class_typing


@match_class_typing
class Settings(TypedDict):
    """Class for checking the typing of a Settings dictioanry.

    Args:
        TypedDict: inherits TypeDict class.
    """
    baseurl: str
    comment: dict
    domain_name: str
    endpoint: dict
    issue: dict
    pat: str
    scope_id: str
    scope_type: str
    watcher: dict


@match_class_typing
class Issue(TypedDict):
    """Class for checking the typing of a Issue dictioanry within
    Settings dictionary.

    Args:
        TypedDict: inherits TypeDict class.
    """
    state: str
    per_page: str


@match_class_typing
class Comment(TypedDict):
    """Class for checking the typing of a Comment dictionary
    within settings dictioanry.

    Args:
        TypedDict: inherits TypeDict class.
    """
    per_page: str


class SettingsValidator():
    """A class for valdiating types and values of a settings dictionary
    created by the SettingsGetter class.

    Raises:
        TypeError: If the settings dict contains wrong kind of k-v typing.
        TypeError: If the issue dict contains wrong kind of k-v typing.
        TypeError: If the comment dict contains wrong kind of k-v typing.
        ValueError: If the value provided in the settings dictionary key for
        baseurl is malformatted.
        ValueError: If the value provided in the settings dictionary key for
        domain_name is malformatted.
        ValueError: If the value provided in the settings dictionary key for
        baseurl is malformatted.
        ValueError: If the value provided in the settings dictionary key for
        pat is malformatted.
        ValueError: If the value provided in the settings dictionary key for
        scope_id is malformatted.
        ValueError: If the value provided in the settings dictionary key for
        scope_type is malformatted.

    Returns: True if validation passes. Raises an exception if validation
    fails.
    """

    valid_scope_types = ['group', 'project']
    valid_deconst_attributes = ['Comments', 'Labels', 'Watchers']
    allowed_states = [
        'opened',
        'closed',
        'all'
    ]

    @classmethod
    def validate_http_settings(cls, settings: dict) -> bool:
        """Umbrella function for checking the http request settings' typing
        and provided values

        Args:
            settings (dict): dictionary containing the settings dictionary
            parsed by SettingsGetter.

        Returns: True if typing and validation checks. Otherwise raises an
        exception (TypeError or ValueError).

        """

        cls.settings_type_validation(settings)

        cls.settings_input_validation(settings)

        return True

    @classmethod
    def settings_type_validation(cls, settings: dict) -> bool:
        """Fuction to run typing checks on settings dictionary and its
        sub-dictionaries for issue and comment requests.

        Args:
            settings (dict): dictionary containing the settings dictionary
            parsed by SettingsGetter.

        Raises:
            TypeError: If the settings dict contains wrong kind of k-v typing.
            TypeError: If the issue dict contains wrong kind of k-v typing.
            TypeError: If the comment dict contains wrong kind of k-v typing.

        Returns:
            bool: Returns True if settings type cehck passes. Raises
            exception if the type check fails.
        """

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

        return True

    @classmethod
    def settings_input_validation(cls, settings: dict) -> bool:
        """Function to validate the values provided in the settings
        dictionary. The values are parsed by ConfigParser from config.cfg
        file.

        Args:
            settings (dict): dictionary containing the settings dictionary
            parsed by SettingsGetter.

        Raises:
            ValueError: If the value provided in the settings dictionary key for
            baseurl is malformatted.
            ValueError: If the value provided in the settings dictionary key for
            domain_name is malformatted.
            ValueError: If the value provided in the settings dictionary key for
            baseurl is malformatted.
            ValueError: If the value provided in the settings dictionary key for
            pat is malformatted.
            ValueError: If the value provided in the settings dictionary key for
            scope_id is malformatted.
            ValueError: If the value provided in the settings dictionary key for
            scope_type is malformatted.

        Returns:
            bool: Returns True if settings validation passes. Raises
            exception if the validation fails.
        """

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

        if not cls.validate_issue_state(settings['issue']['state']):
            raise ValueError('Incorrect issue state parameter given!')

        return True

    @classmethod
    def validate_url(cls, url: str) -> re.match:
        """Function to validate provided URL with regex match.
        Accepted types are http(s) and www with maximum of one point
        in the domain's name and ending with /.

        Returns:
            Returns a re.match iterable object.

        """

        validation_re = (r"""(https?:\/\/|www\.)(([a-z0-9-]+\.[a-z0-9]+/$)|"""
                         r"""([a-z0-9-]+)\.[a-z0-9-]+\.[a-z0-9]+/$)""")

        pattern = re.compile(validation_re)
        return pattern.match(url)

    @classmethod
    def validate_domain_name(cls, domain_name: str) -> re.match:
        """Function to regex check if provided domain name is valid.
        accepts domain names with single comma between unspecified amount
        of characters.

        Args:
            domain_name (str): domain name parsed from the config.cfg section
            COMMON.

        Returns:
            Returns a re.match iterable object.
        """

        validation_re = r"^[a-z0-9]+\.[a-z0-9]+$"

        pattern = re.compile(validation_re)
        return pattern.match(domain_name.strip().lower())

    @classmethod
    def validate_gl_pat(cls, gl_pat: str) -> re.match:
        """Validates if the provided GitLab Persona Access Token is of
        correct format. Currently it starts with 'glpat-' and contains
        a total of 20-40 alphanumerical characters.

        Args:
            gl_pat (str): GitLab Personal Access Token fetched from the
            .env file.

        Returns:
            Returns a re.match iterable object.
        """

        validation_re = r"glpat-[0-9a-zA-Z\-_]{20,40}$"

        pattern = re.compile(validation_re)

        return pattern.match(gl_pat)

    @classmethod
    def validate_scope_type(cls, scope_type: str) -> bool:
        """Function to validate scope type provided in the config.cfg file.
        Currently supported values are 'group' and 'project'.

        Args:
            scope_type (str): Scope type parsed from config.cfg as a string.

        Returns:
           Returns true if the provided value is in the Class' validation
           list valid_scope_types.
        """

        return scope_type in cls.valid_scope_types

    @classmethod
    def validate_scope_id(cls, scope_id: str) -> bool:
        """Function to validate scope id provided in the config.cfg file.

        Args:
            scope_id (str): scope id provided as a string. The value must
            possbile to recast as an integer. E.g. it is an integer as a
            string.

        Returns:
            bool: returns True if the value provided is positive integer.
        """

        try:
            test_scope_id = int(scope_id.strip())
        except ValueError:
            test_scope_id = scope_id

        if isinstance(test_scope_id, int):
            return True

        return False

    @classmethod
    def validate_issue_state(cls, state: str) -> bool:
        """Function to validate that issue state is within the list of
        allowed values for state.

        Args:
            state (str): value of the state. Available options: 'opened',
            'closed' and 'all'.

        Returns:
            bool: Returns True if the value is in the list and False if
            it is not.
        """

        if state not in cls.allowed_states:
            return False

        return True

    @classmethod
    def validate_deconstruction_attributes(cls, attribut_list: list) -> bool:

        attributes_ok = True

        for attribute in attribut_list:
            if attribute not in cls.valid_deconst_attributes:
                attributes_ok = False

        return attributes_ok
