import tkinter as tk
from gui.main_window import GraphSearchApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x900")       
    root.minsize(600, 700)         
    root.eval('tk::PlaceWindow . center')  
    app = GraphSearchApp(root)
    root.mainloop()