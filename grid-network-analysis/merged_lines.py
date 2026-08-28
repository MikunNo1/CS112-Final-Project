import pandas as pd
import matplotlib.pyplot as plt

utilities = pd.read_csv('data_sets/utilities.csv')
substations = pd.read_csv('data_sets/substations.csv')
lines = pd.read_csv('data_sets/lines.csv')

# Merge lines with substations to get source substation details
lines_with_source = lines.merge(
    substations[['Substation ID', 'Name', 'Region', 'Country']],
    left_on='Source Substation ID', right_on='Substation ID',
    how='left', suffixes=('', '_source'))
 
# Merge with destination substation details
lines_with_subs = lines_with_source.merge(
    substations[['Substation ID', 'Name', 'Region', 'Country']],
    left_on='Destination Substation ID', right_on='Substation ID',
    how='left', suffixes=('_source', '_dest'))
 
# Bring in the utility name/code too
lines_with_utility = lines_with_subs.merge(
    utilities[['Utility ID', 'Name', 'Code']], on='Utility ID', how='left')
 
# Preview merged data
print("Merged Lines DataFrame:")
print(lines_with_utility[['Code', 'Source Substation', 'Region_source',
                           'Destination Substation', 'Region_dest', 'Voltage (kV)']].head(), "\n")

lines_with_utility.to_csv('merged_lines.csv')
 
# Analyse lines by utility and source region
lines_by_utility_region = (lines_with_utility
    .groupby(['Code', 'Region_source'])
    .size().reset_index(name='Line Count'))
top_lines = lines_by_utility_region.sort_values(by='Line Count', ascending=False).head(10)
print("Top 10 Utility/Region Combinations by Line Count:")
print(top_lines, "\n")
 
# Visualize top combinations
plt.figure(figsize=(12, 6))
top_lines.plot(kind='bar', x='Code', y='Line Count',
               title='Top 10 Utility/Region Combinations by Line Count')
plt.xlabel('Utility')
plt.ylabel('Number of Lines')
plt.tight_layout()
plt.show()
