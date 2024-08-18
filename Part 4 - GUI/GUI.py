import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random


class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Prim & Kruskal Visualization")

        self.graph = nx.Graph()
        self.pos = {}  # For storing node positions

        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.mode = tk.StringVar(value="draw")
        tk.Label(master, text="Select Mode:").pack(side=tk.LEFT)
        tk.OptionMenu(master, self.mode, "draw", "adjacency_matrix", "adjacency_list").pack(side=tk.LEFT)

        self.add_node_button = tk.Button(self.master, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side=tk.LEFT)

        self.add_edge_button = tk.Button(self.master, text="Add Edge", command=self.add_edge)
        self.add_edge_button.pack(side=tk.LEFT)

        self.prim_button = tk.Button(self.master, text="Show Prim's MST", command=self.show_prim_mst)
        self.prim_button.pack(side=tk.RIGHT)

        self.kruskal_button = tk.Button(self.master, text="Show Kruskal's MST", command=self.show_kruskal_mst)
        self.kruskal_button.pack(side=tk.RIGHT)

        self.draw_graph()

    def add_node(self):
        if self.mode.get() == "draw":
            self.add_node_draw_mode()
        elif self.mode.get() == "adjacency_matrix":
            self.add_node_matrix_mode()
        elif self.mode.get() == "adjacency_list":
            self.add_node_list_mode()

    def add_node_draw_mode(self):
        label = simpledialog.askstring("Node Label", "Enter node label:", parent=self.master)
        if label:
            self.graph.add_node(label)
            self.pos[label] = (random.uniform(0.1, 0.9), random.uniform(0.1, 0.9))
            self.draw_graph()

    def add_node_matrix_mode(self):
        num_nodes = simpledialog.askinteger("Input", "Enter number of nodes:", parent=self.master)
        self.graph.clear()
        self.pos.clear()

        matrix = []
        for i in range(num_nodes):
            row = simpledialog.askstring("Input", f"Enter row {i + 1} of adjacency matrix (comma-separated):",
                                         parent=self.master)
            matrix.append(list(map(int, row.split(','))))

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if matrix[i][j] > 0:
                    self.graph.add_edge(i, j, weight=matrix[i][j])

        self.pos = nx.spring_layout(self.graph)  # Recompute positions
        self.draw_graph()

    def add_node_list_mode(self):
        num_nodes = simpledialog.askinteger("Input", "Enter number of nodes:", parent=self.master)
        self.graph.clear()
        self.pos.clear()

        for i in range(num_nodes):
            neighbors = simpledialog.askstring("Input", f"Enter neighbors of node {i} (format: node,weight;node,weight):",
                                               parent=self.master)
            if neighbors:
                for entry in neighbors.split(';'):
                    neighbor, weight = map(int, entry.split(','))
                    self.graph.add_edge(i, neighbor, weight=weight)

        self.pos = nx.spring_layout(self.graph)  # Recompute positions
        self.draw_graph()

    def add_edge(self):
        start = simpledialog.askstring("Start Node", "Enter start node:", parent=self.master)
        end = simpledialog.askstring("End Node", "Enter end node:", parent=self.master)
        weight = simpledialog.askfloat("Weight", "Enter edge weight:", parent=self.master)
        if start and end and weight is not None:
            self.graph.add_edge(start, end, weight=weight)
            self.draw_graph()

    def show_prim_mst(self):
        mst = nx.minimum_spanning_tree(self.graph, algorithm='prim')
        self.draw_graph(mst)

    def show_kruskal_mst(self):
        mst = nx.minimum_spanning_tree(self.graph, algorithm='kruskal')
        self.draw_graph(mst)

    def draw_graph(self, mst=None):
        self.ax.clear()
        if mst:
            nx.draw(mst, pos=self.pos, with_labels=True, ax=self.ax, node_color='lightgreen',
                    edge_color='green', width=2)
        else:
            nx.draw(self.graph, pos=self.pos, with_labels=True, ax=self.ax, node_color='lightblue',
                    edge_color='blue')
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos=self.pos, edge_labels=edge_labels, ax=self.ax)
        self.canvas_widget.draw()


def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
