# grid_data.py — Single source of truth
# Yeh file import karenge har jagah se

SUBSTATIONS = [
    ("Sub_A", {"voltage": 132, "city": "Miami"}),
    ("Sub_B", {"voltage": 220, "city": "Orlando"}),
    ("Sub_C", {"voltage": 132, "city": "Tampa"}),
    ("Sub_D", {"voltage": 220, "city": "Jacksonville"}),
    ("Sub_E", {"voltage": 132, "city": "Gainesville"}),
    ("Sub_F", {"voltage": 132, "city": "Tallahassee"}),
]

LINES = [
    ("Sub_A", "Sub_B", {"capacity": 0.08}),
    ("Sub_A", "Sub_C", {"capacity": 0.05}),
    ("Sub_B", "Sub_C", {"capacity": 0.09}),
    ("Sub_B", "Sub_D", {"capacity": 0.02}),
    ("Sub_C", "Sub_E", {"capacity": 0.06}),
    ("Sub_D", "Sub_E", {"capacity": 0.03}),
    ("Sub_D", "Sub_F", {"capacity": 0.02}),
    ("Sub_E", "Sub_F", {"capacity": 0.07}),
]

def build_grid():
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(SUBSTATIONS)
    G.add_edges_from(LINES)
    return G