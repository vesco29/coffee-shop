import pandas
from ormar import Model
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import date

data_format = ('customer_since', 'birthdate', 'transaction_date')

def prepare_row(element, fields):
    row = dict()
    for el in element.keys():
        key = el.replace('-', '_')
        if key in fields and  key in data_format:
            date = pandas.to_datetime(element[el])
            row[key] = date
            if key == 'birthdate':
                row['birthday'] = f'{ date.month }-{ date.day }'
        elif key in fields:
            row[key] = element[el]

    if 'transaction_date' in row  and 'transaction_time' in row:
        row['transaction_datetime'] = pandas.to_datetime(f'{element["transaction_date"]} {element["transaction_time"]}')
    return row


async def get_birthday_customer(table: object):
    today = datetime.date.today()
    return await table.objects.filter(birthday=f'{today.month}-{today.day}').values(['customer_id', 'customer_first_name']) 


async def top_selling_products(year: int, sells: object):
    return []

async def last_order_per_customer(customer: object, sells: object):
    return []
    #today = datetime.date.today()
    #return await table.objects.filter(birthday=f'{today.month}-{today.day}').values(['customer_id', 'customer_first_name']) 


async def load_table(table: object, csv_file: str):
    fields = table.__fields__.keys()
    data_frame = pandas.read_csv(csv_file)
    data_dict = data_frame.to_dict(orient='records')
    for el in data_dict:
        new_el = prepare_row(el, fields)
        #await table.objects.get_or_create(**new_el)
        await table.objects.create(**new_el)
    