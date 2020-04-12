import pandas as pd

# Data Source:
# https://www.kaggle.com/martincontreras/volcanic-eruptions-dataset-all-to-2020
df = pd.read_excel('INPUT/volcanic_dataset.xls', header=1)

# Cleaning the dataframe
# Remove eruptions which started before 2015
df = df[df['Start Year'] >= 2015].reset_index()


# Drop the unnecessary columns
df = df.drop(columns = ['index','VEI Modifier', 'Start Year Modifier', 'Start Day Modifier', 'End Year Modifier',
                   'End Day Modifier', 'Start Year Uncertainty', 'End Year Uncertainty', 'End Day Uncertainty',
                       'Area of Activity', 'Start Day Uncertainty', 'Evidence Method (dating)'])


# And rename the columns that we are going to use                       
df.columns = ['v_num', 'v_name', 'erup_num',
       'erup_cat', 'vei', 'start_y', 'start_m', 'start_d',
        'end_y', 'end_m', 'end_d', 'lat', 'lon']

# Unify dates into a single column for `start` and `end` variables
## first, turn the string values to integers
toint = lambda x: int(x)
df['start_d'] = df['start_d'].map(toint)
df['start_m'] = df['start_m'].map(toint)
df['start_y'] = df['start_y'].map(toint)
df['end_d'] = df['end_d'].map(toint)
df['end_m'] = df['end_m'].map(toint)
df['end_y'] = df['end_y'].map(toint)

## and create the new columns
df['start'] = pd.to_datetime(df[['start_d','start_m','start_y']]
                   .astype(str).apply(' '.join, 1), format='%d %m %Y')
df['end'] = pd.to_datetime(df[['end_d','end_m','end_y']]
                   .astype(str).apply(' '.join, 1), format='%d %m %Y')


# Calculate duration of eruptive phase (a.k.a. `delta`)
df['delta'] = df.end - df.start
df[['v_name', 'start', 'end', 'delta']].sort_values('delta', ascending=False)


# ♠ OPTIMIZATION IDEA:
##  drop also the eruption phases that started before the
##  API's oldest data point (2015-06-13) or filter the
##  events so that at least the end date is available


print(df.columns)

# Save the data we processed as a new dataset
df.to_csv('OUTPUT/volcanic-eruptions.csv')