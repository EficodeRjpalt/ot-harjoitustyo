import configparser

def main():

    config = configparser.ConfigParser()
    config.read('config.cfg')

    print(config['mapping']['title'])

if __name__ == "__main__":
    main()