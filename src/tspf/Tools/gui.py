"""
Modulo dedicado a la interfaz grafica de usuario

"""
from . import bcolors
from ..Algorithms import GeneticAlgorithm, SimulatedAnnealing, LocalSearch, IteratedLocalSearch, timer
from .. import Enum, os, sys, AlgorithmsOptions, Tsp, Tour, MHType, InitialSolution, TSPMove, CoolingType, SelectionType, SelectionStrategy, CrossoverType, PerturbationType

from tkinter import Label, Tk, Frame, Button, Checkbutton, LabelFrame, Entry, StringVar, Text, END, Menu
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
import webbrowser



# Tipos de letra y tamaño para los elementos de la interfaz
menuLabelFont = ('Arial', 9, 'bold')
feedbackFont = ('consolas',11,'bold')
buttonFont = ('consolas', 12, 'bold')

class TextRedirector(object):
    """ Clase destinada a redireccionar el texto de los print (stdout) a el widget de tkinter """
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag
        self.flush = sys.stdout.flush
        
    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


class Gui():

    options: AlgorithmsOptions
    
    frame: Frame
    
    frameOptions: Frame
    
    frameFeedback: Frame
    
    textFeed: Text
    
    
    def __init__(self, root: Tk, options: AlgorithmsOptions) -> None:
        
        self.root = root
        self.options = options
        
        self.configureWindow()
        self.welcomeScreen()
        
        
    def configureWindow(self) -> None:
        """ Configura la ventana principal de la interfaz """
        self.root.title('TSP-Framework')
        #self.root.resizable(0,0)
        self.root.geometry('700x300')
        #self.root.configure(background='white')

        self.root.bind_all("<Button-1>", lambda event: self.setFocus(event) ) # fuerza el focus donde el usuario haga click
        
        #root.geometry('1366x768')
    
    def setFocus(self, event) -> None:
        """ Fuerza el focus en cualquier widget a traves de un evento """
        try:
            event.widget.focus_set()
        except:
            return 
        
    def onQuit(self) -> None:
        """ Al salir o cerrar ventana """
        if messagebox.askokcancel("Salir", "¿Quieres salir de TSP-Framework?", icon="warning", parent=self.root):
            quit(self.root)
            
            
    def openFile(self, var: StringVar = None) -> None:
        """ Abrir archivo de instancia TSP """
                        
        arch = filedialog.askopenfilename(title='Abrir archivo de instancia con problema TSP', 
                                                    initialdir='instances/',
                                                    filetypes=(('Archivo de instancia con problema TSP', '*.tsp'),))
        if arch:
            self.options.instance = arch
    
        if var:
            var.set(self.options.instance)
                
        
            
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
    
    
    """ S E L E C C I O N   D E   M E T O D O   D E   B U S Q U E D A """
        
    def mainScreen(self) -> None:
        
        self.root.geometry('960x540')
        self.frame.destroy()
        self.frame = LabelFrame(
                    self.root,
                    text='Metodo de Busqueda',
                    bg='#f0f0f0',
                    font=('consolas', 20)
                )
        
        self.frame.pack(anchor='center', pady=10)
        
        f = Frame(self.frame)
        f.grid(row=0, column=0)
        
        b = Button(f, text='Simulated Annealing', command=self.simulatedAnnealing)
        b.config(font=buttonFont)
        #b.pack(anchor='ne', side='left', padx=50, pady=50)
        b.grid(row=0, column=0, padx=25, pady=25)
        
        b = Button(self.frame, text='Algoritmo Genetico', command=self.geneticAlgorithm)
        b.config(font=buttonFont)
        #b.pack(anchor='se', side='left', padx=50, pady=50)
        b.grid(row=0, column=1, padx=25, pady=25)
        
        b = Button(self.frame, text='Local Search', command=self.localSearch)
        b.config(font=buttonFont)
        #b.pack(anchor='nw', side='right', padx=50, pady=50)
        b.grid(row=1, column=0, padx=25, pady=25)
        
        b = Button(self.frame, text='Iterated Local Search', command=self.iteratedLocalSearch)
        b.config(font=buttonFont)
        #b.pack(anchor='sw', side='right', padx=50, pady=50)
        b.grid(row=1, column=1, padx=25, pady=25)
        
        
        
    """ S I M U L A T E D   A N N E A L I N G """
    
    def simulatedAnnealing(self) -> None:
        """ Configurar opciones de simulated annealing """
        
        self.frame.destroy()
        self.optionsFrame()
        self.options.metaheuristic = MHType.SA
        
        self.menubar = MenuBar(self.root, self)
        
        frameSA = LabelFrame(
                    self.frameOptions,
                    text='Simulated Annealing',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameSA.pack(anchor='n', side='right', padx=25, pady=15)
        frameSA.grid(row=0, column=3, padx=15, pady=10)
        
        # movimiento
        lm = Label(frameSA, text='Tipo de movimiento a utilizar: ', font=menuLabelFont)
        lm.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        comboM = Combobox(frameSA, 
                               state='readonly', 
                               values=[ move.value for move in TSPMove ])
        comboM.set(self.options.move.value)
        comboM.grid(row=0, column=1, padx=5, pady=5)
        comboM.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboM, TSPMove, 'move'))
        
        # Enfriamiento
        le = Label(frameSA, text='Tipo de enfriamiento a utilizar: ', font=menuLabelFont)
        le.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        comboE = Combobox(frameSA, 
                               state='readonly', 
                               values=[ cool.value for cool in CoolingType ])
        comboE.set(self.options.cooling.value)
        comboE.grid(row=1, column=1, padx=5, pady=5)
        comboE.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboE, CoolingType))
        
        # alpha
        la = Label(frameSA, text='Valor para Alpha: ', font=menuLabelFont)
        la.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        sva = StringVar(frameSA, value=self.options.alpha)
        ea = Entry(frameSA, textvariable=sva, validate="focusout", validatecommand=lambda: self.validateNumberSA(sva, 'alpha'))
        ea.grid(row=2, column=1, padx=5, pady=5)
        
        # temperatura inicial
        lti = Label(frameSA, text='Temperatura Inicial: ', font=menuLabelFont)
        lti.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        svti = StringVar(frameSA, value=self.options.t0)
        eti = Entry(frameSA, textvariable=svti, validate="focusout", validatecommand=lambda: self.validateNumberSA(svti, 't0'))
        eti.grid(row=3, column=1, padx=5, pady=5)
        
        # temperatura minima
        ltm = Label(frameSA, text='Temperatura Minima: ', font=menuLabelFont)
        ltm.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        svtm = StringVar(frameSA, value=self.options.tmin)
        etm = Entry(frameSA, textvariable=svtm, validate="focusout", validatecommand=lambda: self.validateNumberSA(svtm, 'tmin'))
        etm.grid(row=4, column=1, padx=5, pady=5)
        
    def validateNumberSA(self, value: StringVar, atribute: str) -> None:
        #print( value.get())
        
        if atribute == 'alpha':
            try:
                self.options.alpha = float(value.get())
            except:
                print('alpha debe ser numero')
            return self.options.alpha
        elif atribute == 't0':
            try:
                self.options.t0 = float(value.get())
            except:
                print('Temperatura inicial debe ser numero')  
            return self.options.t0
        elif atribute == 'tmin':
            try:
                self.options.tmin = float(value.get())
            except:
                print('Temperatura minima debe ser numero')
            return self.options.tmin
        return 0
    
    
    """ A L G O R I T M O   G E N E T I C O """
    
    def geneticAlgorithm(self) -> None:
        """ Configurar opciones de algoritmo genetico """
        self.frame.destroy()
        self.optionsFrame()
        self.options.metaheuristic = MHType.GA
        
        self.menubar = MenuBar(self.root, self)
        
        frameGA = LabelFrame(
                    self.frameOptions,
                    text='Algoritmo Genetico',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameGA.pack(anchor='n', side='right', padx=25, pady=15)
        frameGA.grid(row=0, column=3, padx=10, pady=10)
        
        # cantidad de poblacion
        lps = Label(frameGA, text='Cantidad de individuos de la poblacion: ', font=menuLabelFont)
        lps.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        svps = StringVar(frameGA, value=self.options.pop_size)
        eps = Entry(frameGA, textvariable=svps, validate="focusout", validatecommand=lambda: self.validateNumberGA(svps, 'pop_size'))
        eps.grid(row=0, column=1, padx=5, pady=5)
        
        # cantidad de hijos
        los = Label(frameGA, text='Cantidad de hijos de la poblacion: ', font=menuLabelFont)
        los.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        svos = StringVar(frameGA, value=self.options.offspring_size)
        eos = Entry(frameGA, textvariable=svos, validate="focusout", validatecommand=lambda: self.validateNumberGA(svos, 'offspring_size'))
        eos.grid(row=1, column=1, padx=5, pady=5)
        
        # Seleccion de padres
        lps = Label(frameGA, text='Tipo de seleccion de padres: ', font=menuLabelFont)
        lps.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        comboPs = Combobox(frameGA, 
                               state='readonly', 
                               values=[ sel.value for sel in SelectionType ])
        comboPs.set(self.options.pselection_type.value)
        comboPs.grid(row=2, column=1, padx=5, pady=5)
        comboPs.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboPs, SelectionType, 'ps'))
        
        # Tipo de cruzamiento
        lcr = Label(frameGA, text='Tipo de cruzamiento: ', font=menuLabelFont)
        lcr.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        comboCr = Combobox(frameGA, 
                               state='readonly', 
                               values=[ cro.value for cro in CrossoverType ])
        comboCr.set(self.options.crossover_type.value)
        comboCr.grid(row=3, column=1, padx=5, pady=5)
        comboCr.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboCr, CrossoverType))
        
        # Tipo de mutacion
        lmt = Label(frameGA, text='Tipo de mutacion: ', font=menuLabelFont)
        lmt.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        comboMt = Combobox(frameGA, 
                               state='readonly', 
                               values=[ mu.value for mu in TSPMove ])
        comboMt.set(self.options.mutation_type.value)
        comboMt.grid(row=4, column=1, padx=5, pady=5)
        comboMt.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboMt, TSPMove, 'mu'))
        
        # probabilidad de mutacion
        lmp = Label(frameGA, text='Probabilidad de mutacion: ', font=menuLabelFont)
        lmp.grid(row=5, column=0, padx=5, pady=5, sticky='e')
        svmp = StringVar(frameGA, value=self.options.mutation_prob)
        emp = Entry(frameGA, textvariable=svmp, validate="focusout", validatecommand=lambda: self.validateNumberGA(svmp, 'mutation_prob'))
        emp.grid(row=5, column=1, padx=5, pady=5)
        
        # Estrategia nueva poblacion
        lss = Label(frameGA, text='Estrategia de seleccion nueva poblacion: ', font=menuLabelFont)
        lss.grid(row=6, column=0, padx=5, pady=5, sticky='e')
        comboSs = Combobox(frameGA, 
                               state='readonly', 
                               values=[ sel.value for sel in SelectionStrategy ])
        comboSs.set(self.options.selection_strategy.value)
        comboSs.grid(row=6, column=1, padx=5, pady=5)
        comboSs.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboSs, SelectionStrategy))
        
        # Tipo seleccion nueva poblacion
        lgs = Label(frameGA, text='Tipo de seleccion nueva poblacion: ', font=menuLabelFont)
        lgs.grid(row=7, column=0, padx=5, pady=5, sticky='e')
        comboGs = Combobox(frameGA, 
                               state='readonly', 
                               values=[ sel.value for sel in SelectionType ])
        comboGs.set(self.options.gselection_type.value)
        comboGs.grid(row=7, column=1, padx=5, pady=5)
        comboGs.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboGs, SelectionType, 'gs'))
        
        
    def validateNumberGA(self, value: StringVar, atribute: str) -> None:
        #print( value.get())
        
        if atribute == 'pop_size':
            try:
                self.options.pop_size = int(value.get())
            except:
                print('La cantidad de poblacion debe ser un numero entero')
            return self.options.pop_size
        elif atribute == 'offspring_size':
            try:
                self.options.offspring_size = int(value.get())
            except:
                print('La cantidad de hijos de la poblacion debe ser un numero entero')  
            return self.options.offspring_size
        elif atribute == 'mutation_prob':
            try:
                self.options.mutation_prob = float(value.get())
            except:
                print('Probabilidad de mutacion debe ser numero')
            return self.options.tmin
        return 0
    
    """ L O C A L   S E A R C H """    
        
    def localSearch(self) -> None:
    
        self.frame.destroy()
        self.optionsFrame()
        self.options.metaheuristic = MHType.LS
        
        self.menubar = MenuBar(self.root, self)
        
        frameLS = LabelFrame(
                    self.frameOptions,
                    text='Local Search',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameLS.pack(anchor='n', side='right', padx=25, pady=15)
        frameLS.grid(row=0, column=3, padx=10, pady=10)
        
        # tipo de busqueda
        lm = Label(frameLS, text='Tipo de busqueda local a utilizar: ', font=menuLabelFont)
        lm.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        comboM = Combobox(frameLS, 
                               state='readonly', 
                               values=[ move.value for move in TSPMove ])
        comboM.set(self.options.move.value)
        comboM.grid(row=0, column=1, padx=5, pady=5)
        comboM.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboM, TSPMove, 'move'))
        
        # Best Improvement
        bi = StringVar(frameLS)
        cbi = Checkbutton(frameLS, text='Best Improvement', variable=bi, onvalue=1, offvalue=0, command=lambda : self.setBool(bi, 'bestImprovement'))
        cbi.deselect()
        cbi.grid(row=1, column=1, padx=5, pady=5, sticky='e')
        
        
    """ I T E R A T E D   L O C A L   S E A R C H """
        
    def iteratedLocalSearch(self) -> None:
        
        self.frame.destroy()
        self.optionsFrame()
        self.options.metaheuristic = MHType.ILS
        
        self.menubar = MenuBar(self.root, self)
        
        frameILS = LabelFrame(
                    self.frameOptions,
                    text='Iterated Local Search',
                    bg='#f0f0f0',
                    font=("consolas", 20)
                )
        
        #frameLS.pack(anchor='n', side='right', padx=25, pady=15)
        frameILS.grid(row=0, column=3, padx=10, pady=10)
        
        # tipo de busqueda
        lm = Label(frameILS, text='Tipo de busqueda local a utilizar: ', font=menuLabelFont)
        lm.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        comboM = Combobox(frameILS, 
                               state='readonly', 
                               values=[ move.value for move in TSPMove ])
        comboM.set(self.options.move.value)
        comboM.grid(row=0, column=1, padx=5, pady=5)
        comboM.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboM, TSPMove, 'move'))
        
        # Tipo de perturbacion
        lp = Label(frameILS, text='Tipo de perturbacion a aplicar: ', font=menuLabelFont)
        lp.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        comboP = Combobox(frameILS, 
                               state='readonly', 
                               values=[ per.value for per in PerturbationType ])
        comboP.set(self.options.perturbation.value)
        comboP.grid(row=1, column=1, padx=5, pady=5)
        comboP.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboP, PerturbationType))
        
        # cantidad de perturbaciones
        lnp = Label(frameILS, text='Cantidad de perturbaciones: ', font=menuLabelFont)
        lnp.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        svnp = StringVar(frameILS, value=self.options.nPerturbations)
        enp = Entry(frameILS, textvariable=svnp, validate="focusout", validatecommand=lambda: self.validateNumberG(svnp, 'nPerturbations'))
        enp.grid(row=2, column=1, padx=5, pady=5)
    
        # Best Improvement
        bi = StringVar(frameILS)
        cbi = Checkbutton(frameILS, text='Best Improvement', variable=bi, onvalue=1, offvalue=0, command=lambda : self.setBool(bi, 'bestImprovement'))
        cbi.deselect()
        cbi.grid(row=3, column=1, padx=5, pady=5, sticky='e')
        
    
    
    
    
    """ P A N T A L L A   D E   O P C I O N E S """



    def optionsFrame(self) -> None:
        """ Configura frame de opciones """
        
        # Maximizar ventana para windows y linux
        if os.name == 'nt':
            self.root.state('zoomed')
        else:
            self.root.attributes('-zoomed', True)

        # Configurar seccion de opciones 
        self.frameOptions = LabelFrame(
                    self.root,
                    text='Opciones',
                    bg='#f0f0f0',
                    font=("consolas", 20)
                )
        
        # Si se esta en replit se mueve el frame de opciones al centro
        if not self.options.replit:
            self.frameOptions.pack(anchor='nw', side='left', padx=5, pady=5)
        else:
            self.frameOptions.pack(anchor='center', side='top', padx=5, pady=5)
        #self.frameOptions.grid(column=0, row=0, padx=25, pady=15)
        
        # Si se esta en replit no se muestra el frame de opciones ya que no que espacio y se muestra la salida por la terminal
        if not self.options.replit:
            # configurar seccion de Feedback
            self.frameFeedback = LabelFrame(
                        self.root,
                        text='Salida',
                        bg='#f0f0f0',
                        font=("consolas", 22)
                    )

            self.frameFeedback.pack(anchor='ne', side='right', padx=5, pady=5)
            #self.frameFeedback.grid(column=0, row=1, padx=25, pady=15)
            
            self.textFeed = Text(self.frameFeedback, bg='#fff', fg='#000')
            self.textFeed.config(state='disable', padx=10, pady=10, width=500, height=700, font=feedbackFont)
            self.textFeed.pack(fill="y", padx=5, pady=5)
            
            # Redireccionar todos los print desde el stdout a el texto de feedback
            sys.stdout = TextRedirector(self.textFeed, "stdout")
        
        
        # configurar seccion de opciones generales
        frameGeneral = LabelFrame(
                    self.frameOptions,
                    text='Generales',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameGeneral.pack(anchor='n', side='left', padx=25, pady=15)
        frameGeneral.grid(row=0, column=0, padx=15, pady=10)
        
        # Opciones Generales
        # archivo de intancia
        lins = Label(frameGeneral, text='Archivo de instancia: ', font=menuLabelFont)
        lins.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ins = StringVar(frameGeneral, value=self.options.instance)
        eins = Entry(frameGeneral, textvariable=ins, state='disabled')
        eins.grid(row=1, column=1, padx=5, pady=5)
        bins = Button(frameGeneral, text='Cambiar', command=lambda: self.openFile(ins))
        bins.grid(row=1, column=2, padx=5, pady=5)
        
        # archivo de solucion
        l = Label(frameGeneral, text='Archivo para la solucion: ', font=menuLabelFont)
        l.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        sol = StringVar(frameGeneral, value=self.options.solution)
        e = Entry(frameGeneral, textvariable=sol, state='disabled')
        e.grid(row=2, column=1, padx=5, pady=5)
        b = Button(frameGeneral, text='Cambiar', command=lambda: self.saveFile('.txt', sol))
        b.grid(row=2, column=2, padx=5, pady=5)
        
        # archivo de trayectoria
        l = Label(frameGeneral, text='Archivo para la trayectoria: ', font=menuLabelFont)
        l.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        tra = StringVar(frameGeneral, value=self.options.trajectory)
        e = Entry(frameGeneral, textvariable=tra, state='disabled')
        e.grid(row=3, column=1, padx=5, pady=5)
        b = Button(frameGeneral, text='Cambiar', command=lambda: self.saveFile('.csv', tra))
        b.grid(row=3, column=2, padx=5, pady=5)
        
        # seed
        ls = Label(frameGeneral, text='Seed: ', font=menuLabelFont)
        ls.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        svs = StringVar(frameGeneral, value=self.options.seed)
        es = Entry(frameGeneral, textvariable=svs, validate="focusout", validatecommand=lambda: self.validateNumberG(svs, 'seed'))
        es.grid(row=4, column=1, padx=5, pady=5)
        
        # solucion inicial
        ls = Label(frameGeneral, text='Tipo de solucion inicial: ', font=menuLabelFont)
        ls.grid(row=5, column=0, padx=5, pady=5, sticky='e')
        comboIS = Combobox(frameGeneral, 
                               state='readonly', 
                               values=[ sol.value for sol in InitialSolution ])
        comboIS.set(self.options.initial_solution.value)
        comboIS.grid(row=5, column=1, padx=5, pady=5)
        comboIS.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboIS, InitialSolution))
        
        # Visualizar
        self.options.visualize = True
        v = StringVar(frameGeneral)
        chv = Checkbutton(frameGeneral, text='Visualizar trayectoria', variable=v, onvalue=1, offvalue=0, command=lambda : self.setBool(v, 'visualize'))
        chv.select()
        chv.grid(row=6, column=1, padx=5, pady=5, sticky='e')

        
        # Opciones Condicion de termino
        frameTermino = LabelFrame(
                    self.frameOptions,
                    text='Condicion de termino',                   
                    bg='#f0f0f0',
                    font=("consolas", 20)
                )
        
        #frameTermino.pack(anchor='ne', padx=25, pady=15)
        frameTermino.grid(row=7, column=0, padx=10, pady=10)
        
        # Iteraciones maximas
        li = Label(frameTermino, text='Iteraciones maximas: ', font=menuLabelFont)
        li.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        svi = StringVar(frameTermino, value=self.options.max_iterations)
        ei = Entry(frameTermino, textvariable=svi, validate="focusout", validatecommand=lambda: self.validateNumberG(svi, 'iterations'))
        ei.grid(row=0, column=1, padx=5, pady=5)
        
        # Evaluaciones maximas
        le = Label(frameTermino, text='Evaluaciones maximas: ', font=menuLabelFont)
        le.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        sve = StringVar(frameTermino, value=self.options.max_evaluations)
        ee = Entry(frameTermino, textvariable=sve, validate="focusout", validatecommand=lambda: self.validateNumberG(sve, 'evaluations'))
        ee.grid(row=1, column=1, padx=5, pady=5)
        
        # Tiempo maximo
        lt = Label(frameTermino, text='Tiempo maximo de ejecucion (segundos): ', font=menuLabelFont)
        lt.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        svt = StringVar(frameTermino, value=self.options.max_time)
        et = Entry(frameTermino, textvariable=svt, validate="focusout", validatecommand=lambda: self.validateNumberG(svt, 'time'))
        et.grid(row=2, column=1, padx=5, pady=5)
        
        
        # boton ejecutar
        frameEj = LabelFrame(
                    self.frameOptions,
                    text='',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameEj.pack(anchor='n', side='right', padx=25, pady=15)
        frameEj.grid(row=7, column=3, padx=25, pady=10)

        bej = Button(frameEj, text='EJECUTAR', command=self.run)
        bej.config(fg='#f00', font=('consolas', 22, 'bold'))
        bej.grid(row=0, column=0, padx=20, pady=20)
        
    
    def setBool(self, chk: StringVar, var: str) -> None:
        """ Asigna los booleandos a las variables correspondientes desde checkbox """
        #print(chk.get())
        if var == 'visualize':
            if chk.get() == '1':
                self.options.visualize = True
            else:
                self.options.visualize = False
        if var == 'bestImprovement':
            if chk.get() == '1':
                self.options.bestImprovement = True
            else:
                self.options.bestImprovement = False
        
    def setCombobox(self, combo: Combobox, opt: Enum, var: str = '') -> None:
        """ Actualiza los valores a las variables representadas por los combobox y Enum de las opciones """
        
        # General
        if opt == InitialSolution:
            self.options.initial_solution = InitialSolution(combo.get())
        
        # Simulated Annealing  
        elif opt == TSPMove and var == 'move':
            self.options.move = TSPMove(combo.get())
        elif opt == CoolingType:
            self.options.cooling = CoolingType(combo.get())
        
        # Algoritmo Genetico    
        elif opt == SelectionType and var == 'ps':
            self.options.pselection_type = SelectionType(combo.get())
        elif opt == CrossoverType:
            self.options.crossover_type = CrossoverType(combo.get())
        elif opt == TSPMove and var == 'mu':
            self.options.mutation_type = TSPMove(combo.get())
        elif opt == SelectionStrategy:
            self.options.selection_strategy = SelectionStrategy(combo.get())
        elif opt == SelectionType and var == 'gs':
            self.options.gselection_type = SelectionType(combo.get())
            
        elif opt == PerturbationType:
            self.options.perturbation = PerturbationType(combo.get())

    def validateNumberG(self, value: StringVar, atribute: str) -> None:
        #print( value.get())
        if atribute == 'seed':
            try:
                self.options.seed = int(value.get())
            except:
                print('Seed debe ser numero entero')
            return self.options.seed
        elif atribute == 'iterations':
            try:
                self.options.max_iterations = int(value.get())
            except:
                print('Las iteraciones meximas deben ser numero entero')
            return self.options.max_iterations
        elif atribute == 'evaluations':
            try:
                self.options.max_evaluations = int(value.get())
            except:
                print('Las evaluaciones meximas deben ser numero entero')
            return self.options.max_iterations
        elif atribute == 'time':
            try:
                self.options.max_time = float(value.get())
            except:
                print('Las evaluaciones meximas deben ser numero')
            return self.options.max_time
        
        elif atribute == 'nPerturbations':
            try:
                self.options.nPerturbations = int(value.get())
            except:
                print('El numero de perturbaciones debe ser numero')   
            return self.options.nPerturbations
        
        return 0
    
    
    
    """ P A N TA L L A   D E   I N I C I O """

    def welcomeScreen(self) -> None:
        """ Pantalla de inicio y lectura de archivo de instancia """
        
        #self.frame = Frame(self.root)
        self.frame = LabelFrame(
                    self.root,
                    text='Selecciona un archivo de instancia TSP',
                    bg='#f0f0f0',
                    font=("consolas", 13)
                )
        
        self.frame.pack(anchor='center', pady=10)
        
        f = Frame(self.frame)
        f.grid(row=0, column=0)
        
        l = Label(f, text='Instancia del problema TSP: ', font=menuLabelFont)
        l.grid(row=1, column=0, padx=2, pady=5, sticky='e')
        #l.pack(anchor='nw')
        sol = StringVar(f, value=self.options.instance)
        e = Entry(f, textvariable=sol, state='disabled')
        e.grid(row=1, column=1, padx=2, pady=5)
        #e.pack(anchor='ne')
        
        
        b = Button(f, text='Cambiar', command=lambda: self.openFile(sol))
        b.config()
        #b.pack(anchor='center', padx=50, pady=25)
        b.grid(row=1, column=2, sticky='w', padx=5, pady=5)
        
        b2 = Button(f, text='Continuar', command=lambda: self.mainScreen())
        b2.config(fg='#f00', font=('consolas',12, 'bold'))
        #b2.pack(anchor='center', padx=50, pady=25)
        b2.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        
    
    """ E J E C U C I O N """   
     
    def run(self) -> None:
        """ Ejecuta el algoritmo con las opciones configuradas """
        if not self.options.replit:
            self.textFeed.delete(1.0, END)
        
        start = timer() # tiempo inicial de ejecucion
        # leer e inicializar las opciones 
        options = self.options
        if not options.replit:
            bcolors.disable(bcolors)
            
        # validar optiones
        if options.errors():
            messagebox.showerror(title='Error', message='Se detectaron errores de configuracion')
            return
        
        # Mostrar Opciones 
        options.printOptions()

        # leer e interpretar el problema TSP leido desde la instancia definida
        problem = Tsp(filename=options.instance)

        # Ejecutar Metaheuristica Simulated Annealing
        if (options.metaheuristic == MHType.SA):
                
            # Solucion inicial
            first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
            # Crear solver
            solver = SimulatedAnnealing(options=options, problem=problem)
            # Ejecutar la busqueda
            solver.search(first_solution)

        # Ejecutar Metaheuristica Algoritmo Genetico
        elif (options.metaheuristic == MHType.GA):
            # Crear solver
            solver = GeneticAlgorithm(options=options, problem=problem)
            # Ejecutar la busqueda
            solver.search()
            
        elif (options.metaheuristic == MHType.LS):
            # Solucion inicial
            first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
            # Crear solver
            solver = LocalSearch(options=options, problem=problem)
            # Ejecutar la busqueda
            solver.search(first_solution)
            
        elif (options.metaheuristic == MHType.ILS):
            # Solucion inicial
            first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
            # Crear solver
            solver = IteratedLocalSearch(options=options, problem=problem)
            # Ejecutar la busqueda
            solver.search(first_solution)

        else: 
            # Crear solver
            solver = GeneticAlgorithm(options=options, problem=problem)
            # Ejecutar la busqueda
            solver.search()

        # Guardar la solucion y trayectoria en archivo
        solver.printSolFile(options.solution)
        solver.printTraFile(options.trajectory)
        # Escribir la solucion por consola
        solver.print_best_solution()
        
        end = timer() # tiempo final de ejecucion
        print(f"{bcolors.BOLD}Tiempo total de ejecucion: {bcolors.ENDC}{bcolors.OKBLUE} {end-start:.3f} segundos{bcolors.ENDC}")
        print(f'\n------------------------------------------------------------------------------------------------------------------\n')
        
        if options.visualize:
            solver.visualize()

        if not self.options.replit:
            self.textFeed.insert(END, "spam\n")
            self.textFeed.see(END)
   

def main(options: AlgorithmsOptions) -> None:
    
    root = Tk()

    frame = Frame(root)
    frame.config(bd=10, relief='ridge')
    frame.pack(anchor='center', side='top', padx=5, pady=15)
    label = Label(frame, text='TSP-Framework')
    label.config(font=('consolas', 40))
    label.pack(pady=10)
       
    gui = Gui(root=root, options=options)
    
    
    root.protocol("WM_DELETE_WINDOW", gui.onQuit)
    root.mainloop()
    
class MenuBar:
    """ Clase que representa el menu de herramientas superior """
    def __init__(self, window: Tk, gui: Gui):
        
        self.menuBar = Menu(window)
        self.gui = gui
        
        # Archivo
        fileMenu = Menu(self.menuBar, tearoff = False)
        #fileMenu.add_command(label = "New")
        #fileMenu.add_command(label = "Open...")
        #fileMenu.add_command(label = "Close")
        fileMenu.add_separator()
        fileMenu.add_command(label = "Salir", command=gui.onQuit)
        self.menuBar.add_cascade(menu = fileMenu, label = "Archivo")
          
        # cambiar metodo
        editMenu = Menu(self.menuBar, tearoff = False)
        editMenu.add_command(label="Simulated Annealing", command=lambda: self.changeSearch(MHType.SA))
        editMenu.add_command(label="Algoritmo Genetico", command=lambda: self.changeSearch(MHType.GA))
        editMenu.add_command(label="Local Search", command=lambda: self.changeSearch(MHType.LS))
        editMenu.add_command(label="Iterated Local Search", command=lambda: self.changeSearch(MHType.ILS))

        self.menuBar.add_cascade(menu=editMenu, label="Cambiar Metodo de Busqueda")
  
        # Menu ayuda
        helpMenu = Menu(self.menuBar, tearoff = False)
        helpMenu.add_command(label="Documentacion", command=lambda: webbrowser.open_new(r'https://javernaver.github.io/TSP-Framework/'))
        helpMenu.add_command(label="GitHub", command=lambda: webbrowser.open_new(r'https://github.com/Javernaver/TSP-Framework'))
        helpMenu.add_separator()
        helpMenu.add_command(label="Acerca de...", command=lambda: messagebox.showinfo(title="Acerca de", message=f'TSP-Framework \nJavier del Canto\njavier.delcanto.m@mail.pucv.cl'))
        self.menuBar.add_cascade(menu=helpMenu, label="Ayuda")
        window.config(menu=self.menuBar)
        
    def changeSearch(self, searchType: MHType):
        
        self.gui.frameOptions.destroy()
        self.gui.frameFeedback.destroy()
        
        if searchType == MHType.SA:
            self.gui.simulatedAnnealing()
        elif searchType == MHType.GA:
            self.gui.geneticAlgorithm()
        elif searchType == MHType.LS:
            self.gui.localSearch()
        elif searchType == MHType.ILS:
            self.gui.iteratedLocalSearch()