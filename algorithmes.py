from collections import deque
from time import sleep

def dfs_iteratif(graphe, source):
    visites = set()
    pile = [(source, 0)]

    while pile:
        sommet, cout = pile.pop()

        if sommet not in visites:
            visites.add(sommet)
            print(f"Visite {sommet} | Coût cumulé : {cout}")

            for voisin, poids in reversed(graphe[sommet]):
                if voisin not in visites:
                    pile.append((voisin, cout + poids))

def dfs(grillage):
    visites = []
    source,objectif = grillage.idMaison,grillage.idEcole
    pile = [(source, 0,None,[])]
    while pile:
        grillage.canvas.update()
        sommet, cout,parent,chemin = pile.pop()
        if sommet not in visites:
            sleep(0.05)
            visites.append(sommet)
            voisins = grillage.voisins(sommet)

            fleche = grillage.tracer_fleche(parent,sommet)
            chemin.append(fleche)

            if sommet == objectif:
                chemin_final = chemin[:]
                cout_final = cout
                grillage.zone_text.insert("end",chemin_final)
            
            for voisin in voisins:
                poids = 1 if grillage.canvas.itemcget(voisin, "fill") != "blue" else 5
                if voisin not in visites:
                    pile.append((voisin, cout + poids,sommet,chemin[:]))

    grillage.zone_text.insert("end",f"Arrivé à l'école en {cout_final} minutes\n")
    for sommet in chemin_final:
        grillage.canvas.itemconfig(sommet, fill="yellow")


def dijkstra(graphe, source, objectif):
    distances = {sommet: float('inf') for sommet in graphe}
    distances[source] = 0
    precedents = {source: None}
    non_visites = list(graphe.keys())
    
    while non_visites:
        noeud_courant = min(non_visites, key=lambda node: distances[node])
        print(f"Visite du sommet '{noeud_courant}' avec une distance cumulée de {distances[noeud_courant]}")

        if noeud_courant == objectif:
            print(f"Objectif '{objectif}' atteint!")
            chemin = []
            while noeud_courant is not None:
                chemin.append(noeud_courant)
                noeud_courant = precedents[noeud_courant]
            return chemin[::-1]
        
        for voisin, distance in graphe[noeud_courant]:
            nouvelle_distance = distances[noeud_courant] + distance
            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                precedents[voisin] = noeud_courant
        
        non_visites.remove(noeud_courant)
    
    print(f"Objectif '{objectif}' inaccessible.")
    return None

def algorithme_glouton(graphe, source, objectif, heuristique):
    noeud_courant = source
    chemin = [noeud_courant]
    visites = set()

    while noeud_courant != objectif:
        visites.add(noeud_courant)
        voisins_non_visites = [(voisin, distance) for voisin, distance in graphe[noeud_courant] if voisin not in visites]
        
        if not voisins_non_visites:
            print(f"Aucun voisin non visité disponible depuis '{noeud_courant}'. L'algorithme échoue.")
            return None
        
        prochain_noeud, _ = min(voisins_non_visites, key=lambda x: heuristique[x[0]])
        print(f"Avance vers '{prochain_noeud}' avec une heuristique de {heuristique[prochain_noeud]}")
        chemin.append(prochain_noeud)
        noeud_courant = prochain_noeud
    
    print(f"Objectif '{objectif}' atteint!")
    return chemin

def a_star(graphe, source, objectif, heuristique):
    chemin_dijkstra = dijkstra(graphe, source, objectif)
    if chemin_dijkstra is None:
        print("A* : Le chemin via Dijkstra n'a pas été trouvé.")
        return None

    chemin_glouton = algorithme_glouton(graphe, source, objectif, heuristique)
    
    print(f"Chemin via Dijkstra : {chemin_dijkstra}")
    print(f"Chemin via Glouton : {chemin_glouton}")
    
    return chemin_dijkstra

def bfs_iteratif(graphe, source):
    visites = set()
    file = deque([source])

    visites.add(source)

    while file:
        sommet = file.popleft()
        print(f"Visite {sommet}")

        for voisin, _ in graphe[sommet]:
            if voisin not in visites:
                visites.add(voisin)
                file.append(voisin)


def bellman_ford(graphe, source):
    distances = {sommet: float('inf') for sommet in graphe}
    distances[source] = 0

    for _ in range(len(graphe) - 1):
        modifie = False
        for u in graphe:
            for v, poids in graphe[u]:
                if distances[u] != float('inf') and distances[u] + poids < distances[v]:
                    distances[v] = distances[u] + poids
                    modifie = True
        if not modifie:
            break

    # Si cycle négatif
    for u in graphe:
        for v, poids in graphe[u]:
            if distances[u] != float('inf') and distances[u] + poids < distances[v]:
                raise ValueError("Cycle de poids négatif détecté")

    return distances
