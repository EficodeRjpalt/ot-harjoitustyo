import configparser
from services.csv_reader import CSVReader


def main():

    config = configparser.ConfigParser()
    config.read('src/config.cfg')

    input_filepath = config['FILEPATHS']['input']
    mapping_filepath = config['FILEPATHS']['mapping']

    lukija = CSVReader(mapping_filepath, input_filepath)

    dicts = lukija.read_csv_to_dict()
    lista = lukija.transform_dict_items_into_issues(dicts)
    for item in lista:
        item.displaynames_to_emails('eficode.com')
        item.timestamps_to_jira()
        print(item.issue_to_dict())


if __name__ == "__main__":
    main()

####
# 2 Do
# - Koodin refaktorointi
# - Testit koko tähän mennessä luodulle koodille
