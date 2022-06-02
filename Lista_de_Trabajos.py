from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class listaDeTrabajos():
    
    db_nombre = 'database.db'
    with sqlite3.connect(db_nombre) as conn:
            cursor = conn.cursor()         
    
    
    def __init__(self,window):
        self.wind=window
        self.wind.title("Lista de Trabajos")
        self.wind.geometry("1024x800")
        
        self.t1=tk.StringVar()
        self.t2=tk.StringVar()
        self.t3=tk.StringVar()
        self.t4=tk.StringVar()
        
        #Creando el contenedor
        wrapper1 = LabelFrame(window, text="Lista de Trabajos")
        wrapper2 = LabelFrame(window, text="Busqueda")
        wrapper3 = LabelFrame(window, text="Carga y Modificacion de Datos")
        
        wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
        wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)
        
        #------------------------------Seccion de lista
        
        #Creando el treeview
        self.tabla = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6), show="headings", height="6")
        self.tabla.pack()
        
        self.tabla.heading(1, text="Estado")
        self.tabla.heading(2, text="Fecha")
        self.tabla.heading(3, text="Cliente")
        self.tabla.heading(4, text="Trabajo")
        self.tabla.heading(5, text="Precio")
        self.tabla.heading(6, text="Id Trabajo")
        
        self.tabla.bind('<Double-1>', self.getrow)# al hacer doble click selecciona un cliente con los datos
        
        #lleno la lista de elementos
        query="SELECT Estado, Fecha, Cliente, Trabajo, Precio, Id FROM Lista_de_Trabajos" 
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.updateLista(rows)
        
        #------------------------------Seccion de busqueda
        
        self.lbl = Label(wrapper2, text="Busqueda")
        self.lbl.pack(side=tk.LEFT, padx=10)
        self.ent = Entry(wrapper2)
        self.ent.pack(side=tk.LEFT, padx=6)
        self.btn = Button(wrapper2, text="busqueda", command=self.search)
        self.btn.pack(side=tk.LEFT, padx=6)
        self.lbtn = Button(wrapper2, text="Limpiar",command=self.limpiar)
        self.lbtn.pack(side=tk.LEFT, padx=6) 
        
        #------------Seccion de carga y modificacion de datos                     

        self.lbl1 = Label(wrapper3, text="Cliente")
        self.lbl1.grid(row=1, column=0, padx=5, pady=3)
        self.ent1= Entry(wrapper3, textvariable=self.t1)
        self.ent1.grid(row=1, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl2 = Label(wrapper3, text="Trabajo")
        self.lbl2.grid(row=2, column=0, padx=5, pady=3)
        self.ent2= Entry(wrapper3, textvariable=self.t2)
        self.ent2.grid(row=2, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl3 = Label(wrapper3, text="Precio")
        self.lbl3.grid(row=3, column=0, padx=5, pady=3)
        self.ent3= Entry(wrapper3, textvariable=self.t3)
        self.ent3.grid(row=3, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.ag_btn=Button(wrapper3, text= "Agregar", command= self.agregar)
        self.ag_btn.grid(row=4, column=0, padx=5, pady=3)
        
        self.mod_btn=Button(wrapper3, text="Modificar", command=self.modificar)
        self.mod_btn.grid(row=4, column=1, padx=5, pady=3)
        
        self.el_btn=Button(wrapper3, text="Eliminar", command= self.eliminar)
        self.el_btn.grid(row=4, column=2, padx=5, pady=3)
        
        
#---------------------------METODOS------------------------        
    
    def updateLista(self,rows):
        #limpiando la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando los datos
        for i in rows:
            self.tabla.insert('', 'end', values=i)    
        
    def search(self):
        q2=self.ent.get()
        query= 'SELECT Estado, Fecha, Cliente, Trabajo, Precio, Id FROM Lista_de_Trabajos WHERE Cliente = ?'
        self.cursor.execute(query, [q2])
        rows = self.cursor.fetchall()
        self.updateLista(rows)
    
    def limpiar(self):
        query = "SELECT Estado, Fecha, Cliente, Trabajo, Precio, Id FROM Lista_de_Trabajos"        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.updateLista(rows)
    
    def getrow(self, event): #selecciono los datos y los paso a las variables t1,t2 y t3
        rowid = self.tabla.identify_row(event.y)
        item = self.tabla.item(self.tabla.focus())
        self.t1.set(item['values'][2])
        self.t2.set(item['values'][3])
        self.t3.set(item['values'][4])
        self.t4.set(item['values'][5])#variable que guarda el ID para eliminar
        
    def agregar(self):
        estado='Listo'
        fecha='Hoy'
        cliente=self.t1.get()
        trabajo=self.t2.get()
        precio=self.t3.get()
        query='INSERT INTO Lista_de_Trabajos(Estado, Fecha, Cliente, Trabajo, Precio, Id) VALUES(?,?,?,?,?,NULL)' 
        self.cursor.execute(query,(estado,fecha,cliente,trabajo,precio))
        self.conn.commit()
        messagebox.showinfo(message="Trabajo Agregado Correctamente!", title="Confirmacion")
        self.limpiar()
        
    def modificar(self):
        estado='Listo'
        fecha='Hoy'
        cliente=self.t1.get()
        trabajo=self.t2.get()
        precio=self.t3.get()
        id=self.t4.get()
        if messagebox.askyesno("Confirmar Modificacion","Estas Seguro de Modificar este trabajo?"):
            query = "UPDATE Lista_de_Trabajos SET Estado=?, Fecha=?, Cliente=?, Trabajo=?, Precio=?, Id=? WHERE Id= ?" 
            self.cursor.execute(query,(estado,fecha,cliente,trabajo,precio,id,id))
            self.conn.commit()
            self.limpiar()
        else:
            return True    
            
    def eliminar(self):
        idLista= self.t4.get()
        if messagebox.askyesno("Confirma que quiere eliminar?", "Estas seguro de eliminar este Trabajo?"): # Mensaje para confirmar eliminacion
            query='DELETE FROM Lista_de_Trabajos WHERE Id = ?'
            self.cursor.execute(query,(idLista))
            self.conn.commit()
            self.limpiar()
        else:
            return True       
        
window = Tk()
programa = listaDeTrabajos(window)



window.mainloop()        