from django.shortcuts import render
#from django.db import connection
import pymysql.cursors
import json
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

    categories = [item["state"] for item in regions]
    values = [float(item["cnt"]) for item in regions]

    data = {
        'labels': categories,
        'datasets': [{
            'label': 'Value',
            'data': values,
            'backgroundColor':[
                'rgba(133, 190, 233, 1)'
            ],
            'borderColor':[
                'rgba(133, 190, 233, 1)'
            ],
            'borderWidth': 1
        }]
    }

    region_chart = json.dumps(data)

    # Query for latest reviews
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
        'region_chart': region_chart,
        'reviews': list(reviews),
    })

def customers(request):

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='ecommerce_data',
        cursorclass=pymysql.cursors.DictCursor
    )

    # average spend
    with connection.cursor() as cursor:
        query = 'SELECT c.customer_unique_id, AVG(p.payment_value) AS average_spend FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_payments p ON o.order_id = p.order_id GROUP BY c.customer_unique_id ORDER BY average_spend DESC;'
        cursor.execute(query)
        avg_spend = cursor.fetchone()

    spend = round(avg_spend["average_spend"], 2)

    # average orders per customer

    with connection.cursor() as cursor:
        query = 'SELECT AVG(order_count) AS avg_orders_per_customer FROM ( SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id ) AS customer_orders;'
        cursor.execute(query)
        opc = cursor.fetchone()

    order_pc = round(opc["avg_orders_per_customer"], 2)

    # number of repeat customers
    with connection.cursor() as cursor:
        query = 'SELECT c.customer_unique_id, COUNT(o.order_id) AS orders_count FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_unique_id HAVING orders_count > 1 ORDER BY orders_count DESC;'
        cursor.execute(query)
        mult_order = cursor.fetchone()

    # number of customers who left a review
    with connection.cursor() as cursor:
        query = 'SELECT COUNT(*) AS total_reviews FROM order_reviews;'
        cursor.execute(query)
        tot_reviews = cursor.fetchone()

    # average review score
    with connection.cursor() as cursor:
        query = 'SELECT AVG(review_score) AS average_review_score FROM order_reviews;'
        cursor.execute(query)
        rev_score = cursor.fetchone()

    avg_rev = round(rev_score["average_review_score"], 2)

    # spending categories pie chart

    with connection.cursor() as cursor:
        query = "SELECT spending_category, COUNT(*) AS number_of_customers FROM ( SELECT c.customer_unique_id, CASE WHEN SUM(p.payment_value) < 100 THEN 'Low Spenders' WHEN SUM(p.payment_value) BETWEEN 100 AND 500 THEN 'Moderate Spenders' ELSE 'High Spenders' END AS spending_category FROM customers c INNER JOIN orders o ON c.customer_id = o.customer_id INNER JOIN order_payments p ON o.order_id = p.order_id GROUP BY c.customer_unique_id ) AS spending_data GROUP BY spending_category;"
        cursor.execute(query)
        pie = cursor.fetchall()

    pie_cats = [item["spending_category"] for item in pie]
    pie_vals = [item["number_of_customers"] for item in pie]

    pie_data = {
        'labels': pie_cats,
        'datasets': [{
            'data': pie_vals,
            'backgroundColor': ['rgba(104, 198, 104)', 'rgba(123, 166, 180, 1)', 'rgba(255, 255, 50, 1)'],
            'borderColor': ['rgba(104, 198, 104)', 'rgba(123, 166, 180, 1)', 'rgba(255, 255, 50, 1)'],
            'borderWidth': 1
        }]
    }

    pie_chart = json.dumps(pie_data)

    # new customers per month

    with connection.cursor() as cursor:
        query = "SELECT DATE_FORMAT(order_purchase_timestamp, '%Y-%m') AS month, COUNT(DISTINCT customer_id) AS new_customers FROM orders GROUP BY month ORDER BY month;"
        cursor.execute(query)
        line = cursor.fetchall()

    line_cats = [item["month"] for item in line]
    line_vals = [item["new_customers"] for item in line]

    line_data = {
        'labels' : line_cats,
        'datasets' : [{
            'data' : line_vals,
            'fill': 'false',
            'borderColor': 'rgb(75, 192, 192)',
            'tension' : '0.1' 
        }]
    }

    line_plot = json.dumps(line_data)

    template='main/customers.html'
    return render(request, template, {
        'avg_spend' : spend,
        'order_pc' : order_pc,
        'mult_orders' : mult_order["orders_count"],
        'tot_revs' : tot_reviews["total_reviews"],
        'avg_rev' : avg_rev,
        'pie_chart' : pie_chart,
        'line_plot' : line_plot,
    })

def products(request):

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='ecommerce_data',
        cursorclass=pymysql.cursors.DictCursor
    )

    # catalog
    with connection.cursor() as cursor:
        query = "SELECT product_category_name, COUNT(*) AS total_products FROM product GROUP BY product_category_name ORDER BY total_products DESC LIMIT 10;"
        cursor.execute(query)
        catalog = cursor.fetchall()

    # best selling category
    with connection.cursor() as cursor:
        query = "SELECT p.product_category_name, COUNT(*) AS total_sales FROM order_items oi JOIN product p ON oi.product_id = p.product_id GROUP BY p.product_category_name ORDER BY total_sales DESC;"
        cursor.execute(query)
        prod_sales = cursor.fetchall()

    bar_cats = [item["product_category_name"] for item in prod_sales]
    bar_vals = [float(item["total_sales"]) for item in prod_sales]

    data = {
        'labels': bar_cats,
        'datasets': [{
            'label': 'Value',
            'data': bar_vals,
            'backgroundColor':[
                '#2196F3'
            ],
            'borderColor':[
                '#2196F3'
            ],
            'borderWidth': 1
        }]
    }

    bar_plot = json.dumps(data)

    with connection.cursor() as cursor:
        query = "SELECT DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS sales_month, SUM(p.payment_value) AS total_sales FROM orders o JOIN order_payments p ON o.order_id = p.order_id GROUP BY sales_month ORDER BY sales_month;"
        cursor.execute(query)
        line = cursor.fetchall()

    line_cats = [item["sales_month"] for item in line]
    line_vals = [item["total_sales"] for item in line]

    line_data = {
        'labels' : line_cats,
        'datasets' : [{
            'data' : line_vals,
            'fill': 'false',
            'borderColor': '#2196F3',
            'tension' : '0.1' 
        }]
    }

    line_plot = json.dumps(line_data)

    template='main/products.html'
    return render(request, template, {
        'catalog' : catalog,
        'bar_plot' : bar_plot,
        'line_plot' : line_plot,
    })

def orders(request):

    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='ecommerce_data',
        cursorclass=pymysql.cursors.DictCursor
    )

    # recent orders
    with connection.cursor() as cursor:
        query = "SELECT order_id, customer_id, order_purchase_timestamp AS dt, order_status AS state FROM orders WHERE order_status <> 'canceled' ORDER BY order_purchase_timestamp DESC LIMIT 5;"
        cursor.execute(query)
        order_list = cursor.fetchall()

    # orders by status pie chart

    with connection.cursor() as cursor:
        query = "SELECT order_status, COUNT(*) AS number_of_orders FROM orders GROUP BY order_status;"
        cursor.execute(query)
        status_cnt = cursor.fetchall()

    pie_cats = [item["order_status"] for item in status_cnt]
    pie_vals = [item["number_of_orders"] for item in status_cnt]

    pie_data = {
        'labels': pie_cats,
        'datasets': [{
            'data': pie_vals,
            'backgroundColor': ['#FFA500','#FF0000', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#00FF7F', '#00FF00'],
            'borderColor': ['#FFA500','#FF0000', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF', '#00FF7F', '#00FF00'],
            'borderWidth': 1
        }]
    }

    pie_data = json.dumps(pie_data)

    # average order delay line chart

    with connection.cursor() as cursor:
        query = "SELECT CONCAT(YEAR(order_purchase_timestamp), '-', QUARTER(order_purchase_timestamp)) AS quarter, AVG(TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_approved_at)) AS average_processing_time_hours FROM orders WHERE order_purchase_timestamp IS NOT NULL AND order_approved_at IS NOT NULL GROUP BY CONCAT(YEAR(order_purchase_timestamp), '-', QUARTER(order_purchase_timestamp)) ORDER BY CONCAT(YEAR(order_purchase_timestamp), '-', QUARTER(order_purchase_timestamp)) LIMIT 8 OFFSET 1;"
        cursor.execute(query)
        line = cursor.fetchall()

    line_cats = [item["quarter"] for item in line]
    line_vals = [float(item["average_processing_time_hours"]) for item in line]

    line_data = {
        'labels' : line_cats,
        'datasets' : [{
            'data' : line_vals,
            'fill': 'false',
            'borderColor': '#FF0000',
            'tension' : '0.1' 
        }]
    }

    line_data = json.dumps(line_data)

    template='main/orders.html'
    return render(request, template, {
        'order_list' : list(order_list),
        'pie_data' : pie_data,
        'line_data' : line_data,
    })
