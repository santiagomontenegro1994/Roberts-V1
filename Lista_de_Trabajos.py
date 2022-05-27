from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class listaDeTrabajos():
    
    
    def __init__(self,window):
        self.wind=window
        self.wind.title("Lista de Clientes")
        self.wind.geometry("800x700")
        
        wrapper1 = LabelFrame(window, text="Customer List")
        wrapper2 = LabelFrame(window, text="Busqueda")
        wrapper3 = LabelFrame(window, text="Customer Data")
        
        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
        
  
  
        
window = Tk()
programa = listaDeTrabajos(window)

window.mainloop()        