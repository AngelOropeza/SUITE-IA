import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkintertable import TableCanvas, TableModel
import pandastable as pt
import pandas as pd
import main as IA

class menuDatos(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.dataframepath = ''
        self.separador = ''
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
        self.frame_left = tk.Frame(self.master, bg='#3f6e3f')
        #self.frame_left.configure(width=800, height=500)
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        #TÍTULO
        ttk.Label(self.frame_left, background='#3f6e3f', text="DATOS", font=("Arial Bold", 50)).grid(column=0, columnspan=2, row=0, padx=100, pady=30)
        #BOTON BUSCAR ARCHIVO
        ttk.Label(self.frame_left, background='#3f6e3f', textvariable=self.filelabel, font=("Arial normal", 13)).grid(column=0, row=1, padx=15, pady=30)
        ttk.Button(self.frame_left, text="Buscar", style = 'TButton', command=self.selectDataset).grid(column=1,row=1,padx=0,pady=10)
        #FORM SEPARADOR
        ttk.Label(self.frame_left, background='#3f6e3f', text="Separador", font=("Arial normal", 13)).grid(column=0, row=2, padx=15, pady=30)
        self.separadorForm = ttk.Entry(self.frame_left)
        self.separadorForm.grid(column=1, row=2, padx=0, pady=30)
        self.separadorForm.grid_propagate(0)
        #BOTÓN VISUALIZAR DATOS
        ttk.Button(self.frame_left, text="Visualizar datos", style = 'TButton', command=self.showData, width=30).grid(column=0, columnspan=2, row=3,padx=0,pady=10)

    def frame_der(self):
        self.frame_right = tk.Frame(self.master,  bg='#8ecb93')
        #self.frame_right.configure(width=800, height=500)
        self.frame_right.grid(row=0, column=1, sticky="nsew")

        self.l1 = tk.Label(self.frame_right, textvariable=self.filepath)
        self.l1.grid(row=0, column=1)

        self.l1.grid_propagate(0)    


#        self.table = TableCanvas(self.frame_right, cellwidth=60, cellbackgr='lightgray',
#			thefont=('Arial',11),rowheight=18, rowheaderwidth=30,
#			rowselectedcolor='blue', read_only=True)
#       self.table.show()

    #METODOS MENU_DATOS
    def selectDataset(self):
        self.path = filedialog.askopenfilename(initialdir="C:/Users/Angel Oropeza/Desktop/ProyectoFinal/Suite/datasets", title="Seleccionar dataset", filetypes=(("csv files", "*.csv"),("txt files", "*.txt"),("xls files", "*.xls")))
        self.filepath.set(self.path)
        pathlist = self.filepath.get().split('/')
        self.filelabel.set(pathlist[len(pathlist)-1])
        print(self.filepath.get())

    def showData(self):
        separador = self.separadorForm.get()
        print(separador) 
        if(self.filepath.get() != ''):
            df = pd.read_table(self.filepath.get(), sep=separador)
            self.setFilepath(self.filepath.get())
            self.setSeparador(separador)
            print("ruta = {}".format(self.dataframepath))
            self.table = pt.Table(self.frame_right, dataframe=df, showtoolbar=False, showstatusbar=True)
            self.table.show()
            loadData = ttk.Button(self.frame_left, text="CARGAR DATOS", style = 'TButton', command=self.cargarDatos).grid(columnspan=2,row=8, pady=50, sticky=tk.S)
            
    def cargarDatos(self):
        master = tk.Tk()
        master.minsize(width="1000", height="600")
        app = IA.Application(master, self.dataframepath, self.separador)
        app.mainloop()

    def setFilepath(self, dataframepath):
        self.dataframepath = dataframepath
    
    def setSeparador(self, separador):
        self.separador = separador

    def getFilepath(self):
        return str(self.filepath.get())

# Main window
master = tk.Tk()
master.title("DATOS")
master.minsize(width="1000", height="600")
master.grid_columnconfigure(0, weight=1, uniform="group1")
master.grid_columnconfigure(1, weight=1, uniform="group1")
master.grid_rowconfigure(0, weight=1)
app = menuDatos(master)
#Start program
app.mainloop()

""" TENEMOS UN ERROR EN EL RADIOBUTTON DE LA CORRELACIÓN DE PEARSON, INDIVIDUALMENTE SÍ FUNCIONA, EN CONJUNTO 
NO """