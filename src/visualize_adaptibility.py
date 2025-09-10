# src/visualize_adaptivity.py
import networkx as nx
import matplotlib.pyplot as plt

def visualize_adaptivity():
    # Define nodes, edges, weights
    vertices = {
        "auth_voter": 1,
        "eligibility_check": 1,
        "submit_vote": 1,
        "audit_review": 1,
        "finalize_count": 1,
        "retry_policy": 3
    }
    edges = [
        ("auth_voter", "eligibility_check"),
        ("eligibility_check", "submit_vote"),
        ("submit_vote", "audit_review"),
        ("audit_review", "finalize_count"),
        ("submit_vote", "finalize_count"),
        ("auth_voter", "retry_policy")
    ]
    query_nodes = {"auth_voter","eligibility_check","submit_vote","audit_review","finalize_count"}

    # Build graph
    G = nx.DiGraph()
    for v,w in vertices.items():
        G.add_node(v, weight=w, query=(v in query_nodes))
    G.add_edges_from(edges)

    # Use graphviz layout (top-to-bottom layered)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    plt.figure(figsize=(8,6))

    # Query nodes = blue, Non-query = gray
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[n for n,d in G.nodes(data=True) if d["query"]],
        node_color="skyblue", node_size=2500, edgecolors="black"
    )
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=[n for n,d in G.nodes(data=True) if not d["query"]],
        node_color="lightgray", node_size=2500, edgecolors="black"
    )

    # Edges
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color="black")

    # Labels with weights
    node_labels = {n: f"{n}\n(w={d['weight']})" for n,d in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9, font_weight="bold")

    plt.title("Adaptivity Flow Diagram for DigiVote (AdaptFun-inspired)", fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    visualize_adaptivity()
