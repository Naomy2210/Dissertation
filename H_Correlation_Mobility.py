import pandas as pd
import matplotlib.pyplot as plt

'''Mobility Apple chart'''

    # Read the Excel file of Scotland into a DataFrame
df_1 = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Apple/Apple_Report_Assess.xlsx',
        sheet_name='Scotland')
    # Ensure the 'date' column is in datetime format
df_1['date'] = pd.to_datetime(df_1['date'])

    # Set the 'date' column as the DataFrame index
df_1.set_index('date', inplace=True)

    # List of columns to drop
columns_to_drop = ['sub-region', 'subregion_and_city']
df_1.drop(columns=columns_to_drop, inplace=True)

    # Resample the dataframe by week and calculate the mean driving value per week (no need to add the percentage because the values are already in percentages)
weekly_df_1 = df_1['transit'].resample('W').mean()
weekly_df_1 = weekly_df_1.iloc[7:]


'''Mobility Google chart'''

# Read the Excel file of Scotland into a DataFrame
df = pd.read_excel(
    'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Google/GB_Region_Mobility_Report.xlsx',
    sheet_name='Scotland')
# Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Set the 'date' column as the DataFrame index
df.set_index('date', inplace=True)

# List of columns to drop
columns_to_drop = ['country', 'sub_region', 'iso_3166_2', 'place_id']
df.drop(columns=columns_to_drop, inplace=True)

# Resample the dataframe by week and calculate the mean driving value per week (no need to add the percentage because the values are already in percentages)
weekly_df = df['residential'].resample('W').mean()
weekly_df = weekly_df.iloc[:58]


'''PLOT GRAPH'''

    # Create the figure and axis for the second plot (weekly differences between days)
fig, ax1 = plt.subplots()

'''Plot Apple'''
ax1.plot(weekly_df_1.index, weekly_df_1.values, label='Weekly Apple', color='green')

    # Set the x-axis label
ax1.set_xlabel('Week')
    # Set the y-axis label
ax1.set_ylabel('Weekly Apple')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc='upper left')


'''Plot google'''
ax2 = ax1.twinx()
ax2.plot(weekly_df.index, weekly_df.values, label='Weekly Google', color='blue')

    # Set the x-axis label
ax2.set_xlabel('Week')
    # Set the y-axis label
ax2.set_ylabel('Weekly Google')
ax2.tick_params(axis='y', labelcolor='green')
ax2.legend(loc='upper right')


    # Show the plot for the analysis
plt.show()

'''CORRELATION CALCUL'''

    # Calculate the correlation between daily sentiment percentage difference and weekly driving percentage difference
correlation = weekly_df.corr(weekly_df_1)

print("Correlation :", correlation)
