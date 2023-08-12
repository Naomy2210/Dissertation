import pandas as pd
import matplotlib.pyplot as plt
from A_ConnexionDB import connect, sql_to_dataframe
from datetime import datetime

'''Mobility chart'''

    # Read the Excel file of Scotland into a DataFrame
df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Google/GB_Region_Mobility_Report.xlsx',sheet_name='Edinburgh')
    # Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

    # Set the 'date' column as the DataFrame index
df.set_index('date', inplace=True)

    # List of columns to drop
columns_to_drop = ['country', 'sub_region','iso_3166_2', 'place_id']
df.drop(columns=columns_to_drop, inplace=True)

    # Resample the dataframe by week and calculate the mean driving value per week (no need to add the percentage because the values are already in percentages)
weekly_df = df['residential'].resample('W').mean()
weekly_df = weekly_df.iloc[:58]


'''Sentiment chart'''

    # Load the data
query = """SELECT msg,wgslat, wgslng,created_at,id,screenname,source,geom, roberta_sentiment_labels                         
            FROM table_roberta_prepro
            """
column_names = ['msg', 'wgslat', 'wgslng', 'created_at', 'id', 'screenname', 'source', 'geom',
                'roberta_sentiment_labels']
conn = connect()
df = sql_to_dataframe(conn, query, column_names)

    # Convert the 'created_at' column to a datetime object
df['created_at'] = pd.to_datetime(df['created_at'])

    # Group the dataframe by week and calculate the number of 'NEG' sentiments per week
weekly_counts = df[df['roberta_sentiment_labels'] == 'NEG'].groupby(pd.Grouper(key='created_at', freq='W'))['roberta_sentiment_labels'].count()

    # Calculate the weekly percentage distribution of 'NEG' sentiments
weekly_distribution = 100 * weekly_counts / weekly_counts.sum()

    # Calculate the weekly differences between each day
weekly_diff = weekly_counts.diff()
weekly_percentage_diff = weekly_diff.pct_change()


'''PLOT GRAPH'''

    # Create the figure and axis for the second plot (weekly differences between days)
fig, ax1 = plt.subplots()

'''Plot the NEG sentiments in Scotland'''
ax1.plot(weekly_percentage_diff.index, weekly_percentage_diff.values, label='Weekly Sentiment NEG Percentage Difference', color='green')

    # Set the x-axis label
ax1.set_xlabel('Week')
    # Set the y-axis label
ax1.set_ylabel('Difference in NEG sentiment')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc='upper left')


'''Plot the mobility in Scotland'''
ax2 = ax1.twinx()
ax2.plot(weekly_df.index, weekly_df.values, label='Weekly Percentage Difference', color='blue')

    # Set the x-axis label
ax2.set_xlabel('Week')
    # Set the y-axis label
ax2.set_ylabel('Percentage Difference')
ax2.tick_params(axis='y', labelcolor='green')
ax2.legend(loc='upper right')


    # Show the plot for the analysis
plt.show()

'''CORRELATION CALCUL'''

    # Calculate the correlation between daily sentiment percentage difference and weekly driving percentage difference
correlation = weekly_percentage_diff.corr(weekly_df)

print("Correlation :", correlation)