import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from tkintertable import TableCanvas, TableModel


DATASETPATH = 'C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets/store_data.csv'

class uiApriori(tk.Frame):
    def __init__(self, master=None, dataframepath=None):
        super().__init__(master)
        self.dataframepath = dataframepath
        #V A R I A B L E S
        self.filelabel = tk.StringVar()
        self.filelabel.set('Seleccione archivo')
        self.filepath = tk.StringVar()
        self.filepath.set('')
        
        #UserInterface
        self.master = master
        self.grid()
        self.frame_izq()
        self.frame_der()

    def frame_izq(self):
        self.frame_left = tk.Frame(self.master, bg='CadetBlue')
        self.frame_left.configure(width=500, height=600)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        #TÍTULO
        ttk.Label(self.frame_left, background="CadetBlue", text="APRIORI", font=("Arial Bold", 50)).grid(column=0, columnspan=2, row=0, padx=120, pady=30)

        ttk.Label(self.frame_left, background="CadetBlue", text="Soporte Mínimo", font=("Arial Bold", 15)).grid(column=0, row=1, padx=30, pady=30)
        self.soporte = ttk.Entry(self.frame_left)
        self.soporte.grid(column=1, row=1, padx=30, pady=30)

        ttk.Label(self.frame_left, background="CadetBlue", text="Confianza mínima", font=("Arial Bold", 15)).grid(column=0, row=2, padx=30, pady=30)
        self.confianza = ttk.Entry(self.frame_left)
        self.confianza.grid(column=1, row=2, padx=30, pady=30)

        ttk.Label(self.frame_left, background="CadetBlue", text="Elevación", font=("Arial Bold", 15)).grid(column=0, row=3, padx=30, pady=30)
        self.elevacion = ttk.Entry(self.frame_left)
        self.elevacion.grid(column=1, row=3, padx=30, pady=30)

        self.reglasG = ttk.Button(self.frame_left, text="Generar reglas de asociación", style = 'TButton', command=self.renderRA, width = 50).grid(column=0, columnspan=2 ,row=4,padx=0,pady=10)        

    def frame_der(self):
        self.frame_right = tk.Frame(self.master,  bg='Azure2')
        self.frame_right.configure(width=500, height=600)
        self.frame_right.configure(relief="sunken")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        
        ttk.Label(self.frame_right, background="Azure2", text="Reglas de asociación", font=("Arial Bold", 25)).grid(column=0, columnspan=2, row=0, padx=50, pady=30)

        self.canvas = tk.Canvas(self.frame_right, bg="Azure2",width="500", height="500")
        self.scrollBar = tk.Scrollbar(self.frame_right, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="Azure2")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0,0),window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollBar.set)

        self.canvas.grid(row=1, column=0)
        self.scrollBar.grid(row=1,column=1, sticky="ns")

    #METODOS APRIORI
    def renderRA(self):
        elementoRA = ''
        rowix = 1
        sp = float(self.soporte.get())
        cf = float(self.confianza.get())
        lf = float(self.elevacion.get())
        registros = datos2list(self.dataframepath)
        print("DATOS LEIDOS Y CONVERTIDOS EN LISTA")
        reglas = RA(registros, sp, cf, lf, 2)
        print("REGLAS GENERADAS")
        for item in reglas:
            pair = item[0] 
            items = [x for x in pair]
            ruleStr = "◘ Regla: " + items[0] + " -> " + items[1]
            suppStr = "◘ Soporte: " + str(item[1]) 
            confStr = "◘ Confianza: " + str(item[2][0][2])
            liftStr = "◘ Lift: " + str(item[2][0][3]) 
            diviStr = "====================================="
            elementoRA= ruleStr + "\n" + suppStr + "\n" + confStr + "\n" + liftStr + "\n" + diviStr
            ttk.Label(self.scrollable_frame, text=elementoRA, background="Azure3").grid(column=0, columnspan=2, row=rowix, padx=110, pady=5)
            rowix+=1


#Procesamiento de datos
def datos2list(datasethpath):
    datospd = pd.read_csv(datasethpath, header=None) # Instanciar los datos en el objeto Datos. 
    registros = []
    num_filas=len(datospd.index)
    num_columnas=len(datospd.axes[1])
    for i in range(0, num_filas):
            registros.append([str(datospd.values[i,j]) for j in range(0, num_columnas)]) #Introducimos todos las transacciones en una lista.
    return registros

#Reglas de asociación
def RA(registros, soporte, confianza, elevacion, long_min):
    reglas_a = apriori(registros, min_support=soporte, min_confidence=confianza, min_lift=elevacion, min_length=long_min)
    reglas = list(reglas_a)
    return reglas
    
'''
# Main window
master = tk.Tk()
master.minsize(width="1000", height="600")
master.grid_columnconfigure(0, weight=1, uniform="group1")
master.grid_columnconfigure(1, weight=1, uniform="group1")
master.grid_rowconfigure(0, weight=1)
app = uiApriori(master, DATASETPATH)
#Start program
app.mainloop()
'''
