import configparser
from os import getenv
from dotenv import load_dotenv
from services.csv_services import CSVTool as csvtool
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
    gl_note_fetch_settings = config['NOTES']
    gl_note_fetch_settings['pat'] = getenv('GL_PAT')

    scope_data = DF.fetch_data(gl_fetch_settings, data_type='issue')

    filtered_scope_data = f.format_response_data_to_dict(scope_data)

    issue_dict_list = f.transform_dict_items_into_issues(filtered_scope_data)

    f.add_comments_to_all_issues(issue_dict_list, gl_note_fetch_settings)

    csvtool.write_issues_to_csv(issue_dict_list, 'pandas_output.csv', mappings)


if __name__ == "__main__":
    main()

# 2-do
# Siisti CSV-lukijan rakenne: sen ei tarvitse olla tilallinen.
# Linttaus 100%
# Testit kuntoon kaikelle
# Docstringit