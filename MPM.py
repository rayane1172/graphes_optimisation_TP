import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkinter import ttk


class MPM:
    def __init__(self):
        self.taches = {}  # Dictionnaire pour les tâches
        self.predecesseurs = {}  # Dictionnaire pour les predecesseurs
        self.niveaux = {}
        # self.taches = {
        #     "A": {"duree": 10},
        #     "B": {"duree": 25},
        #     "C": {"duree": 25},
        #     "D": {"duree": 20},
        #     "E": {"duree": 35},
        #     "F": {"duree": 20},
        #     "G": {"duree": 25},
        #     "H": {"duree": 15},
        #     "I": {"duree": 40},
        #     "J": {"duree": 30},
        #     "K": {"duree": 20},
        #     "L": {"duree": 40},
        #     "M": {"duree": 10},
        #     "N": {"duree": 15},
        # }

        # # Define predecessors for each task
        # self.predecesseurs = {
        #     "A": [],
        #     "B": ["A"],
        #     "C": ["B", "E", "G"],
        #     "D": [],
        #     "E": [],
        #     "F": ["E", "G"],
        #     "G": ["A", "D"],
        #     "H": ["E"],
        #     "I": [],
        #     "J": ["C", "F", "H"],
        #     "K": ["B", "E", "G"],
        #     "L": ["J", "M"],
        #     "M": ["K", "N"],
        #     "N": ["A"],
        # }

    def calculer_niveaux(self):

        self.niveaux = {}

        #todo -> level 0 tasks
        for task in self.taches:
            if not self.predecesseurs[task]:
                self.niveaux[task] = 0

        # Calculate levels for remaining tasks
        changed = True
        while changed:
            changed = False
            for task in self.taches:
                if task not in self.niveaux:
                    #todo -> verifier si tout les predecesseur ayant assignee avec niveaux
                    if all(pred in self.niveaux for pred in self.predecesseurs[task]):
                        # todo -> niveaux c'est max + 1
                        self.niveaux[task] = (max([self.niveaux[pred] for pred in self.predecesseurs[task]],default=-1) + 1)
                        changed = True

    def complet_graph(self):
        self.calculer_niveaux()
        print("before levels : ",self.niveaux)
        # todo ->  add node debut and it's secesseurs

        start_tasks = [task for task in self.taches if not self.predecesseurs[task]]
        if start_tasks:
            if "DEBUT" not in self.taches:
                self.taches["DEBUT"] = {"duree": 0}
                self.predecesseurs["DEBUT"] = []
            for task in start_tasks:
                self.predecesseurs[task] = ["DEBUT"]

        # todo -> search for node "fin" predecesseurs
        end_tasks = [
            task
            for task in self.taches
            if not any(task in pred_list for pred_list in self.predecesseurs.values())
        ]
        if end_tasks:
            # print("end tasks --> ", end_tasks)
            if "FIN" not in self.taches:
                self.taches["FIN"] = {"duree": 0}
                self.predecesseurs["FIN"] = end_tasks

        self.calculer_niveaux()
        print("after levels : ",self.niveaux)
        return self.taches

    def ajouter_tache(self, tache, duree, predecesseurs=[]):
        self.taches[tache] = {"duree": duree}
        self.predecesseurs[tache] = predecesseurs

    def calculer_dates_plus_tot(self):
        self.complet_graph()
        dates_plus_tot = {node: 0 for node in self.taches}

        # todo -> sorted tasks respecting levels
        for node in sorted(self.taches.keys(), key=lambda x: self.niveaux.get(x, 0)):
            for pred in self.predecesseurs.get(node, []):
                # todo -> compare with current value and new value calculated
                dates_plus_tot[node] = max(
                    dates_plus_tot[node],
                    dates_plus_tot[pred] + self.taches[pred]["duree"],
                )
        return dates_plus_tot

    def calculer_dates_plus_tard(self, dates_plus_tot):
        dates_plus_tard = {}
        duree_projet = max(
            dates_plus_tot[node] + self.taches[node]["duree"] for node in self.taches
        )
        # duree_projet = dates_plus_tot["E"] + self.taches["E"]["duree"]
        # print(duree_projet)

        for node in sorted(self.taches.keys(), key=lambda x: self.niveaux.get(x, 0),reverse=True):
            successeurs = [
                n for n, preds in self.predecesseurs.items() if node in preds
            ]
            if not successeurs:  # node fin : duree ta3o zero
                dates_plus_tard[node] = duree_projet - self.taches[node]["duree"]
            else:
                dates_plus_tard[node] = (
                    min(dates_plus_tard[s] for s in successeurs)
                    - self.taches[node]["duree"]
                )
        return dates_plus_tard

    def calculer_marges(self, dates_plus_tot, dates_plus_tard):
        marges_totales = {}
        marges_libres = {}

        for node in self.taches:
            marges_totales[node] = dates_plus_tard[node] - dates_plus_tot[node]

            successeurs = [
                n for n, preds in self.predecesseurs.items() if node in preds
            ]
            # todo -> if current task ('node') is a predecessor of task 'n' return it as successor
            if successeurs:
                marges_libres[node] = min(
                    dates_plus_tot[s]
                    - dates_plus_tot[node]
                    - self.taches[node]["duree"]
                    for s in successeurs
                )
            else:  # node fin
                marges_libres[node] = marges_totales[node]

        return marges_totales, marges_libres

    # def trouver_tout_chemin(self, marges_totales):
    #     return [node for node, marge in marges_totales.items() if marge == 0]

    def trouver_tout_chemin(self, marges_totales):
        def find_all_paths(current, end, path, all_paths, critical_tasks):
            # Add the current task to the path
            # print(f"ctask {current}, path == {path}")
            path = path + [current]

            # If the current task is the end task, append the full path to all_paths
            if current == end:
                all_paths.append(path)
            else:
                # Find all possible next critical tasks
                for next_task in critical_tasks:
                    # Avoid cycles
                    if next_task not in path:
                        # Ensure the next_task is a valid successor of the current task
                        if current in self.predecesseurs.get(next_task, []):
                            # Recursively find all paths
                            find_all_paths(next_task, end, path, all_paths, critical_tasks)

        # Identify all critical tasks (those with zero margin)
        critical_tasks = [node for node, marge in marges_totales.items() if marge == 0]
        # Initialize a list to store all critical paths
        all_critical_paths = []

        # Start finding paths from 'DEBUT' to 'FIN'
        find_all_paths("DEBUT", "FIN", [], all_critical_paths, critical_tasks)

        # Return the list of all critical paths
        return all_critical_paths


class InterfaceMPM:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordonnancement MPM")

        # Création des cadres
        self.cadre_saisie = Frame(root)
        self.cadre_saisie.pack(side=TOP, pady=10)

        self.cadre_graphe = Frame(root)
        self.cadre_graphe.pack(side=LEFT, padx=10)

        self.cadre_tableau = Frame(root)
        self.cadre_tableau.pack(side=RIGHT, padx=10)

        self.ordonnanceur = MPM()
        self.creer_widgets()

    def creer_widgets(self):
        # Widgets de saisie
        Label(self.cadre_saisie, text="Tâche:").grid(row=0, column=0)
        self.id_tache = Entry(self.cadre_saisie)
        self.id_tache.grid(row=0, column=1)

        Label(self.cadre_saisie, text="Durée:").grid(row=0, column=2)
        self.duree = Entry(self.cadre_saisie)
        self.duree.grid(row=0, column=3)

        Label(self.cadre_saisie, text="Tâches Antérieures:").grid(row=0, column=4)
        self.predecesseurs = Entry(self.cadre_saisie)
        self.predecesseurs.grid(row=0, column=5)

        Button(
            self.cadre_saisie, text="Ajouter Tâche", command=self.ajouter_tache
        ).grid(row=0, column=6)
        Button(self.cadre_saisie, text="Calculer", command=self.calculer).grid(
            row=0, column=7
        )

    def ajouter_tache(self):
        id_tache = self.id_tache.get()
        duree = int(self.duree.get())
        predecesseurs = (
            self.predecesseurs.get().split(",") if self.predecesseurs.get() else []
        )
        self.ordonnanceur.ajouter_tache(id_tache, duree, predecesseurs)
        self.dessiner_graphe()

    def calculer(self):
        dates_plus_tot = self.ordonnanceur.calculer_dates_plus_tot()
        dates_plus_tard = self.ordonnanceur.calculer_dates_plus_tard(dates_plus_tot)
        marges_totales, marges_libres = self.ordonnanceur.calculer_marges(dates_plus_tot, dates_plus_tard)
        chemin_critique = self.ordonnanceur.trouver_tout_chemin(marges_totales)
        self.mettre_a_jour_affichage(
            dates_plus_tot,
            dates_plus_tard,
            marges_totales,
            marges_libres,
            chemin_critique,
        )

    def dessiner_graphe(self):
        plt.clf()
        G = nx.DiGraph()

        # Création des noeuds et des arêtes du graphe
        for tache, data in self.ordonnanceur.taches.items():
            G.add_node(tache, duree=data["duree"])
        for tache, predecesseurs in self.ordonnanceur.predecesseurs.items():
            for pred in predecesseurs:
                G.add_edge(pred, tache)

        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            arrowsize=20,
        )

        # Mise à jour du canvas
        if hasattr(self, "canvas"):
            self.canvas.draw()
        else:
            figure = plt.gcf()
            self.canvas = FigureCanvasTkAgg(figure, self.cadre_graphe)
            self.canvas.get_tk_widget().pack()

    def mettre_a_jour_affichage(
        self,
        dates_plus_tot,
        dates_plus_tard,
        marges_totales,
        marges_libres,
        chemin_critique,
    ):
        # Clear previous table
        for widget in self.cadre_tableau.winfo_children():
            widget.destroy()

        # Create Treeview widget
        columns = (
            "Tâche",
            "Durée",
            "Date au plus tôt",
            "Date au plus tard",
            "Marge totale",
            "Marge libre",
            "Critique",
        )
        tree = ttk.Treeview(
            self.cadre_tableau, columns=columns, show="headings", height=15
        )

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")  # Adjust width as needed

        # Add data to Treeview
        for node in list(self.ordonnanceur.taches):
            if node != "DEBUT" and node != "FIN":
                tree.insert(
                    "",
                    "end",
                    values=(
                        node,
                        self.ordonnanceur.taches[node]["duree"],
                        dates_plus_tot[node],
                        dates_plus_tard[node],
                        marges_totales[node],
                        marges_libres[node],
                        "Oui" if marges_totales[node] == 0 else "Non",
                    ),
                )
        # Pack the Treeview
        tree.pack(expand=True, fill="both")

        # Display all critical paths
        print(chemin_critique)
        for i,chemin in enumerate(chemin_critique,1):
            chemin_label = Label(
                self.cadre_tableau,
                text=f"Chemin critique {i} " + " -> ".join(chemin),
                font=("Arial", 12),
            )
            chemin_label.pack(pady=2)


root = Tk()
app = InterfaceMPM(root)
root.mainloop()
