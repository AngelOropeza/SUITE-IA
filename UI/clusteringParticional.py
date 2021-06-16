import tkinter as tk
from tkinter import ttk, OptionMenu, Listbox
import numpy as np
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


DATASETPATH = 'C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets/WDBCOriginal.csv'
SEPARADOR = ','

class uiClustering(tk.Frame):         
    def __init__(self, master=None, dataframepath=None, separador=None):
        super().__init__(master)
        self.dataframepath = dataframepath
        self.separador = separador

        self.dataframe = pd.read_csv(self.dataframepath, sep=self.separador)
        #self.variablesModelo
        #V A R I A B L E S
        self.variablesModelo = np.empty(2)   
        #UserInterface
        self.master = master
        self.grid()
        self.frame_izq()
        self.frame_der()

    def frame_izq(self):
        self.frame_left = tk.Frame(self.master, bg='#d4c76b')
        self.frame_left.configure(width=500, height=600)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        #TÍTULO
        ttk.Label(self.frame_left, background='#d4c76b',text="CLUSTERING PARTICIONAL", font=("Arial Bold", 30)).grid(column=0, columnspan=2, row=0, padx=20, pady=5)
        ttk.Label(self.frame_left, background='#d4c76b',text="K-MEANS", font=("Arial Normal", 15)).grid(column=0, columnspan=2, row=1, padx=20, pady=0)
        #1 VARIABLES
        ttk.Label(self.frame_left, background='#d4c76b',text="1) Selección de variables", font=("Arial Normal", 12)).grid(column=0, row=2, padx=0, pady=20)
        self.variablesBox = df2listBox(self.frame_left, self.dataframe)
        self.variablesBox.grid(column=0, columnspan=2, row=3, padx=15, pady=0)
        ttk.Button(self.frame_left, text="Seleccionar variables", style = 'TButton', command=self.selectVariables, width = 20).grid(column=0, columnspan=2 ,row=4,padx=0,pady=10)
        ttk.Button(self.frame_left, text="Obtener clusteres", style = 'TButton', command=self.clusteringParticional, width = 30).grid(column=0, columnspan=2 ,row=5,padx=0,pady=10)
        

    def frame_der(self):
        self.frame_right = tk.Frame(self.master,  bg='#e7e0ac')
        self.frame_right.configure(width=700, height=600)
        self.frame_right.configure(relief="sunken")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        
    #METODOS 
    def selectVariables(self):
        indextuple=self.variablesBox.curselection()
        listvars=[]
        for ix in indextuple:
            listvars.append(self.variablesBox.get(ix))
        print(listvars)
        self.variablesModelo = np.array(self.dataframe[listvars])
        print(self.variablesModelo)

    def clusteringParticional(self):
        #CALCULO DE # DE CLUSTERS
        SSE = []
        for i in range(2, 16):
            km = KMeans(n_clusters=i, random_state=0)
            km.fit(self.variablesModelo)
            SSE.append(km.inertia_)
        kl = KneeLocator(range(2, 16), SSE, curve="convex", direction="decreasing")
        nClusters = kl.elbow
        #Creación de clusters
        self.Mparticional = KMeans(nClusters, random_state=0).fit(self.variablesModelo)
        self.Mparticional.predict(self.variablesModelo)
        self.dataframe['clusterP'] = self.Mparticional.labels_
        clusteres = self.dataframe.groupby(['clusterP'])['clusterP'].count()
        #Cluster descripcion
        elem=tk.Label(self.frame_right, background='#e7e0ac', text="CLUSTERS", font=("Arial Bold", 20))
        elem.grid(column=0, columnspan=6, row=0, pady=5, padx=5)
        for i in range(len(clusteres)):
            elem=tk.Label(self.frame_right, background='#e7e0ac', text="CLUSTER_"+str(i+1)+"->"+str(clusteres[i])+"  ")
            elem.grid(column=i, row=1, pady=5, padx=5)
        #Centroides de clusteres
        self.centroidesP = self.Mparticional.cluster_centers_
        centroides = pd.DataFrame(self.centroidesP.round(4))
        elem=tk.Label(self.frame_right, background='#e7e0ac', text="Centroides", font=("Arial Bold", 15))
        elem.grid(column=0, columnspan=6, row=len(clusteres+1), pady=5, padx=5)

        elem = tk.Label(self.frame_right, background='#e7e0ac', text="CLUSTER", relief="solid")
        elem.grid(column=0,row=len(clusteres)+2,pady=10, padx=5)
        for i in range(len(centroides)):
            elem=tk.Label(self.frame_right, background='#e7e0ac', text=str(i+1), relief="solid")
            elem.grid(column=i+1, row=len(clusteres)+2, pady=10, padx=5)
        for j in range(len(centroides[0])):
            elem=tk.Label(self.frame_right, background='#e7e0ac', text=str(j+1), relief="solid")
            elem.grid(column=0, row=len(clusteres)+3+j, pady=10, padx=5)
        for i in range(len(centroides)):
            for j in range(len(centroides[0])):
                elem=tk.Label(self.frame_right, background='#e7e0ac', text=str(centroides[i][j]))
                elem.grid(column=j+1, row=len(clusteres)+3+i, pady=10, padx=5)
        ttk.Button(self.frame_right, text="Mostrar gráfico", style = 'TButton', command=self.showPlot, width = 30).grid(column=0, columnspan=6 ,row=2*len(centroides)+3,padx=0,pady=10)

    def showPlot(self):
        plt.rcParams['figure.figsize'] = (10, 7)
        plt.style.use('ggplot')
        colores=['red', 'blue', 'cyan', 'green', 'yellow']
        asignar=[]
        for row in self.Mparticional.labels_:
            asignar.append(colores[row])
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter (self.variablesModelo[:, 0], self.variablesModelo[:, 1], self.variablesModelo[:, 2], marker='o', c=asignar, s=60)
        ax.scatter(self.centroidesP[:, 0], self.centroidesP[:, 1], self.centroidesP[:, 2], marker='*', c=colores, s=1000)
        plt.show()

def df2listBox(masterTk,df):
    variables = list(df)
    variablesBox = tk.Listbox(masterTk, selectmode=tk.MULTIPLE, bg='#e7e0ac', selectbackground='#31621c')
    for i in range(len(variables)):
        variablesBox.insert(i, variables[i])
    return variablesBox

'''
# Main window
master = tk.Tk()
master.minsize(width="1200", height="600")
master.grid_columnconfigure(0, weight=1, uniform="group1")
master.grid_columnconfigure(1, weight=1, uniform="group1")
master.grid_rowconfigure(0, weight=1)
app = uiClustering(master, DATASETPATH, SEPARADOR)
#Start program
app.mainloop()
'''