# neo4j_import.py
from neo4j import GraphDatabase
from grid_data import build_grid

URI      = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "fplgrid123"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
G = build_grid()    # ← ek line, data repeat nahi

def import_grid(tx, G):
    tx.run("MATCH (n) DETACH DELETE n")
    
    for node, data in G.nodes(data=True):
        tx.run("""
            CREATE (s:Substation {
                name: $name,
                city: $city,
                voltage: $voltage
            })
        """, name=node, city=data["city"], voltage=data["voltage"])
    
    for u, v, data in G.edges(data=True):
        tx.run("""
            MATCH (a:Substation {name: $from_node})
            MATCH (b:Substation {name: $to_node})
            CREATE (a)-[:LINE {capacity: $capacity}]->(b)
        """, from_node=u, to_node=v, capacity=data["capacity"])

with driver.session(database="neo4j") as session:
    session.execute_write(import_grid, G)
    print("✅ Grid successfully imported to Neo4j!")
    
    result = session.run("MATCH (n:Substation) RETURN count(n) as nodes")
    print(f"📊 Nodes in Neo4j: {result.single()['nodes']}")
    
    result = session.run("MATCH ()-[r:LINE]->() RETURN count(r) as edges")
    print(f"🔌 Edges in Neo4j: {result.single()['edges']}")

driver.close()