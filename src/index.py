import configparser

def main():

    config = configparser.ConfigParser()
    config.read('config.cfg')

    print(config['DEFAULT']['test'])

if __name__ == "__main__":
    main()