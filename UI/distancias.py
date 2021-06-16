import tkinter as tk
from tkinter import ttk, OptionMenu
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from tkintertable import TableCanvas, TableModel
from math import sqrt
from scipy.spatial import distance 

DATASETPATH = 'C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets/Empleados.txt'
SEPARADOR = '\t'

class uiDistancias(tk.Frame):
    def __init__(self, master=None, dataframepath=None, separador=None):
        super().__init__(master)
        self.dataframepath = dataframepath
        self.separador = separador

        self.dataframe = pd.read_csv(self.dataframepath, sep=self.separador, header=None)
        #V A R I A B L E S
        self.opciones_Dist = {'euclidiana', 'chebyshev', 'manhattan','minkowski'}
        self.Dtipo_med = tk.StringVar(master)        
        #UserInterface
        self.master = master
        self.grid()
        self.frame_izq()
        self.frame_der()

    def frame_izq(self):
        self.frame_left = tk.Frame(self.master, bg='#8c92ac')
        self.frame_left.configure(width=500, height=600)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        #TÍTULO
        ttk.Label(self.frame_left, background='#8c92ac',text="MÉTRICAS DE SIMILITUD", font=("Arial Bold", 35)).grid(column=0, columnspan=2, row=0, padx=20, pady=30)

        self.popupMenu = OptionMenu(self.frame_left, self.Dtipo_med, *self.opciones_Dist)
        ttk.Label(self.frame_left, background='#8c92ac', text="Seleccione tipo de medición", font=("Arial Bold", 13)).grid(row = 1, column = 0, pady=30)
        self.popupMenu.grid(row = 1, column =1, padx=0, pady=0)

        ttk.Button(self.frame_left, text="Calcular matriz", style = 'TButton', command=self.renderMat, width = 50).grid(column=0, columnspan=2,row=6,padx=0,pady=50)

    def frame_der(self):
        self.frame_right = tk.Frame(self.master,  bg='#cee2e1')
        self.frame_right.configure(width=700, height=600)
        self.frame_right.configure(relief="sunken")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        
    #METODOS DISTANCIAS
    def renderMat(self):
        dfl = df2tuples(self.dataframe)
        matList = matrizSimilitud(dfl, self.Dtipo_med.get())
        ttk.Label(self.frame_right, background='#cee2e1',text="Matriz de similitud", font=("Times normal", 25)).grid(column=0, columnspan=len(matList), row=0, padx=50, pady=30)
        for i in range(0, len(matList)):
            for j in range(0, len(matList[0])):
                elem = tk.Label(self.frame_right, text=str(round(matList[i][j],2)), width=6, borderwidth=2, relief="sunken", font=("Arial", 7))
                elem.grid(padx=1, pady=1,row=i+1,column=j)

def distanciaEuclidiana(E1, E2):
    dEuclidiana = sqrt(sum((E1-E2)**2 for E1, E2 in zip(E1,E2)))
    return dEuclidiana

def df2tuples(df):
    dfl = []
    columnas = len(df.columns) 
    filas = len(df.index) 
    for i in range(1, filas): #ignoramos primera fila (header)
        elem = []
        for j in range(1, columnas): #ignoramos primera columna (id)
            elem.append(float(df.iloc[i][j]))
        dfl.append(tuple(elem))
    return dfl

def matrizSimilitud(listuple, method):
    total = []
    if method == 'euclidiana':
        for i in range(0, len(listuple)):
            elem =[]
            for j in range(0, len(listuple)):
                elem.append(distanciaEuclidiana(listuple[i],listuple[j]))
            total.append(elem)
    elif method == 'chebyshev':
        for i in range(0, len(listuple)):
            elem =[]
            for j in range(0, len(listuple)):
                elem.append(distance.chebyshev(listuple[i],listuple[j]))
            total.append(elem)
    elif method == 'manhattan':
        for i in range(0, len(listuple)):
            elem =[]
            for j in range(0, len(listuple)):
                elem.append(distance.cityblock(listuple[i],listuple[j]))
            total.append(elem)
    elif method == 'minkowski':
        for i in range(0, len(listuple)):
            elem =[]
            for j in range(0, len(listuple)):
                elem.append(distance.minkowski(listuple[i],listuple[j]))
            total.append(elem)
    return total

'''
# Main window
master = tk.Tk()
master.minsize(width="1200", height="600")
master.grid_columnconfigure(0, weight=1, uniform="group1")
master.grid_columnconfigure(1, weight=1, uniform="group1")
master.grid_rowconfigure(0, weight=1)
app = uiDistancias(master, DATASETPATH, SEPARADOR)
#Start program
app.mainloop()
'''