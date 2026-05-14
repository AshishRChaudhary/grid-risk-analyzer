# ⚡ FPL Grid Risk Analyzer

Graph-based power grid risk analysis using NetworkX, Neo4j, and Streamlit.

## What it does
- Models Florida power grid as a graph
- Calculates substation risk using Degree, Betweenness, and PageRank centrality
- Stores grid in Neo4j graph database
- Interactive risk dashboard via Streamlit

## Tech Stack
- Python, NetworkX, Pandas
- Neo4j + Cypher
- Streamlit + PyVis

## Run the app
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Project Structure
