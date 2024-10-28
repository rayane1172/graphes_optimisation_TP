from collections import deque
from Graph import Graph

exit_program = False
mon_graph = Graph()


test_graph = {
    "A": ["B", "E"],
    "B": ["C", "A","D"],
    "C": ["B","E"],
    "D": ["B"],
    "E": ["A","C"]
}

test_graph2 = {
    "A": ["B"],
    "B": ["A"],
    "C": []
}

test_graph_is_tree = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A"],
    "D": ["B"],
    "E": ["B"]
}
test_graph_dict = {
        "A": ["B", "E"],
        "B": ["C", "A", "D"],
        "C": ["B", "E"],
        "D": ["B"],
        "E": ["A", "C"]
    }

test_graph = Graph(test_graph)
test_graph_is_tree = Graph(test_graph_is_tree)
test_graph2 = Graph(test_graph2)
test_graph_dict = Graph(test_graph_dict)

# test_graph.display_graph()
# print(test_graph.BFS(start_node="A"))
# print(test_graph.is_tree())

print("-"*15)

test_graph2.display_graph()

print(test_graph2.BFS(start_node="A"))

print(f"Est ce que le graphe est un ARBRE ? -> {test_graph.is_tree()}")

test_graph2.fermeture_transitive().display_graph()
test_graph2.visualize()
test_graph2.welsh_powell()

color_assignment = test_graph.welsh_powell()
print("Color assignment:", color_assignment)

# while not exit_program:
#     print("Donner moi votre graphe d'abord ".center(20, "*"))
#     n = int(input("Donner moi le nombre de nœuds -> "))

#     # Generate nodes using letters (A, B, C, ...)
#     nodesName = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

#     for i in range(n):
#         print(f"Node-{nodesName[i]}")
#         node1 = nodesName[i]
#         node2_input = input("|-> Go to (separated nodes names with -,-) -> ")
#         node2_list = node2_input.split(",")

#         for node2 in node2_list:
#             node2 = node2.strip()
#             if node2 == "": continue # input vide of nodes relation
#             if node2 in nodesName :  # Ensure the input node exists in the generated nodes (alphabet majiscule)
#                 mon_graph.add_edge(node1, node2)
#             else:
#                 print(f"Node {node2} does not exist. Please use valid node names.")

#     mon_graph.display_graph()

#     while True:
#         print("Menu:".center(20,"*"))
#         print("1. BFS")
#         print("2. Check if the graph is a tree")
#         print("3. Exit")
#         choice = input("Choose an option (1, 2, or 3) -> ")

#         if choice == '1':
#                 start_node = input("\nEnter the start node for BFS -> (A,B,C...)->")
#                 if start_node in mon_graph.graph:
#                     bfs_result = mon_graph.BFS(start_node)
#                     print(f"\n\t--> BFS result: {bfs_result}")
#                 else:
#                     print("Node not found in the graph.")
#         elif choice == '2':
#                 if mon_graph.is_tree():
#                     print("----> The graph is a tree.")
#                 else:
#                     print("----> The graph is not a tree.")
#         elif choice == '3':
#             exit_program = True
#             print("Exiting the program.")
#             break
#         else:
#             print("Invalid choice, please try again.")
