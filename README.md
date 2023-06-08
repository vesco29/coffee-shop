# Code Challenge for Data Engineers
Maria is a coffee shop owner who wants to know more about her company in order to
improve her sales.
She wants an application (web service) that will provide her the following information:
### Request 1: 
She wants to know if the customers who are visiting her shop today have their
birthday, because she wants to provide their coffee for free.

- Endpoint: `/customers/birthday`

- Response:
```
{
  "customers": [
    {
      "customer_id": 12345,
      "customer_first_name": "Joe Doe"
    }
  ]
}
```
***
### Request 2: 
She wants to know which are the top 10 selling products for a specific year. The
year will be provided by her.
- Endpoint: `/products/top-selling-products/{year}`
- Response:
```
{
  "products": [
    {
      "product_name": "Espresso Roast",
      "total_sales": 12345
    }
  ]
}
```
***
### Request 3:
 She wants to know which is the last order per customer in order to retarget
these customers using an email campaign.
- Endpoint: `/customers/last-order-per-customer`
- Response:
```
{
  "customers": [
    {
      "customer_id": 12345,
      "customer_email": "yyyyy@zzzzz.xx",
      "last_order_date": "2023-01-01"
    }
  ]
}
```
***
## TO-DOS:
1) Setup PostgreSQL (or MariaDB/MySQL), create the tables you need for the tasks
above and then ingest the data that you will find at the attached files. SQLAlchemy is
a good tool for this task.
2) The above queries should be performed using SQL queries and after you get the
results, you should serve them using FastAPI (or Flask).
3) Create the endpoints that will provide the results retrieved from the database.
4) Dockerise the service or at least provide us the requirements (requirements.txt file)
you needed to make the service running.
5) Create a README file that will explain to us how to run the service.
6) Push the code to the GitHub repo you are invited to.

### The following practices are more than welcome, but not mandatory:
- Tests
- Docstrings
- Type Hinting
- Logging
***