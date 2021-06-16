import tkinter as tk
from tkinter import ttk, OptionMenu, Listbox
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

DATASETPATH = 'C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets/WDBCOriginal.csv'
SEPARADOR = ','

class uiRLogistica(tk.Frame):         
    def __init__(self, master=None):
        super().__init__(master)
        self.dataframepath = 'C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets/WDBCOriginal.csv'
        self.separador = ','

        self.dataframe = pd.read_csv(self.dataframepath, sep=self.separador)
        #self.variablesModelo
        #V A R I A B L E S

        #UserInterface
        self.master = master
        self.grid()
        self.frame_izq()
        self.frame_der()

    def frame_izq(self):
        self.frame_left = tk.Frame(self.master, bg='#80dbd7')
        self.frame_left.configure(width=250, height=500)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        #TÍTULO
        ttk.Label(self.frame_left, background='#80dbd7',text="REGRESIÓN LOGÍSTICA", font=("Arial Bold", 30)).grid(column=0, columnspan=4, row=0, padx=50, pady=5)
        ttk.Label(self.frame_left, background='#80dbd7',text="Modelo de predicción de diagnóstico de cancer de mama", font=("Arial Normal", 12)).grid(column=0, columnspan=4, row=1, padx=0, pady=10)
        
        ttk.Label(self.frame_left, background='#80dbd7',text="ID Paciente", font=("Arial Bold", 13)).grid(column=0, row=2, padx=0, pady=10)
        self.id_paciente = ttk.Entry(self.frame_left)
        self.id_paciente.grid(column=1, row=2, padx=0, pady=30)

        ttk.Label(self.frame_left, background='#80dbd7',text="Texture", font=("Arial Bold", 13)).grid(column=2, row=2, padx=0, pady=10)
        self.texture = ttk.Entry(self.frame_left)
        self.texture.grid(column=3, row=2, padx=0, pady=30)

        ttk.Label(self.frame_left, background='#80dbd7',text="Area", font=("Arial Bold", 13)).grid(column=0, row=3, padx=0, pady=10)
        self.area = ttk.Entry(self.frame_left)
        self.area.grid(column=1, row=3, padx=0, pady=30)

        ttk.Label(self.frame_left, background='#80dbd7',text="Compactness", font=("Arial Bold", 13)).grid(column=2, row=3, padx=0, pady=10)
        self.compactness = ttk.Entry(self.frame_left)
        self.compactness.grid(column=3, row=3, padx=0, pady=30)

        ttk.Label(self.frame_left, background='#80dbd7',text="Concavity", font=("Arial Bold", 13)).grid(column=0, row=4, padx=0, pady=10)
        self.concavity = ttk.Entry(self.frame_left)
        self.concavity.grid(column=1, row=4, padx=0, pady=30)

        ttk.Label(self.frame_left, background='#80dbd7',text="Symmetry", font=("Arial Bold", 13)).grid(column=2, row=4, padx=0, pady=10)
        self.symmetry = ttk.Entry(self.frame_left)
        self.symmetry.grid(column=3, row=4, padx=0, pady=30)

        ttk.Label(self.frame_left, background='#80dbd7',text="Fractal Dimension", font=("Arial Bold", 13)).grid(column=0, row=5, padx=0, pady=10)
        self.fractalD = ttk.Entry(self.frame_left)
        self.fractalD.grid(column=1, row=5, padx=0, pady=30)

        ttk.Button(self.frame_left, text="Obtener diagnóstico", style = 'TButton', command=self.diagnostico, width = 80).grid(column=0, columnspan=4 ,row=6,padx=0,pady=10)
        

    def frame_der(self):
        self.frame_right = tk.Frame(self.master,  bg='#d9ffd5')
        self.frame_right.configure(width=250, height=500)
        self.frame_right.configure(relief="sunken")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        
    #METODOS 
    def diagnostico(self):
        self.BCancer = self.dataframe.replace({'M':0, 'B':1})
        #Variables predictoras
        X = np.array(self.BCancer[['Texture', 'Area', 'Compactness','Concavity', 'Symmetry', 'FractalDimension']])
        #Variable clase
        Y = np.array(self.BCancer[['Diagnosis']])
        self.Clasificacion= linear_model.LogisticRegression()
        validation_size = 0.2
        seed=1234
        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed, shuffle = True)
        self.Clasificacion.fit(X_train, Y_train)
        #Predicciones probabilisticas
        self.Probabilidad = self.Clasificacion.predict_proba(X_train)
        #Predicciones con clasificación final
        self.Predicciones = self.Clasificacion.predict(X_train)

        self.Paciente = pd.DataFrame({'Texture': [float(self.texture.get())], 'Area': [float(self.area.get())], 'Compactness': [float(self.compactness.get())], 'Concavity': [float(self.concavity.get())], 'Symmetry': [float(self.symmetry.get())], 'FractalDimension': [float(self.fractalD.get())]})

        resultado = self.Clasificacion.predict(self.Paciente)
        ttk.Label(self.frame_right, background='#d9ffd5',text="DIAGNÓSTICO", font=("Helvetica Bold", 15)).grid(column=0, columnspan=2, row=0, padx=50, pady=5)
        self.cuadro = tk.Text(self.frame_right, width=40, height=14, background='#a0ffaa')
        self.cuadro.insert(tk.INSERT, "\n\n\tIDpaciente: "+str(self.id_paciente.get())+"\n\tTexture: "+str(self.texture.get())+"\n\tArea: "+str(self.area.get())+"\n\tCompactness: "+str(self.compactness.get())+"\n\tConcavity: "+str(self.concavity.get())+"\n\tSymmetry: "+str(self.symmetry.get())+"\n\tFractalDimension: "+self.fractalD.get())
        if(resultado[0]==1):
            self.cuadro.insert(tk.END, "\n\n\n\tEl tumor es BENIGNO")
        else:
            self.cuadro.insert(tk.END, "\n\n\n\tEl tumor es MALIGNO")
        self.cuadro.grid(column=0, row=1, columnspan=2, padx=60, pady=10)
'''
# Main window
master = tk.Tk()
master.minsize(width="1000", height="500")
master.grid_columnconfigure(0, weight=1, uniform="group1")
master.grid_columnconfigure(1, weight=1, uniform="group1")
master.grid_rowconfigure(0, weight=1)
app = uiRLogistica(master)
#Start program
app.mainloop()
'''