from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from Lista_de_Clientes import ListaDeClientes
from Lista_de_Proveedores import ListaDeProveedores
from Lista_de_Productos import listaDeProductos



class listaDeTrabajos():
    
    db_nombre = 'database.db'
    with sqlite3.connect(db_nombre) as conn:
            cursor = conn.cursor()         
    
    
    def __init__(self,window):
        self.wind=window
        self.wind.title("Lista de Trabajos")
        self.wind.geometry("1200x800")
        
        self.t1=tk.StringVar()
        self.t2=tk.StringVar()
        self.t3=tk.StringVar()
        self.t4=tk.StringVar()
        self.t5=tk.StringVar()
        self.t6=tk.StringVar()
        self.t7=tk.StringVar()
        
        #Creando el contenedor
        wrapper1 = LabelFrame(window, text="Lista de Trabajos")
        wrapper2 = LabelFrame(window, text="Busqueda")
        wrapper3 = LabelFrame(window)
        wrapper4 = LabelFrame(wrapper3, text="Cargar Lista de Trabajos")
        wrapper5 = LabelFrame(wrapper3, text="Cargar Lista de Productos")
        wrapper6 = LabelFrame(wrapper3, text="Cargar Lista de Clientes")
        wrapper7 = LabelFrame(wrapper3, text="Cargar Lista de Proveedores")
        
        
        wrapper1.grid(row=0, column=0, padx=20, pady=10)
        wrapper2.grid(row=1, column=0, padx=20, pady=10)
        wrapper3.grid(row=2, column=0, padx=20, pady=10)
        wrapper4.grid(row=0,column=0, padx=15, pady=10)
        wrapper5.grid(row=0,column=1, padx=15, pady=10)
        wrapper6.grid(row=0,column=2, padx=15, pady=10)
        wrapper7.grid(row=0,column=3, padx=15, pady=10)
        
        #------------------------------Seccion de lista
        
        #Creando el treeview
        self.tabla = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6,7,8,9), show="headings")
        self.style=ttk.Style(self.tabla)
        self.style.configure('Treeview', rowheight=25)
        
        self.tabla.grid(row=0,column=0)
        self.tabla.heading(1, text="Estado")
        self.tabla.heading(2, text="Fecha")
        self.tabla.heading(3, text="Cliente")
        self.tabla.heading(4, text="Trabajo")
        self.tabla.heading(5, text="Enviado a")
        self.tabla.heading(6, text="Precio")
        self.tabla.heading(7, text="Seña")
        self.tabla.heading(8, text="Saldo")
        self.tabla.heading(9, text="Id")
        
        #dando el ancho de las columnas
        self.tabla.column('#1', width=70, anchor='c')
        self.tabla.column('#2', width=70, anchor='c')
        self.tabla.column('#3', width=300, anchor='c')
        self.tabla.column('#4', width=300, anchor='c')
        self.tabla.column('#5', width=100, anchor='c')
        self.tabla.column('#6', width=70, anchor='c')
        self.tabla.column('#7', width=70, anchor='c')
        self.tabla.column('#8', width=70, anchor='c')
        self.tabla.column('#9', width=50, anchor='c')
        
        self.tabla.bind('<Double-1>', self.getrow)# al hacer doble click selecciona un cliente con los datos
        
        #Agregando la scrollbar
        self.yscrollbar=ttk.Scrollbar(wrapper1, orient="vertical", command=self.tabla.yview)
        self.yscrollbar.grid(row=0,column=1,  sticky=N + S)
        self.tabla.configure(yscrollcommand=self.yscrollbar.set)
        
        #lleno la lista de elementos
        query="SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos" 
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.updateLista(rows)
        
        #------------------------------Seccion de busqueda
        
        self.lbl = Label(wrapper2, text="Busqueda")
        self.lbl.grid(row=0, column=0)
        self.ent = Entry(wrapper2)
        self.ent.grid(row=0, column=1)
        self.btn = Button(wrapper2, text="busqueda", command=self.search)
        self.btn.grid(row=0, column=2)
        self.lbtn = Button(wrapper2, text="Limpiar",command=self.limpiar)
        self.lbtn.grid(row=0, column=3) 
        
        #------------Seccion de carga y modificacion de datos                     

        self.lbl1 = Label(wrapper4, text="Estado")
        self.lbl1.grid(row=1, column=0, padx=5, pady=3)
        self.ent1= Entry(wrapper4, textvariable=self.t1)
        self.ent1.grid(row=1, column=1, pady=3, columnspan=3, sticky= W+E)
        self.lbl1 = Label(wrapper4, text="P / EP / L / E")
        self.lbl1.grid(row=1, column=4, padx=5, pady=3)
        
        self.lbl1 = Label(wrapper4, text="Cliente")
        self.lbl1.grid(row=2, column=0, padx=5, pady=3)
        self.ent1= Entry(wrapper4, textvariable=self.t2)
        self.ent1.grid(row=2, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl2 = Label(wrapper4, text="Trabajo")
        self.lbl2.grid(row=3, column=0, padx=5, pady=3)
        self.ent2= Entry(wrapper4, textvariable=self.t3)
        self.ent2.grid(row=3, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl2 = Label(wrapper4, text="Enviado a:")
        self.lbl2.grid(row=4, column=0, padx=5, pady=3)
        self.ent2= Entry(wrapper4, textvariable=self.t4)
        self.ent2.grid(row=4, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl3 = Label(wrapper4, text="Precio")
        self.lbl3.grid(row=5, column=0, padx=5, pady=3)
        self.ent3= Entry(wrapper4, textvariable=self.t5)
        self.ent3.grid(row=5, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl3 = Label(wrapper4, text="Seña")
        self.lbl3.grid(row=6, column=0, padx=5, pady=3)
        self.ent3= Entry(wrapper4, textvariable=self.t6)
        self.ent3.grid(row=6, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.ag_btn=Button(wrapper4, text= "Agregar", command= self.agregar)
        self.ag_btn.grid(row=1, column=6, padx=5, pady=3)
        
        self.mod_btn=Button(wrapper4, text="Modificar", command=self.modificar)
        self.mod_btn.grid(row=2, column=6, padx=5, pady=3)
        
        self.el_btn=Button(wrapper4, text="Eliminar", command= self.eliminar)
        self.el_btn.grid(row=3, column=6, padx=5, pady=3)
        
        self.lim_btn=Button(wrapper4, text="Limpiar", command= self.limpiarc)
        self.lim_btn.grid(row=4, column=6, padx=5, pady=3)
        
        self.listProd_btn=Button(wrapper5, text="Ver Lista de Productos", command= self.listaProductos)
        self.listProd_btn.grid(row=0, column=0, padx=50, pady=70)
        
        self.listClie_btn=Button(wrapper6, text="Ver Lista de Clientes", command= self.listaClientes)
        self.listClie_btn.grid(row=0, column=0, padx=50, pady=70)
        
        self.listPro_btn=Button(wrapper7, text="Ver Lista de Proveedores", command= self.listaProveedores)
        self.listPro_btn.grid(row=0, column=0, padx=50, pady=70)
 
        
#---------------------------METODOS------------------------        
    
    def updateLista(self,rows):
        #limpiando la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando los datos
        for i in rows:
            self.tabla.insert('', 'end', values=i) 
    
    def listaClientes(self):
        listClientes = Toplevel()
        ListaDeClientes(listClientes)      
        
    def listaProductos(self):
        listProductos = Toplevel()
        listaDeProductos(listProductos)
        
    def listaProveedores(self):
        listProveedores = Toplevel()
        ListaDeProveedores(listProveedores)            
    
    def limpiarc(self):
        self.t1.set('')
        self.t2.set('')
        self.t3.set('')
        self.t4.set('')
        self.t5.set('')
        self.t6.set('')
        self.t7.set('')                        
        
    def search(self):
        q2=self.ent.get()
        query= 'SELECT Estado, Fecha, Cliente, Trabajo, Precio, Proveedor, Seña, Saldo, Id FROM Lista_de_Trabajos WHERE Cliente = ?'
        self.cursor.execute(query, [q2])
        rows = self.cursor.fetchall()
        self.updateLista(rows)
    
    def limpiar(self):
        query = "SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos"        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.updateLista(rows)
    
    def getrow(self, event): #selecciono los datos y los paso a las variables t
        rowid = self.tabla.identify_row(event.y)
        item = self.tabla.item(self.tabla.focus())
        self.t1.set(item['values'][0])
        self.t2.set(item['values'][2])
        self.t3.set(item['values'][3])
        self.t4.set(item['values'][4])
        self.t5.set(item['values'][5])
        self.t6.set(item['values'][6])
        self.t7.set(item['values'][8])#varible que guarda el ID para eliminar
        
    def agregar(self):
        estado=self.t1.get()
        fecha=datetime.now()
        fecha=fecha.strftime('%d-%m-%Y')
        cliente=self.t2.get()
        trabajo=self.t3.get()
        proveedor=self.t4.get()
        precio=self.t5.get()
        seña=self.t6.get()
        
        if  len(estado) != 0 and len(cliente) !=0 and len(trabajo) !=0 and len(precio) !=0  and len(seña) !=0 :  #valido que no le pasen valores vacios
            saldo= int(precio)-int(seña)
            query='INSERT INTO Lista_de_Trabajos(Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id) VALUES(?,?,?,?,?,?,?,?,NULL)' 
            self.cursor.execute(query,(estado,fecha,cliente,trabajo,proveedor,precio,seña,saldo))
            self.conn.commit()
            messagebox.showinfo(message="Trabajo Agregado Correctamente!", title="Confirmacion")
            self.limpiar()
        else:
            messagebox.showinfo(message="No se puede agregra trabajo con datos vacios", title="Aviso!")
            
    def modificar(self):
        estado=self.t1.get()
        fecha='Hoy'
        cliente=self.t2.get()
        trabajo=self.t3.get()
        proveedor=self.t4.get()
        precio=self.t5.get()
        seña=self.t6.get()
        id=self.t7.get()
        if  len(estado) != 0 and len(cliente) !=0 and len(trabajo) !=0 and len(precio) !=0 and len(seña) !=0:  #valido que no le pasen valores vacios
            saldo= int(precio)-int(seña)
            if messagebox.askyesno("Confirmar Modificacion","Estas Seguro de Modificar este trabajo?"):
                query = "UPDATE Lista_de_Trabajos SET Estado=?, Fecha=?, Cliente=?, Trabajo=?, Proveedor=?, Precio=?, Seña=?, Saldo=?, Id=? WHERE Id= ?" 
                self.cursor.execute(query,(estado,fecha,cliente,trabajo,proveedor,precio,seña,saldo,id,id))
                self.conn.commit()
                self.limpiar()
            else:
                return True    
        else:
            messagebox.showinfo(message="No se puede modificar un trabajo con datos vacios", title="Aviso!")
                
    def eliminar(self):
        idLista= self.t7.get()
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