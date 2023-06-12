# app/db.py

import databases
import ormar
import sqlalchemy
from ormar import String, Integer, Date, Time
from sqlalchemy_utils import database_exists, create_database, drop_database

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Customer(ormar.Model):
    """
    Model representing the customers table.

    Attributes:
        customer_id (int): The unique identifier for the customer (primary key).
        home_store (int): The identifier of the customer's home store.
        customer_first_name (str): The first name of the customer.
        customer_email (str): The email address of the customer.
        customer_since (datetime.date): The date when the customer started.
        loyalty_card_number (str): The loyalty card number of the customer.
        birthdate (datetime.date): The birthdate of the customer.
        birthday (str): The formatted birthday of the customer.
        gender (str): The gender of the customer.
        birth_year (int): The birth year of the customer.
    """
    class Meta(BaseMeta):
        tablename = 'customers'

    customer_id = ormar.Integer(primary_key=True)
    home_store = ormar.Integer()
    customer_first_name = ormar.String(max_length=50)
    customer_email = ormar.String(max_length=100)
    customer_since = ormar.Date()
    loyalty_card_number = ormar.String(max_length=50)
    birthdate = ormar.Date()
    birthday = ormar.String(max_length=50)
    gender = ormar.String(max_length=1, default='N')
    birth_year = ormar.Integer()


class Sales(ormar.Model):
    """
    Model representing the sales_reciepts table.

    Attributes:
        id (int): The unique identifier for the sales receipt (primary key).
        transaction_id (int): The identifier for the transaction.
        transaction_date (datetime.date): The date of the transaction.
        transaction_time (datetime.time): The time of the transaction.
        transaction_datetime (datetime.datetime): The combined date and time of the transaction.
        sales_outlet_id (int): The identifier for the sales outlet.
        staff_id (int): The identifier for the staff.
        customer_id (int): The identifier for the customer.
        instore_yn (str): Indicator whether the transaction occurred in-store or not.
        order (int): The order of the line item.
        line_item_id (int): The identifier for the line item.
        product_id (int): The identifier for the product.
        quantity (int): The quantity of the product sold.
        line_item_amount (float): The amount of the line item.
        unit_price (float): The unit price of the product.
        promo_item_yn (str): Indicator whether the product is a promotional item or not.
    """
    class Meta(BaseMeta):
        tablename = 'sales_reciepts'

    id = ormar.Integer(primary_key=True)
    transaction_id = ormar.Integer()
    transaction_date = ormar.Date()
    transaction_time = ormar.Time()
    transaction_datetime = ormar.DateTime()
    sales_outlet_id = ormar.Integer()
    staff_id = ormar.Integer()
    customer_id = ormar.Integer()
    instore_yn = ormar.String(max_length=1, default='N')
    order = ormar.Integer()
    line_item_id = ormar.Integer()
    product_id = ormar.Integer()
    quantity = ormar.Integer()
    line_item_amount = ormar.Float()
    unit_price = ormar.Float()
    promo_item_yn =ormar.String(max_length=1, default='N')


class Product(ormar.Model):
    """
    Model representing the product table.

    Attributes:
        product_id (int): The unique identifier for the product (primary key).
        product_group (str): The group of the product.
        product_category (str): The category of the product.
        product_type (str): The type of the product.
        product (str): The name of the product.
        product_description (str): The description of the product.
        unit_of_measure (str): The unit of measure for the product.
        current_wholesale_price (float): The current wholesale price of the product.
        current_retail_price (str): The current retail price of the product.
        tax_exempt_yn (str): Indicator whether the product is tax-exempt or not.
        promo_yn (str): Indicator whether the product is a promotional item or not.
        new_product_yn (str): Indicator whether the product is a new product or not.
    """
    class Meta(BaseMeta):
        tablename = 'product'

    product_id = ormar.Integer(primary_key=True)
    product_group = ormar.String(max_length=100)
    product_category = ormar.String(max_length=100)
    product_type = ormar.String(max_length=100)
    product = ormar.String(max_length=100)
    product_description = ormar.String(max_length=100)
    unit_of_measure = ormar.String(max_length=20)
    current_wholesale_price = ormar.Float()
    current_retail_price = ormar.String(max_length=20)
    tax_exempt_yn = ormar.String(max_length=1, default='N')
    promo_yn = ormar.String(max_length=1, default='N')
    new_product_yn = ormar.String(max_length=1, default='N')



engine = sqlalchemy.create_engine(settings.db_url)
if database_exists(engine.url):
    drop_database(engine.url)
create_database(engine.url)

metadata.create_all(engine)
