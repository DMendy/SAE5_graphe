def dfs_pondere_iteratif(graphe, source):
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


graphe = {
    'A': [('B', 2), ('C', 5)],
    'B': [('D', 4)],
    'C': [('D', 1), ('E', 3)],
    'D': [],
    'E': []
}


dfs_pondere_iteratif(graphe, 'A')