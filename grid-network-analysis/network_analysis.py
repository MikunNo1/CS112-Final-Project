import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

utilities = pd.read_csv('data_sets/utilities.csv')
substations = pd.read_csv('data_sets/substations.csv')
lines = pd.read_csv('data_sets/lines.csv')

# Create network graph — undirected, since AC power can flow either way
# along a line depending on system conditions (unlike a scheduled flight,
# which always has a fixed origin and destination)
G = nx.Graph()

for index, row in substations.iterrows():
    G.add_node(
        row['Substation ID'],
        name=row['Name'],
        short_name=row['Short Name'],
        region=row['Region'],
        country=row['Country'],
        latitude=row['Latitude'],
        longitude=row['Longitude'],
        voltage_kv=row['Voltage (kV)'],
        capacity_mva=row['Capacity (MVA)'],
        commissioning_year=row['Commissioning Year'],
        type=row['Type'],
        status=row['Status']
    )

# Add lines as edges, using Substation ID to match the nodes above
for index, row in lines.iterrows():
    G.add_edge(
        row['Source Substation ID'],
        row['Destination Substation ID'],
        length_km=row['Length (km)'],
        voltage_kv=row['Voltage (kV)']
    )

print(f"Number of nodes (substations): {G.number_of_nodes()}")
print(f"Number of edges (lines): {G.number_of_edges()}")

# Degree centrality — number of connections per substation
degree_centrality = nx.degree_centrality(G)
top_substations = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

print("\nTop 10 Substations by Degree Centrality (by ID):")
for substation_id, centrality in top_substations:
    name = G.nodes[substation_id]['name']
    print(f"{name} (ID {substation_id}): {centrality:.4f}")

# N-1 contingency: remove the top substation and see how the network fragments
top_hub_id = top_substations[0][0]
top_hub_name = G.nodes[top_hub_id]['name']

G_minus = G.copy()
G_minus.remove_node(top_hub_id)

print(f"\nConnected components before removing top hub ({top_hub_name}):", nx.number_connected_components(G))
print("Connected components after removing top hub:", nx.number_connected_components(G_minus))

# Visualize the network
plt.figure(figsize=(12, 8))
labels = {node: G.nodes[node]['name'] for node in G.nodes}
nx.draw(G, labels=labels, with_labels=True, node_size=200, node_color='lightblue', font_size=6)
plt.title('National Grid Substation Network')
plt.tight_layout()
plt.savefig('network_graph.png')
plt.show()

