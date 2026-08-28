import plotly.express as px
import networkx as nx
 
# Interactive map of substations
fig = px.scatter_geo(substations, lat='Latitude', lon='Longitude', hover_name='Name',
                     color='Region', title='National Grid Substation Locations',
                     projection='natural earth')
fig.show()
 
# Network analysis of lines — undirected, since power can flow either direction
G = nx.from_pandas_edgelist(lines, source='Source Substation', target='Destination Substation',
                            edge_attr=['Length (km)', 'Voltage (kV)'], create_using=nx.Graph())
print(f"Number of nodes (substations): {G.number_of_nodes()}")
print(f"Number of edges (lines): {G.number_of_edges()}")

# Calculate degree centrality (number of connections per substation)
degree_centrality = nx.degree_centrality(G)
top_substations = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 Substations by Degree Centrality:")
for substation, centrality in top_substations:
    print(f"{substation}: {centrality:.4f}")
 
# N-1 contingency: remove the top substation and see how the network fragments
top_hub = top_substations[0][0]
G_minus = G.copy()
G_minus.remove_node(top_hub)
print('\nConnected components before removing top hub (' + top_hub + '):', nx.number_connected_components(G))
print('Connected components after removing top hub:', nx.number_connected_components(G_minus))
 
# Visualize a subset of the network for clarity
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_size=200, node_color='lightblue', font_size=6)
plt.title('National Grid Substation Network')
plt.show()
