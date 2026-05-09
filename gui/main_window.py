import tkinter as tk
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.ids import ids
from algorithms.greedy import greedy
from algorithms.astar import astar
from core.graph import Graph
from visualization.graph_visualizer import visualize

class GraphSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Search System")
        self.root.configure(bg="#2E3440")
        self.graph = Graph()

        # ── Main PanedWindow splits window LEFT | RIGHT ──────
        paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#2E3440",
                               sashwidth=6, sashrelief="raised")
        paned.pack(fill="both", expand=True)

        # ── LEFT SIDE — scrollable input panel ───────────────
        left_container = tk.Frame(paned, bg="#2E3440", width=420)
        left_container.pack_propagate(False)
        paned.add(left_container, minsize=380)

        canvas_scroll = tk.Canvas(left_container, bg="#2E3440", highlightthickness=0)
        scrollbar = tk.Scrollbar(left_container, orient="vertical", command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)

        left_panel = tk.Frame(canvas_scroll, bg="#2E3440")
        canvas_scroll.create_window((0, 0), window=left_panel, anchor="nw")

        def on_frame_configure(e):
            canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        left_panel.bind("<Configure>", on_frame_configure)

        # ── RIGHT SIDE — visualization panel ─────────────────
        right_container = tk.Frame(paned, bg="#2E3440")
        paned.add(right_container, minsize=400)

        self.viz_frame = tk.LabelFrame(right_container, text="Visualization",
                                       padx=5, pady=5, bg="#3B4252", fg="white")
        self.viz_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ── Node Frame ───────────────────────────────────────
        node_frame = tk.LabelFrame(left_panel, text="Nodes", padx=10, pady=10,
                                   bg="#3B4252", fg="white")
        node_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(node_frame, text="Node Name", bg="#3B4252", fg="white").grid(row=0, column=0, padx=5)
        self.node_entry = tk.Entry(node_frame, bg="#ECEFF4", fg="black", width=20)
        self.node_entry.grid(row=0, column=1, padx=5)
        tk.Button(node_frame, text="Add Node", command=self.add_node,
                  bg="#88C0D0", fg="black", activebackground="#81A1C1").grid(row=0, column=2, padx=5)
        self.node_list = tk.Listbox(node_frame, height=5, bg="#4C566A", fg="white")
        self.node_list.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)

        # ── Edge Frame ───────────────────────────────────────
        edge_frame = tk.LabelFrame(left_panel, text="Edges", padx=10, pady=10,
                                   bg="#3B4252", fg="white")
        edge_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(edge_frame, text="node1, node2, weight", bg="#3B4252", fg="white").grid(row=0, column=0, padx=5)
        self.edge_entry = tk.Entry(edge_frame, bg="#ECEFF4", fg="black", width=20)
        self.edge_entry.grid(row=0, column=1, padx=5)
        tk.Button(edge_frame, text="Add Edge", command=self.add_edge,
                  bg="#88C0D0", fg="black", activebackground="#81A1C1").grid(row=0, column=2, padx=5)
        self.edge_list = tk.Listbox(edge_frame, height=5, bg="#4C566A", fg="white")
        self.edge_list.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)

        # ── Heuristic Frame ──────────────────────────────────
        heuristic_frame = tk.LabelFrame(left_panel, text="Heuristics", padx=10, pady=10,
                                        bg="#3B4252", fg="white")
        heuristic_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(heuristic_frame, text="node, value", bg="#3B4252", fg="white").grid(row=0, column=0, padx=5)
        self.heuristic_entry = tk.Entry(heuristic_frame, bg="#ECEFF4", fg="black", width=20)
        self.heuristic_entry.grid(row=0, column=1, padx=5)
        tk.Button(heuristic_frame, text="Add Heuristic", command=self.add_heuristic,
                  bg="#88C0D0", fg="black", activebackground="#81A1C1").grid(row=0, column=2, padx=5)
        self.heuristic_list = tk.Listbox(heuristic_frame, height=5, bg="#4C566A", fg="white")
        self.heuristic_list.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)

        # ── Control Frame ────────────────────────────────────
        control_frame = tk.LabelFrame(left_panel, text="Controls", padx=10, pady=10,
                                      bg="#3B4252", fg="white")
        control_frame.pack(padx=10, pady=5, fill="x")

        tk.Label(control_frame, text="Start Node", bg="#3B4252", fg="white").grid(row=0, column=0, padx=5, pady=3)
        self.start_entry = tk.Entry(control_frame, bg="#ECEFF4", fg="black", width=20)
        self.start_entry.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Goal Node", bg="#3B4252", fg="white").grid(row=1, column=0, padx=5, pady=3)
        self.goal_entry = tk.Entry(control_frame, bg="#ECEFF4", fg="black", width=20)
        self.goal_entry.grid(row=1, column=1, padx=5)

        self.algorithm_var = tk.StringVar(value="BFS")
        tk.OptionMenu(control_frame, self.algorithm_var,
                      "BFS", "DFS", "UCS", "IDS", "Greedy", "A*").grid(row=2, column=0, columnspan=2, pady=5)

        tk.Button(control_frame, text="Run Search", command=self.run_search,
                  bg="#A3BE8C", fg="black", activebackground="#8FBC8F").grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(control_frame, text="Clear Graph", command=self.clear_graph,
                  bg="#BF616A", fg="white", activebackground="#A34B4B").grid(row=3, column=2, pady=5)

        # ── Output Frame ─────────────────────────────────────
        output_frame = tk.LabelFrame(left_panel, text="Output", padx=10, pady=10,
                                     bg="#3B4252", fg="white")
        output_frame.pack(padx=10, pady=5, fill="x")

        self.output_text = tk.Text(output_frame, height=6, wrap="word",
                                   bg="#4C566A", fg="white")
        self.output_text.pack(fill="both", expand=True)

        # ── Draw placeholder on startup ───────────────────────
        self.root.after(200, self.refresh_visualization)

    # ── Methods ──────────────────────────────────────────────

    def add_node(self):
        node = self.node_entry.get().strip()
        if node and node not in self.graph.edges:
            self.graph.edges[node] = []
            self.node_list.insert(tk.END, node)
            self.node_entry.delete(0, tk.END)
            self.refresh_visualization()
        else:
            self.output_text.insert(tk.END, "Invalid or duplicate node.\n")

    def add_edge(self):
        try:
            parts  = self.edge_entry.get().split(",")
            node1  = parts[0].strip()
            node2  = parts[1].strip()
            weight = int(parts[2].strip())
            if node1 in self.graph.edges and node2 in self.graph.edges:
                self.graph.add_edge(node1, node2, weight)
                self.edge_list.insert(tk.END, f"{node1} --{weight}--> {node2}")
                self.edge_entry.delete(0, tk.END)
                self.refresh_visualization()
            else:
                self.output_text.insert(tk.END, "Both nodes must exist before adding an edge.\n")
        except:
            self.output_text.insert(tk.END, "Invalid edge format. Use: node1, node2, weight\n")

    def add_heuristic(self):
        try:
            parts = self.heuristic_entry.get().split(",")
            node  = parts[0].strip()
            value = int(parts[1].strip())
            if node in self.graph.edges:
                self.graph.add_heuristic(node, value)
                self.heuristic_list.insert(tk.END, f"{node} = {value}")
                self.heuristic_entry.delete(0, tk.END)
                self.refresh_visualization()
            else:
                self.output_text.insert(tk.END, "Node must exist before adding heuristic.\n")
        except:
            self.output_text.insert(tk.END, "Invalid heuristic format. Use: node, value\n")

    def refresh_visualization(self, path=None):
        visualize(
            self.graph,
            path=path,
            heuristics=self.graph.heuristics if self.graph.heuristics else None,
            canvas_frame=self.viz_frame
        )

    def run_search(self):
        start = self.start_entry.get().strip()
        goal  = self.goal_entry.get().strip()
        algo  = self.algorithm_var.get()

        if start not in self.graph.edges or goal not in self.graph.edges:
            self.output_text.insert(tk.END, "Start or goal node does not exist in the graph.\n")
            return

        if algo == "BFS":
            path, cost = bfs(self.graph, start, goal)
        elif algo == "DFS":
            path, cost = dfs(self.graph, start, goal)
        elif algo == "UCS":
            path, cost = ucs(self.graph, start, goal)
        elif algo == "IDS":
            path, cost = ids(self.graph, start, goal)
        elif algo == "Greedy":
            if not self.graph.heuristics:
                self.output_text.insert(tk.END, "Heuristic values required for Greedy search.\n")
                return
            path, cost = greedy(self.graph, start, goal)
        elif algo == "A*":
            if not self.graph.heuristics:
                self.output_text.insert(tk.END, "Heuristic values required for A* search.\n")
                return
            path, cost = astar(self.graph, start, goal)
        else:
            path, cost = None, None

        self.output_text.delete(1.0, tk.END)
        if path:
            self.output_text.insert(tk.END, f"Algorithm : {algo}\n")
            self.output_text.insert(tk.END, f"Path      : {' -> '.join(path)}\n")
            self.output_text.insert(tk.END, f"Cost      : {cost}\n")
            self.refresh_visualization(path=path)
        else:
            self.output_text.insert(tk.END, "No path found.\n")
            self.refresh_visualization()

    def clear_graph(self):
        self.graph = Graph()
        self.node_list.delete(0, tk.END)
        self.edge_list.delete(0, tk.END)
        self.heuristic_list.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.start_entry.delete(0, tk.END)
        self.goal_entry.delete(0, tk.END)
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        self.refresh_visualization()
