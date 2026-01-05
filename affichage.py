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


        # Dessiner la grille d'hexagones
        self.dessiner_grille()



    
    def draw_hexagon(self, x, y, size):
        #Algorithme qui permet de déssiner un hexagone
        points = []
        for i in range(6):
            angle = math.radians(i * 60) + math.pi / 6 
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        return self.canvas.create_polygon(points, outline="black", fill="white", width=2)

    def dessiner_grille(self):
        # Nouvelles formules d'espacement pour l'orientation "pointue"
        horizontal_spacing = math.sqrt(3) * self.size
        vertical_spacing = 1.5 * self.size # Distance entre les rangées (chevauchement)

        for row in range(self.rows):
            for col in range(self.rows): # Utilisez self.cols si défini
                x = col * horizontal_spacing
                
                # Décalage horizontal pour les lignes impaires
                if row % 2 == 1:
                    x += horizontal_spacing / 2
                
                y = row * vertical_spacing
                
                id_case = self.draw_hexagon(x, y, self.size)
                self.hexagones.append(id_case)
        

