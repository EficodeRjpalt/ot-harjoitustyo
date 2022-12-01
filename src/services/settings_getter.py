import configparser
from os import getenv
from dotenv import load_dotenv
from services.json_reader import JSONReader as jreader


class SettingsGetter():

    load_dotenv()

    def __init__(self, config_filepath: str, config: configparser):
        self.config = config
        self.config.read(config_filepath)

    def get_http_request_settings(self):
        settings = dict(self.config['COMMON'])
        settings['pat'] = getenv('GL_PAT')
        settings['issue'] = dict(self.config['ISSUE'])
        settings['comment'] = dict(self.config['COMMENT'])
        settings['watcher'] = dict(self.config['WATCHER'])
        settings['endpoint'] = {}
        settings['endpoint']['project'] = self.create_endpoint('project')
        settings['endpoint']['group'] = self.create_endpoint('group')

        return settings

    def get_header_mappings(self):
        mappings = jreader.read_json_to_dict(
            self.config['FILEPATHS']['mapping'])

        return mappings

    def create_endpoint(self, scope: str) -> str:

        base = self.config['COMMON']['baseURL']
        scope_id = self.config['COMMON']['scope_id']

        if scope == 'project':

            return base + self.config['ENDPOINTS']['project'] + scope_id + '/issues'

        return base + self.config['ENDPOINTS']['group'] + scope_id + '/issues'

    def get_deconstruction_attributes(self):
        deconst_attrs = self.config['DECONSTRUCT']['allowed'].split(',')

        return deconst_attrs
