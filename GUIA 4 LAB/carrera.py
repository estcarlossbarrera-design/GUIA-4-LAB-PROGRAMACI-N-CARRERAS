import tkinter as tk
from tkinter import ttk,messagebox
from vehiculo import Vehiculo

class Carrera:
    def __init__(self,root):
        self.root=root
        self.root.title("Competencia Automovilística")
        self.root.geometry("950x650")
        self.vehiculos=[]
        self.resultados=[]
        self.fin=0
        self.crear()

    def crear(self):
        top=tk.Frame(self.root)
        top.pack(pady=10)
        tk.Label(top,text="Apuesta:").pack(side="left")
        self.apuesta=tk.IntVar(value=1)
        ttk.Combobox(top,textvariable=self.apuesta,values=list(range(1,11)),width=5,state="readonly").pack(side="left",padx=5)
        tk.Label(top,text="Rondas:").pack(side="left")
        self.rondas=tk.IntVar(value=1)
        tk.Spinbox(top,from_=1,to=10,textvariable=self.rondas,width=5).pack(side="left",padx=5)
        tk.Label(top,text="Velocidad:").pack(side="left")
        self.slider=tk.Scale(top,from_=0.3,to=2,resolution=0.1,orient="horizontal",length=150)
        self.slider.set(1)
        self.slider.pack(side="left",padx=5)
        self.boton=tk.Button(top,text="Iniciar",command=self.iniciar)
        self.boton.pack(side="left",padx=10)
        self.canvas=tk.Canvas(self.root,width=900,height=400,bg="white")
        self.canvas.pack()
        self.dibujar_pista()
        self.imgs=[tk.PhotoImage(file=f"imgs/car{i}.png").subsample(20,20) for i in range(1,11)]
        cols=("Posición","Vehículo","Tiempo")
        self.tabla=ttk.Treeview(self.root,columns=cols,show="headings",height=8)
        for c in cols:
            self.tabla.heading(c,text=c)
        self.tabla.pack(pady=10)

    def dibujar_pista(self):
        self.canvas.create_line(30,10,30,390,width=3)
        self.canvas.create_line(800,10,800,390,width=3)
        self.canvas.create_text(30,395,text="SALIDA")
        self.canvas.create_text(800,395,text="META")

    def iniciar(self):
        self.canvas.delete("all")
        self.dibujar_pista()
        self.resultados=[]
        self.fin=0
        self.vehiculos=[]
        self.boton.config(state="disabled")

        velocidad=self.slider.get()
        rondas=self.rondas.get()

        for i in range(10):
            y=20+i*35
            v=Vehiculo(i+1,self.canvas,y,760,rondas,velocidad,self.fin_hilo,self.imgs[i])
            self.vehiculos.append(v)

        for v in self.vehiculos:
            v.start()

    def fin_hilo(self,v):
        self.root.after(0,self.termino,v)

    def termino(self,v):
        self.resultados.append(v)
        self.fin+=1
        if self.fin==10:
            self.mostrar()

    def mostrar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        self.resultados.sort(key=lambda x:x.tiempo)

        for i,v in enumerate(self.resultados,1):
            self.tabla.insert("",tk.END,values=(i,f"Vehículo {v.id}",round(v.tiempo,2)))

        ganador=self.resultados[0].id
        self.boton.config(state="normal")

        if ganador==self.apuesta.get():
            messagebox.showinfo("Resultado",f"¡Ganaste!\nEl vehículo {ganador} llegó primero.")
        else:
            messagebox.showinfo("Resultado",f"Perdiste.\nGanó el vehículo {ganador}.")