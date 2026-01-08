from time import sleep
import random

def dfs(grillage):
    """Parcours en profondeur (DFS) sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        None.
    """
    visites = []
    chemin_final=[]
    cout_final = 0
    grillage.effacer_fleches()
    source,objectif = grillage.idMaison,grillage.idEcole
    pile = [(source, 0,None,[])]
    while pile:
        grillage.canvas.update()
        sommet, cout,parent,chemin = pile.pop()
        if sommet not in visites:
            sleep(0.005)
            visites.append(sommet)
            voisins = grillage.voisins(sommet)

            if parent:
                fleche = grillage.tracer_fleche(parent,sommet,cout)
                chemin.append(fleche)

            if sommet == objectif:
                chemin_final = chemin[:]
                cout_final = cout
            
            random.shuffle(voisins)
            for voisin in voisins:
                poids = grillage.get_cout(voisin)
                if voisin not in visites:
                    pile.append((voisin, cout + poids,sommet,chemin[:]))
    if cout_final== 0:
        grillage.zone_text.insert("end",f"École inaccessible\n")
    else:
        grillage.zone_text.insert("end",f"Arrivé à l'école en {chemin_final} minutes\n")
        for sommet in chemin_final:
            grillage.canvas.itemconfig(sommet[0], fill="yellow")

def bfs(grillage):
    """Parcours en largeur (BFS) sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        None.
    """
    visites = []
    chemin_final=[]
    cout_final = 0
    grillage.effacer_fleches()
    source,objectif = grillage.idMaison,grillage.idEcole
    pile = [(source, 0,None,[])]
    while pile:
        grillage.canvas.update()
        sommet, cout,parent,chemin = pile.pop(0)
        if sommet not in visites:
            sleep(0.05)
            visites.append(sommet)
            voisins = grillage.voisins(sommet)

            if parent:
                fleche = grillage.tracer_fleche(parent,sommet,cout)
                chemin.append(fleche)

            if sommet == objectif:
                chemin_final = chemin[:]
                cout_final = cout
            
            random.shuffle(voisins)
            for voisin in voisins:
                poids = grillage.get_cout(voisin)
                if voisin not in visites:
                    pile.append((voisin, cout + poids,sommet,chemin[:]))

    if cout_final== 0:
        grillage.zone_text.insert("end",f"École inaccessible\n")
    else:
        grillage.zone_text.insert("end",f"Arrivé à l'école en {cout_final} minutes\n")
        for sommet in chemin_final:
            grillage.canvas.itemconfig(sommet[0], fill="yellow")



def _dijkstra_choisir(distances, a_traiter):
    """Sélectionne le prochain sommet à traiter selon la distance minimale.

    Args:
        distances: Dictionnaire des distances courantes par sommet.
        a_traiter: Liste des sommets candidats.

    Returns:
        Le sommet sélectionné.
    """
    courant = min(a_traiter, key=lambda s: distances[s])
    a_traiter.remove(courant)
    return courant


def dijkstra(grillage):
    """Algorithme de Dijkstra sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        Liste des identifiants de flèches du chemin optimal, ou None si inaccessible.
    """
    grillage.effacer_fleches()

    source, objectif = grillage.idMaison, grillage.idEcole

    distances = {source: 0}
    precedents = {source: None}
    fleches = {sommet : [] for sommet in grillage.dico_coord.keys()}

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
                fleches[voisin] = fleches[courant]+[grillage.tracer_fleche(courant,voisin,distances[voisin])]
                a_traiter.append(voisin)

    if objectif not in distances:
        grillage.zone_text.insert("end", "École inaccessible.\n")
        return None

    grillage.zone_text.insert(
        "end",
        f"Arrivé à l'école en {distances[objectif]} minutes\n"
    )
    for fleche in fleches[objectif]:
        grillage.canvas.itemconfig(fleche[0], fill="yellow")


def glouton(grillage):
    """Recherche gloutonne sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        None.
    """
    visites=[]
    grillage.effacer_fleches()
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
        grillage.tracer_fleche(source,best_voisin,cout)
        source = best_voisin
        best_voisin = None

    grillage.zone_text.insert("end",f"Arrivé à l'école en {cout} minutes\n")
    for sommet in grillage.canvas.find_withtag("fleche"):
        grillage.canvas.itemconfig(sommet, fill="yellow")

def a_star(grillage):
    """Algorithme A* sur un graphe pondéré.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        None.
    """
    
    grillage.effacer_fleches()

    source, objectif = grillage.idMaison, grillage.idEcole

    open_set = [source]
    visites = set()

    g = {source: 0}
    precedents = {source: None}
    fleches = {sommet: [] for sommet in grillage.dico_coord.keys()}

    while open_set:
        grillage.canvas.update()
        sleep(0.02)

        courant = min(
            open_set,
            key=lambda s: g[s] + grillage.get_dist(s, objectif)
        )
        open_set.remove(courant)

        if courant == objectif:
            break

        visites.add(courant)

        voisins = grillage.voisins(courant)
        random.shuffle(voisins)

        for voisin in voisins:
            if voisin in visites:
                continue

            poids = grillage.get_cout(voisin)
            tentative_g = g[courant] + poids

            if tentative_g < g.get(voisin, float('inf')):
                g[voisin] = tentative_g
                precedents[voisin] = courant
                fleches[voisin] = (
                    fleches[courant] + [grillage.tracer_fleche(courant, voisin,g[voisin])]
                )
                if voisin not in open_set:
                    open_set.append(voisin)

    if objectif not in g:
        grillage.zone_text.insert("end", "École inaccessible\n")
        return

    grillage.zone_text.insert(
        "end",
        f"Arrivé à l'école en {g[objectif]} minutes\n"
    )

    for fleche in fleches[objectif]:
        grillage.canvas.itemconfig(fleche[0], fill="yellow")


def bellmanFord(grillage):
    """Algorithme de Bellman-Ford sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        None.
    """
    grillage.effacer_fleches()

    sommets = grillage.dico_coord.keys()
    cout = {sommet : float('inf') for sommet in sommets }
    cout[grillage.idMaison] = 0

    fleches = {sommet : [] for sommet in sommets }
    for i in range(len(sommets)-1):
        modification = False
        for sommet in sommets:
            for voisin in grillage.voisins(sommet):
                poids = grillage.get_cout(voisin)
                if cout[sommet] != float('inf') and cout[sommet]+poids<cout[voisin]:
                    cout[voisin] = cout[sommet]+poids
                    grillage.canvas.update()
                    sleep(0.005)
                    if fleches.get(voisin):
                        grillage.canvas.delete(fleches[voisin][-1][0])
                        grillage.canvas.delete(fleches[voisin][-1][1])
                    fleches[voisin] = fleches[sommet]+[grillage.tracer_fleche(sommet,voisin,cout[voisin])]
                    modification = True
        if not modification:
            break
    
    if cout[grillage.idEcole] == float('inf') : 
        grillage.zone_text.insert("end","École inaccessible\n")
    else : 
        grillage.zone_text.insert(
            "end",
            f"Arrivé à l'école en {cout[grillage.idEcole]} minutes\n"
        )
        for sommet in fleches[grillage.idEcole]:
            grillage.canvas.itemconfig(sommet[0], fill="yellow")
