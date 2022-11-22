import configparser
from dotenv import load_dotenv
from os import getenv
from services.csv_reader import CSVReader
from services.data_fetcher import DataFetcher as DF


def main():

    config = configparser.ConfigParser()
    config.read('src/config.cfg')
    load_dotenv()

    input_filepath = config['FILEPATHS']['input']
    mapping_filepath = config['FILEPATHS']['mapping']
    gl_fetch_settings = config['GITLAB']
    gl_fetch_settings['pat'] = getenv('GL_PAT')

    DF.fetch_data(gl_fetch_settings)

    lukija = CSVReader(mapping_filepath, input_filepath)

    lukija.transform_export_csv_to_import_csv()


if __name__ == "__main__":
    main()
