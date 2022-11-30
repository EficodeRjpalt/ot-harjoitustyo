import configparser
from os import getenv
from dotenv import load_dotenv
from services.json_reader import JSONReader as jreader

class SettingsGetter():

    load_dotenv()

    def __init__(self, config_filepath: str):
        self.config_filepath = config_filepath
        self.config = configparser.ConfigParser()
        self.config.read('src/config.cfg')

    def get_http_request_settings(self):
        settings = dict(self.config['COMMON'])
        settings['pat'] = getenv('GL_PAT')
        settings['issue'] = dict(self.config['ISSUE'])
        settings['comment'] = dict(self.config['COMMENT'])
        settings['watcher'] = dict(self.config['WATCHER'])

        return settings

    def get_header_mappings(self):
        mappings = jreader.read_json_to_dict(self.config['FILEPATHS']['mapping'])

        return mappings

    def get_deconstruction_attributes(self):
        deconst_attrs = self.config['DECONSTRUCT']['allowed'].split(',')

        return deconst_attrs