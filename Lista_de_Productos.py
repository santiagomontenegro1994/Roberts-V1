from tkinter import *
from tkinter import ttk

class listaDeProductos:
    
    def __init__(self,window):
        self.wind = window
        self.wind.title("Lista de Productos")
        
        #creando contenedor
        frame=LabelFrame(self.wind, text = 'Registra un nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady = 20)
        
        #nombre cliente
        Label(frame, text='Producto: ' ).grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        
        #telefono cliente
        Label(frame, text='Precio: ' ).grid(row=2, column=0)
        self.telefono = Entry(frame)
        self.telefono.grid(row=2, column=1)
        
        #boton agregar cliente
        ttk.Button(frame, text="Guardar Producto").grid(row= 4, columnspan=2, sticky=W + E)
        
        #mensajes de notificacion
        self.mensaje = Label(text = '', fg = 'red')
        self.mensaje.grid(row=3, column=0, columnspan=3, sticky=W + E)
        
        #tabla de clientes
        self.tabla = ttk.Treeview(columns=("Precio"))
        self.tabla.grid(row=6, column=0, columnspan=3)
        self.tabla.heading('#0', text= 'Producto', anchor=CENTER)
        self.tabla.heading('#1', text= 'Precio', anchor=CENTER)



window = Tk()
programa = listaDeProductos(window)
window.mainloop()        