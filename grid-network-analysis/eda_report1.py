import matplotlib.pyplot as plt
 
# Substations: distribution by region
plt.figure(figsize=(10, 6))
substations['Region'].value_counts().head(10).plot(kind='bar', title='Top Regions by Number of Substations')
plt.xlabel('Region')
plt.ylabel('Number of Substations')
plt.tight_layout()
plt.savefig('eda_regions.png')
plt.show()

# Lines: top 10 source substations
plt.figure(figsize=(10, 6))
lines['Source Substation'].value_counts().head(10).plot(kind='bar', title='Top 10 Source Substations by Number of Lines')
plt.xlabel('Substation')
plt.ylabel('Number of Lines')
plt.tight_layout()
plt.savefig('eda_top_substations.png')
plt.show()
 
# Summary statistics for numeric columns in substations
print("Substations Numeric Summary:")
print(substations[['Latitude', 'Longitude', 'Voltage (kV)', 'Capacity (MVA)']].describe(), "\n")
 
# Count of active vs. inactive substations
print("Substation Status Count:")
print(substations['Status'].value_counts(), "\n")
