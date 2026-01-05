# CAHIER DES CHARGES : Logiciel Pédagogique de Théorie des Graphes

## 1. Introduction
Nous sommes une équipe de 4 développeurs travaillant sur un projet informatique : SAE FA3 - Réalisation d'un logiciel pédagogique de théorie des graphes. L’objectif de ce projet est de mettre en place un logiciel interactif en Python, destiné à proposer des modèles mathématiques afin de permettre des calculs et des visualisations de graphes. Le logiciel comportera :
* Une interface de création et de manipulation de graphes,
* Un tableau de bord avec les différents modules de calculs,
* Une vidéo ou animation explicative de l'exécution des algorithmes.

## 2. Énoncé
Le logiciel permet d’effectuer des calculs sur les graphes. Les acteurs et fonctionnalités sont les suivants :
* **Utilisateur :** Accès à un tableau de bord contenant les différents modules de calculs pour :
    * Créer manuellement un graphe (sommets, arêtes et poids),
    * Charger ou enregistrer des structures de graphes,
    * Lancer les simulations algorithmiques.
* **Modules de calculs :** Accès aux 5 algorithmes fondamentaux sélectionnés :
    1. **Parcours en profondeur (DFS)** : Pour l'exploration exhaustive.
    2. **Parcours en largeur (BFS)** : Pour le calcul de distance par couches.
    3. **Dijkstra** : Pour le plus court chemin pondéré.
    4. **Glouton** : Pour la recherche de chemin via heuristique.
    5. **A*** : Pour l'optimisation combinant Dijkstra et Glouton.
* **Administrateur / Développeur :** Accès au code source pour :
    * Assurer la maintenance des modules,
    * Consulter les modifications et la documentation technique sur GitHub.

## 3. Pré-requis
L'application sera installée et configurée pour :
* **Le système d'exploitation :** Compatible Windows/Linux (via Python),
* **Le langage de programmation :** Python,
* **L'interface graphique :** Utilisation d'une bibliothèque dédiée (Tkinter),
* **La gestion de version :** Un dépôt Git pour le suivi des versions et le travail collaboratif.

## 4. Priorités
Les priorités de développement, établies avec le client, sont :
* **Fonctionnalités essentielles :** Créer l'interface de dessin interactive et implémenter les 5 modules de calculs avec des résultats exacts.
* **Pédagogie :** Renforcer l'aspect visuel (couleurs des sommets, étapes de l'algorithme) pour faciliter la compréhension du fonctionnement interne des graphes.
* **Ergonomie :** Optimiser l'interface pour être ergonomique et responsive, assurant une utilisation intuitive sur ordinateurs.
* **Maintenance :** Fournir une documentation complète sur GitHub pour garantir la pérennité du logiciel et la maîtrise technique lors de la soutenance.