import configparser


def main():

    config = configparser.ConfigParser()
    config.read('config.cfg')

    print('This is the main program!')

if __name__ == "__main__":
    main()
