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
