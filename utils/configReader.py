import configparser
import datetime


def get_today():
    return datetime.date.today().strftime("%Y%m%d")


def get_application_config(section):
    config = configparser.ConfigParser()
    config.read('config.ini')

    pathDict = {}

    for (key, value) in config.items(section):
        pathDict[key] = value

    return pathDict


def get_email_config(section):
    config = configparser.ConfigParser()
    config.read('config.ini')

    email_dict = {}

    for (key, value) in config.items(section):
        email_dict[key] = value

    return email_dict

# print(get_application_config('FILE_PATH'))
