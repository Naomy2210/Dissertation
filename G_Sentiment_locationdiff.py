import pandas as pd
import matplotlib.pyplot as plt
from A_ConnexionDB import connect, sql_to_dataframe

'''Glasgow'''

    # Load the data
query = """SELECT sentiment, geom, id, dates
            FROM glasgow
            """
column_names = ['sentiment', 'geom', 'id', 'dates']
conn = connect()
df_glasgow = sql_to_dataframe(conn, query, column_names)

    # Convert the 'created_at' column to a datetime object
df_glasgow['dates'] = pd.to_datetime(df_glasgow['dates'])

    # Group the dataframe by week and calculate the mean of 'NEG' sentiments per week
weekly_counts_glasgow = df_glasgow.groupby(pd.Grouper(key='dates', freq='W'))['sentiment'].count()
weekly_counts_glasgow_neg = df_glasgow[df_glasgow['sentiment'] == 'NEG'].groupby(pd.Grouper(key='dates', freq='W'))['sentiment'].count()

    # Calculate the weekly percentage distribution of 'NEG' sentiments
weekly_distribution_glasgow = 100 * weekly_counts_glasgow_neg / weekly_counts_glasgow

'''Edinburgh'''

    # Load the data
query = """SELECT sentiment, geom, id, dates
            FROM edinburgh
            """
column_names = ['sentiment', 'geom', 'id', 'dates']
conn = connect()
df_edinburgh = sql_to_dataframe(conn, query, column_names)

    # Convert the 'created_at' column to a datetime object
df_edinburgh['dates'] = pd.to_datetime(df_edinburgh['dates'])

    # Group the dataframe by week and calculate the mean of 'NEG' sentiments per week
weekly_counts_edinburgh = df_edinburgh.groupby(pd.Grouper(key='dates', freq='W'))['sentiment'].count()
weekly_counts_edinburgh_neg = df_edinburgh[df_edinburgh['sentiment'] == 'NEG'].groupby(pd.Grouper(key='dates', freq='W'))['sentiment'].count()


    # Calculate the weekly percentage distribution of 'NEG' sentiments
weekly_distribution_edinburgh = 100 * weekly_counts_edinburgh_neg / weekly_counts_edinburgh

'''Shetland'''

    # Load the data
query = """SELECT sentiment, geom, id, dates
            FROM shetland
            """
column_names = ['sentiment', 'geom', 'id', 'dates']
conn = connect()
df_shetland = sql_to_dataframe(conn, query, column_names)

    # Convert the 'created_at' column to a datetime object
df_shetland['dates'] = pd.to_datetime(df_shetland['dates'])

    # Group the dataframe by week and calculate the mean of 'NEG' sentiments per week
weekly_counts_shetland = df_shetland.groupby(pd.Grouper(key='dates', freq='W'))['sentiment'].count()
weekly_counts_shetland_neg = df_shetland[df_shetland['sentiment'] == 'NEG'].groupby(pd.Grouper(key='dates', freq='W'))['sentiment'].count()


    # Calculate the weekly percentage distribution of 'NEG' sentiments
weekly_distribution_shetland = 100 * weekly_counts_shetland_neg / weekly_counts_shetland


'''PLOT'''

plt.figure(figsize=(12, 6))
plt.plot(weekly_distribution_glasgow.index, weekly_distribution_glasgow.values, label='Glasgow', color='green')
plt.plot(weekly_distribution_edinburgh.index, weekly_distribution_edinburgh.values, label='Edinburgh', color='blue')
plt.plot(weekly_distribution_shetland.index, weekly_distribution_shetland.values, label='Shetland', color='red')


plt.xlabel('Week')
plt.ylabel('Percentage NEG')
plt.legend()
plt.title('Weekly ditribution of NEG sentiment by location')
plt.tight_layout()
plt.show()



