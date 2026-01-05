import tkinter as tk
import math



class Grillage:
    def __init__(self, root):
        self.root = root
        self.HEIGHT = 800
        self.WIDTH = 800
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)


        self.rows = 40
        self.size = self.HEIGHT//self.rows
        
        
        self.hexagones = []  # Liste des héxagones

        self.dessiner_grille()

        self.mode = "white"  # Mode par défaut : couleur des carrés

        # Ajouter des boutons pour modifier la couleur des carrés
        self.bouton_black = tk.Button(root, text="Bloqué", command=lambda: self.changer_mode("black"))
        self.bouton_black.grid(row=1, column=1, padx=10, pady=10)


        self.bouton_white = tk.Button(root, text="Clear", command=lambda: self.changer_mode("white"))
        self.bouton_white.grid(row=2, column=1, padx=10, pady=10)


        self.bouton_green = tk.Button(root, text="Départ", command=lambda: self.changer_mode("green"))
        self.bouton_green.grid(row=3, column=1, padx=10, pady=10)


        self.bouton_red = tk.Button(root, text="Objectif", command=lambda: self.changer_mode("red"))
        self.bouton_red.grid(row=4, column=1, padx=10, pady=10)


    
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
                x = col * horizontal_spacing
                
                # Décalage horizontal pour les lignes impaires
                if row % 2 == 1:
                    x += horizontal_spacing / 2
                
                y = row * vertical_spacing
                
                id_case = self.draw_hexagon(x, y, self.size)
                self.hexagones.append(id_case)
                
                self.canvas.tag_bind(id_case, "<Button-1>", 
                                    lambda event, item_id=id_case: self.changer_couleur(item_id))
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def on_drag(self, event):
        # Trouve l'élément sous le curseur pendant le mouvement
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.changer_couleur(item[0])


    def changer_mode(self, mode):
        #Changer le mode
        self.mode = mode


    def changer_couleur(self, item_id):
        #Changer la couleur du carré lorsqu'on clique dessus
        current_color = self.canvas.itemcget(item_id, "fill")
        if current_color != self.mode:
            self.canvas.itemconfig(item_id, fill=self.mode)


