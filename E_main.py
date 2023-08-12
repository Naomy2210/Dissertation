from A_ConnexionDB import connect, sql_to_dataframe, engine, dataframe_to_sql, disconnect
from B_Preprocessing import preprocessing_msg
from C_BERT import run_ROBERTA

# 1 Creating variables
# 1a creating a query variable to store our query to pass into the function
query = """SELECT msg,wgslat, wgslng,created_at,id,screenname,source,geom                         
            FROM covid_virus_149556
            """
# 1b creating a list with columns names to pass into the function
column_names = ['msg', 'wgslat', 'wgslng', 'created_at', 'id', 'screenname', 'source', 'geom']

# 2 opening the connection
conn = connect()

# 3 loading our dataframe
df1 = sql_to_dataframe(conn, query, column_names)

# 4 preprocessing
df = preprocessing_msg(df1)

# 5 Analysis
df = run_ROBERTA(df)
model = 'roberta'

# 6 create table in the DB
table_name = f"table_{model}_prepro"
engine = engine()
dataframe_to_sql(df, table_name, engine)

# 7 close connections
disconnect(engine, conn)
