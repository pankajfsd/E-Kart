from utils import dataReader
import datetime


def get_product_master_dict():
    master_data = dataReader.read_master_data()
    product_list = []  # Create an empty list to store dictionaries for each record

    for record in master_data:
        record_data = record.split(',')
        product_dict = {
            'product_id': record_data[0],
            'product_name': record_data[1],
            'price': record_data[2],
            'category': record_data[3]
        }
        product_list.append(product_dict)  # Append the dictionary to the list

    return product_list


def get_product_price_dict():
    master_data = dataReader.read_master_data()
    prod_price_dict = {}

    for record in master_data:
        prod_price_dict[record.split(',')[0]] = record.split(',')[2]

    return prod_price_dict


def get_prod_ids():
    master_data = dataReader.read_master_data()
    prod_ids = []
    for record in master_data:
        prod_ids.append(record.split(',')[0])

    return prod_ids


def validate_prod_id(order_prod_id, prod_ids):
    if order_prod_id in prod_ids:
        return True
    return False


def validate_sales(order_product_id, sales, qty):
    prod_price_dict = get_product_price_dict()

    if order_product_id in prod_price_dict.keys():
        return int(prod_price_dict[order_product_id]) * int(qty) == int(sales)

    return False


def validate_order_date(order_date):
    dt = datetime.datetime.strptime(order_date, '%Y-%m-%d').date()
    today_date = datetime.date.today()
    delta = (today_date - dt).days
    if delta >= 0:
        return True
    return False


def validate_city(city):
    if city in ['Mumbai', 'Bangalore']:
        return True
    return False


def validate_emptiness(order):
    empty_cols = []
    for (key, val) in order.items():
        # Check if the value is falsy (None, '', 0, etc.)
        if not order[key] or order[key] == '':
            empty_cols.append(key)
    return empty_cols
