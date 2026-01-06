###############################################################################
# File Name: assignment_02.py
#
# Description: This program plots precipitation levels in Athens, GA 
# between 2000 and 2010.
#
# Record of Revisions (Date | Author | Change):
# 01/30/2024 | Rhys DeLoach | Initial creation
###############################################################################

# Initialize Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file into a DataFrame
df = pd.read_csv('data/data.csv', parse_dates=['DATE'])

# Set the date column as the index
df.set_index('DATE', inplace=True)

# Resample the data to a daily sum
daily_data = df.resample('D').sum()

# Resample the data to a monthly average
monthly_data = df['HPCP'].resample('M').mean()

# Use Seaborn to create a line plot
sns.lineplot(data=monthly_data)
plt.xlabel('Date')
plt.ylabel('Precipitation (inches)')
plt.title('Athens, GA Rain Gauge')

# Save the figure
plt.savefig('output/athens_rain_gauge.png', dpi=300, bbox_inches='tight')
plt.show()
