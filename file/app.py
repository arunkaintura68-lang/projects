import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("College Friendship Network Model")

st.markdown("""
### Project Overview

This project models **student friendship connections** using graph theory.

- Nodes → Students
- Edges → Friendships

We analyze:
- Social connectivity
- Important students (centrality)
- Friendship communities
""")

# Session State
if "edges" not in st.session_state:
    st.session_state.edges = []

# Input
st.subheader("Add Friendship")
s1 = st.text_input("Student 1", key="s1")
s2 = st.text_input("Student 2", key="s2")

def add_edge():
    a = st.session_state.s1.strip()
    b = st.session_state.s2.strip()

    edge = tuple(sorted((a,b)))

    if not a or not b:
        st.warning("Enter both students")

    elif a == b:
        st.warning("Same student")

    elif edge not in st.session_state.edges:
        st.session_state.edges.append(edge)
        st.success("Friendship Added")

    else:
        st.warning("Already Exists")

    st.session_state.s1=""
    st.session_state.s2=""

col1,col2,col3 = st.columns(3)

with col1:
    st.button("Add", on_click=add_edge)

with col2:
    if st.button("Reset"):
        st.session_state.edges=[]
        st.rerun()

with col3:
    if st.button("Example Data"):
        st.session_state.edges=[
("A","B"),
("A","C"),
("B","C"),
("C","D"),
("D","E"),
("E","F"),
("F","G"),
("E","G"),
("H","I")
]

# Graph
G = nx.Graph()
G.add_edges_from(st.session_state.edges)

# Table
df = pd.DataFrame(st.session_state.edges, columns=["Student 1","Student 2"])

if st.session_state.edges:

    st.subheader("Friendship Table")
    st.table(df)

    st.subheader("Network Graph")

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, seed=2)

    nx.draw(G,pos,with_labels=True,node_size=2000,font_size=12,ax=ax)

    ax.axis("off")
    st.pyplot(fig)

# ---------------- CENTRALITY ----------------

    st.subheader("Graph Metrics")

    degree = nx.degree_centrality(G)
    closeness = nx.closeness_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    metrics_df = pd.DataFrame({
        "Student":list(degree.keys()),
        "Degree":list(degree.values()),
        "Closeness":list(closeness.values()),
        "Betweenness":list(betweenness.values())
    })

    st.table(metrics_df)

# ---------------- CONNECTIVITY ----------------

    st.subheader("Connectivity Analysis")

    st.info(f"Number of Connected Components: {nx.number_connected_components(G)}")

    components = list(nx.connected_components(G))

    for i,c in enumerate(components):
        st.write(f"Group {i+1}:", list(c))

# ---------------- COMMUNITY DETECTION ----------------

    st.subheader("Community Detection")

    from networkx.algorithms.community import greedy_modularity_communities

    comm = greedy_modularity_communities(G)

    for i,c in enumerate(comm):
        st.success(f"Community {i+1}: {list(c)}")

# ---------------- BAR CHART ----------------

    st.subheader("Centrality Comparison")

    plot_df = metrics_df.set_index("Student")

    fig2, ax2 = plt.subplots()

    plot_df.plot(kind="bar", ax=ax2)

    ax2.set_ylabel("Value")
    st.pyplot(fig2)
