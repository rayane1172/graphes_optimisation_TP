import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import os
from Graph import Graph


class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Algorithm Application")
        self.master.geometry("400x500")

        # Main Frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # File Selection Section
        self.file_label = tk.Label(
            self.main_frame, text="Add Graph", font=("Arial", 12, "bold")
        )
        self.file_label.pack(pady=(0, 10))

        self.select_file_btn = tk.Button(
            self.main_frame, text="Select JSON File", command=self.load_graph_from_file
        )
        self.select_file_btn.pack(pady=5)

        # Manual Input Section
        self.manual_input_btn = tk.Button(
            self.main_frame,
            text="Create Graph Manually",
            command=self.create_graph_manually,
        )
        self.manual_input_btn.pack(pady=5)

        # Algorithms Section
        self.algo_label = tk.Label(
            self.main_frame, text="Graph Algorithms", font=("Arial", 12, "bold")
        )
        self.algo_label.pack(pady=(10, 5))

        # Algorithm Buttons
        algo_buttons = [
            ("Breadth First Search (BFS)", self.run_bfs),
            ("Is Tree Check", self.run_is_tree),
            ("Transitive Closure", self.run_transitive_closure),
            ("RLF Coloring", self.run_rlf),
            ("DSATUR Coloring", self.run_dsatur),
            ("Welsh-Powell Coloring", self.run_welsh_powell),
            ("Visualize Graph", self.visualize_graph),
        ]

        self.algo_buttons = []
        for text, command in algo_buttons:
            btn = tk.Button(
                self.main_frame, text=text, command=command, state=tk.DISABLED
            )
            btn.pack(pady=3)
            self.algo_buttons.append(btn)

        self.graph = None

    def load_graph_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    graph_dict = json.load(file)
                self.graph = Graph(graph_dict)
                self.enable_algo_buttons()
                messagebox.showinfo("Success", "Graph loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load graph: {str(e)}")

    def create_graph_manually(self):
        graph_dict = {}
        while True:
            node = simpledialog.askstring(
                "Input", "Enter a node (or press Cancel to finish):"
            )
            if not node:
                break
            neighbors = simpledialog.askstring(
                "Input", f"Enter neighbors for {node} (comma-separated):"
            )
            if neighbors:
                graph_dict[node] = [n.strip() for n in neighbors.split(",")]

        if graph_dict:
            self.graph = Graph(graph_dict)
            self.enable_algo_buttons()
            messagebox.showinfo("Success", "Graph created successfully!")

    def enable_algo_buttons(self):
        for btn in self.algo_buttons:
            btn.config(state=tk.NORMAL)

    def run_bfs(self):
        if self.graph:
            start_node = simpledialog.askstring("Input", "Enter start node for BFS:")
            if start_node in self.graph.graph:
                result = self.graph.BFS(start_node)
                messagebox.showinfo("BFS Result", str(result))
            else:
                messagebox.showerror("Error", "Invalid start node")

    def run_is_tree(self):
        if self.graph:
            is_tree = self.graph.is_tree()
            messagebox.showinfo("Tree Check", f"Is the graph a tree? {is_tree}")

    def run_transitive_closure(self):
        if self.graph:
            closed_graph = self.graph.fermeture_transitive()
            closed_graph.display_graph()
            messagebox.showinfo(
                "Transitive Closure", "Closure graph printed in console"
            )

    def run_rlf(self):
        if self.graph:
            self.graph.RLF()

    def run_dsatur(self):
        if self.graph:
            self.graph.dsatur_algo()

    def run_welsh_powell(self):
        if self.graph:
            self.graph.welsh_powell()

    def visualize_graph(self):
        if self.graph:
            self.graph.visualize()


def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# test_graph = {
#     "A": ["B", "E"],
#     "B": ["C", "A", "D"],
#     "C": ["B", "E"],
#     "D": ["B"],
#     "E": ["A", "C"],
# }

# test_graph2 = {"A": ["B"], "B": ["A"], "C": []}

# test_graph_is_tree = {
#     "A": ["B", "C"],
#     "B": ["A", "D", "E"],
#     "C": ["A"],
#     "D": ["B"],
#     "E": ["B"],
# }
# test_graph_dict = {
#     "A": ["B", "C", "D", "E"],
#     "B": ["A", "C", "F"],
#     "C": ["A", "B", "G", "H"],
#     "D": ["A", "E", "I"],
#     "E": ["A", "D", "J"],
#     "F": ["B", "G", "K"],
#     "G": ["C", "F", "L", "H"],
#     "H": ["C", "G", "M", "N"],
#     "I": ["D", "J", "O"],
#     "J": ["E", "I", "P"],
#     "K": ["F", "L"],
#     "L": ["G", "K", "M"],
#     "M": ["H", "L", "N"],
#     "N": ["H", "M"],
#     "O": ["I", "P"],
#     "P": ["J", "O"],
# }
