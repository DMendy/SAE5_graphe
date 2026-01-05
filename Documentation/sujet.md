# SAE FA3 : Réalisation d'un logiciel pédagogique de théorie des graphes

L'objectif de cette SAE est de réaliser un logiciel intéractif permettant de visualiser l'éxécution d'algorithmes de théorie des graphes.

## Exemple : le logiciel *hexa*

A titre d'exemple, la vidéo ci-jointe présente un logiciel nommé *hexa* réalisé en python-tkinter qui permet de visualiser les algorithmes de plus courts chemins dans les graphes : algorithmes de parcours en largeur, de Dijkstra, de Bellman-Ford, algorithme A*. L'algorithme de parcours en profondeur est également implémenté.

Le principe ici est que les hexagones sont les sommets du graphe. On peut changer l'origine et la destination pour les algorithmes de parcours en largeur (si on veut reconstituer le chemin le plus court). L'algorithme affiche également les distances depuis le sommet de départ.

La couleur noire permet de complètement supprimer des sommets du graphe. Les autres couleurs (vert, jaune, bleu) correspondent à des distances plus ou moins importantes. Normalement, on compte une distance 1 entre deux hexagones mais par exemple le bleu, qui représente de l'eau (penser à une carte), ajoute 5 à la distance pour entrer ou sortir de l'hexagone.

## Votre travail

Votre objectif n'est pas forcément de refaire à l'identique ce logiciel mais de faire un logiciel dans le même esprit. Vous pouvez faire les algorithmes déjà présents dans *hexa*, mais vous pouvez aussi illustrer d'autres algorithmes :

* calcul des composantes connexes
* arbres de poids minimum (Prim/Kruskal)
* calcul d'un stable maximum
* calcul d'un flot maximum dans un graphe (Ford-Fulkerson)
ou tout autre algorithme que vous connaissez.

Vous serez évalués sur les aspects suivants :

* aspects techniques de programmation
* algorithmes présentés (aspects pédagogiques et techniques)
* ergonomie du logiciel

Le code doit être suffisamment commenté et explicite pour qu'on puisse le lire facilement. Attention, comme d'habitude vous devez maîtriser tout ce que vous utilisez, tant au niveau du code que des algorithmes présentés.

Le langage de programmation et le support (application, web etc) est au choix.

## Déroulement de la soutenance finale

Vous présenterez :

* l'ensemble du logiciel et ses fonctionnalités
* vous insisterez sur les aspects pédagogiques et illustrations des algorithmes
* vous détaillez un algorithme de votre choix, en expliquant (sur un exemple ?) le principe de l'algorithme, et comment le logiciel permet de l'illustrer, comme un petit cours/tuto de théorie des graphes.

Ensuite il y a aura des questions, principalement sur les aspects techniques.