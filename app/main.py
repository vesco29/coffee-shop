# # app/main.py
from fastapi import FastAPI
import os
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from sqlalchemy_utils import database_exists, create_database, drop_database

from app.db import database, engine, metadata, Customer, Sales, Product
from app.common import load_table, get_birthday_customer, last_order_per_customer, top_selling_products


HOME = os.path.abspath(os.path.dirname(__file__))


app = FastAPI(title="Coffee shop - FastAPI and Docker")

@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple greeting message.

    Returns:
        dict: A dictionary with a "hello" key and "world" value.
    """
    return {"hello": "world"}


@app.get("/customers/birthday")
async def read_birthday():
    """
    API endpoint to retrieve customers with birthdays today.

    Returns:
        JSONResponse: A JSON response containing the customer information.
    """
    birthday = await get_birthday_customer(Customer)
    customer_dict = {'customer': birthday } 
    content = jsonable_encoder(customer_dict)
    return JSONResponse(content=content)

@app.get("/products/top-selling-products/{year}")
async def read_last_order(year: int):
    """
    API endpoint to retrieve the top selling products for a specific year.

    Args:
        year (int): The year to filter the sales receipts.

    Returns:
        JSONResponse: A JSON response containing the top selling products.
    """
    products = await top_selling_products(year, engine)
    customer_dict = {'products': products} 
    content = jsonable_encoder(customer_dict)
    return JSONResponse(content=content)


@app.get("/customers/last-order-per-customer")
async def read_last_order():
    """
    API endpoint to retrieve the last order per customer.

    Returns:
        JSONResponse: A JSON response containing the customer's last order information.
    """
    last_order = await last_order_per_customer(engine)
    customers = {'customers': last_order } 
    content = jsonable_encoder(customers)
    return JSONResponse(content=content)


@app.on_event("startup")
async def startup():
    """
    Event function that runs on application startup.

    It establishes a connection to the database and loads the table data.
    """
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await load_table(Customer, csv_file=os.path.join(HOME,'..', 'dataset', 'customer.csv'))
    await load_table(Product, csv_file=os.path.join(HOME,'..', 'dataset', 'product.csv'))
    await load_table(Sales, csv_file=os.path.join(HOME,'..', 'dataset', 'sales_reciepts.csv'))
    


@app.on_event("shutdown")
async def shutdown():
    """
    Event function that runs on application shutdown.

    It disconnects from the database.
    """
    if database.is_connected:
        await database.disconnect()