import pandas
from ormar import Model
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import date

data_format = ('customer_since', 'birthdate', 'transaction_date')

def prepare_row(element: dict, fields: list) -> dict:
    """
    Prepare a row of data by converting dates to appropriate formats.

    Args:
        element (dict): The row of data.
        fields (list): List of field names.

    Returns:
        dict: The prepared row of data.
    """
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


async def get_birthday_customer(table: object) -> list:
    """
    Retrieve customers with birthdays matching the current date.

    Args:
        table (object): The customer table object.

    Returns:
        list: A list of dictionaries containing customer_id and customer_first_name.
    """
    today = datetime.date.today()
    return await table.objects.filter(birthday=f'{today.month}-{today.day}').values(['customer_id', 'customer_first_name']) 


async def top_selling_products(year: int, engine: object) -> list:
    """
    Retrieve the top-selling products for a specific year.

    Args:
        year (int): The year to filter the sales.
        engine (object): The database engine object.

    Returns:
        list: A list of dictionaries containing product_name and total_sales.
    """
    column_names = ("product_name", "total_sales")
    sql_query  = f'''SELECT p.product, SUM(sr.quantity) AS total_quantity
                    FROM sales_reciepts sr
                    JOIN product p ON sr.product_id = p.product_id
                    WHERE EXTRACT(YEAR FROM sr.transaction_date) = {year}
                    GROUP BY  p.product
                    ORDER BY total_quantity DESC
                    LIMIT 10;
                        '''
    selected = engine.execute(sql_query)
    result = [{column_names[0]: row[0], column_names[1]: row[1]} for row in selected]
    selected.close()
    return result

async def last_order_per_customer(engine: object) -> list:
    """
    Retrieve the last order (based on transaction_date) for each customer.

    Args:
        engine (object): The database engine object.

    Returns:
        list: A list of dictionaries containing customer_id, customer_email, and last_order_date.
    """
    column_names = ("customer_id", "customer_email", "last_order_date")
    sql_query  = '''SELECT DISTINCT s.customer_id,c.customer_email, s.transaction_date
                    FROM sales_reciepts s
                    JOIN (
                        SELECT customer_id, MAX(transaction_datetime) AS max_datetime
                        FROM sales_reciepts
                        GROUP BY customer_id
                    ) t ON s.customer_id = t.customer_id AND s.transaction_datetime = t.max_datetime
                    JOIN customers c ON s.customer_id = c.customer_id
                    ORDER BY s.customer_id;
                        '''
    selected = engine.execute(sql_query)
    result = [{column_names[0]: row[0], column_names[1]: row[1], column_names[2]: row[2]} for row in selected]    
    selected.close()
    return result

async def load_table(table: object, csv_file: str) -> None:
    """
    Load data from a CSV file into a table.

    Args:
        table (object): The table object to load the data into.
        csv_file (str): The path to the CSV file.

    Returns:
        None
    """
    fields = table.__fields__.keys()
    data_frame = pandas.read_csv(csv_file)
    data_dict = data_frame.to_dict(orient='records')
    for el in data_dict:
        new_el = prepare_row(el, fields)
        #await table.objects.get_or_create(**new_el)
        await table.objects.create(**new_el)
    