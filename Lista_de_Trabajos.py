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
        
        self.t1=tk.StringVar()
        self.t2=tk.StringVar()
        self.t3=tk.StringVar()
        self.t4=tk.StringVar()
        self.t5=tk.StringVar()
        self.t6=tk.StringVar()
        self.t7=tk.StringVar()
        self.seleccion=tk.IntVar()
        bgcolor='#D3A7D4'
        bgcolor1='#D3A7D4'
        bgbuttoncolor='#99339C'
        
        self.wind.configure(bg=bgcolor)
        
        #Creando el contenedor
        wrapper1 = LabelFrame(window,bg=bgcolor, text="LISTA DE TRABAJOS")
        wrapper2 = LabelFrame(window,bg=bgcolor, text="BUSQUEDA")
        wrapper3 = LabelFrame(window,bg=bgcolor)
        wrapper4 = LabelFrame(wrapper1,bg=bgcolor, text="Cargar Lista de Trabajos")
        wrapper5 = LabelFrame(wrapper1,bg=bgcolor, text="Cargar Lista de Productos")
        wrapper6 = LabelFrame(wrapper1,bg=bgcolor, text="Cargar Lista de Clientes")
        wrapper7 = LabelFrame(wrapper1,bg=bgcolor, text="Cargar Lista de Proveedores")
        
        
        wrapper1.grid(row=0, column=0, padx=20, pady=10)
        wrapper2.grid(row=1, column=0, padx=20, pady=10)
        wrapper3.grid(row=2, column=0, padx=20, pady=10)
        wrapper4.grid(row=0,column=0, padx=15, pady=10)
        wrapper5.grid(row=0,column=1, padx=15, pady=10)
        wrapper6.grid(row=0,column=2, padx=15, pady=10)
        wrapper7.grid(row=0,column=3, padx=15, pady=10)
        
        #------------------------------Seccion de lista
        
        #Creando el treeview
        self.tabla = ttk.Treeview(wrapper3, columns=(1,2,3,4,5,6,7,8,9), show="headings")
        self.style=ttk.Style(self.tabla)
        self.style.theme_use('clam')
        self.style.configure('Treeview', rowheight=20)
        self.style.configure('Treeview.Heading',font=('Sans','8','bold'),foreground="#FFFFFF", background=bgbuttoncolor)
      
        self.tabla.grid(row=0,column=0)
        self.tabla.heading(1, text="ESTADO")
        self.tabla.heading(2, text="FECHA")
        self.tabla.heading(3, text="CLIENTE")
        self.tabla.heading(4, text="TRABAJO")
        self.tabla.heading(5, text="ENVIADO A")
        self.tabla.heading(6, text="PRECIO")
        self.tabla.heading(7, text="SEÑA")
        self.tabla.heading(8, text="SALDO")
        self.tabla.heading(9, text="ID")
        
        #dando el ancho de las columnas
        self.tabla.column('#1', width=120, anchor='c')
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
        self.yscrollbar=ttk.Scrollbar(wrapper3, orient="vertical", command=self.tabla.yview)
        self.yscrollbar.grid(row=0,column=1,  sticky=N + S)
        self.tabla.configure(yscrollcommand=self.yscrollbar.set)
        
        #lleno la lista de elementos
        self.limpiar()
        
        #------------------------------Seccion de busqueda
        
        self.lbl = Label(wrapper2, text="Busqueda",bg=bgcolor)
        self.lbl.grid(row=0, column=0)
        self.ent = Entry(wrapper2)
        self.ent.grid(row=0, column=1)
        self.btn = Button(wrapper2, text="BUSCAR",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command=self.search)
        self.btn.grid(row=0, column=2, padx=5)
        self.lbtn = Button(wrapper2, text="LIMPIAR",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 ,command=self.limpiar)
        self.lbtn.grid(row=0, column=3, padx=5)
        self.rbotonTrabajo = tk.Radiobutton(wrapper2, text="Nombre", bg=bgcolor, variable=self.seleccion, value=1, command=self.search)
        self.rbotonTrabajo.grid(row=0, column=4, padx=15, pady=5)
        self.rbotonTrabajo = tk.Radiobutton(wrapper2, text="Trabajo", bg=bgcolor, variable=self.seleccion, value=2, command=self.search)
        self.rbotonTrabajo.grid(row=0, column=5, padx=15, pady=5) 
        self.rbotonFecha = tk.Radiobutton(wrapper2, text="Fecha", bg=bgcolor, variable=self.seleccion, value=3, command=self.search)
        self.rbotonFecha.grid(row=0, column=6, padx=15, pady=5)
        self.rbotonEstado = tk.Radiobutton(wrapper2, text="Estado", bg=bgcolor, variable=self.seleccion, value=4, command=self.search)
        self.rbotonEstado.grid(row=0, column=7, padx=15, pady=5)
        self.rbotonId = tk.Radiobutton(wrapper2, text="Id", bg=bgcolor, variable=self.seleccion, value=5, command=self.search)
        self.rbotonId.grid(row=0, column=8, padx=15, pady=5)
        
        #------------Seccion de carga y modificacion de datos                     

        self.lbl1 = Label(wrapper4, text="Estado",bg=bgcolor)
        self.lbl1.grid(row=1, column=0, padx=5, pady=3)
        self.combo4= ttk.Combobox(wrapper4, textvariable=self.t1, state="readonly")
        self.combo4.grid(row=1, column=1, pady=3, columnspan=3, sticky= W+E)
        self.combo4["values"]=("PENDIENTE","PENDIENTE IMPRES.","DISEÑO EMPEZADO","MUESTRA ENVIADA","IMPRESO","ENVIADO","LISTO","ENTREGADO","FALTA DE PAGO")
        
        self.lbl1 = Label(wrapper4, text="Cliente",bg=bgcolor)
        self.lbl1.grid(row=2, column=0, padx=5, pady=3)
        self.combo1= ttk.Combobox(wrapper4, textvariable=self.t2, state="readonly")
        self.combo1.grid(row=2, column=1, pady=3, columnspan=3, sticky= W+E)
        self.llenarCombo1()
        
        self.lbl2 = Label(wrapper4, text="Trabajo",bg=bgcolor)
        self.lbl2.grid(row=3, column=0, padx=5, pady=3)
        self.combo3= ttk.Combobox(wrapper4, textvariable=self.t3)
        self.combo3.grid(row=3, column=1, pady=3, columnspan=3, sticky= W+E)
        self.llenarCombo3()
        
        self.lbl2 = Label(wrapper4, text="Enviado a:",bg=bgcolor)
        self.lbl2.grid(row=4, column=0, padx=5, pady=3)
        self.combo2= ttk.Combobox(wrapper4, textvariable=self.t4, state="readonly")
        self.combo2.grid(row=4, column=1, pady=3, columnspan=3, sticky= W+E)
        self.llenarCombo2()
        
        self.lbl3 = Label(wrapper4, text="Precio",bg=bgcolor)
        self.lbl3.grid(row=5, column=0, padx=5, pady=3)
        self.ent3= Entry(wrapper4, textvariable=self.t5)
        self.ent3.grid(row=5, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.lbl3 = Label(wrapper4, text="Seña",bg=bgcolor)
        self.lbl3.grid(row=6, column=0, padx=5, pady=3)
        self.ent3= Entry(wrapper4, textvariable=self.t6)
        self.ent3.grid(row=6, column=1, pady=3, columnspan=3, sticky= W+E)
        
        self.ag_btn=Button(wrapper4, text= " AGREGAR ",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command= self.agregar)
        self.ag_btn.grid(row=1, column=6, padx=5, pady=3)
        
        self.mod_btn=Button(wrapper4, text="MODIFICAR",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command=self.modificar)
        self.mod_btn.grid(row=2, column=6, padx=5, pady=3)
        
        self.el_btn=Button(wrapper4, text=" ELIMINAR ",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command= self.eliminar)
        self.el_btn.grid(row=3, column=6, padx=5, pady=3)
        
        self.lim_btn=Button(wrapper4, text="  LIMPIAR  ",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command= self.limpiarc)
        self.lim_btn.grid(row=4, column=6, padx=5, pady=3)
        
        self.listProd_btn=Button(wrapper5, text="LISTA DE PRODUCTOS",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command= self.listaProductos)
        self.listProd_btn.grid(row=0, column=0, padx=50, pady=30)
        self.actProd_btn=Button(wrapper5, text="ACTUALIZAR",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 , command= self.llenarCombo3)
        self.actProd_btn.grid(row=1, column=0, padx=50, pady=30)
        
        self.listClie_btn=Button(wrapper6, text="LISTA DE CLIENTES",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 ,command= self.listaClientes)
        self.listClie_btn.grid(row=0, column=0, padx=50, pady=30)
        self.actClie_btn=Button(wrapper6, text="ACTUALIZAR",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 ,command= self.llenarCombo1)
        self.actClie_btn.grid(row=1, column=0, padx=50, pady=30)
        
        self.listPro_btn=Button(wrapper7, text="LISTA PROVEEDORES",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor,borderwidth=3 ,command= self.listaProveedores)
        self.listPro_btn.grid(row=0, column=0, padx=50, pady=16)
        self.listPro_btn=Button(wrapper7, text="TRABAJOS PENDIENTES",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 ,command= self.listaProveedores)
        self.listPro_btn.grid(row=1, column=0, padx=50, pady=15)
        self.actPro_btn=Button(wrapper7, text="ACTUALIZAR",font=('Sans','8','bold'),fg="#FFFFFF" ,background=bgbuttoncolor, borderwidth=3 ,command= self.llenarCombo2)
        self.actPro_btn.grid(row=2, column=0, padx=50, pady=16)
        
        
 
        
#---------------------------METODOS------------------------        
    
    def updateLista(self,rows):
        #limpiando la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando los datos
        for i in rows:
            self.tabla.insert('', 'end', values=i, tags = (i[0],))
        #Le agrego color a la fila depende su estado    
        self.tabla.tag_configure('PENDIENTE', background='#D55E3B')
        self.tabla.tag_configure('PENDIENTE IMPRES.', background='#D55E3B')
        self.tabla.tag_configure('DISEÑO EMPEZADO', background='#F3F705')
        self.tabla.tag_configure('MUESTRA ENVIADA', background='#F3F705')
        self.tabla.tag_configure('IMPRESO', background='#B4E968')
        self.tabla.tag_configure('ENVIADO', background='#B4E968')
        self.tabla.tag_configure('LISTO', background='#B4E968')
        self.tabla.tag_configure('ENTREGADO', background='#D3A7D4')
        self.tabla.tag_configure('FALTA DE PAGO', background='#0078FF')     
    
    def listaClientes(self):
        listClientes = Toplevel()
        ListaDeClientes(listClientes)      
        
    def listaProductos(self):
        listProductos = Toplevel()
        listaDeProductos(listProductos)
        
    def listaProveedores(self):
        listProveedores = Toplevel()
        ListaDeProveedores(listProveedores)            

    def llenarCombo1(self):
        query = "SELECT nombre FROM Clientes ORDER BY nombre ASC"     
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        lista=[]
        for i in rows:
            string = str(i)
            new_string = string.lstrip("('")
            lista.append(new_string[:-3])
        self.combo1["values"]=lista
    
    def llenarCombo2(self):
        query = "SELECT nombre FROM Proveedores ORDER BY nombre ASC"     
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        lista=[]
        for i in rows:
            string = str(i)
            new_string = string.lstrip("('")
            lista.append(new_string[:-3])
        self.combo2["values"]=lista
    
    def llenarCombo3(self):
        query = "SELECT producto FROM Productos ORDER BY producto ASC"     
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        lista=[]
        for i in rows:
            string = str(i)
            new_string = string.lstrip("('")
            lista.append(new_string[:-3])
        self.combo3["values"]=lista
    
    def limpiarc(self):
        self.t1.set('')
        self.t2.set('')
        self.t3.set('')
        self.t4.set('')
        self.t5.set('')
        self.t6.set('')
        self.t7.set('')                        
        
    def search(self):
        if self.seleccion.get()==1:
            q2='%'+self.ent.get().upper()+'%'
            query= "SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos WHERE Cliente LIKE ?"
            self.cursor.execute(query,[q2])
            rows = self.cursor.fetchall()
            self.updateLista(rows)
        elif self.seleccion.get()==2:
            q2='%'+self.ent.get().upper()+'%'
            query= 'SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos WHERE Trabajo LIKE ?'
            self.cursor.execute(query, [q2])
            rows = self.cursor.fetchall()
            self.updateLista(rows)
        elif self.seleccion.get()==3:
            q2='%'+self.ent.get().upper()+'%'
            query= 'SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos WHERE Fecha LIKE ?'
            self.cursor.execute(query, [q2])
            rows = self.cursor.fetchall()
            self.updateLista(rows)
        elif self.seleccion.get()==4:
            q2=self.ent.get().upper()
            query= 'SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos WHERE Estado = ?'
            self.cursor.execute(query, [q2])
            rows = self.cursor.fetchall()
            self.updateLista(rows)
        elif self.seleccion.get()==5:
            q2=self.ent.get().upper()
            query= 'SELECT Estado, Fecha, Cliente, Trabajo, Proveedor, Precio, Seña, Saldo, Id FROM Lista_de_Trabajos WHERE Id = ?'
            self.cursor.execute(query, [q2])
            rows = self.cursor.fetchall()
            self.updateLista(rows)    
        else:    
            messagebox.showinfo(message="No ha seleccionado ningun parametro de busqueda", title="Confirmacion")
    
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
        trabajo=self.t3.get().upper()
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
            self.limpiarc()
        else:
            messagebox.showinfo(message="No se puede agregra trabajo con datos vacios", title="Aviso!")
            
    def modificar(self):
        estado=self.t1.get()
        cliente=self.t2.get()
        trabajo=self.t3.get().upper()
        proveedor=self.t4.get()
        precio=self.t5.get()
        seña=self.t6.get()
        id=self.t7.get()
        if  len(estado) != 0 and len(cliente) !=0 and len(trabajo) !=0 and len(precio) !=0 and len(seña) !=0:  #valido que no le pasen valores vacios
            saldo= int(precio)-int(seña)
            if messagebox.askyesno("Confirmar Modificacion","Estas Seguro de Modificar este trabajo?"):
                query = "UPDATE Lista_de_Trabajos SET Estado=?, Cliente=?, Trabajo=?, Proveedor=?, Precio=?, Seña=?, Saldo=?, Id=? WHERE Id= ?" 
                self.cursor.execute(query,(estado,cliente,trabajo,proveedor,precio,seña,saldo,id,id))
                self.conn.commit()
                self.limpiar()
                self.limpiarc()
            else:
                return True    
        else:
            messagebox.showinfo(message="No se puede modificar un trabajo con datos vacios", title="Aviso!")
                
    def eliminar(self):
        idLista= self.t7.get()
        if messagebox.askyesno("Confirma que quiere eliminar?", "Estas seguro de eliminar este Trabajo?"): # Mensaje para confirmar eliminacion
            query='DELETE FROM Lista_de_Trabajos WHERE Id = ?'
            self.cursor.execute(query,[idLista])
            self.conn.commit()
            self.limpiar()
            self.limpiarc()
        else:
            return True       

if __name__ =="__main__":        
    window = Tk()
    programa = listaDeTrabajos(window)
    window.mainloop()        