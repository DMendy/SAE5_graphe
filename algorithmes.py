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