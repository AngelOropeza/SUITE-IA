import tkinter as tk
from tkinter import ttk
from tkinter import OptionMenu, IntVar, StringVar
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
from tkintertable import TableCanvas, TableModel
import seaborn as sb
from pylab import *
from matplotlib import style
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import pandastable as pt

style.use("ggplot")

DATASETPATH = 'C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets/1Cancer.txt'
SEPARADORR='\t'

class uiCorrPearson(tk.Frame):
    def __init__(self, master=None, dataframepath=None, separador=None):
        super().__init__(master)
        self.dataframepath = dataframepath
        self.separador = separador
        #V A R I A B L E S
        self.dataframe = pd.read_table(self.dataframepath, sep=self.separador)
        #self.dataframe = pd.read_table(self.dataframepath)
        self.CPvarAnterior = 0
        self.CPselvar1 = StringVar()
        self.CPselvar2 = StringVar()
        setVariables = self.getVars() 
        self.opc_VAR1 = setVariables
        self.opc_VAR2 = setVariables

        #UserInterface
        self.master = master
        self.grid()
        self.frame_izq()
        self.frame_der()

    def frame_izq(self):
        RBst = ttk.Style()
        RBst.configure('Wild.TRadiobutton',
                background='#82A1B1',
                foreground='black',
                font=("Arial", 13))
        self.frame_left = tk.Frame(self.master, bg='#82A1B1')
        self.frame_left.configure(width=500, height=600)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        #TÍTULO
        ttk.Label(self.frame_left, background="#82A1B1", text="CORRELACIÓN DE PEARSON", font=("Arial Bold", 30)).grid(column=0, columnspan=2, row=0, padx=10, pady=30)

        self.CPvar = IntVar()
        self.RB1 = ttk.Radiobutton(self.frame_left, style='Wild.TRadiobutton', text="Matriz de correlaciones", variable=self.CPvar, value=0, command=self.sel_CPmode).grid(column=0, row=1, padx=0, pady=0)
        self.RB2 = ttk.Radiobutton(self.frame_left, style='Wild.TRadiobutton', text="Par de Variables", variable=self.CPvar, value=1, command=self.sel_CPmode).grid(column=1, row=1, padx=0, pady=30)

        self.popupMenu = OptionMenu(self.frame_left, self.CPselvar1, *self.opc_VAR1)
        ttk.Label(self.frame_left, background="#82A1B1", text="VARIABLE 1", font=("Arial Bold", 13)).grid(row = 2, column = 1)
        self.popupMenu.grid(row = 3, column =1)

        self.popupMenu = OptionMenu(self.frame_left, self.CPselvar2, *self.opc_VAR2)
        ttk.Label(self.frame_left, background="#82A1B1", text="VARIABLE 2", font=("Arial Bold", 13)).grid(row = 4, column = 1)
        self.popupMenu.grid(row = 5, column =1)

        ttk.Button(self.frame_left, text="Calcular correlación", style = 'TButton', command=self.renderCP, width = 50).grid(column=0, columnspan=2,row=7,padx=30,pady=50)    

    def frame_der(self):
        self.frame_right = tk.Frame(self.master,  bg='lightgray')
        self.frame_right.configure(width=500, height=600)
        self.frame_right.configure(relief="sunken")
        self.frame_right.grid(row=0, column=1, sticky="nsew")

    def getVars(self):
        dictVar = {}
        variables = list(self.dataframe)
        print(variables)        
        return set(variables)

    def sel_CPmode(self):
        seleccion = "Has seleccionado " + str(self.CPvar.get())
        print(seleccion)

    def renderCP(self):
        self.mCorrelacion = self.matrizCorrelacion() 
        self.mCorTable = pt.Table(self.frame_right, dataframe=self.mCorrelacion, showtoolbar=False, showstatusbar=True)
        if self.CPvar.get() == 0: #Matriz de correlaciones
            self.mCorTable.show()
            ttk.Button(self.frame_right, text="Mostrar Gráfico", style = 'TButton', command=self.muestraMcorrelaciones).grid(column=1,row=7,padx=100,pady=30)    
        else: #Par de variables
            var1 = self.CPselvar1.get()
            var2 = self.CPselvar2.get()
            corr = self.mCorrelacion[var1][var2]
            ttk.Label(self.frame_right, text="Correlacion: "+str(corr), font=("Arial Bold", 15)).grid(column=0, columnspan=2, row=0, padx=30, pady=30)
            fig = Figure(figsize=(4,4),dpi=100)
            plot1 = fig.add_subplot(111) 
            plot1.plot(self.dataframe[var1],self.dataframe[var2], 'r+')
            #plt.ylabel(var2)
            #plt.xlabel(var1)
            self.canvas = FigureCanvasTkAgg(fig, master = self.frame_right)
            self.canvas.draw() 

            self.canvas.get_tk_widget().grid(column=0, columnspan=2, row=1, padx=30, pady=30)

#METODOS CORR_PEARSON
    def matrizCorrelacion(self):
        mCorrelaciones = self.dataframe.corr(method='pearson')
        return mCorrelaciones

    def muestraMcorrelaciones(self):
        plt.matshow(self.mCorrelacion)
        matplotlib.pyplot.show()

def grafParVar(dataframe, var1, var2):
    plt.plot(dataframe[var1],dataframe[var2], 'r+')
    plt.ylabel(var2)
    plt.xlabel(var1)
    matplotlib.pyplot.show()

'''
# Main window
master = tk.Tk()
master.minsize(width="1000", height="600")
master.grid_columnconfigure(0, weight=1, uniform="group1")
master.grid_columnconfigure(1, weight=1, uniform="group1")
master.grid_rowconfigure(0, weight=1)
app = uiCorrPearson(master, DATASETPATH, SEPARADORR)
#Start program
app.mainloop()
'''