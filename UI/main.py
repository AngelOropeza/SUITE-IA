import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkintertable import TableCanvas, TableModel
import apriori as aP
import corrPearson as cP
import distancias as dM
import clusteringParticional as kM
import rLogistica as rL
#TODO enviar dataframe o ruta a los constructores de los algoritmos
DATASETPATH = ''

class Application(tk.Frame):
    def __init__(self, master=None, dataframepath=None, separador=None):
        super().__init__(master)
        self.master = master
        self.dataframepath = dataframepath
        self.separador = separador
        #UserInterface
        self.grid()
        self.navbar()
        #--------------------
        self.apriori()
        self.correlacion()
        self.distancia()
        self.clustering()
        self.logistica()

    def navbar(self):
        self.master.title("SUITE ARTIFICIAL INTELLIGENCE")
        #Creación de notebook
        self.pestañas = ttk.Notebook(self, width=1200, height=600, padding=10)
        #Algoritmo 1
        self.pest_apriori = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pest_apriori, text = 'APRIORI')
        #Algoritmo 2
        self.pest_correlacion = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pest_correlacion, text = 'CORRELACIÓN DE PEARSON')
        #Algoritmo 3
        self.pest_medicion = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pest_medicion, text = 'MÉTRICAS DE SIMILITUD')
        #Algoritmo 4
        self.pest_clustering = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pest_clustering, text = 'CLUSTERING PARTICIONAL')
        #Algoritmo 5
        self.pest_logistica = ttk.Frame(self.pestañas)
        self.pestañas.add(self.pest_logistica, text = 'REGRESIÓN LOGÍSTICA')

        self.pestañas.pack(expand=True, fill=tk.BOTH)
    
    def apriori(self):
        self.pest_apriori.grid_columnconfigure(0, weight=1, uniform="group1")
        self.pest_apriori.grid_columnconfigure(1, weight=1, uniform="group1")
        self.pest_apriori.grid_rowconfigure(0, weight=1)
        app_ap = aP.uiApriori(self.pest_apriori, self.dataframepath)
        #Start program
        #app_ap.mainloop()

    def correlacion(self):
        self.pest_correlacion.grid_columnconfigure(0, weight=1, uniform="group1")
        self.pest_correlacion.grid_columnconfigure(1, weight=1, uniform="group1")
        self.pest_correlacion.grid_rowconfigure(0, weight=1)
        app_cP = cP.uiCorrPearson(self.pest_correlacion, self.dataframepath, self.separador)
        #Start program
        #app_ap.mainloop()

    def distancia(self):
        self.pest_medicion.grid_columnconfigure(0, weight=1, uniform="group1")
        self.pest_medicion.grid_columnconfigure(1, weight=1, uniform="group1")
        self.pest_medicion.grid_rowconfigure(0, weight=1)
        app_dM = dM.uiDistancias(self.pest_medicion, self.dataframepath, self.separador)
        #Start program
        #app_ap.mainloop()

    def clustering(self):
        self.pest_clustering.grid_columnconfigure(0, weight=1, uniform="group1")
        self.pest_clustering.grid_columnconfigure(1, weight=1, uniform="group1")
        self.pest_clustering.grid_rowconfigure(0, weight=1)
        app_kM = kM.uiClustering(self.pest_clustering, self.dataframepath, self.separador)

    def logistica(self):
        self.pest_logistica.grid_columnconfigure(0, weight=1, uniform="group1")
        self.pest_logistica.grid_columnconfigure(1, weight=1, uniform="group1")
        self.pest_logistica.grid_rowconfigure(0, weight=1)
        app_rL = rL.uiRLogistica(self.pest_logistica)

    def renderApp(self):        
        # Main window
        master = tk.Tk()
        master.minsize(width="1000", height="600")
        app = Application(master, self.dataframepath)
        #Start program
        app.mainloop()
