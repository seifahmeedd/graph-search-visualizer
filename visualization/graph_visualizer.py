import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Keep a reference to the canvas so we can clear it on next call
_current_canvas = None

def visualize(graph, path=None, heuristics=None, canvas_frame=None):
    """
    Draws the graph embedded inside a tkinter frame.
    - graph        : your Graph object
    - path         : list of nodes representing the solution path
    - heuristics   : dict of {node: h_value} for informed search
    - canvas_frame : the tkinter frame to embed the plot in
    """
    global _current_canvas

    # ── Clear previous drawing ──────────────────────────────
    if _current_canvas:
        _current_canvas.get_tk_widget().destroy()
        _current_canvas = None

    # Clear all widgets inside the frame
    if canvas_frame:
        for widget in canvas_frame.winfo_children():
            widget.destroy()

    # ── Build networkx graph ────────────────────────────────
    G = nx.DiGraph()
    for node, neighbors in graph.edges.items():
        G.add_node(node)
        for neighbor, weight in neighbors:
            G.add_edge(node, neighbor, weight=weight)

    if len(G.nodes) == 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("#2E3440")
        ax.set_facecolor("#3B4252")
        ax.text(0.5, 0.5, "Add nodes and edges\nto see the graph here",
                ha="center", va="center", fontsize=14,
                color="white", transform=ax.transAxes)
        ax.axis("off")
        plt.tight_layout()
        if canvas_frame:
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        return

    # ── Layout ──────────────────────────────────────────────
    pos = nx.spring_layout(G, seed=42)  # seed=42 keeps layout stable

    # ── Node colors ─────────────────────────────────────────
    node_colors = []
    for node in G.nodes:
        if path and node == path[0] and node == path[-1]:
            node_colors.append("gold")          # start == goal
        elif path and node == path[0]:
            node_colors.append("gold")          # start node
        elif path and node == path[-1]:
            node_colors.append("tomato")        # goal node
        elif path and node in path:
            node_colors.append("lightgreen")    # nodes along path
        else:
            node_colors.append("lightblue")     # regular nodes

    # ── Draw figure ─────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor("#2E3440")  # match app dark background
    ax.set_facecolor("#3B4252")

    # Draw all edges
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color="#88C0D0",
        arrows=True,
        arrowsize=20,
        width=1.5
    )

    # Highlight path edges
    if path and len(path) > 1:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edgelist=path_edges,
            edge_color="orange",
            arrows=True,
            arrowsize=25,
            width=3.5
        )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        node_size=1000
    )

    # Draw node labels — include heuristic if available
    if heuristics:
        labels = {
            node: f"{node}\nh={heuristics[node]}"
            if node in heuristics else node
            for node in G.nodes
        }
    else:
        labels = {node: node for node in G.nodes}

    nx.draw_networkx_labels(
        G, pos, labels=labels, ax=ax,
        font_color="black", font_size=9, font_weight="bold"
    )

    # Draw edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, ax=ax,
        font_color="white",
        font_size=9,
        font_weight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#4C566A", edgecolor="none", alpha=0.85)
    )

    # ── Legend ───────────────────────────────────────────────
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="gold",       label="Start Node"),
        Patch(facecolor="tomato",     label="Goal Node"),
        Patch(facecolor="lightgreen", label="Path Node"),
        Patch(facecolor="lightblue",  label="Other Node"),
    ]
    ax.legend(handles=legend_elements, loc="upper left",
              facecolor="#4C566A", labelcolor="white", fontsize=8)

    ax.set_title("Graph Visualization", color="white", fontsize=11)
    ax.axis("off")
    plt.tight_layout()

    # ── Embed in tkinter frame ───────────────────────────────
    if canvas_frame:
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        _current_canvas = canvas
    else:
        plt.show()  # fallback if no frame given
