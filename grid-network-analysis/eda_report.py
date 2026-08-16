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
    kind="bar",
    color="pink"
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

plt.title("Distribution of Voltage Levels")
plt.xlabel("Voltage (kV)")
plt.ylabel("Number of Substations")

plt.show()

status_counts = substations["Status"].value_counts()
print(status_counts)

plt.figure(figsize=(6,6))

plt.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Substation Status")

plt.show()

type_counts = substations["Type"].value_counts()
print(type_counts)

plt.figure(figsize=(8,5))

type_counts.plot(
    kind="bar",
    color="green"
)

plt.title("Substation Types")
plt.xlabel("Type")
plt.ylabel("Count")

plt.show()

merged = pd.merge(
    lines,
    utilities,
    on="Utility ID"
)

utility_counts = merged["Alias"].value_counts()
print(utility_counts)

plt.figure(figsize=(8,5))

utility_counts.plot(
    kind="bar",
    color="purple"
)

plt.title("Number of Lines Operated by Utility")
plt.xlabel("Utility")
plt.ylabel("Number of Lines")

plt.show()

source_counts = lines["Source Substation"].value_counts()
print(source_counts.head(10))

plt.figure(figsize=(10,6))

source_counts.head(10).plot(
    kind="bar",
    color="red"
)

plt.title("Top 10 Source Substations")
plt.xlabel("Substation")
plt.ylabel("Number of Lines")

plt.show()

connections = pd.concat([
    lines["Source Substation"],
    lines["Destination Substation"]
])

connection_counts = connections.value_counts()
print(connection_counts.head(10))

plt.figure(figsize=(10,6))

connection_counts.head(10).plot(
    kind="bar",
    color="darkblue"
)

plt.title("Top 10 Most Connected Substations")
plt.xlabel("Substation")
plt.ylabel("Connections")

plt.show()

plt.figure(figsize=(8,5))

plt.hist(
    substations["Capacity (MVA)"],
    bins=10
)

plt.title("Distribution of Substation Capacity")
plt.xlabel("Capacity (MVA)")
plt.ylabel("Frequency")

plt.show

plt.figure(figsize=(8,5))

plt.hist(
    substations["Commissioning Year"],
    bins=12
)

plt.title("Commissioning Years")
plt.xlabel("Year")
plt.ylabel("Number of Substations")

plt.show()

plt.figure(figsize=(8,7))

plt.scatter(
    substations["Longitude"],
    substations["Latitude"]
)

plt.title("Geographical Distribution of Substations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.grid(True)

plt.show()

plt.savefig("substations_by_region.png")
plt.show()