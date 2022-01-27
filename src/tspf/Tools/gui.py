"""
Modulo dedicado a la interfaz grafica de usuario

"""

from .. import AlgorithmsOptions, MHType, InitialSolution
from tkinter import Label, Tk, Frame, Button, Checkbutton, LabelFrame, Entry, StringVar
from tkinter import messagebox, filedialog, ttk
import os


class Gui():


    options: AlgorithmsOptions
    
    algorithm: MHType
    
    frame: Frame
    
    frameOptions: Frame
    
    frameFeedback: Frame
    
    
    def __init__(self, root) -> None:
        self.root = root
        
        self.configureWindow()
        self.welcomeScreen()
        

    def configureWindow(self) -> None:
        """ Configura la ventana principal de la interfaz """
        self.root.title('TSP-Framework')
        #self.root.resizable(0,0)
        self.root.geometry('700x500')
        #self.root.bind_all("<Button-1>", lambda event: event.widget.focus_set()) # fuerza el focus donde el usuario haga click
        #self.root.eval('tk::PlaceWindow . right')
        
        #root.geometry('1366x768')
        
    def onQuit(self) -> None:
        """ Al salir o cerrar ventana """
        if messagebox.askokcancel("Salir", "¿Quieres salir de TSP-Framework?", icon="warning", parent=self.root):
            quit(self.root)
            
            
    def openFile(self) -> None:
        """ Abrir archivo de instancia TSP """
        self.options.instance = filedialog.askopenfilename(title='Abrir archivo de instancia con problema TSP', 
                                                    initialdir='instances/',
                                                    filetypes=(('Archivo de instancia con problema TSP', '*.tsp'),))
        if self.options.instance:
            self.mainScreen()
            
    def saveFile(self, extension: str, ar: StringVar) -> None:
        """ Abrir archivo de instancia TSP """
        sol = ''
        tra = ''
        if extension == '.txt':
            sol = filedialog.asksaveasfilename(title='Abrir archivo de solucion al problema TSP', 
                                                    initialdir=os.getcwd(),
                                                    filetypes=(('Archivo de solucion', '*.txt'),))
        elif extension == '.csv':
            tra = filedialog.asksaveasfilename(title='Abrir archivo de trayectoria a la solucion al problema TSP', 
                                                    initialdir=os.getcwd(),
                                                    filetypes=(('Archivo de trayectoria a la solucion', '*.csv'),))    
        
        if sol:
            if not '.txt' in sol:
                sol += '.txt'
            self.options.solution = sol
            ar.set(sol)
        if tra:
            if not '.csv' in tra:
                tra += '.csv'
            self.options.trajectory = tra
            ar.set(tra)
        
    def mainScreen(self) -> None:
        
        self.root.geometry('1366x768')
        self.frame.destroy()
        self.frame = LabelFrame(
                    self.root,
                    text='Selecciona un metodo de busqueda para solucionar el problema',
                    bg='#f0f0f0',
                    font=('consolas', 15)
                )
        
        self.frame.pack(anchor='center', pady=10)
        
        b = Button(self.frame, text='Simulated Annealing', command=self.simulatedAnnealing)
        b.config()
        b.pack(anchor='ne', side='left', padx=50, pady=50)
        
        b = Button(self.frame, text='Algoritmo Generico', command=self.geneticAlgorithm)
        b.config()
        b.pack(anchor='se', side='left', padx=50, pady=50)
        
        b = Button(self.frame, text='Local Search', command=self.localSearch)
        b.config()
        b.pack(anchor='sw', side='right', padx=50, pady=50)
        
        b = Button(self.frame, text='Iterated Local Search', command=self.iteratedLocalSearch)
        b.config()
        b.pack(anchor='nw', side='right', padx=50, pady=50)
        
        
    
    
    def simulatedAnnealing(self) -> None:
        """  """
        
        self.frame.destroy()
        self.optionsFrame()
        self.algorithm = MHType.SA
        
        
        frameSA = LabelFrame(
                    self.frameOptions,
                    text='Opciones Simulated Annealing',
                    bg='#f0f0f0',
                    font=(20)
                )
        
        #frameSA.pack(anchor='n', side='right', padx=25, pady=15)
        frameSA.grid(column=3, row=0, padx=25, pady=15)
        
        l = Label(frameSA, text='Archivo de salida para la solucion: ')
        l.grid(row=1, column=2, padx=5, pady=5)
        v = StringVar(frameSA, value=self.options.solution)
        e = Entry(frameSA, textvariable=v, state='disabled')
        e.grid(row=1, column=2, padx=5, pady=5)
        
    
    def geneticAlgorithm(self) -> None:
        """  """
        self.frame.destroy()
        self.optionsFrame()
        self.algorithm = MHType.GA
        
    def localSearch(self) -> None:
        """  """
        self.frame.destroy()
        self.optionsFrame()
        self.algorithm = MHType.LS
        
    def iteratedLocalSearch(self) -> None:
        """  """
        self.frame.destroy()
        self.optionsFrame()
        self.algorithm = MHType.ILS
    
        

    def optionsFrame(self) -> None:
        """ Configurar frame de opciones """
        
        # Configurar seccion de opciones 
        self.frameOptions = LabelFrame(
                    self.root,
                    text='Opciones',
                    bg='#f0f0f0',
                    width=720,
                    height=900,
                    font=("consolas", 20)
                )
        
        self.frameOptions.pack(anchor='nw', side='left', padx=25, pady=5)
        #self.frameOptions.grid(column=0, row=0, padx=25, pady=15)
        
        # configurar seccion de Feedback
        self.frameFeedback = LabelFrame(
                    self.root,
                    text='Output',
                    bg='#f0f0f0',
                    width=720,
                    height=900,
                    font=(20)
                )
        
        self.frameFeedback.pack(anchor='n', side='right', padx=25, pady=5)
        #self.frameFeedback.grid(column=0, row=1, padx=25, pady=15)
        
        # configurar seccion de opciones generales
        frameGeneral = LabelFrame(
                    self.frameOptions,
                    text='Opciones Generales',
                    bg='#f0f0f0',
                    width=720,
                    height=900, 
                    font=("consolas", 22)
                )
        
        #frameGeneral.pack(anchor='n', side='left', padx=25, pady=15)
        frameGeneral.grid(row=0, column=0, padx=25, pady=15)
        
        # Opciones
        # archivo de solucion
        l = Label(frameGeneral, text='Archivo para la solucion: ')
        l.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        sol = StringVar(frameGeneral, value=self.options.solution)
        e = Entry(frameGeneral, textvariable=sol, state='disabled')
        e.grid(row=1, column=1, padx=5, pady=5)
        b = Button(frameGeneral, text='Cambiar', command=lambda: self.saveFile('.txt', sol))
        b.grid(row=1, column=2, padx=5, pady=5)
        
        # archivo de trayectoria
        l = Label(frameGeneral, text='Archivo para la trayectoria de la solucion: ')
        l.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tra = StringVar(frameGeneral, value=self.options.trajectory)
        e = Entry(frameGeneral, textvariable=tra, state='disabled')
        e.grid(row=2, column=1, padx=5, pady=5)
        b = Button(frameGeneral, text='Cambiar', command=lambda: self.saveFile('.csv', tra))
        b.grid(row=2, column=2, padx=5, pady=5)
        
        # seed
        ls = Label(frameGeneral, text='Seed: ')
        ls.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        svs = StringVar(frameGeneral, value=self.options.seed)
        es = Entry(frameGeneral, textvariable=svs, validate="focusout", validatecommand=lambda: self.validateSeed(svs))
        es.grid(row=3, column=1, padx=5, pady=5)
        
        
        # solucion inicial
        ls = Label(frameGeneral, text='Tipo de solucion inicial: ')
        ls.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        comboIS = ttk.Combobox(frameGeneral, 
                               state='readonly', 
                               values=[ sol.value for sol in InitialSolution ])
        comboIS.set(self.options.initial_solution.value)
        comboIS.grid(row=4, column=1, padx=5, pady=5)
        comboIS.bind("<<ComboboxSelected>>", lambda a: self.setInitialSolution(comboIS))

        
        
        frameTermino = LabelFrame(
                    frameGeneral,
                    text='Condicion de termino',
                    
                    bg='#f0f0f0',
                    width=200,
                    height=200, 
                    font=(20)
                )
        
        #frameTermino.pack(anchor='ne', padx=25, pady=15)
        #frameTermino.grid(column=0, row=2, padx=25, pady=15)
        
    def setInitialSolution(self, combo: ttk.Combobox) -> None:
        """"""
        self.options.initial_solution = InitialSolution(combo.get()) 

    def validateSeed(self, value: StringVar) -> None:
        
        #print( value.get())
        try:
            self.options.seed = int(value.get())
        except:
            print('Seed debe ser numero entero')
            
        return self.options.seed  

    def welcomeScreen(self) -> None:
        """ Pantalla de inicio y lectura de archivo de instancia """
        
        #self.frame = Frame(self.root)
        self.frame = LabelFrame(
                    self.root,
                    text='Selecciona un archivo de instancia TSP',
                    bg='#f0f0f0',
                    font=(20)
                )
        
        self.frame.pack(anchor='center', pady=10)
        
        b = Button(self.frame, text='Seleccionar archivo', command=self.openFile)
        b.config()
        b.pack(anchor='center', padx=50, pady=25)
        #b.grid(row=0, column=3, sticky='w', padx=10, pady=10)

        
    def a(self):
        print(self.options.instance, self.algorithm, self.options.solution, self.options.seed, self.options.initial_solution.value)

def main() -> None:
    
    root = Tk()

    
    frame = Frame(root)
    frame.config(bd=10, relief='ridge')
    frame.pack(anchor='center', side='top')
    label = Label(frame, text='TSP-Framework')
    label.config(font=('consolas', 40))
    label.pack()
    
    gui = Gui(root)

    Button(root, text='Seleccionar', command=gui.a).pack()
    
    root.protocol("WM_DELETE_WINDOW", gui.onQuit)
    root.mainloop()
    
    
if __name__ == '__main__':
    main()