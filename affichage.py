import tkinter as tk
import math



class Grillage:
    def __init__(self, root):
        self.root = root
        self.HEIGHT = 800
        self.WIDTH = 800
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)


        self.toolbar = tk.Frame(root)
        self.toolbar.grid(row=0, column=0, pady=5)

        self.rows = 40
        self.size = self.HEIGHT//self.rows
        
        
        self.hexagones = []  # Liste des héxagones

        self.dessiner_grille()

        self.mode = "white"  # Mode par défaut : couleur des carrés

        # Ajout des boutons
        self.idMaison, self.idEcole = None,None

        self.bouton_green = tk.Button(self.toolbar, text="Maison", command=lambda: self.changer_mode("green"))
        self.bouton_green.grid(row=0, column=0, padx=10, pady=10)


        self.bouton_red = tk.Button(self.toolbar, text="École", command=lambda: self.changer_mode("red"))
        self.bouton_red.grid(row=0, column=1, padx=10, pady=10)


        self.bouton_black = tk.Button(self.toolbar, text="Placer un mur", command=lambda: self.changer_mode("black"))
        self.bouton_black.grid(row=0, column=2, padx=10, pady=10)


        self.bouton_blue = tk.Button(self.toolbar, text="Rivière", command=lambda: self.changer_mode("blue"))
        self.bouton_blue.grid(row=0, column=3, padx=10, pady=10)


        self.bouton_white = tk.Button(self.toolbar, text="Effacer", command=lambda: self.changer_mode("white"))
        self.bouton_white.grid(row=0, column=4, padx=10, pady=10)

        self.bouton_reset = tk.Button(self.toolbar, text="Reset", command=lambda: self.reset())
        self.bouton_reset.grid(row=0, column=5, padx=10, pady=10)

        self.actionbar = tk.Frame(root)
        self.actionbar.grid(row=1, column=1, pady=5)

        self.bouton_dijkstra = tk.Button(self.toolbar, text="Dijkstra", command=self.executer_dijkstra)
        self.bouton_dijkstra.grid(row=0, column=6, padx=10)


    
    def draw_hexagon(self, x, y, size):
        points = []
        for i in range(6):
            # On ajoute math.pi / 6 pour pivoter l'hexagone
            angle = math.radians(i * 60) + math.pi / 6 
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        return self.canvas.create_polygon(points, outline="black", fill="white", width=2)

    def dessiner_grille(self):
        # Création de la grille
        horizontal_spacing = math.sqrt(3) * self.size
        vertical_spacing = 1.5 * self.size 
        for row in range(self.rows):
            for col in range(self.rows):
                x = col * horizontal_spacing+5
                
                # Décalage horizontal pour les lignes impaires
                if row % 2 == 1:
                    x += horizontal_spacing / 2
                
                y = row * vertical_spacing
                
                id_case = self.draw_hexagon(x, y, self.size)
                self.hexagones.append(id_case)
                
                self.canvas.tag_bind(id_case, "<Button-1>", 
                                    lambda event, item_id=id_case: self.changer_couleur(item_id))
        self.canvas.bind("<B1-Motion>", self.on_drag)
        for hexa in self.hexagones:
            x1,y1,x2,y2 = self.canvas.bbox(hexa)
            if (x1 < 0 or y1 < 0 or x2 > self.WIDTH or y2 > self.HEIGHT):
                self.canvas.delete(hexa)
        


    def on_drag(self, event):
        # Trouve l'élément sous le curseur pendant le mouvement
        if self.mode not in ["green","red"] : 
            item = self.canvas.find_closest(event.x, event.y)
            if item:
                self.changer_couleur(item[0])


    def changer_mode(self, mode):
        #Changer le mode
        self.mode = mode


    def changer_couleur(self, item_id):
        #Changer la couleur du carré lorsqu'on clique dessus
        current_color = self.canvas.itemcget(item_id, "fill")
        if current_color != self.mode and not (current_color in ["green","red"] and self.mode!="white"):
            if self.mode == "green" : 
                self.canvas.itemconfig(self.idMaison, fill="white")
                self.idMaison = item_id
            elif self.mode == "red" : 
                self.canvas.itemconfig(self.idEcole, fill="white")
                self.idEcole = item_id
            self.canvas.itemconfig(item_id, fill=self.mode)
    def reset (self):
        self.changer_mode("white")
        for hexa in self.hexagones:
            self.canvas.itemconfig(hexa, fill=self.mode)
            
    def generer_graphe(self):
        graphe = {}
        depart = None
        objectif = None
        # On stocke les positions pour retrouver les voisins facilement
        # Ici, une simple logique de distance entre centres d'hexagones suffit

        # 1. Identifier les rôles de chaque hexagone
        all_items = self.canvas.find_all()
        for item in all_items:
            color = self.canvas.itemcget(item, "fill")
            if color == "black": continue  # On ignore les murs

            if color == "green": depart = item
            if color == "red": objectif = item

            # Trouver les voisins (les hexagones proches géométriquement)
            coords_item = self.canvas.coords(item)
            center_x = sum(coords_item[0::2]) / 6
            center_y = sum(coords_item[1::2]) / 6

            voisins = []
            # Rayon de recherche légèrement supérieur à la distance entre deux centres
            seuil = self.size * 1.8

            for potential in all_items:
                if potential == item: continue
                couleur_potentielle = self.canvas.itemcget(potential, "fill")
                if couleur_potentielle == "black": continue

                coords_p = self.canvas.coords(potential)
                px = sum(coords_p[0::2]) / 6
                py = sum(coords_p[1::2]) / 6

                dist = math.sqrt((center_x - px) ** 2 + (center_y - py) ** 2)
                if dist < seuil:
                    # On ajoute le voisin avec un poids par défaut de 1
                    poids = 1
                    if couleur_potentielle == "blue":
                        poids = 4
                    voisins.append((potential, poids))

            graphe[item] = voisins

        return graphe, depart, objectif

    def executer_dijkstra(self):
        from algorithmes import dijkstra  # Importez vos fonctions

        graphe, start, end = self.generer_graphe()

        if start and end:
            chemin = dijkstra(graphe, start, end)
            if chemin:
                for node in chemin:
                    if node != start and node != end:
                        self.canvas.itemconfig(node, fill="yellow")
        else:
            print("Il manque un point de départ ou d'arrivée !")