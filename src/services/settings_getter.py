import csv
import configparser
from os import getenv
from dotenv import load_dotenv
from services.json_reader import JSONReader as jreader
from typesets.settings import SettingsValidator


class SettingsGetter():
    """Class for parsing the config.cfg configurations with ConfigParser.
    Provides separate functions for fetching http request settings,
    header mappings and deconstructable attributes.
    """

    load_dotenv()

    def __init__(self, config_filepath: str, config: configparser):
        """Init block.

        Args:
            config_filepath (str): Relative filepath to the config.cfg file.
            config (configparser): A configparser object.
        """
        self.config = config
        self.config.read(config_filepath)

    def get_http_request_settings(self) -> dict:
        """Function for parsing the config.cfg file and providing http
        request settings as adictioanry.

        Returns:
            dict: returns the parsed http request dictionary.
        """
        settings = dict(self.config['COMMON'])
        settings['pat'] = getenv('GL_PAT')
        settings['issue'] = dict(self.config['ISSUE'])
        settings['comment'] = dict(self.config['COMMENT'])
        settings['watcher'] = dict(self.config['WATCHER'])
        settings['endpoint'] = {}
        settings['endpoint']['project'] = self.create_endpoint('project')
        settings['endpoint']['group'] = self.create_endpoint('group')

        try:
            SettingsValidator.validate_http_settings(settings)
        except (TypeError, ValueError) as err:
            print('Please check out the error message and re-check your settings.')
            print(err)

        return settings

    def get_header_mappings(self) -> dict:
        """Function to read header mappings between GitLab and Jira
        issues. Reads the mappings' configuration file provided in the
        parsed configurations.

        Returns:
            dict: returns a flat dictionary containing the header mappings.
        """
        mappings = jreader.read_json_to_dict(
            self.config['FILEPATHS']['mapping'])

        return mappings

    def create_endpoint(self, scope_type: str) -> str:
        """Function to generate both group and project level issue fetching
        endpoitns from parsed configuration settings. Combines information
        form baseurl and scope type to construct the correct endpoint.

        Args:
            scope (str): Scope type provided as a string. Turns value
            'project' to project level entry point. Other values are treated
            as group level scope types.

        Returns:
            str: returns the constructed issue fetching entrypoint as a string.
        """

        base = self.config['COMMON']['baseURL']
        scope_id = self.config['COMMON']['scope_id']

        if scope_type == 'project':

            return base + self.config['ENDPOINTS']['project'] + scope_id + '/issues'

        return base + self.config['ENDPOINTS']['group'] + scope_id + '/issues'

    def get_deconstruction_attributes(self):
        """Function to fetch from config.cfg all the fields that are
        to be deconstructed and reconstructed into the final CSV file.

        Returns:
            Returns the deconstructed values as a list containing string
            objects.
        """
        deconst_attrs = self.config['DECONSTRUCT']['allowed'].split(',')

        return deconst_attrs

    def trim_and_lower_settings_input(self, settings: dict) -> None:
        """Fucntion to trim and lower provided input in the configuration
        file to make inputs case insensitive and immune to trailing
        whitespaces.

        Args:
            settings (dict): _description_
        """

    def get_csv_settings(self) -> dict:
        """Function to get settings for the CSVTool.

        Returns:
            dict: Returns a dict containing the target Jira project's
            information (project key) and a dictionary that specifies how
            to turn labels into issue fields and with what values.
        """

        return dict(self.config['JIRA'])

    def get_user_mappings(self) -> dict:
        """Function to fetch user mappings from a defined CSV file. The users
        are read into a flat dict of key-value pairs.

        Args:
            filepath (str): Filepath to the location of the user mapping
            CSV file.

        Returns:
            dict: Dict containing the key-value pairings of the defined
            users with user's full name as the key and email address as
            the value.
        """

        return_dict = {}

        filepath = self.config['FILEPATHS']['user_mappings']

        with open(filepath, 'r', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                return_dict[row['username']] = row['email']

        return return_dict

    def get_label_configs(self) -> dict:

        return jreader.read_json_to_dict(self.config['FILEPATHS']['label_configs'])
