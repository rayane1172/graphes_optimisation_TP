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
        "A": ["B", "C", "D", "E"],
    "B": ["A", "C", "F"],
    "C": ["A", "B", "G", "H"],
    "D": ["A", "E", "I"],
    "E": ["A", "D", "J"],
    "F": ["B", "G", "K"],
    "G": ["C", "F", "L", "H"],
    "H": ["C", "G", "M", "N"],
    "I": ["D", "J", "O"],
    "J": ["E", "I", "P"],
    "K": ["F", "L"],
    "L": ["G", "K", "M"],
    "M": ["H", "L", "N"],
    "N": ["H", "M"],
    "O": ["I", "P"],
    "P": ["J", "O"]
    }

afrique_graph = {
    "Algerie": ["Tunisie", "Libye", "Niger", "Mali", "Mauritanie", "Maroc"],
    "Angola": ["Namibie", "Congo-Brazzaville", "Zambie"],
    "Benin": ["Togo", "Burkina Faso", "Niger", "Nigeria"],
    "Botswana": ["Namibie", "Afrique du Sud", "Zimbabwe", "Zambie"],
    "Burkina Faso": ["Mali", "Niger", "Benin", "Togo", "Ghana", "Cote d'Ivoire"],
    "Burundi": ["Rwanda", "Tanzanie", "Republique Democratique du Congo"],
    "Cameroun": ["Nigeria", "Tchad", "Republique Centrafricaine", "Congo-Brazzaville", "Gabon", "Guinee Equatoriale"],
    "Cap-Vert": [],
    "Republique Centrafricaine": ["Tchad", "Soudan", "Soudan du Sud", "Republique Democratique du Congo", "Cameroun"],
    "Tchad": ["Libye", "Soudan", "Republique Centrafricaine", "Cameroun", "Nigeria", "Niger"],
    "Comores": [],
    "Congo-Brazzaville": ["Cameroun", "Republique Centrafricaine", "Republique Democratique du Congo", "Gabon", "Angola"],
    "Republique Democratique du Congo": ["Republique Centrafricaine", "Soudan du Sud", "Ouganda", "Rwanda", "Burundi", "Tanzanie", "Zambie", "Angola", "Congo-Brazzaville"],
    "Djibouti": ["Erythree", "Ethiopie", "Somalie"],
    "Egypte": ["Libye", "Soudan"],
    "Guinee Equatoriale": ["Cameroun", "Gabon"],
    "Erythree": ["Soudan", "Ethiopie", "Djibouti"],
    "Eswatini": ["Afrique du Sud", "Mozambique"],
    "Ethiopie": ["Erythree", "Djibouti", "Somalie", "Kenya", "Soudan du Sud", "Soudan"],
    "Gabon": ["Guinee Equatoriale", "Cameroun", "Congo-Brazzaville"],
    "Gambie": ["Senegal"],
    "Ghana": ["Cote d'Ivoire", "Burkina Faso", "Togo"],
    "Guinee": ["Senegal", "Mali", "Cote d'Ivoire", "Liberia", "Sierra Leone"],
    "Guinee-Bissau": ["Senegal", "Guinee"],
    "Cote d'Ivoire": ["Liberia", "Guinee", "Mali", "Burkina Faso", "Ghana"],
    "Kenya": ["Ouganda", "Tanzanie", "Somalie", "Soudan du Sud", "Ethiopie"],
    "Lesotho": ["Afrique du Sud"],
    "Liberia": ["Sierra Leone", "Guinee", "Cote d'Ivoire"],
    "Libye": ["Egypte", "Soudan", "Tchad", "Niger", "Algerie", "Tunisie"],
    "Madagascar": [],
    "Malawi": ["Zambie", "Tanzanie", "Mozambique"],
    "Mali": ["Algerie", "Niger", "Burkina Faso", "Cote d'Ivoire", "Guinee", "Senegal", "Mauritanie"],
    "Maroc": ["Algerie"],
    "Mauritanie": ["Senegal", "Mali", "Algerie"],
    "Maurice": [],
    "Mozambique": ["Malawi", "Zambie", "Zimbabwe", "Afrique du Sud", "Eswatini", "Tanzanie"],
    "Namibie": ["Angola", "Zambie", "Botswana", "Afrique du Sud"],
    "Niger": ["Libye", "Tchad", "Nigeria", "Benin", "Burkina Faso", "Mali", "Algerie"],
    "Nigeria": ["Benin", "Niger", "Tchad", "Cameroun"],
    "Ouganda": ["Soudan du Sud", "Kenya", "Tanzanie", "Rwanda", "Republique Democratique du Congo"],
    "Rwanda": ["Ouganda", "Tanzanie", "Burundi", "Republique Democratique du Congo"],
    "Sao Tome-et-Principe": [],
    "Senegal": ["Mauritanie", "Mali", "Guinee", "Guinee-Bissau", "Gambie"],
    "Seychelles": [],
    "Sierra Leone": ["Guinee", "Liberia"],
    "Somalie": ["Djibouti", "Ethiopie", "Kenya"],
    "Afrique du Sud": ["Namibie", "Botswana", "Zimbabwe", "Mozambique", "Lesotho", "Eswatini"],
    "Soudan": ["Egypte", "Libye", "Tchad", "Republique Centrafricaine", "Soudan du Sud", "Ethiopie", "Erythree"],
    "Soudan du Sud": ["Soudan", "Republique Centrafricaine", "Republique Democratique du Congo", "Ouganda", "Kenya", "Ethiopie"],
    "Tanzanie": ["Ouganda", "Rwanda", "Burundi", "Republique Democratique du Congo", "Zambie", "Malawi", "Mozambique", "Kenya"],
    "Togo": ["Ghana", "Burkina Faso", "Benin"],
    "Tunisie": ["Algerie", "Libye"],
    "Zambie": ["Tanzanie", "Malawi", "Mozambique", "Zimbabwe", "Botswana", "Namibie", "Republique Democratique du Congo", "Angola"],
    "Zimbabwe": ["Zambie", "Mozambique", "Afrique du Sud", "Botswana"]
}



test_graph = Graph(test_graph)
test_graph_is_tree = Graph(test_graph_is_tree)
test_graph2 = Graph(test_graph2)
test_graph_dict = Graph(test_graph_dict)

afrique_graph = Graph(afrique_graph)

# test_graph.display_graph()
# print(test_graph.BFS(start_node="A"))
# print(test_graph.is_tree())

print("-"*15)


print(afrique_graph.BFS(start_node="Algerie"))
# print(f"Est ce que le graphe est un ARBRE ? -> {test_graph_dict.is_tree()}")

# test_graph_dict.fermeture_transitive().display_graph()
print("-"*15)

afrique_graph.visualize()
# test_graph_is_tree.fermeture_transitive().visualize()
color_assignment = afrique_graph.welsh_powell()
# print("Color assignment with welsh algo:", color_assignment)


# color_assignment2= afrique_graph.dsatur_algo()
# print("color assignmenet with DSATUR -> ",color_assignment)




















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
