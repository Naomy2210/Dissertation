import random
from A_ConnexionDB import connect
from langdetect import detect

def table_creation():
    # Connect to the PostgreSQL database
    conn = connect()

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # Create a new table to store the random rows
    cur.execute("CREATE TABLE trained AS SELECT * FROM covid_virus WHERE 1=0")

    # Retrieve the total number of rows in the table
    cur.execute("SELECT COUNT(*) FROM covid_virus")
    total_rows = cur.fetchone()[0]

    # Generate a random sample of row indices
    sample_indices = random.sample(range(total_rows), 2000)

    # Create a comma-separated string of the sample indices
    indices_string = ','.join(str(index) for index in sample_indices)

    # Retrieve the random rows from the table using a subquery
    cur.execute(f"INSERT INTO trained (msg,wgslat, wgslng,created_at,id,screenname,source,geom ) SELECT msg,wgslat, wgslng,created_at,id,screenname,source,geom  FROM (SELECT msg,wgslat, wgslng,created_at,id,screenname,source,geom, ROW_NUMBER() OVER () as row_num FROM covid_virus_149556) AS subq WHERE row_num IN ({indices_string})")

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cur.close()
    conn.close()

    return "trained table has been created"


#table_creation()

'''import pandas as pd
import psycopg2
import openpyxl

psql tool
\copy trained FROM 'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Di
ssertation/to_be_trained.csv' CSV HEADER

# Load the Excel file and read the data
df = pd.read_excel('C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/to_be_trained.xlsx')


# Establish a connection to the database
conn = psycopg2.connect('dbname=postgis_33_sample user=postgres password=root')

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Iterate over the data and insert into the database table
for index, row in df.iterrows():
    label_neu = row['sentiment_NONEU']
    label = row['sentiments_labels']

    # Construct the SQL INSERT statement
    sql = f"INSERT INTO trained (neu_label_column, label_column) VALUES ('{label_neu}', '{label}')"

    # Execute the SQL statement
    cur.execute(sql)

# Commit the changes to the database
conn.commit()

# Close the cursor and database connection
cur.close()
conn.close()'''



