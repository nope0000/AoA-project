import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

class GraphVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("FINDING MST WITH PRIM AND KRUSKAL")

        # Create a frame for buttons
        button_frame = tk.Frame(self.master)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Create buttons for different input types
        self.adj_matrix_button = ttk.Button(button_frame, text="Input Adjacency Matrix", command=self.input_adj_matrix)
        self.adj_matrix_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.adj_list_button = ttk.Button(button_frame, text="Input Adjacency List", command=self.input_adj_list)
        self.adj_list_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.prim_button = ttk.Button(button_frame, text="Prim", command=self.find_prim)
        self.prim_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.kruskal_button = ttk.Button(button_frame, text="Kruskal", command=self.find_kruskal)
        self.kruskal_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.org_graph_button = ttk.Button(button_frame, text="Original", command=self.org_graph)
        self.org_graph_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.graph = nx.Graph()

        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.axis('off')
        self.canvas_widget = FigureCanvasTkAgg(self.fig, self.canvas)
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def clear_graph(self):
        """Clear the graph and the figure for a new query."""
        self.graph.clear()  # Clear the graph data
        self.ax.clear()  # Clear the figure
        self.ax.axis('off')  # Turn off the axis
        self.canvas_widget.draw()  # Update the canvas

    def input_adj_matrix(self):
        self.clear_graph()  # Clear the graph data

        # Ask for the number of nodes
        num_nodes = tk.simpledialog.askinteger("Input", "Enter number of nodes:")

        if num_nodes:
            adj_matrix = []

            # Prompt the user for each row of the adjacency matrix
            for i in range(num_nodes):
                row_str = tk.simpledialog.askstring("Input", f"Enter adjacency row for node {i + 1} (space-separated):")
                row = list(map(int, row_str.split()))
                adj_matrix.append(row)

            adj_matrix = np.array(adj_matrix)

            # Create the graph from adjacency matrix
            self.create_graph_from_adj_matrix(adj_matrix)
            self.draw_graph()

    def input_adj_list(self):
        self.clear_graph()  # Clear the graph data

        # Ask for the number of nodes
        num_nodes = tk.simpledialog.askinteger("Input", "Enter number of nodes:")

        if num_nodes:
            # Create an empty adjacency matrix (DataFrame)
            adj_df = pd.DataFrame(0, index=range(1, num_nodes + 1), columns=range(1, num_nodes + 1))

            # Prompt the user for each node's adjacency list
            for i in range(num_nodes):
                neighbors_str = tk.simpledialog.askstring("Input", f"Enter neighbors and weights for node {i + 1} (format: neighbor,weight neighbor,weight ...):")
                if neighbors_str:
                    neighbors = neighbors_str.split()
                    for neighbor_str in neighbors:
                        neighbor, weight = neighbor_str.split(',')
                        neighbor = int(neighbor)
                        weight = float(weight)
                        adj_df.at[i + 1, neighbor] = weight  # Store weight in the adjacency matrix

            # Create the graph from adjacency list
            self.create_graph_from_adj_list(adj_df)
            self.draw_graph()

    def create_graph_from_adj_matrix(self, adj_matrix):
        # Create graph from adjacency matrix
        self.graph = nx.from_numpy_array(adj_matrix)

    def create_graph_from_adj_list(self, adj_df):
        # Create graph from adjacency list
        self.graph = nx.Graph(adj_df)

    def draw_graph(self, MST=None):
        # Clear the existing figure and axis
        self.ax.clear()

        # Draw the graph using NetworkX
        pos = nx.spring_layout(self.graph)  # Layout for the nodes
        if MST is None:
            print(self.graph.edges.items())
            nx.draw(self.graph, pos, with_labels=True, ax=self.ax, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
            org_edge_labels = nx.get_edge_attributes(self.graph, 'weight')
            nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=org_edge_labels, ax=self.ax)
        else:
            nx.draw(MST, pos, with_labels=True, ax=self.ax, node_color='lightgreen', edge_color='gray', node_size=500, font_size=10)
            mst_edge_labels = nx.get_edge_attributes(MST, 'weight')
            nx.draw_networkx_edge_labels(MST, pos, edge_labels=mst_edge_labels, ax=self.ax)

        self.canvas_widget.draw()

    def find_prim(self):
        prim = nx.minimum_spanning_tree(self.graph, algorithm='prim')
        self.master.title('Prim')
        self.draw_graph(prim)

    def find_kruskal(self):
        prim = nx.minimum_spanning_tree(self.graph, algorithm='kruskal')
        self.master.title('Kruskal')
        self.draw_graph(prim)

    def org_graph(self):
        self.master.title('Original Graph')
        self.draw_graph()


def main():
    root = tk.Tk()

    # Initialize the GraphVisualizer with the Tkinter root
    app = GraphVisualizer(master=root)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
