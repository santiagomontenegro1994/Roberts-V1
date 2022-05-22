
from tkinter import *
from tkinter import ttk
import sqlite3


class ListaDeClientes:
    
    db_nombre = 'database.db' 
    
    def __init__(self,window):
        self.wind=window
        self.wind.title("Lista de Clientes")
        
        #creando contenedor
        frame=LabelFrame(self.wind, text = 'Registra un nuevo Cliente')
        frame.grid(row=0, column=0, columnspan=3, pady = 20)
        
        #nombre cliente
        Label(frame, text='Nombre: ' ).grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        
        #telefono cliente
        Label(frame, text='Telefono: ' ).grid(row=2, column=0)
        self.telefono = Entry(frame)
        self.telefono.grid(row=2, column=1)
        
        #cuit cliente
        Label(frame, text='Cuit: ' ).grid(row=3, column=0)
        self.cuit = Entry(frame)
        self.cuit.grid(row=3, column=1)
        
        #boton agregar cliente
        ttk.Button(frame, text="Guardar Cliente").grid(row= 4, columnspan=2, sticky=W + E)
        
        
        #tabla de clientes
        self.tabla = ttk.Treeview(columns=("tel", "cuit"))
        self.tabla.grid(row=6, column=0, columnspan=3)
        self.tabla.heading('#0', text= 'Nombre', anchor=CENTER)
        self.tabla.heading('#1', text= 'Telefono', anchor=CENTER)
        self.tabla.heading('#2', text= 'Cuit', anchor=CENTER)
        
        self.get_clientes()
        
    def run_query(self, query, parameters =()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result        

    def get_clientes(self):
        #limpiando la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando los datos    
        query = 'SELECT * FROM Clientes ORDER BY nombre ASC'
        db_rows=self.run_query(query)
        #rellenando los datos
        for row in db_rows:
            print(row)
            #self.tabla.insert('', 0, text = [1], value = row[2],)
        
    
if __name__ == '__main__':
    window = Tk()
    aplicacion = ListaDeClientes(window) 
    window.mainloop()  

        
    

