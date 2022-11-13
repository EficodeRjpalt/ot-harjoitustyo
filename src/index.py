import configparser
from services.csv_reader import CSVReader

def main():

    config = configparser.ConfigParser()
    config.read('config.cfg')

    print('This is the main program!')

    lukija = CSVReader('src/resources/mapping.json', 'src/resources/sample.csv')

    lukija.transform_export_csv_to_import_csv()

if __name__ == "__main__":
    main()
