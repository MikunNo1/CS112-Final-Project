import pandas as pd
import matplotlib.pylot as plt
import seaborn as sns

plt.style.use("ggplot")

utilities = pd.read_csv("utilities.csv")
substations = pd.read_csv("substations.csv")
lines = pd.read_csv("lines")

print("Utilities")
print(utilities.head())
print()

print("Substations")
print(substations.head())
print()

print("Lines")
print(lines.head())
print()

print("========== UTILITIES ==========")
print(utilities.describe(include='all'))

print("\n========== SUBSTATIONS ==========")
print(substations.describe(include='all'))

print("\n========== LINES ==========")
print(lines.describe(include='all'))

region_counts = substations["Region"].value_counts()
print(region_counts)

plt.figure(figsize=(10.6))

region_counts.plot(
    kind='bar',
    color='pink'
)

plt.title("Number os Substations by Region")
plt.xlabel("Region")
plt.ylabel("Number of Substations")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

voltage_counts = substations["Voltage (kV)"].value_counts().sort_index()
print(voltage_counts)

plt.figure(figsize=(8,5))

voltage_counts.plot(
    kind="bar",
    color="blue"
)

plt.title("Distribution")
