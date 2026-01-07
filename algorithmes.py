from collections import deque
from time import sleep
import random

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
    chemin_final=[]
    cout_final = 0
    grillage.canvas.delete("fleche")
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
            
            random.shuffle(voisins)
            for voisin in voisins:
                poids = grillage.get_cout(voisin)
                if voisin not in visites:
                    pile.append((voisin, cout + poids,sommet,chemin[:]))

    grillage.zone_text.insert("end",f"Arrivé à l'école en {cout_final} minutes\n")
    for sommet in chemin_final:
        grillage.canvas.itemconfig(sommet, fill="yellow")

def bfs(grillage):
    visites = []
    chemin_final=[]
    cout_final = 0
    grillage.canvas.delete("fleche")
    source,objectif = grillage.idMaison,grillage.idEcole
    pile = [(source, 0,None,[])]
    cout_commun = 0
    while pile:
        grillage.canvas.update()
        sommet, cout,parent,chemin = pile.pop(0)
        if sommet not in visites:
            if cout_commun != cout:
                cout_commun = cout
                sleep(0.05)
            visites.append(sommet)
            voisins = grillage.voisins(sommet)

            fleche = grillage.tracer_fleche(parent,sommet)
            chemin.append(fleche)

            if sommet == objectif:
                chemin_final = chemin[:]
                cout_final = cout
            
            random.shuffle(voisins)
            for voisin in voisins:
                poids = grillage.get_cout(voisin)
                if voisin not in visites:
                    pile.append((voisin, cout + poids,sommet,chemin[:]))

    grillage.zone_text.insert("end",f"Arrivé à l'école en {cout_final} minutes\n")
    for sommet in chemin_final:
        grillage.canvas.itemconfig(sommet, fill="yellow")

def dijkstra_iteratif(graphe, source, objectif):
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


def _dijkstra_choisir(distances, a_traiter):
    courant = min(a_traiter, key=lambda s: distances[s])
    a_traiter.remove(courant)
    return courant


def _dijkstra_reconstruire(precedents, objectif):
    chemin = []
    cur = objectif
    while cur is not None:
        chemin.append(cur)
        cur = precedents[cur]
    chemin.reverse()
    return chemin


def _dijkstra_afficher(grillage, chemin, cout_total):
    grillage.zone_text.insert(
        "end",
        f"Arrivé à l'école en {cout_total} minutes\n"
    )
    for node in chemin:
        grillage.canvas.itemconfig(node, fill="yellow")


def dijkstra(grillage):
    grillage.canvas.delete("fleche")

    source, objectif = grillage.idMaison, grillage.idEcole

    distances = {source: 0}
    precedents = {source: None}

    a_traiter = [source]
    visites = set()

    while a_traiter:
        grillage.canvas.update()

        courant = _dijkstra_choisir(distances, a_traiter)
        if courant in visites:
            continue
        visites.add(courant)

        sleep(0.02)

        if courant == objectif:
            break

        voisins = grillage.voisins(courant)
        random.shuffle(voisins)

        for voisin in voisins:
            poids = grillage.get_cout(voisin)
            nouvelle_distance = distances[courant] + poids

            if nouvelle_distance < distances.get(voisin, float("inf")):
                distances[voisin] = nouvelle_distance
                precedents[voisin] = courant
                a_traiter.append(voisin)
                grillage.tracer_fleche(courant, voisin)

    if objectif not in distances:
        grillage.zone_text.insert("end", "École inaccessible.\n")
        return None

    chemin = _dijkstra_reconstruire(precedents, objectif)
    _dijkstra_afficher(grillage, chemin, distances[objectif])
    return chemin


def methode_gloutonne_iteratif(graphe, source, objectif, heuristique):
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

def glouton(grillage):
    visites=[]
    grillage.canvas.delete("fleche")
    source,objectif = grillage.idMaison,grillage.idEcole
    cout = 0
    best_voisin = None
    while source != objectif :
        visites.append(source)
        grillage.canvas.update()
        sleep(0.05)
        voisins = grillage.voisins(source)
        min = float('inf')

        for voisin in voisins :
            if voisin not in visites and grillage.get_dist(voisin,objectif) <min: 
                min = grillage.get_dist(voisin,objectif) 
                best_voisin = voisin

        if not best_voisin:#Si aucun voisin non visité
            grillage.zone_text.insert("end",f"Je n'arrive pas à aller à l'école\n")
            return
        
        cout+=grillage.get_cout(best_voisin)
        grillage.tracer_fleche(source,best_voisin)
        source = best_voisin
        best_voisin = None

    grillage.zone_text.insert("end",f"Arrivé à l'école en {cout} minutes\n")
    for sommet in grillage.canvas.find_withtag("fleche"):
        grillage.canvas.itemconfig(sommet, fill="yellow")

def a_star(graphe, source, objectif, heuristique):
    open_set = {source}
    closed_set = set()
    g = {s: float('inf') for s in graphe}
    g[source] = 0
    precedents = {source: None}

    while open_set:
        courant = min(open_set, key=lambda n: g[n] + heuristique[n])
        if courant == objectif:
            chemin = []
            while courant is not None:
                chemin.append(courant)
                courant = precedents[courant]
            return chemin[::-1]

        open_set.remove(courant)
        closed_set.add(courant)

        for voisin, cout in graphe[courant]:
            if voisin in closed_set:
                continue
            tentative_g = g[courant] + cout
            if tentative_g < g[voisin]:
                g[voisin] = tentative_g
                precedents[voisin] = courant
                open_set.add(voisin)
    return None

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
