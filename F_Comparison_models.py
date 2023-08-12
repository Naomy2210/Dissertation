from A_ConnexionDB import connect, sql_to_dataframe, engine, dataframe_to_sql, disconnect
from B_Preprocessing import preprocessing_msg
from C_BERT import run_BERT, run_DISTILBERT, run_ROBERTA
from C_FLAIR import run_FLAIR
from C_GPT import run_GPT2
from C_SentiStrength import run_SentiStrength
from C_VADER import run_VADER


# 1 Creating variables
# 1a creating a query variable to store our query to pass into the function
query = """SELECT msg,wgslat, wgslng,created_at,id,screenname,source,geom                         
            FROM trained
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
model = int(input("which analysis you want to run [1] for BERT, [2] for SentiStrength, [3] for VADER, [4] for GPT-2, [5] for FLAIR, [6] for DISTILBERT or [7] for ROBERTA ?"))
if model == 1:
    df = run_BERT(df)
    model = "bert"
elif model == 2:
    df = run_SentiStrength(df)
    model = "sentistrength"
elif model == 3:
    df = run_VADER(df)
    model = "vader"
elif model == 4:
    df = run_GPT2(df)
    model = "gpt2"
elif model == 5:
    df = run_FLAIR(df)
    model = "flair"
elif model == 6:
    df = run_DISTILBERT(df)
    model = "distilbert"
elif model == 7:
    df = run_ROBERTA(df)
    model = "roberta"


# 6 create table in the DB
table_name = f"table_{model}"
engine = engine()
dataframe_to_sql(df, table_name, engine)

# 7 close connections
disconnect(engine, conn)