from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3

class listaDeProductos():
    
    db_nombre = 'database.db'
    with sqlite3.connect(db_nombre) as conn:
            cursor = conn.cursor() 
    
    def __init__(self,window):
        self.wind = window
        self.wind.title("Lista de Productos")
        
        self.seleccion=tk.IntVar()
        
        #creando contenedor
        frame=LabelFrame(self.wind, text = 'Registra un nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady = 20)
        frame1=LabelFrame(self.wind, text = 'Busqueda')
        frame1.grid(row=1, column=0, columnspan=3, pady = 20)
        
        #producto
        Label(frame, text='Producto: ' ).grid(row=1, column=0)
        self.producto = Entry(frame)
        self.producto.focus()
        self.producto.grid(row=1, column=1)
        
        #precio
        Label(frame, text='Precio: ' ).grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)
        
        #boton agregar producto
        ttk.Button(frame, text="Guardar Producto", command = self.add_productos).grid(row= 4, columnspan=2, sticky=W + E)
        
        #mensajes de notificacion
        self.mensaje = Label(self.wind, text = '', fg = 'red')
        self.mensaje.grid(row=3, column=0, columnspan=3, sticky=W + E)
        
        #------------------------------Seccion de busqueda
        
        self.ent = Entry(frame1)
        self.ent.grid(row=0, column=0,columnspan=2, sticky= W+E)
        self.btn = Button(frame1, text="busqueda", command=self.search)
        self.btn.grid(row=0, column=2)
        self.lbtn = Button(frame1, text="Limpiar",command=self.get_productos)
        self.lbtn.grid(row=0, column=3)
        self.rbotonTrabajo = tk.Radiobutton(frame1, text="Producto", variable=self.seleccion, value=1, command=self.search)
        self.rbotonTrabajo.grid(row=1, column=0, padx=15, pady=5)
        self.rbotonTrabajo = tk.Radiobutton(frame1, text="Precio", variable=self.seleccion, value=2, command=self.search)
        self.rbotonTrabajo.grid(row=1, column=1, padx=15, pady=5) 
        
        #tabla de productos
        self.tabla = ttk.Treeview(self.wind, columns=("Precio"))
        self.tabla.grid(row=6, column=0, columnspan=3)
        self.tabla.heading('#0', text= 'Producto', anchor=CENTER)
        self.tabla.heading('#1', text= 'Precio', anchor=CENTER)
        
        #Agregando la scrollbar
        self.yscrollbar=ttk.Scrollbar(self.wind, orient="vertical", command=self.tabla.yview)
        self.yscrollbar.grid(row=6,column=4,  sticky=N + S)
        self.tabla.configure(yscrollcommand=self.yscrollbar.set)
        
        #boton para eliminar y Editar
        ttk.Button(self.wind, text = 'Eliminar', command=self.delete_productos).grid(row=5, column=0, sticky=W + E)
        ttk.Button(self.wind, text = 'Editar', command=self.edit_productos).grid(row=5, column=1, sticky=W + E)
        
        #llenando las filas de la tabla 
        self.get_productos()
    

        
    def run_query(self, query, parameters =()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def get_productos(self):
        #limpiando la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando los datos    
        query = 'SELECT * FROM Productos ORDER BY producto ASC'
        db_rows=self.run_query(query)
        #rellenando los datos
        for row in db_rows:
            self.tabla.insert('', 0, text = row[1], value = row[2])

    def search(self):
        if self.seleccion.get()==1:
            q2=self.ent.get().upper()
            #limpiando la tabla
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #consultando los datos    
            query = 'SELECT * FROM Productos WHERE producto = ?'
            db_rows=self.run_query(query,[q2])
            #rellenando los datos
            for row in db_rows:
                self.tabla.insert('', 0, text = row[1], value = (row[2])) 
        elif self.seleccion.get()==2:
            q2=self.ent.get().upper()
            #limpiando la tabla
            records = self.tabla.get_children()
            for element in records:
                self.tabla.delete(element)
            #consultando los datos    
            query = 'SELECT * FROM Productos WHERE precio = ?'
            db_rows=self.run_query(query,[q2])
            #rellenando los datos
            for row in db_rows:
                self.tabla.insert('', 0, text = row[1], value = (row[2]))     
        else:    
            self.mensaje['text'] = 'Parametros de busqueda son requeridos'

    def validacion(self): #valida para que no pase un dato vacio
        return len(self.producto.get()) != 0 and len(self.precio.get()) !=0 
    
    def add_productos(self):  #metodo para agregar clientes
        if self.validacion():
            query = 'INSERT INTO Productos VALUES(NULL, ?, ?)'
            parameters = (self.producto.get().upper(), self.precio.get().upper())
            self.run_query(query, parameters)
            self.mensaje['text'] = 'Producto: {} agregado'.format(self.producto.get())
            self.producto.delete(0,END)
            self.precio.delete(0,END)
            self.get_productos()
        else:
            self.mensaje['text'] = 'Producto y Precio son requeridos'
            self.get_productos()

    def delete_productos(self):
        self.mensaje['text'] = '' # vacio la casilla del mensaje
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='Porfavor selecciona un producto'
            return
        self.mensaje['text'] = '' # vacio la casilla del mensaje
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM Productos WHERE producto = ?'
        self.run_query(query, (nombre,))
        self.mensaje['text'] = 'Producto: {} se elimino satisfactoriamente'.format(nombre)
        self.get_productos()

    def edit_productos(self):
        self.mensaje['text'] = ''
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='Porfavor selecciona un producto'
            return
        
        old_producto = self.tabla.item(self.tabla.selection())['text']
        old_precio = self.tabla.item(self.tabla.selection())['values'][0]
        self.ventana_editar = Toplevel() # ventana de editar
        self.ventana_editar.title = 'Editar Producto'
        
        # Producto Anterior
        Label(self.ventana_editar, text = 'Producto anterior: ').grid(row=0, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_producto), state = 'readonly').grid(row=0, column=2)
        # Producto Nuevo
        Label(self.ventana_editar, text ='Nuevo Producto').grid(row=1, column=1)
        nuevo_producto = Entry(self.ventana_editar,  textvariable=StringVar(self.ventana_editar, value= old_producto))
        nuevo_producto.grid(row=1, column=2)
        
        # Precio Anterior
        Label(self.ventana_editar, text = 'Precio anterior: ').grid(row=2, column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_precio), state = 'readonly').grid(row=2, column=2)
        # Precio Nuevo
        Label(self.ventana_editar, text ='Nuevo Precio').grid(row=3, column=1)
        nuevo_precio = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value= old_precio))
        nuevo_precio.grid(row=3, column=2)
        
        #boton para agregar 
        Button(self.ventana_editar, text='Editar', command=lambda: self.edit_records(nuevo_producto.get(), old_producto, nuevo_precio.get(), old_precio)).grid(row=6, column=2, sticky=W + E)
  
    def edit_records(self, nuevo_producto, old_producto, nuevo_precio, old_precio):
        if  len(nuevo_producto) != 0 and len(nuevo_precio) !=0:  #valido que no le pasen valores vacios
            query= 'UPDATE Productos set producto = ?, precio = ? WHERE producto = ? AND precio = ?'
            parameters = (nuevo_producto.upper(), nuevo_precio, old_producto, old_precio)
            self.run_query(query, parameters) #le paso la consulta
            self.ventana_editar.destroy() #cierro la ventana editar
            self.mensaje['text'] = 'Datos del producto {} modificados correctamente'.format(nuevo_producto)
            self.get_productos()
        else:
            self.mensaje['text'] = 'Producto y Precio son requeridos'
            
            
#window = Tk()
#programa = listaDeProductos(window)
#window.mainloop()        