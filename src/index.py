import configparser
from services.csv_reader import CSVReader


def main():

    config = configparser.ConfigParser()
    config.read('src/config.cfg')

    input_filepath = config['FILEPATHS']['input']
    mapping_filepath = config['FILEPATHS']['mapping']

    lukija = CSVReader(mapping_filepath, input_filepath)

    lukija.transform_export_csv_to_import_csv()


if __name__ == "__main__":
    main()
