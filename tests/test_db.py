import os
import sys
import unittest
from unittest.mock import patch
from pydantic import BaseSettings, Field
import sqlalchemy
import datetime
from datetime import date
from sqlalchemy_utils import database_exists, create_database, drop_database

HOME = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(HOME,'..')))


POSTGRES_USER = 'fastapi'
POSTGRES_PASSWORD = 'fastapi'
POSTGRES_DB = 'fastapi_test'
DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@0.0.0.0:5432/{POSTGRES_DB}'
#DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}'
os.environ["DATABASE_URL"] = DATABASE_URL

engine = sqlalchemy.create_engine(DATABASE_URL)
if database_exists(engine.url):
    drop_database(engine.url)
create_database(engine.url)

from app.common import get_birthday_customer, load_table, top_selling_products, last_order_per_customer
import app.db as db

class TestingDBLoad(unittest.IsolatedAsyncioTestCase):

    async def startup(self):
        if not db.database.is_connected:
            await db.database.connect()


    async def shutdown(self):
        if db.database.is_connected:
            await db.database.disconnect()

    @classmethod
    def setUpClass(cls) -> None:
        if database_exists(engine.url):
            drop_database(engine.url)
        create_database(engine.url)
        db.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls) -> None:
        pass
        if database_exists(engine.url):
            drop_database(engine.url)

    def setUp(self) -> None:
        self.maxDiff = None
        self.testdata = os.path.join(HOME, 'testdata')
    
    def tearDown(self) -> None:
        pass
        #self.shutdown()

    async def test_load_Customer(self):
        await self.startup()
        customer = os.path.join(self.testdata, 'customer.csv')
        await load_table(db.Customer, csv_file=customer)
        
        available = await db.Customer.objects.all()
        await self.shutdown()
        available = [dict(row)  for row in available]
        self.assertListEqual(available, 
                            [{'customer_id': 1, 'home_store': 3, 'customer_first_name': 'Kelly Key', 'customer_email': 'Venus@adipiscing.edu', 'customer_since': datetime.date(2017, 1, 4), 'loyalty_card_number': '908-424-2890', 'birthdate': datetime.date(1950, 5, 29), 'birthday': '5-29', 'gender': 'M', 'birth_year': 1950}, 
                             {'customer_id': 2, 'home_store': 3, 'customer_first_name': 'Clark Schroeder', 'customer_email': 'Nora@fames.gov', 'customer_since': datetime.date(2017, 1, 7), 'loyalty_card_number': '032-732-6308', 'birthdate': datetime.date(1950, 7, 30), 'birthday': '7-30', 'gender': 'M', 'birth_year': 1950}, 
                             {'customer_id': 3, 'home_store': 3, 'customer_first_name': 'Elvis Cardenas', 'customer_email': 'Brianna@tellus.edu', 'customer_since': datetime.date(2017, 1, 10), 'loyalty_card_number': '459-375-9187', 'birthdate': datetime.date(1950, 9, 30), 'birthday': '9-30', 'gender': 'M', 'birth_year': 1950}, 
                             {'customer_id': 4, 'home_store': 3, 'customer_first_name': 'Rafael Estes', 'customer_email': 'Ina@non.gov', 'customer_since': datetime.date(2017, 1, 13), 'loyalty_card_number': '576-640-9226', 'birthdate': datetime.date(1950, 12, 1), 'birthday': '12-1', 'gender': 'M', 'birth_year': 1950}, 
                             {'customer_id': 5, 'home_store': 3, 'customer_first_name': 'Colin Lynn', 'customer_email': 'Dale@Integer.com', 'customer_since': datetime.date(2017, 1, 15), 'loyalty_card_number': '344-674-6569', 'birthdate': datetime.date(1951, 2, 1), 'birthday': '2-1', 'gender': 'M', 'birth_year': 1951}])


    @patch('datetime.date') 
    async def test_today_Customer(self, mock_date):
        mock_date.today.return_value = date(2023, 12, 1)
        await self.startup()
        customer = os.path.join(self.testdata, 'customer.csv')
        await db.Customer.objects.delete(each=True)
        await load_table(db.Customer, csv_file=customer)
        
        available = await get_birthday_customer(db.Customer)

        await self.shutdown()
        available = [dict(row)  for row in available]

        self.assertListEqual(available, 
                             [{'customer_id': 4, 'customer_first_name': 'Rafael Estes' }])
    
    async def test_load_seles(self):
        await self.startup()
        sales_reciepts = os.path.join(self.testdata, 'sales_reciepts.csv')
        await load_table(db.Sales, csv_file=sales_reciepts)
        
        available = await db.Sales.objects.all()
        await self.shutdown()
        available = [dict(row)  for row in available]
        self.assertListEqual(available, 
                           [{'transaction_id': 1,'id': 1, 'transaction_date': datetime.date(2019, 3, 1), 'transaction_time': datetime.time(12, 4, 43), 'transaction_datetime': datetime.datetime(2019, 3, 1, 12, 4, 43), 'sales_outlet_id': 3, 'staff_id': 12, 'customer_id': 1, 'instore_yn': 'N', 'order': 1, 'line_item_id': 1, 'product_id': 1, 'quantity': 1, 'line_item_amount': 2.5, 'unit_price': 2.5, 'promo_item_yn': 'N'}, 
                            {'transaction_id': 2, 'id': 2,'transaction_date': datetime.date(2019, 4, 1), 'transaction_time': datetime.time(15, 54, 39), 'transaction_datetime': datetime.datetime(2019, 4, 1, 15, 54, 39), 'sales_outlet_id': 3, 'staff_id': 17, 'customer_id': 2, 'instore_yn': 'N', 'order': 1, 'line_item_id': 1, 'product_id': 1, 'quantity': 2, 'line_item_amount': 7.0, 'unit_price': 3.5, 'promo_item_yn': 'N'}, 
                            {'transaction_id': 3, 'id': 3,'transaction_date': datetime.date(2019, 6, 1), 'transaction_time': datetime.time(14, 34, 59), 'transaction_datetime': datetime.datetime(2019, 6, 1, 14, 34, 59), 'sales_outlet_id': 3, 'staff_id': 17, 'customer_id': 3, 'instore_yn': 'Y', 'order': 1, 'line_item_id': 1, 'product_id': 2, 'quantity': 2, 'line_item_amount': 5.0, 'unit_price': 2.5, 'promo_item_yn': 'N'}, 
                            {'transaction_id': 4, 'id': 4,'transaction_date': datetime.date(2019, 4, 1), 'transaction_time': datetime.time(16, 6, 4), 'transaction_datetime': datetime.datetime(2019, 4, 1, 16, 6, 4), 'sales_outlet_id': 3, 'staff_id': 12, 'customer_id': 4, 'instore_yn': 'N', 'order': 1, 'line_item_id': 1, 'product_id': 3, 'quantity': 2, 'line_item_amount': 5.0, 'unit_price': 2.5, 'promo_item_yn': 'N'}, 
                            {'transaction_id': 5, 'id': 5,'transaction_date': datetime.date(2019, 4, 1), 'transaction_time': datetime.time(16, 18, 37), 'transaction_datetime': datetime.datetime(2019, 4, 1, 16, 18, 37), 'sales_outlet_id': 3, 'staff_id': 17, 'customer_id': 5, 'instore_yn': 'Y', 'order': 1, 'line_item_id': 1, 'product_id': 4, 'quantity': 1, 'line_item_amount': 2.45, 'unit_price': 2.45, 'promo_item_yn': 'N'}, 
                            {'transaction_id': 6,'id': 6, 'transaction_date': datetime.date(2019, 4, 1), 'transaction_time': datetime.time(18, 54, 46), 'transaction_datetime': datetime.datetime(2019, 4, 1, 18, 54, 46), 'sales_outlet_id': 3, 'staff_id': 17, 'customer_id': 6, 'instore_yn': 'Y', 'order': 1, 'line_item_id': 1, 'product_id': 5, 'quantity': 1, 'line_item_amount': 3.0, 'unit_price': 3.0, 'promo_item_yn': 'N'}])
    
    
    async def test_load_product(self):
        await self.startup()
        product = os.path.join(self.testdata, 'product.csv')
        await load_table(db.Product, csv_file=product)
        
        available = await db.Product.objects.all()
        await self.shutdown()
        available = [dict(row)  for row in available]
        self.assertListEqual(available, 
                           [{'product_id': 1, 'product_group': 'Whole Bean/Teas', 'product_category': 'Coffee beans', 'product_type': 'Organic Beans', 'product': 'Brazilian - Organic', 'product_description': "It's like Carnival in a cup. Clean and smooth.", 'unit_of_measure': '12 oz', 'current_wholesale_price': 14.4, 'current_retail_price': '$18.00 ', 'tax_exempt_yn': 'Y', 'promo_yn': 'N', 'new_product_yn': 'N'},
                            {'product_id': 2, 'product_group': 'Whole Bean/Teas', 'product_category': 'Coffee beans', 'product_type': 'House blend Beans', 'product': 'Our Old Time Diner Blend', 'product_description': 'Out packed blend of beans that is reminiscent of the cup of coffee you used to get at a diner. ', 'unit_of_measure': '12 oz', 'current_wholesale_price': 14.4, 'current_retail_price': '$18.00 ', 'tax_exempt_yn': 'Y', 'promo_yn': 'N', 'new_product_yn': 'N'}, 
                            {'product_id': 3, 'product_group': 'Whole Bean/Teas', 'product_category': 'Coffee beans', 'product_type': 'Espresso Beans', 'product': 'Espresso Roast', 'product_description': 'Our house blend for a good espresso shot.', 'unit_of_measure': '1 lb', 'current_wholesale_price': 11.8, 'current_retail_price': '$14.75 ', 'tax_exempt_yn': 'Y', 'promo_yn': 'N', 'new_product_yn': 'N'}, 
                            {'product_id': 4, 'product_group': 'Whole Bean/Teas', 'product_category': 'Coffee beans', 'product_type': 'Espresso Beans', 'product': 'Primo Espresso Roast', 'product_description': 'Our primium single source of hand roasted beans.', 'unit_of_measure': '1 lb', 'current_wholesale_price': 16.36, 'current_retail_price': '$20.45 ', 'tax_exempt_yn': 'Y', 'promo_yn': 'N', 'new_product_yn': 'N'},
                            {'product_id': 5, 'product_group': 'Whole Bean/Teas', 'product_category': 'Coffee beans', 'product_type': 'Gourmet Beans', 'product': 'Columbian Medium Roast', 'product_description': 'A smooth cup of coffee any time of day. ', 'unit_of_measure': '1 lb', 'current_wholesale_price': 12.0, 'current_retail_price': '$15.00 ', 'tax_exempt_yn': 'Y', 'promo_yn': 'N', 'new_product_yn': 'N'}, 
                            {'product_id': 6, 'product_group': 'Whole Bean/Teas', 'product_category': 'Coffee beans', 'product_type': 'Gourmet Beans', 'product': 'Ethiopia', 'product_description': 'From the home of coffee.', 'unit_of_measure': '1 lb', 'current_wholesale_price': 16.8, 'current_retail_price': '$21.00 ', 'tax_exempt_yn': 'Y', 'promo_yn': 'N', 'new_product_yn': 'N'}])


    async def test_select_seles(self):
        await self.startup()
        sales_reciepts = os.path.join(self.testdata, 'sales_reciepts.csv')
        await load_table(db.Sales, csv_file=sales_reciepts)
        
        available = await top_selling_products(2019, engine=engine)
        await self.shutdown()
        self.assertListEqual(available, 
                             [{'product_name': 'Brazilian - Organic', 'total_sales': 6}, 
                              {'product_name': 'Espresso Roast', 'total_sales': 4}, 
                              {'product_name': 'Our Old Time Diner Blend', 'total_sales': 4}, 
                              {'product_name': 'Columbian Medium Roast', 'total_sales': 2}, 
                              {'product_name': 'Primo Espresso Roast', 'total_sales': 2}])
    

    async def test_last_order_per_customer(self):
        await self.startup()
        sales_reciepts = os.path.join(self.testdata, 'sales_reciepts.csv')
        #await load_table(db.Sales, csv_file=sales_reciepts)
        
        available = await last_order_per_customer(engine=engine)

        await self.shutdown()
        self.assertListEqual(available, 
                             [{'product_name': 'Brazilian - Organic', 'total_sales': 6}, 
                              {'product_name': 'Espresso Roast', 'total_sales': 4}, 
                              {'product_name': 'Our Old Time Diner Blend', 'total_sales': 4}, 
                              {'product_name': 'Columbian Medium Roast', 'total_sales': 2}, 
                              {'product_name': 'Primo Espresso Roast', 'total_sales': 2}])
    



if __name__ == '__main__':
    unittest.main()