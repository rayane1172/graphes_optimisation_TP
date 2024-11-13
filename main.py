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



# test_graph = Graph(test_graph)
# test_graph_is_tree = Graph(test_graph_is_tree)
# test_graph2 = Graph(test_graph2)
# test_graph_dict = Graph(test_graph_dict)

# afrique_graph = Graph(afrique_graph)

# test_graph.display_graph()
# print(test_graph.BFS(start_node="A"))
# print(test_graph.is_tree())

print("-"*15)


# print(afrique_graph.BFS(start_node="Algerie"))
# print(f"Est ce que le graphe est un ARBRE ? -> {test_graph_dict.is_tree()}")

# test_graph_dict.fermeture_transitive().display_graph()
# print("-"*15)

# afrique_graph.visualize()
# test_graph_is_tree.fermeture_transitive().visualize()
# color_assignment = afrique_graph.welsh_powell()
# print("Color assignment with welsh algo:", color_assignment)


# color_assignment2= afrique_graph.dsatur_algo()
# print("color assignmenet with DSATUR -> ",color_assignment2)



import json
from Graph import Graph
import os


def read_graph_from_default_file():
    file_name = 'graph_data.json'  # file name
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    try:
        with open(file_path, 'r') as file:
            graph_dict = json.load(file)
        return Graph(graph_dict)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found in the script's directory.")
        return None
    except json.JSONDecodeError:
        print("Error: The file is not in valid JSON format.")
        return None

mon_graph = read_graph_from_default_file()

if mon_graph:
    # print(type(mon_graph))
    mon_graph.visualize()
    # color_assignment2= mon_graph.dsatur_algo()
    # print("color assignmenet with DSATUR -> ",color_assignment2)

    mon_graph.RLF()
    mon_graph.dsatur_algo()
    mon_graph.welsh_powell()
else:
    print("Error")










