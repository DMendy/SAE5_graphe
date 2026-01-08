# Mission : Retrouver le Chemin de l'École

### Bienvenue dans votre simulateur de théorie des graphes !
L'objectif est d'aider un élève à rejoindre l'**École** depuis sa **Maison**. Grâce à une interface interactive, vous pouvez observer comment différents algorithmes "réfléchissent" pour trouver leur chemin à travers les obstacles.

---

## 1. Les Règles
Le terrain est composé d'hexagones. Chaque déplacement consomme du temps (score en minutes) :

| Élément | Visuel | Propriété | Coût (Temps) |
| :--- | :--- | :--- | :--- |
| **Maison** | 🟩 Vert | Point de départ de l'élève. | **0 min** |
| **École** | 🟥 Rouge | Destination finale (l'école). | ** À trouver...** |
| **Plaine** | ⬜ Blanc | Chemin classique. | **1 min** |
| **Rivière** | 🟦 Bleu | Traversée difficile qui ralentit l'élève. | **5 min** |
| **Mur** | ⬛ Noir | Obstacle infranchissable (frontière). | **Bloqué** |
| **autre....** |

---

## 2. Les Guides de Navigation (Algorithmes)
Chaque algorithme utilise une stratégie différente pour explorer la carte. Les **flèches** affichées en temps réel montrent l'ordre de découverte des chemins.

1. **L'algorithme de parcours en profondeur (DFS)** : Il explore chaque rue jusqu'au bout avant de faire demi-tour. Très imprévisible, il peut trouver un chemin très long ou très court par pur hasard.
    

2. **L'algorithme de parcours en largeur (BFS)** : Il avance prudemment en "vague". Il explore tous les voisins à la même distance avant d'aller plus loin. Il trouve toujours le chemin avec le moins d'étapes, mais ignore les coûts de la rivière.
    

3. **L'Algorithme de Dijkstra** : Le plus intelligent. Il analyse les minutes perdues dans l'eau et préfère faire un détour par la plaine si cela permet d'arriver plus vite. **Il garantit le temps de trajet minimum.**
    

4. **L'algorithme glouton** : Il ne regarde que sa boussole. À chaque intersection, il choisit l'hexagone qui le rapproche physiquement de l'école, même s'il s'agit d'un cul-de-sac ou d'une rivière profonde.

<img width="1169" height="730" alt="image" src="https://github.com/user-attachments/assets/f9dedb5d-bc2e-4100-9873-58fc3347f6cd" />
*Aperçu du parcours Glouton : l'élève suit sa boussole et fonce vers l'école en ignorant le coût de la rivière.*

    

---

## 3. Mode d'emploi de la Simulation
1.  **Aménagez la ville** : Placez des **Murs** pour bloquer des rues et de la **Rivière** pour créer des zones de ralentissement.
2.  **Lancez un algorithme** : Cliquez sur un bouton d'algorithme.
3.  **Observez l'exploration** : Des flèches apparaissent pour montrer la progression de l'élève.
4.  **Résultat final** : Une fois l'école atteinte, le chemin optimal est surligné en **Jaune** et le temps total (ex: *12 minutes*) s'affiche dans la zone de texte.

---

## 4. Pourquoi comparer ces algorithmes ?
Ce projet permet de voir que le chemin le plus court "à l'œil nu" n'est pas toujours le plus rapide. 
* Le **BFS** traversera la rivière (temps élevé).
* Le **Dijkstra** contournera la rivière (temps optimisé).

C'est cette logique qui est utilisée chaque jour par vos applications de GPS entre autres!
