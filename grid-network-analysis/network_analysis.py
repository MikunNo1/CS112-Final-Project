import networkx as nx
import matplotlib.pyplot as plt
 
# Create network graph — undirected, since AC power can flow either way
# along a line depending on system conditions (unlike a scheduled flight,
# which always has a fixed origin and destination)
G = nx.Graph()
for row in substations.iterrows():
    G.add_node(
        
            row['Substation ID']
            row['Name']
            row['Short Name']
            row['Region']
            row['Country']
            row['Latitude']
            row['Longitude']
            row['Voltage (kV)']
            row['Capacity (MVA)']
            row['Commissioning Year']
            row['Type']
            row['Status']
            )
# Add substations as nodes with attributes (region, voltage, coordinates, etc.)
# Add lines as edges with weights (length, capacity, etc.)
 
# Calculate network metrics
# - Node centrality measures (degree, betweenness, closeness, PageRank)
# - Network diameter and average path length
# - Clustering coefficients
# - Community detection
# - Critical-substation identification
 
# Analyse network structure
# - Identify the most-connected substations (regional 'superhubs')
# - Find bridge lines (critical single points of connection)
# - Detect isolated components
# - Measure network efficiency
