import configparser
from pprint import pprint
from os import getenv
from dotenv import load_dotenv
from services.csv_services import CSVReader as csvtool
from services.data_fetcher import DataFetcher as DF
from services.formatter import Formatter as f
from services.json_reader import JSONReader as jreader


def main():

    config = configparser.ConfigParser()
    config.read('src/config.cfg')
    load_dotenv()
    mappings = jreader.read_json_to_dict(config['FILEPATHS']['mapping'])

    #input_filepath = config['FILEPATHS']['input']
    gl_fetch_settings = config['GITLAB']
    gl_fetch_settings['pat'] = getenv('GL_PAT')

    scope_data = DF.fetch_data(gl_fetch_settings)

    filtered_scope_data = f.format_response_data_to_dict(scope_data)

    issue_dict = f.transform_dict_items_into_issues(filtered_scope_data)

    csvtool.write_issues_to_csv(issue_dict, 'api_output.csv', mappings)


if __name__ == "__main__":
    main()
