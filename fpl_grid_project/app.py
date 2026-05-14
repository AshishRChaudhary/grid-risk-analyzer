# app.py — FPL Grid Risk Analyzer

import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="FPL Grid Risk Analyzer",
    page_icon="⚡",
    layout="wide"
)

from grid_data import build_grid

G = build_grid()

# ── CENTRALITY CALCULATE KARO ──
degree_centrality     = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight="capacity")
pagerank              = nx.pagerank(G, weight="capacity")

# ── RISK COLOR FUNCTION ──
def risk_color(node):
    b = betweenness_centrality[node]
    if b >= 0.4:   return "#E05252"
    elif b >= 0.15: return "#F0A500"
    else:           return "#1D9E75"

def risk_label(node):
    b = betweenness_centrality[node]
    if b >= 0.4:    return "🔴 Critical"
    elif b >= 0.15: return "🟠 Medium"
    else:           return "🟢 Low"

# ── HEADER ──
st.title("⚡ FPL Grid Risk Analyzer")
st.markdown("**Graph-based substation risk analysis — powered by NetworkX**")
st.divider()

# ── LAYOUT — 2 columns ──
col1, col2 = st.columns([1.2, 1])

# ── COLUMN 1 — Interactive Graph ──
with col1:
    st.subheader("🗺️ Live Grid Map")
    
    net = Network(height="420px", width="100%", bgcolor="#0e1117", font_color="white")
    
    for node in G.nodes():
        city    = G.nodes[node]["city"]
        voltage = G.nodes[node]["voltage"]
        b       = round(betweenness_centrality[node], 3)
        pr      = round(pagerank[node], 3)
        size    = pr * 120 + 20
        color   = risk_color(node)
        title   = f"{node} — {city}\nVoltage: {voltage}kV\nBetweenness: {b}\nPageRank: {pr}\nRisk: {risk_label(node)}"
        net.add_node(node, label=f"{node}\n{city}", color=color, size=size, title=title)
    
    for u, v, data in G.edges(data=True):
        cap = data["capacity"]
        net.add_edge(u, v, value=cap * 30, title=f"Capacity: {cap}Ω", color="#555555")
    
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "stabilization": { "iterations": 200 }
      }
    }
    """)
    
    net.save_graph("grid.html")
    with open("grid.html", "r") as f:
        html = f.read()
    components.html(html, height=440)
    
    st.caption("💡 Hover over Node to see details.")

# ── COLUMN 2 — Risk Table + Substation Detail ──
with col2:
    st.subheader("📊 Risk Table")
    
    df = pd.DataFrame({
        "Substation": list(G.nodes()),
        "City":       [G.nodes[n]["city"] for n in G.nodes()],
        "Risk":       [risk_label(n) for n in G.nodes()],
        "Betweenness":[round(betweenness_centrality[n], 3) for n in G.nodes()],
        "PageRank":   [round(pagerank[n], 3) for n in G.nodes()],
        "Degree":     [round(degree_centrality[n], 3) for n in G.nodes()],
    }).sort_values("Betweenness", ascending=False).reset_index(drop=True)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # ── SUBSTATION DETAIL ──
    st.subheader("🔍 Substation Detail")
    selected = st.selectbox("Substation chuno:", list(G.nodes()))
    
    city    = G.nodes[selected]["city"]
    voltage = G.nodes[selected]["voltage"]
    b       = round(betweenness_centrality[selected], 3)
    pr      = round(pagerank[selected], 3)
    deg     = round(degree_centrality[selected], 3)
    neighbors = list(G.neighbors(selected))
    
    st.markdown(f"### {selected} — {city}")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Voltage",     f"{voltage} kV")
    m2.metric("Betweenness", b)
    m3.metric("PageRank",    pr)
    
    st.markdown(f"**Risk Level:** {risk_label(selected)}")
    st.markdown(f"**Connected to:** {', '.join(neighbors)}")
    
    # Risk explanation
    if b >= 0.4:
        st.error(f"⚠️ Critical node — {selected} if fails, major blackout risk. Immediate monitoring required.")
    elif b >= 0.15:
        st.warning(f"🔶 Medium risk — {selected} important path. Regular inspection needed.")
    else:
        st.success(f"✅ Low risk — {selected} If fails, minimal impact on grid.")