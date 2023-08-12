import pandas as pd
import matplotlib.pyplot as plt

"""APPLE"""

# Read the Excel file into a DataFrame
df1 = input('1 for Scotland, 2 for glasgow, 3 for Edinburgh')
if df1 == '1':
    df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Apple/Apple_Report_Assess.xlsx',
        sheet_name='Scotland')
    location = 'Scotland'
elif df1 == '2':
    df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Apple/Apple_Report_Assess.xlsx',
        sheet_name='Glasgow')
    location = 'Glasgow'
elif df1 == '3':
    df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Apple/Apple_Report_Assess.xlsx',
        sheet_name='Edinburgh')
    location = 'Edinburgh'

# Step 1: Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Step 2: Set the 'date' column as the DataFrame index
df.set_index('date', inplace=True)

# clean the columns
# List of columns to drop
columns_to_drop_1 = ['sub-region', 'subregion_and_city']
df.drop(columns=columns_to_drop_1, inplace=True)

# Step 4: Resample the data to weekly intervals and calculate the weekly differences
weekly_df_1 = df.resample('W').mean()
weekly_df_1['driving_difference'] = weekly_df_1['driving'].diff()
weekly_df_1['transit_difference'] = weekly_df_1['transit'].diff()
weekly_df_1['walking_difference'] = weekly_df_1['walking'].diff()

# Step 6: Plot the weekly differences
plt.figure(figsize=(12, 6))
plt.plot(weekly_df_1.index, weekly_df_1['driving_difference'], label='Driving')
plt.plot(weekly_df_1.index, weekly_df_1['transit_difference'], label='Transit')
plt.plot(weekly_df_1.index, weekly_df_1['walking_difference'], label='Walking')
plt.xlabel('Week')
plt.ylabel('Difference')
plt.legend()
plt.title('Weekly Differences in Driving, Transit, and Walking')
plt.tight_layout()

"""GOOGLE"""
# Read the Excel file into a DataFrame
df1 = input('1 for Scotland, 2 for glasgow, 3 for Edinburgh')
if df1 == '1':
    df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Google/GB_Region_Mobility_Report.xlsx',sheet_name='Scotland')
    location = 'Scotland'
elif df1 == '2':
    df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Google/GB_Region_Mobility_Report.xlsx',sheet_name='Scotland')
    df = df[(df['sub_region'] == 'Glasgow City')]
elif df1 == '3':
    df = pd.read_excel(
        'C:/Users/naomy/Documents/ISEP/A3/Etranger_Cours/Dissertation/mobility/Google/GB_Region_Mobility_Report.xlsx',sheet_name='Scotland')
    df = df[(df['sub_region'] == 'Edinburgh')]

# Step 1: Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Step 2: Set the 'date' column as the DataFrame index
df.set_index('date', inplace=True)

# clean the columns
# List of columns to drop
columns_to_drop = ['country', 'sub_region','iso_3166_2', 'place_id', 'retail_and_recreation', 'grocery_and_pharmacy', 'parks',
                   'transit_stations', 'workplaces', 'residential']
df.drop(columns=columns_to_drop, inplace=True)

# Step 4: Resample the data to weekly intervals and calculate the weekly differences
weekly_df = df.resample('W').mean()
weekly_df = weekly_df.iloc[:58]
weekly_df['retail_and_recreation_difference'] = weekly_df['retail_and_recreation_avg'].diff()
weekly_df['grocery_and_pharmacy_difference'] = weekly_df['grocery_and_pharmacy_avg'].diff()
weekly_df['parks_difference'] = weekly_df['parks_avg'].diff()
weekly_df['transit_stations_difference'] = weekly_df['transit_stations_avg'].diff()
weekly_df['workplaces_difference'] = weekly_df['workplaces_avg'].diff()
weekly_df['residential_difference'] = weekly_df['residential_avg'].diff()

# Step 6: Plot the weekly differences
plt.figure(figsize=(12, 6))
plt.plot(weekly_df.index, weekly_df['retail_and_recreation_difference'], label='recreation & retail')
plt.plot(weekly_df.index, weekly_df['grocery_and_pharmacy_difference'], label='grocery & pharmacy')
plt.plot(weekly_df.index, weekly_df['parks_difference'], label='Parks')
plt.plot(weekly_df.index, weekly_df['transit_stations_difference'], label='Transit Stations')
plt.plot(weekly_df.index, weekly_df['workplaces_difference'], label='Workplaces')
plt.plot(weekly_df.index, weekly_df['residential_difference'], label='Residential')

plt.xlabel('Week')
plt.ylabel('Difference')
plt.legend()
plt.title('Weekly Differences')
plt.tight_layout()
plt.show()
