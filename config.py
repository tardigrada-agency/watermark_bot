import configparser

config = configparser.ConfigParser()
config.read("configuration.ini")


def get(s: str):
    """
    Получаем конфиг для s
    :param s:
    :return:
    """
    return config[s]
