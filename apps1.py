import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

st.title("Corporate Email Network Simulation")

st.markdown("""
### Project Overview

This project simulates a **corporate email communication network** using **graph theory**.

- **Nodes** represent employees in a company.
- **Edges** represent email communication between employees.

By creating this network, we can analyze how employees communicate and identify **important communicators** in the organization.

---
### Objectives
- Model email communication using a **graph structure**
- Visualize communication between employees
- Identify **key communicators** using centrality measures
- Understand how information flows in a network

---

### How to Use

1. Enter **Employee 1** and **Employee 2**
2. Click **Add Edge**
3. The table will show all connections
4. The graph displays the communication network
5. Click **RESET** to clear the graph
6. Or click **Example Data** to load an example balanced dataset for demonstration.

---

This project demonstrates how **graph modeling can analyze communication patterns in organizations.**
""")

if "edge" not in st.session_state:
    st.session_state.edge = []
st.subheader("Add Edges")
node1=st.text_input("Enter Node 1", key="node1")
node2=st.text_input("Enter Node 2", key="node2")
if "refresh_graph" not in st.session_state:
    st.session_state.refresh_graph = False
def add_edge(): 
    node1 = st.session_state.node1.strip()
    node2 = st.session_state.node2.strip()
    edge = tuple(sorted((node1, node2)))
    if not node1 or not node2:
        st.warning("Please add both nodes")
    elif node1 == node2:
        st.warning("Nodes are Same")    
    elif edge not in st.session_state.edge:
        st.session_state.edge.append(edge)
        st.session_state.refresh_graph = True
        st.success("Edge Added Successfully!")
    else:
        st.warning("Edge Already Exists")
    st.session_state.node1 = ""
    st.session_state.node2 = ""

col1, col2, col3 = st.columns(3)

with col1:
    add = st.button("Add Edge", on_click=add_edge)

with col2:
    reset = st.button("RESET")

with col3:
    example = st.button("Example Data")
if example:
    st.session_state.edge=[
("E1","E2"),
("E1","E3"),
("E2","E4"),
("E3","E4"),
("E4","E5"),
("E5","E6"),
("E3","E6")
]
if reset:
    st.session_state.edge=[]
    st.rerun()
G = nx.Graph()
G.add_edges_from(st.session_state.edge)

df = pd.DataFrame(st.session_state.edge, columns=["Node 1", "Node 2"])
if  st.session_state.edge:
    st.table(df)
    st.subheader("Graphical Representation :")
    fig, ax = plt.subplots()

    pos = nx.spring_layout(G, seed=1)

    nx.draw(
        G,
        pos=pos,
        with_labels=True,
        node_size=2000,
        font_size=14,
        ax=ax
    )

    ax.axis("off")

    st.pyplot(fig)

    st.session_state.refresh_graph = False

# Centrality Analysis

    st.subheader("Centrality Analysis (Key Communicators)")

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    centrality_df = pd.DataFrame({
        "Employee": list(degree.keys()),
        "Degree Centrality": list(degree.values()),
        "Betweenness Centrality": list(betweenness.values()),
        "Closeness Centrality": list(closeness.values())
    })

    # Find key communicators
    max_degree = centrality_df["Degree Centrality"].max()
    max_bet = centrality_df["Betweenness Centrality"].max()
    max_close = centrality_df["Closeness Centrality"].max()

    roles = []

    for i, row in centrality_df.iterrows():
        role = []

        if row["Degree Centrality"] == max_degree:
            role.append("Most Active Communicator")

        if row["Betweenness Centrality"] == max_bet:
            role.append("Bridge / Key Communicator")

        if row["Closeness Centrality"] == max_close:
            role.append("Fast Information Spreader")

        roles.append(", ".join(role))

    centrality_df["Meaning / Role"] = roles

    st.table(centrality_df)
    # Get max values
    max_degree = centrality_df["Degree Centrality"].max()
    max_bet = centrality_df["Betweenness Centrality"].max()
    max_close = centrality_df["Closeness Centrality"].max()

    # Get employees with those values
    top_degree = centrality_df[centrality_df["Degree Centrality"] == max_degree]["Employee"].tolist()
    top_betweenness = centrality_df[centrality_df["Betweenness Centrality"] == max_bet]["Employee"].tolist()
    top_closeness = centrality_df[centrality_df["Closeness Centrality"] == max_close]["Employee"].tolist()

    st.subheader("Key Communication Insights")

    st.success(f"Most Active Communicator(s): {', '.join(top_degree)}")

    st.info(f"Bridge / Key Communicator(s): {', '.join(top_betweenness)}")

    st.warning(f"Fast Information Spreader(s): {', '.join(top_closeness)}")

    st.markdown("""
    ### What these measures mean:

    **Degree Centrality**
    - Shows how many direct connections an employee has.
    - Higher value means the employee communicates with many others.

    **Betweenness Centrality**
    - Shows how often an employee acts as a bridge between others.
    - High value indicates a **key coordinator or manager** in communication flow.

    **Closeness Centrality**
    - Measures how quickly an employee can reach all others in the network.
    - Higher value means faster information spreading.

    These measures help identify **important communicators in the corporate email network.**
    """)
    if not (df.empty):
        
        st.subheader("Centrality Comparison Chart")
    # Set employee names as index for plotting
        plot_df = centrality_df.set_index("Employee")

        fig, ax = plt.subplots()

        plot_df[["Degree Centrality","Betweenness Centrality","Closeness Centrality"]].plot(
            kind="bar",
            ax=ax
        )

        ax.set_ylabel("Centrality Value")
        ax.set_title("Employee Centrality Measures")
        ax.legend()

        st.pyplot(fig)
