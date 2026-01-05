import tkinter as tk
from affichage import Grillage



if __name__ == "__main__":
   root = tk.Tk()  # Création de la fenêtre principale
   visualisation = Grillage(root)  # Initialisation de l'interface graphique
   root.mainloop()  # Lancer la boucle principale de Tkinter