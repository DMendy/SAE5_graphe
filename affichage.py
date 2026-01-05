import tkinter as tk




class Grillage:
    def __init__(self, root):
        self.root = root
        self.HEIGHT = 800
        self.WIDTH = 800
        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)


        self.rows = 40
        self.size = self.HEIGHT//self.rows
        
        