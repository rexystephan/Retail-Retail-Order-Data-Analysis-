# Retail Order Data Analysis
## Objective:
To analyze and optimize sales performance by uncovering actionable insights, such as top-performing products, revenue trends, and growth opportunities, using real-world retail order data.
### Key Deliverables:
1. Data insights through 20 SQL queries to answer key business questions.
2. Cleaned, structured data stored in SQL Server for efficient querying.
3. An interactive Streamlit dashboard for visualizing data trends in real-time.
### Tools & Technologies Used:
1.Data Extraction: Kaggle API, Python
2. Data Cleaning: Pandas library in Python
3. Data Storage: SQL Server (Relational database -using PostgreSQL)
4. Data Analysis: SQL queries (using GROUP BY, HAVING and joins)
5. Data Visualization: Streamlit
### Workflow:
#### Step 1: Data Extraction
- **Source**: Kaggle dataset (!kaggle datasets download ankitbansal06/retail-orders -f orders.csv)
- **Process**:
     API setup and dataset retrieval using the Kaggle library.
     Dataset downloaded as orders.csv.
#### Step 2: Data Cleaning
**Tools**: Python (Pandas library)
**Actions**:
- Standardized column names for SQL compatibility.
- Handled missing values.
- Derived new columns:
    * Discount: discount_percent * list_price*0.01
    * sale_price: list_price-discount
    * Profit: sale_price - cost_price
#### Step 3: SQL Server Integration
**Database Design:**
- Imported the cleaned dataset into SQL Server.
- Defined primary and foreign keys to establish relationships for relational queries.
#### Step 4: Data Analysis
- Using SQL, generated actionable insights to address business objectives.
#### Step 5: Streamlit Dashboard
**Features:**
- Display SQL query results as data frames from the DB.
- Dynamic user interactions for viewing the data.
- Real-time connection to the SQL database for seamless updates.
