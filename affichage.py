import tkinter as tk
import math
import algorithmes as algo



class Grillage:
    """
    Classe principale gérant l'interface graphique Tkinter pour la visualisation
    du graphe sous forme de grille hexagonale.
    """
    def __init__(self, root):
        self.root = root
        self.HEIGHT = 800
        self.WIDTH = 800
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.grid(row=1, column=0, padx=10, pady=10)


        self.toolbar = tk.Frame(root)
        self.toolbar.grid(row=0, column=0, pady=5)

        self.rows = 20
        self.size = self.HEIGHT//(self.rows*2)
        
        self.dico_hexa,self.dico_coord = {},{}
        

        self.idMaison, self.idEcole = None,None
        self.dessiner_grille()

        self.mode = "white"  # Mode par défaut : couleur des carrés

        # Ajout des boutons du jeu

        self.bouton_pink = tk.Button(self.toolbar, text="Maison",bg="pink", command=lambda: self.changer_mode("pink"))
        self.bouton_pink.grid(row=0, column=0, padx=10, pady=10)

        self.bouton_red = tk.Button(self.toolbar, text="École", bg="red", command=lambda: self.changer_mode("red"))
        self.bouton_red.grid(row=0, column=1, padx=10, pady=10)

        self.bouton_forest = tk.Button(self.toolbar, text="Forêt", bg="green", command=lambda: self.changer_mode("green"))
        self.bouton_forest.grid(row=0, column=2, padx=10, pady=10)

        self.bouton_black = tk.Button(self.toolbar, text="Placer un mur", bg="black", fg="white" , command=lambda: self.changer_mode("black"))
        self.bouton_black.grid(row=0, column=4, padx=10, pady=10)


        self.bouton_blue = tk.Button(self.toolbar, text="Rivière", bg="blue", command=lambda: self.changer_mode("blue"))
        self.bouton_blue.grid(row=0, column=3, padx=10, pady=10)


        self.bouton_white = tk.Button(self.toolbar, text="Effacer", command=lambda: self.changer_mode("white"))
        self.bouton_white.grid(row=0, column=5, padx=10, pady=10)

        self.actionbar = tk.Frame(root)
        self.actionbar.grid(row=1, column=1, pady=5)

        self.bouton_dijkstra = tk.Button(self.actionbar, text="Dijkstra", command=self.executer_dijkstra)
        self.bouton_dijkstra.grid(row=0, column=0, padx=10, pady=5)

        self.bouton_glouton = tk.Button(self.actionbar, text="Parcours griddy", command=lambda : algo.glouton(self))
        self.bouton_glouton.grid(row=1, column=0, padx=10, pady=5)

        self.bouton_dfs = tk.Button(self.actionbar, text="Parcours en profondeur", command=lambda : algo.dfs(self))
        self.bouton_dfs.grid(row=2, column=0, padx=10, pady=5)

        self.bouton_bfs = tk.Button(self.actionbar, text="Parcours en largeur", command=lambda : algo.bfs(self))
        self.bouton_bfs.grid(row=3, column=0, padx=10, pady=5)

        self.bouton_bellman = tk.Button(self.actionbar, text="Bellman-Ford", command=lambda : algo.bellmanFord(self))
        self.bouton_bellman.grid(row=4, column=0, padx=10, pady=5)

        self.bouton_bellman = tk.Button(self.actionbar, text="Algorithme A*", command=lambda : algo.a_star(self))
        self.bouton_bellman.grid(row=5, column=0, padx=10, pady=5)
    
        self.zone_text = tk.Text(self.actionbar,height=15, width=40)
        self.zone_text.grid(row=self.actionbar.grid_size()[1],column=0,pady=10,padx=10)

        self.bouton_reset = tk.Button(self.actionbar, text="Reset", command=lambda: self.reset())
        self.bouton_reset.grid(row=self.actionbar.grid_size()[1], column=0, padx=10, pady=10)

    def draw_hexagon(self, x, y, size):
        """Calcule les points et dessine un hexagone régulier."""
        points = []
        for i in range(6):
            # On ajoute math.pi / 6 pour pivoter l'hexagone
            angle = math.radians(i * 60) + math.pi / 6 
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        return self.canvas.create_polygon(points, outline="black", fill="white", width=2)

    def dessiner_grille(self):
        """Génère la grille hexagonale avec décalage pour les lignes impaires."""
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
                self.dico_hexa[(row,col)] = id_case
                self.dico_coord[id_case] = (row,col)
                self.canvas.tag_bind(id_case, "<Button-1>", 
                                    lambda event, item_id=id_case: self.changer_couleur(item_id))
        self.canvas.bind("<B1-Motion>", self.on_drag)

        for hexa in list(self.dico_coord.keys()):
            x1,y1,x2,y2 = self.canvas.bbox(hexa)
            if (x1 < 0 or y1 < 0 or x2 > self.WIDTH or y2 > self.HEIGHT):
                self.canvas.delete(hexa)
                del self.dico_hexa[self.dico_coord[hexa]]
                del self.dico_coord[hexa]
        
        #On initialise une maison et une école de base
        self.idEcole,self.idMaison = self.dico_hexa[(19,19)],self.dico_hexa[(1,0)]
        self.canvas.itemconfig(self.idMaison, fill="pink")
        self.canvas.itemconfig(self.idEcole, fill="red")
        
    def voisins(self,hexa):
        """Retourne la liste des hexagones adjacents non bloqués par un mur."""
        voisins = []
        row,col = self.dico_coord[hexa]
        if row % 2 == 0:
            directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1)]
        else:
            directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,1)]
        for dx,dy in directions:
            row_voisin, col_voisin = row+dx,col+dy
            voisin = self.dico_hexa.get((row_voisin,col_voisin))
            if voisin and self.get_couleur(voisin) != "black":
                voisins.append(voisin)
        return voisins


    def on_drag(self, event):
        """Permet de colorier plusieurs cases en glissant la souris."""
        # Trouve l'élément sous le curseur pendant le mouvement
        if self.mode not in ["pink","red"] :
            item = self.canvas.find_closest(event.x, event.y)
            if item and item not in self.canvas.find_withtag("fleche"):
                self.changer_couleur(item[0])


    def changer_mode(self, mode):
        """Définit quel type de terrain sera placé au prochain clic."""
        #Changer le mode
        self.mode = mode


    def changer_couleur(self, item_id):
        """Applique la couleur du mode actuel à l'hexagone sélectionné."""
        #Changer la couleur du carré lorsqu'on clique dessus
        current_color = self.get_couleur(item_id)
        if current_color != self.mode and not (current_color in ["pink","red"] and self.mode!="white"):
            if self.mode == "pink" :
                self.canvas.itemconfig(self.idMaison, fill="white")
                self.idMaison = item_id
                self.zone_text.insert("end",f"Ajout de la maison en {self.dico_coord[item_id]}\n")
            elif self.mode == "red" : 
                self.canvas.itemconfig(self.idEcole, fill="white")
                self.idEcole = item_id
                self.zone_text.insert("end",f"Ajout de l'école en {self.dico_coord[item_id]}\n")
            self.canvas.itemconfig(item_id, fill=self.mode)
            
    def reset (self):
        """Réinitialise toute la grille à l'état initial (tout blanc)."""
        #On réinitialise le mode
        self.changer_mode("white")
        #On remet tous les hexagones en blanc
        for hexa in self.dico_coord.keys():
            self.canvas.itemconfig(hexa, fill=self.mode)
        #On réinitialise la maison et l'école
        self.idEcole,self.idMaison = self.dico_hexa[(19,19)],self.dico_hexa[(1,0)]
        self.canvas.itemconfig(self.idMaison, fill="pink")
        self.canvas.itemconfig(self.idEcole, fill="red")
        #On supprime les flèches
        self.canvas.delete("fleche")
        #On réinitialise la zone de texte
        self.zone_text.delete("1.0","end")  
                  
    
    def executer_dijkstra(self):
        """Lance l'algorithme de Dijkstra via le module externe."""
        algo.dijkstra(self)

    def tracer_fleche(self,hexa1,hexa2):
        """Dessine une flèche entre deux hexagones pour visualiser le chemin."""
        if hexa1 and hexa2 : 
            for fleche in self.canvas.find_withtag("fleche") : 
                self.canvas.itemconfig(fleche, fill="grey")
            coords_hexa1,coords_hexa2 = self.canvas.bbox(hexa1),self.canvas.bbox(hexa2)
            x1,y1 = (coords_hexa1[0]+coords_hexa1[2])/2,(coords_hexa1[1]+coords_hexa1[3])/2
            x2,y2 = (coords_hexa2[0]+coords_hexa2[2])/2,(coords_hexa2[1]+coords_hexa2[3])/2
            return self.canvas.create_line(x1, y1, x2, y2,arrow="last",fill="red",width=10,tags="fleche")
    
    def get_dist(self,hexa1,hexa2):
        """Calcul de la distance de Manhattan."""
        if hexa1 and hexa2:
            x1,y1 = self.dico_coord[hexa1]
            x2,y2 = self.dico_coord[hexa2]
            
            z1 = y1-(x1//2)
            z2 = y2-(x2//2)
            w1,w2 = -z1-x1,-z2-x2

            return int(max(abs(z1-z2),abs(w1-w2),abs(x1-x2)))
    def get_couleur(self,hexa):
        """Retourne la couleur actuelle d'un hexagone."""
        return self.canvas.itemcget(hexa,"fill")
    
    def get_cout(self,hexa):
        """Associe un coût (temps en minutes) à chaque couleur de case."""
        couleur = self.get_couleur(hexa)
        if couleur == "white" or couleur=="red":
            return 1
        elif couleur == "green":
            return 3
        elif couleur == "blue":
            return 5
        else : 
            return 0
