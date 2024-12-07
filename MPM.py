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
        self.taches = {
            "DEBUT": {"duree": 0},
            "A": {"duree": 10},
            "B": {"duree": 25},
            "C": {"duree": 25},
            "D": {"duree": 20},
            "E": {"duree": 35},
            "F": {"duree": 20},
            "G": {"duree": 25},
            "H": {"duree": 15},
            "I": {"duree": 40},
            "J": {"duree": 30},
            "K": {"duree": 20},
            "L": {"duree": 40},
            "M": {"duree": 10},
            "N": {"duree": 15},
            "FIN": {"duree": 0},
        }

        # Define predecessors for each task
        self.predecesseurs = {
            "DEBUT": [],
            "A": ["DEBUT"],
            "B": ["A"],
            "C": ["B", "E", "G"],
            "D": ["DEBUT"],
            "E": ["DEBUT"],
            "F": ["E", "G"],
            "G": ["A", "D"],
            "H": ["E"],
            "I": ["DEBUT"],
            "J": ["C", "F", "H"],
            "K": ["B", "E", "G"],
            "L": ["J", "M"],
            "M": ["K", "N"],
            "N": ["A"],
            "FIN": ["L"],
        }

    def ajouter_tache(self, tache, duree, predecesseurs=[]):
        self.taches[tache] = {"duree": duree}
        self.predecesseurs[tache] = predecesseurs

    def calculer_dates_plus_tot(self):
        dates_plus_tot = {node: 0 for node in self.taches}

        for node in self.taches:
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

        for node in reversed(list(self.taches)):
            # print(f"-----> {node}")
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

    def trouver_chemin_critique(self, marges_totales):
        return [node for node, marge in marges_totales.items() if marge == 0]


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
        marges_totales, marges_libres = self.ordonnanceur.calculer_marges(
            dates_plus_tot, dates_plus_tard
        )
        chemin_critique = self.ordonnanceur.trouver_chemin_critique(marges_totales)
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
        for node in list(self.ordonnanceur.taches)[1:-1]:
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
                    "Oui" if node in chemin_critique else "Non",
                ),
            )
        # Pack the Treeview
        tree.pack(expand=True, fill="both")

        # show at the bottom "chemin critique"
        chemin_label = Label(
            self.cadre_tableau,
            text="Chemin critique: " + " -> ".join(chemin_critique),
            font=("Arial", 12),
        )
        chemin_label.pack(pady=5)


root = Tk()
app = InterfaceMPM(root)
root.mainloop()
