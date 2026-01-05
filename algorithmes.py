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



