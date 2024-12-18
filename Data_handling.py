import zipfile
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#unzip the orders.csv file
with zipfile.ZipFile('C:/Users/Dell/Downloads/orders.csv.zip') as zip_ref:
    zip_ref.extractall()

#read the csv file
df=pd.read_csv('F:/DSProject/Retail_data_analysis/orders.csv')

# data cleaning
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(" ","_")
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")
df['ship_mode'].fillna('0', inplace=True)
for i in df.select_dtypes(include=["object"]).columns:
  df[i]=df[i].str.rstrip()
df['discount']=df['discount_percent']*df['list_price']*0.01
df['sale_price']=df['list_price']-df['discount']
df['profit']=df['sale_price']-df['cost_price']


#spliting into two dataframe
df_order =df[['order_id', 'order_date', 'ship_mode', 'segment', 'country', 'city','state', 'postal_code', 'region', 'category', 'sub_category']]
df_pricing = df[['order_id','product_id', 'cost_price', 'list_price', 'quantity','discount_percent', 'discount', 'sale_price', 'profit']]


#DB connection
client = psycopg2.connect(host='localhost',
                          user="postgres",
                          password="postgre_password",
                          port=5432,
                          database="rexy")

db = client.cursor()
client.autocommit = True

db_name='retail_data'

#Check if the database exists
db.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
exists = db.fetchone()

if exists:
    print(f"Database '{db_name}' already exists. Connecting to it...")
else:
    print(f"Database '{db_name}' does not exist. Creating it...")
    db.execute(f"CREATE DATABASE {db_name}")
    #db.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"Database '{db_name}' created successfully.")

db.close()
client.close()

#new DB creation
db_config = {
    'dbname': 'retail_data',
    'user': 'postgres',
    'password': 'postgre_password',
    'host': 'localhost',
    'port': '5432'
}
# Create connection string
connection_string = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
engine = create_engine(connection_string)
#data transfer to DB
df_order.to_sql('orders', engine, index=False, if_exists='replace')
df_pricing.to_sql('pricing', engine, index=False, if_exists='replace')

client = psycopg2.connect(host='localhost',
                          user="postgres",
                          password="postgre_password",
                          port=5432,
                          database="retail_data")

db = client.cursor()

db.execute("alter table orders add constraint pk_order_id primary key(order_id);")
client.commit()

db.execute("alter table pricing add constraint pk_prdt_id primary key(order_id,product_id);")
client.commit()
db.execute("alter table pricing add constraint fk_order_id foreign key (order_id) references orders (order_id);")
client.commit()

db.close()
client.close()