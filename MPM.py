import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class OrdonanceurMPM:
    def __init__(self):
        self.taches = {}  # Dictionnaire pour les tâches
        self.predecesseurs = {}  # Dictionnaire pour les predecesseurs

    def ajouter_tache(self, tache, duree, predecesseurs=[]):
        self.taches[tache] = {"duree": duree}
        self.predecesseurs[tache] = predecesseurs

    def calculer_dates_plus_tot(self):
        dates_plus_tot = {node: 0 for node in self.taches}

        # Calcul des dates au plus tôt (dates_plus_tot)
        for node in self.taches:
            for pred in self.predecesseurs.get(node, []):
                # todo -> compare with current value and new value calculated
                dates_plus_tot[node] = max(dates_plus_tot[node],
                                           dates_plus_tot[pred] + self.taches[pred]["duree"])
        return dates_plus_tot

    def calculer_dates_plus_tard(self, dates_plus_tot):
        dates_plus_tard = {}
        duree_projet = max(dates_plus_tot[node] + self.taches[node]["duree"] for node in self.taches)

        # Calcul des dates au plus tard (dates_plus_tard)
        for node in reversed(list(self.taches)):
            successeurs = [n for n, preds in self.predecesseurs.items() if node in preds]
            if not successeurs:
                dates_plus_tard[node] = duree_projet - self.taches[node]["duree"]
            else:
                dates_plus_tard[node] = (min(dates_plus_tard[s] for s in successeurs) - self.taches[node]["duree"])
        return dates_plus_tard

    def calculer_marges(self, dates_plus_tot, dates_plus_tard):
        marges_totales = {}
        marges_libres = {}

        # Calcul des marges
        for node in self.taches:
            marges_totales[node] = dates_plus_tard[node] - dates_plus_tot[node]

            successeurs = [n for n, preds in self.predecesseurs.items() if node in preds]
            # todo -> if current task ('node') is a predecessor of task 'n' return it as successor
            if successeurs:
                marges_libres[node] = min(dates_plus_tot[s] - dates_plus_tot[node] - self.taches[node]["duree"] for s in successeurs)
            else:
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

        self.ordonnanceur = OrdonanceurMPM()
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
        predecesseurs = (self.predecesseurs.get().split(",") if self.predecesseurs.get() else [] )
        self.ordonnanceur.ajouter_tache(id_tache, duree, predecesseurs)
        self.dessiner_graphe()

    def calculer(self):
        dates_plus_tot = self.ordonnanceur.calculer_dates_plus_tot()
        dates_plus_tard = self.ordonnanceur.calculer_dates_plus_tard(dates_plus_tot)
        marges_totales, marges_libres = self.ordonnanceur.calculer_marges(dates_plus_tot, dates_plus_tard)
        chemin_critique = self.ordonnanceur.trouver_chemin_critique(marges_totales)
        self.mettre_a_jour_affichage(dates_plus_tot, dates_plus_tard, marges_totales, marges_libres, chemin_critique)

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

    def mettre_a_jour_affichage(self, dates_plus_tot, dates_plus_tard, marges_totales, marges_libres, chemin_critique):
        # Création des données du tableau
        donnees = []
        for node in self.ordonnanceur.taches:
            donnees.append(
                {
                    "Tâche": node,
                    "Durée": self.ordonnanceur.taches[node]["duree"],
                    "Date au plus tôt": dates_plus_tot[node],
                    "Date au plus tard": dates_plus_tard[node],
                    "Marge totale": marges_totales[node],
                    "Marge libre": marges_libres[node],
                    "Critique": node in chemin_critique,
                }
            )

        # Affichage dans le tableau
        df = pd.DataFrame(donnees)
        tableau = Text(self.cadre_tableau)
        tableau.delete("1.0", END)
        tableau.insert(END, "Tableau des tâches:\n\n")
        tableau.insert(END, df.to_string())
        tableau.insert(END, "\n\nChemin critique: " + " -> ".join(chemin_critique))
        tableau.pack()


root = Tk()
app = InterfaceMPM(root)
root.mainloop()
