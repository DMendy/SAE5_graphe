from time import sleep
import random

def dfs(grillage):
    """Parcours en profondeur (DFS) sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        None.
    """
    visites = []    #liste des sommets deja visités
    chemin_final=[]     #chemin final vers l'objectif
    cout_final = 0      #coût total du chemin final
    grillage.effacer_fleches()
    source,objectif = grillage.idMaison,grillage.idEcole
    pile = [(source, 0,None,[])]
    while pile: # tant que la pile n'est pas vide
        grillage.canvas.update()
        sommet, cout,parent,chemin = pile.pop()      #depile le dernier sommet ajouté
        if sommet not in visites:
            sleep(0.005)
            visites.append(sommet)
            voisins = grillage.voisins(sommet)

            if parent:      # si sommet a un parent, on trace la fleche
                fleche = grillage.tracer_fleche(parent,sommet,cout)
                chemin.append(fleche)

            if sommet == objectif:
                chemin_final = chemin[:]
                cout_final = cout
            
            random.shuffle(voisins)     # melange voisins pour une meilleure animation
            for voisin in voisins:
                poids = grillage.get_cout(voisin)
                if voisin not in visites:
                    pile.append((voisin, cout + poids,sommet,chemin[:]))
    if cout_final== 0:      # si aucun chemin trouve
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
    while pile:     # tant que la file n'est pas vide
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
        for sommet in chemin_final:     # colore le chemin final
            grillage.canvas.itemconfig(sommet[0], fill="yellow")



def _dijkstra_choisir(distances, a_traiter):
    """Sélectionne le prochain sommet à traiter selon la distance minimale.

    Args:
        distances: Dictionnaire des distances courantes par sommet.
        a_traiter: Liste des sommets candidats.

    Returns:
        Le sommet sélectionné.
    """
    courant = min(a_traiter, key=lambda s: distances[s])      # trouve le sommet avec la plus petite distance dans la liste des sommets a traiter
    a_traiter.remove(courant)   #supprime le sommet choisi de la liste des sommets a traiter
    return courant


def dijkstra(grillage):
    """Algorithme de Dijkstra sur la grille avec animation.

    Args:
        grillage: Instance de l'interface contenant la grille et le canvas.

    Returns:
        Liste des identifiants de flèches du chemin optimal, ou None si inaccessible.
    """
    grillage.effacer_fleches()  # supprime les fleches precedentes

    source, objectif = grillage.idMaison, grillage.idEcole

    distances = {source: 0} # distance depuis la source
    precedents = {source: None} # pour reconstruire le chemin
    fleches = {sommet : [] for sommet in grillage.dico_coord.keys()}    #flèches pour chaque sommet

    a_traiter = [source]    # liste des sommets a traiter
    visites = set()     # ensemble des sommets deja visites

    while a_traiter:
        grillage.canvas.update()

        courant = _dijkstra_choisir(distances, a_traiter)   # prend le sommet le plus proche connu
        if courant in visites:
            continue
        visites.add(courant)

        sleep(0.02)

        if courant == objectif:
            break

        voisins = grillage.voisins(courant)
        random.shuffle(voisins)

        for voisin in voisins:
            poids = grillage.get_cout(voisin)   # cout pour aller au voisin
            nouvelle_distance = distances[courant] + poids  # pemet de connaitre la distance depuis source

            if nouvelle_distance < distances.get(voisin, float("inf")):
                distances[voisin] = nouvelle_distance
                precedents[voisin] = courant

                # ajoute la flèche dans le chemin graphique
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
    cout = 0    # cout cumule du chemin
    best_voisin = None  
    while source != objectif :
        visites.append(source)
        grillage.canvas.update()
        sleep(0.05)
        voisins = grillage.voisins(source)
        min = float('inf')  # initialise la meilleure distance

        for voisin in voisins :
            # on entre dans la boucle si on a un voisin non visite et plus proche selon l'heuristique
            if voisin not in visites and grillage.get_dist(voisin,objectif) <min: 
                min = grillage.get_dist(voisin,objectif) 
                best_voisin = voisin    # selectionne le meilleur voisin

        if not best_voisin:#Si aucun voisin non visité
            grillage.zone_text.insert("end",f"Je n'arrive pas à aller à l'école\n")
            return
        
        cout+=grillage.get_cout(best_voisin)    # ajoute le cout du voisin
        grillage.tracer_fleche(source,best_voisin,cout)
        source = best_voisin    # permet d'avancer au voisin choisi
        best_voisin = None      # on met None afin de reset pour la prochaine iteration

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

    a_traiter = [source]
    visites = set()     # ensemble des sommets deja visites

    g = {source: 0}     # cout depuis le depart pour chaque sommet
    precedents = {source: None}     # sert a reconstruire le chemin
    fleches = {sommet: [] for sommet in grillage.dico_coord.keys()}

    while a_traiter:
        grillage.canvas.update()
        sleep(0.02)

        # choisi le sommet avec g + heuristique la plus petite
        courant = min(a_traiter,key=lambda s: g[s] + grillage.get_dist(s, objectif))
        a_traiter.remove(courant)   # on le retire de la liste a traiter

        if courant == objectif:
            break

        visites.add(courant)

        voisins = grillage.voisins(courant)
        random.shuffle(voisins)

        for voisin in voisins:
            if voisin in visites:
                continue

            poids = grillage.get_cout(voisin)   # cout pour aller au voisin
            tentative_g = g[courant] + poids    # distance depuis le depart  

            if tentative_g < g.get(voisin, float('inf')):   # si le chemin passant par courant est plus court que le chemin qu'on connait deja pour ce voisin, on met a jour
                g[voisin] = tentative_g
                precedents[voisin] = courant
                fleches[voisin] = (
                    fleches[courant] + [grillage.tracer_fleche(courant, voisin,g[voisin])]
                )
                if voisin not in a_traiter:
                    a_traiter.append(voisin)

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
    grillage.effacer_fleches()  # supprime les fleches precedentes

    sommets = grillage.dico_coord.keys()
    cout = {sommet : float('inf') for sommet in sommets }   # initialise cout a infinie pour tous les sommets
    cout[grillage.idMaison] = 0

    fleches = {sommet : [] for sommet in sommets }  # necessaire pour les chemins graphiques pour chaque sommet
    for i in range(len(sommets)-1): # on fait |V|-1 iterations
        modification = False    # permet de detecter si on a mis a jour au moins une distance
        for sommet in sommets:
            for voisin in grillage.voisins(sommet):
                poids = grillage.get_cout(voisin)   # recupere le cout du voisin

                # si le chemin passant par sommet est meilleur que le chemin connu pour voisin
                if cout[sommet] != float('inf') and cout[sommet]+poids<cout[voisin]:    
                    cout[voisin] = cout[sommet]+poids   # on met a jour le cout
                    grillage.canvas.update()
                    sleep(0.005)

                    # si il y avait deja une fleche pour ce voisin, on supprime
                    if fleches.get(voisin):
                        grillage.canvas.delete(fleches[voisin][-1][0])
                        grillage.canvas.delete(fleches[voisin][-1][1])

                        # on copie le chemin du sommet et on ajoute la nouvelle fleche
                    fleches[voisin] = fleches[sommet]+[grillage.tracer_fleche(sommet,voisin,cout[voisin])]
                    modification = True # on notifie qu'il y a eu une mise a jour
        if not modification:    # si aucune distance n'a ete mise a jour, on arrete
            break
    
    # si l'objectif est inaccessible
    if cout[grillage.idEcole] == float('inf') : 
        grillage.zone_text.insert("end","École inaccessible\n")
    else : 
        grillage.zone_text.insert(
            "end",
            f"Arrivé à l'école en {cout[grillage.idEcole]} minutes\n"
        )

        # colorie le chemin final afin de mieux le visualiser
        for sommet in fleches[grillage.idEcole]:
            grillage.canvas.itemconfig(sommet[0], fill="yellow")
