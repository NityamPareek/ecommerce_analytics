from django.shortcuts import render
#from django.db import connection
import pymysql.cursors
# Create your views here.

def index(request):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='ecommerce_data',
        cursorclass=pymysql.cursors.DictCursor
    )

    # Query for top_stats
    with connection.cursor() as cursor:
        query = 'SELECT COUNT(DISTINCT seller_id) as num_sellers from sellers'
        cursor.execute(query)
        num_sellers = cursor.fetchone()

    with connection.cursor() as cursor:
        query = 'SELECT COUNT(DISTINCT customer_unique_id) as num_customers from customers'
        cursor.execute(query)
        num_customers = cursor.fetchone()

    with connection.cursor() as cursor:
        query = 'SELECT COUNT(DISTINCT product_id) as num_products from product'
        cursor.execute(query)
        num_products = cursor.fetchone()

    with connection.cursor() as cursor:
        query = 'SELECT COUNT(DISTINCT order_id) as num_orders from orders'
        cursor.execute(query)
        num_orders = cursor.fetchone()

    # Query for order_by_state
    with connection.cursor() as cursor:
        query = 'SELECT geolocation_state AS state, COUNT(geolocation_state)/ (SELECT COUNT(geolocation_state) FROM geolocation)*100 AS cnt FROM geolocation GROUP BY geolocation_state ORDER BY cnt DESC LIMIT 7'
        cursor.execute(query)
        regions = cursor.fetchall()

    with connection.cursor() as cursor:
        query = 'select order_id as id, review_score as score, review_answer_timestamp as dt, review_comment_message as msg from order_reviews where char_length(review_comment_message) >=1 order by review_answer_timestamp desc limit 2'
        cursor.execute(query)
        reviews = cursor.fetchall()

    connection.close()

    template = "main/index.html"
    return render(request, template, {
        'num_sellers': num_sellers,
        'num_orders': num_orders,
        'num_products': num_products,
        'num_customers': num_customers,
        'regions': regions,
        'reviews': list(reviews),
    })

def customers(request):
    template='main/customers.html'
    return render(request, template)
