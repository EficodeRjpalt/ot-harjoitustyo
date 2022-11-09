import configparser


def main():

    config = configparser.ConfigParser()
    config.read('config.cfg')


if __name__ == "__main__":
    main()
