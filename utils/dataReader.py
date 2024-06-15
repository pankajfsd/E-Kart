import os
import datetime
from utils import configReader


def get_file_list():
    incoming_folder = configReader.get_application_config('FILE_PATH')['incoming.file.path']
    today = configReader.get_today()
    incoming_file_path = f"{incoming_folder}/{today}"

    return incoming_file_path, os.listdir(path=f'{incoming_file_path}')


def read_orders_data(file):
    incoming_file_path, file_list = get_file_list()

    with open(file=f"{incoming_file_path}/{file}", mode='r') as f:
        # Read each record as string and prepare a list.
        return f.readlines()[1:]


def read_master_data():
    master_file_path = configReader.get_application_config('FILE_PATH')['master.file.path']
    # print(master_file_path)

    with open(f"{master_file_path}", mode='r') as f:
        return f.readlines()[1:]

# print(read_orders_data())
