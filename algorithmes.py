from collections import deque

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



