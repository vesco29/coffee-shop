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
## TO-DO:
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
## To run the service using Docker, follow these steps:

1) Clone the repository to your local machine.  
2) Open a terminal or command prompt and navigate to the cloned repository.  
3) Run the following command to build and run the Docker containers:  
```
docker compose up --build
```
  This will build the Docker images and start the containers.  

Once the service is running, you can access the following endpoints:

- Documentation: [Docs](http://127.0.0.1:8008/docs)  
This link will take you to the API documentation where you can explore the available endpoints and make test requests.

- Endpoint 1: [Customers Birthday](http://127.0.0.1:8008/customers/birthday)  
This link will retrieve the customers who have a birthday today.

- Endpoint 2: [Top Selling Products](http://127.0.0.1:8008/products/top-selling-products/2019)    
This link will retrieve the top-selling products for the year 2019.

- Endpoint 3: [Last Order per Customer](http://127.0.0.1:8008/customers/last-order-per-customer)   
This link will retrieve the last order per customer.

Click on the provided links to access the respective endpoints and view the results.

