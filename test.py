class GestionTaches:
    def __init__(self):
        self.taches = {
            "A": {"duree": 5, "successeurs": ["B", "C"], "niveau": None},
            "B": {"duree": 3, "successeurs": ["D"], "niveau": None},
            "C": {"duree": 2, "successeurs": ["D"], "niveau": None},
            "D": {"duree": 4, "successeurs": [], "niveau": None},
        }

    def calculer_dates_et_niveaux(self):
        # Étape 1 : Initialisation des dates au plus tôt et au plus tard
        dates_plus_tot = {
            tache: 0 for tache in self.taches
        }  # Date au plus tôt pour chaque tâche
        dates_plus_tard = {
            tache: float("inf") for tache in self.taches
        }  # Date au plus tard pour chaque tâche
        dates_plus_tard["D"] = (
            0  # La dernière tâche a sa date au plus tard définie à 0 (fin du projet)
        )

        # Étape 2 : Calcul des niveaux des tâches
        self._calculer_niveaux()

        # Étape 3 : Calcul des dates au plus tôt (dates_plus_tot) en respectant les niveaux
        self._calculer_dates_plus_tot(dates_plus_tot)

        # Étape 4 : Calcul des dates au plus tard (dates_plus_tard) en respectant les niveaux
        self._calculer_dates_plus_tard(dates_plus_tot, dates_plus_tard)

        # Affichage des résultats
        print("Dates au plus tôt :", dates_plus_tot)
        print("Dates au plus tard :", dates_plus_tard)
        print(
            "Niveaux des tâches :",
            {tache: self.taches[tache]["niveau"] for tache in self.taches},
        )

    # Fonction pour calculer les dates au plus tôt, en respectant les niveaux
    def _calculer_dates_plus_tot(self, dates_plus_tot):
        # Trier les tâches par niveau (niveau 0 en premier, etc.)
        taches_par_niveau = sorted(
            self.taches.keys(), key=lambda t: self.taches[t]["niveau"]
        )

        # Calcul des dates au plus tôt dans l'ordre des niveaux
        for tache in taches_par_niveau:
            for succ in self.taches[tache]["successeurs"]:
                dates_plus_tot[succ] = max(
                    dates_plus_tot[succ],
                    dates_plus_tot[tache] + self.taches[tache]["duree"],
                )

    # Fonction pour calculer les dates au plus tard, en respectant les niveaux
    def _calculer_dates_plus_tard(self, dates_plus_tot, dates_plus_tard):
        # Trier les tâches par niveau de manière décroissante (niveau le plus élevé en premier)
        taches_par_niveau = sorted(
            self.taches.keys(), key=lambda t: self.taches[t]["niveau"], reverse=True
        )

        # Calcul des dates au plus tard dans l'ordre inverse des niveaux
        for tache in taches_par_niveau:
            if not self.taches[tache][
                "successeurs"
            ]:  # Si la tâche n'a pas de successeurs, on initialise à la fin du projet
                dates_plus_tard[tache] = dates_plus_tot[tache]
            else:
                dates_plus_tard[tache] = min(
                    dates_plus_tard[succ] - self.taches[tache]["duree"]
                    for succ in self.taches[tache]["successeurs"]
                )

    # Fonction pour calculer les niveaux des tâches
    def _calculer_niveaux(self):
        # Initialisation des niveaux à None
        for tache in self.taches:
            self.taches[tache]["niveau"] = None

        niveau = 0
        taches_a_traiter = [
            tache for tache, data in self.taches.items() if not data["successeurs"]
        ]  # Tâches sans successeurs

        # Calcul des niveaux en fonction des successeurs
        while taches_a_traiter:
            tache = taches_a_traiter.pop(0)
            if self.taches[tache]["niveau"] is None:
                self.taches[tache]["niveau"] = niveau

            for t, data in self.taches.items():
                if tache in data["successeurs"] and self.taches[t]["niveau"] is None:
                    taches_a_traiter.append(t)

            niveau += 1


# Exemple d'utilisation de la classe
gestion_taches = GestionTaches()
gestion_taches.calculer_dates_et_niveaux()
