import psycopg2
import streamlit as st
import pandas as pd

client = psycopg2.connect(host='localhost',
                          user="postgres",
                          password="postgre_password",
                          port=5432,
                          database="retail_data")

db = client.cursor()

#st.sidebar.image("C:/Users/Dell/Downloads/images.png.png", caption="Retail Insights", width=200)
#st.sidebar.image("st.sidebar.image("C:/Users/Dell/Downloads/images.png", width=100)
#st.sidebar.image("C:/Users/Dell/Downloads/df_img.png", width=100)
page = st.sidebar.selectbox("Navigate through the sections below to explore",["About","Retail data Order Analysis"])
if page=="About":
    st.write('# **Retail Data Order Analysis**')
    st.subheader(" Objective:")
    st.write("""To analyze and optimize sales performance by uncovering actionable insights, 
             such as top-performing products, revenue trends, and growth opportunities, 
             using real-world retail order data.""")
    st.subheader("Key Deliverables:")
    st.markdown(
    """
    - Data insights through 20 SQL queries to answer key business questions.
    - An interactive Streamlit dashboard for visualizing data trends in real-time.
    - Cleaned, structured data stored in SQL Server for efficient querying.
    """)
    st.subheader("Tools & Technologies Used:")
    st.markdown(
    """ 
    - Data Extraction: Kaggle API, Python
    - Cleaning: Pandas library in Python
    - Data Storage: SQL Server (Relational database -using PostgreSQL)
    - Data Analysis: SQL queries
    - Data Visualization: Streamlit
    """)
elif page=="Retail data Order Analysis":
    st.write('## **Retail Data Order Analysis**')
    st.write('### Queries')
    q1=['Select a question to view the dataframe',
        'Find top 10 highest revenue generating products',
        'Find the top 5 cities with the highest profit margins',
        'Calculate the total discount given for each category',
        'Find the average sale price per product category',
        'Find the region with the highest average sale price',
        'Find the total profit per category',
        'Identify the top 3 segments with the highest quantity of orders',
        'Determine the average discount percentage given per region',
        'Find the product category with the highest total profit',
        'Calculate the total revenue generated per year']

    q2=['Select a question to view the dataframe',
    'Get most number of shipping methods for cities',
    'Get the product_id and cost_price of a product with or without the sub_category',
    'Calculate the actual profit without the discount for corporate segment',
    'Find the city with most orders',
    'Find the top 5 highest selling products',
    'Which cities have the same day ship_mode available',
    'Top 5 cities with highest profit in technology',
    'Sub-category with least sales',
    'Find the highest quantity order till date with the product id and category',
    'Which date had the highest amount of sales']



    queries=['select product_id,sum(sale_price) as sale_amount from pricing group by product_id order by sale_amount desc limit 10;',
    'select o.city,sum(p.profit) as total_profit from pricing p join orders o on o.order_id=p.order_id group by city order by total_profit desc limit 5;',
    'select sum(p.discount) as total_discount,o.category from pricing p join orders o on o.order_id=p.order_id group by o.category;',
    'with sale_details as (select sum(sale_price) sale_value, row (category,sub_category) as products,count(*) as total_count from orders o join pricing p on p.order_id=o.order_id group by category,sub_category) select sd.sale_value/sd.total_count as average_val,sd.products, sd.sale_value, sd.total_count from sale_details sd;',
    'with region_sale as( select sum(p.sale_price) sale_price,o.region region,count(*) as sale_count from orders o join pricing p on o.order_id=p.order_id group by o.region) select rs.sale_price/rs.sale_count as avg_value,rs.region from region_sale rs order by avg_value desc limit 1;',
    'select sum(p.profit) total_profit,o.category from orders o join pricing p on p.order_id=o.order_id group by category;',
    'select count(order_id) as total_orders, row (category,sub_category) as products from orders group by category,sub_category order by total_orders desc limit 3;',
    'select avg(p.discount_percent) avg_discount,o.region from pricing p join orders o on o.order_id=p.order_id group by o.region order by avg_discount desc;',
    'select o.category,sum(p.profit) total_profit from orders o join pricing p on p.order_id=o.order_id group by o.category order by total_profit desc limit 1;',
    'select extract(year from o.order_date) as year,sum(p.sale_price) as revenue from pricing p join orders o on o.order_id=p.order_id group by year order by year;']

    queries1=['select count(ship_mode) as ship_mode_count,ship_mode,city from orders group by city,ship_mode order by ship_mode_count desc;',
    'select o.category,p.product_id,p.cost_price from pricing p right join orders o on o.order_id=p.order_id;',
    "with sale_details as (SELECT sum(sale_price) sale_value,sum(list_price) list_val from orders o join pricing p on o.order_id=p.order_id where o.segment='Corporate') select sd.list_val-sd.sale_value as difference_amount from sale_details sd;",
    'select count(*) as total_count,city from orders group by city order by total_count desc;',
    'SELECT (category,sub_category) as category,count(*) as total_count from orders group by category,sub_category order by total_count desc limit 5;',
    "select distinct city from orders where ship_mode='Same Day';",
    "select o.city,p.profit from orders o join pricing p on p.order_id=o.order_id where o.category='Technology' order by p.profit desc limit 5;",
    'select o.sub_category,count(*) as total_count from orders o join pricing p on p.order_id=o.order_id group by o.sub_category order by total_count limit 5;',
    'select p.quantity,p.order_id,o.category,p.product_id from orders o join pricing p on p.order_id=o.order_id where quantity=(select quantity from pricing order by quantity desc limit 1) order by quantity desc;',
    'select o.order_date,sum(p.sale_price) from orders o join pricing p on p.order_id=o.order_id group by order_date order by sum desc limit 1;']

    q=st.selectbox("Orders and Pricing dataframe",q1)
    if q== q1[1]:
        db.execute(queries[0])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[2]:
        db.execute(queries[1])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[3]:
        db.execute(queries[2])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[4]:
        db.execute(queries[3])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[5]:
        db.execute(queries[4])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[6]:
        db.execute(queries[5])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[7]:
        db.execute(queries[6])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[8]:
        db.execute(queries[7])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[9]:
        db.execute(queries[8])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif q== q1[10]:
        db.execute(queries[9])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)


    select_button2=st.selectbox("Orders and Pricing dataframe",q2)
    if select_button2== q2[1]:
        db.execute(queries1[0])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[2]:
        db.execute(queries1[1])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[3]:
        db.execute(queries1[2])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[4]:
        db.execute(queries1[3])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[5]:
        db.execute(queries1[4])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[6]:
        db.execute(queries1[5])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[7]:
        db.execute(queries1[6])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[8]:
        db.execute(queries1[7])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[9]:
        db.execute(queries1[8])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)
    elif select_button2== q2[10]:
        db.execute(queries1[9])
        data=db.fetchall()
        column_names = [desc[0] for desc in db.description]
        df = pd.DataFrame(data, columns=column_names)
        df.index += 1
        st.dataframe(df)