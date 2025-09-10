# src/visualize_demo.py
import matplotlib.pyplot as plt
import networkx as nx

try:
    from . import flow   # force decorators to run
    from .annotations import build_graph
    from .adaptbd import critical_path
except ImportError:
    import flow
    from annotations import build_graph
    from adaptbd import critical_path


def visualize_graph():
    # Get graph components
    V, E, W, Q = build_graph()

    # Build graph
    G = nx.DiGraph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    # Compute critical path
    crit_path = critical_path(V, E, W, Q)

    # Node colors: red for query, blue for others
    node_colors = ["red" if v in Q else "skyblue" for v in G.nodes]

    # Layout
    pos = nx.shell_layout(G)

    # --- Figure with 2 subplots: Graph + Table ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6),
                                   gridspec_kw={"width_ratios": [2, 1]})

    # ===================== Graph Panel =====================
    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors,
                           node_size=2200,
                           edgecolors="black",
                           ax=ax1)
    nx.draw_networkx_edges(G, pos,
                           edge_color="gray",
                           arrows=True,
                           width=1.5,
                           ax=ax1)

    if crit_path and len(crit_path) > 1:
        crit_edges = [(crit_path[i], crit_path[i+1]) for i in range(len(crit_path)-1)]
        nx.draw_networkx_edges(G, pos,
                               edgelist=crit_edges,
                               edge_color="red",
                               arrows=True,
                               width=3,
                               ax=ax1)

    # Labels
    labels = {v: v for v in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels,
                            font_size=10, font_color="black", ax=ax1)

    # Weights under nodes
    weight_labels = {v: f"W={W.get(v,1)}" for v in G.nodes}
    weight_pos = {v: (pos[v][0], pos[v][1] - 0.08) for v in G.nodes}
    nx.draw_networkx_labels(G, weight_pos, labels=weight_labels,
                            font_size=9, font_color="darkgreen", ax=ax1)

    ax1.set_title("Adaptivity Flow Graph (DIGIVOTE Demo)", fontsize=12)
    ax1.axis("off")

    # ===================== Table Panel =====================
    # Make table data
    table_data = [[v, W.get(v, 1)] for v in G.nodes]

    table = ax2.table(cellText=table_data,
                      colLabels=["Node", "Weight"],
                      loc="center",
                      cellLoc="center",
                      colWidths=[0.5, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    ax2.set_title("Weights Table", fontsize=12)
    ax2.axis("off")  # Hide axes behind table

    plt.tight_layout()
    plt.show(block=True)


if __name__ == "__main__":
    visualize_graph()
