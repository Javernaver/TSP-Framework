"""
Módulo dedicado a la interfaz gráfica de usuario

"""
from . import bcolors, plot
from ..Algorithms import GeneticAlgorithm, SimulatedAnnealing, LocalSearch, IteratedLocalSearch, timer
from .. import Enum, os, sys, AlgorithmsOptions, Tsp, Tour, MHType, InitialSolution, TSPMove, CoolingType, SelectionType, SelectionStrategy, CrossoverType, PerturbationType, TSPlibReader

from tkinter import Label, Tk, Frame, Button, Checkbutton, LabelFrame, Entry, StringVar, Text, Menu
from tkinter import END
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox, Scrollbar
import webbrowser
import pickle


# Tipos de letra y tamaño para los elementos de la interfaz
menuLabelFont = ('Arial', 9, 'bold')
feedbackFont = ('consolas',11,'bold')
buttonFont = ('consolas', 12, 'bold')

# URLs & Paths
GIT_HUB = r'https://github.com/Javernaver/TSP-Framework'
DOCUMENTATION = r'https://javernaver.github.io/TSP-Framework/'
MANUAL_FILE = 'documentation/Manual.pdf'

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

    options: AlgorithmsOptions = None
    
    frame: Frame = None
    
    frameL: Frame = None
    
    frameOptions: Frame = None
    
    frameFeedback: Frame = None
    
    textFeed: Text = None
    
    
    def __init__(self, root: Tk, options: AlgorithmsOptions) -> None:
        """Clase que representa la intefaz gráfica

        Args:
            root (Tk): raiz con la intefaz tkinter
            options (AlgorithmsOptions): instancia con las opciones
        """
        
        self.root = root
        self.options = options
        self.solver = None
        self.saved = ''
        self.watchButton = None
        
        self.configureWindow()
        self.welcomeScreen()
        
        
    def configureWindow(self) -> None:
        """ Configura la ventana principal de la interfaz """
        if not self.options.replit:
            frame = Frame(self.root)
            frame.config(bd=10, relief='ridge')
            frame.pack(anchor='center', side='top', padx=5, pady=15)
            label = Label(frame, text='TSP-Framework')
            label.config(font=('consolas', 40))
            label.pack(pady=10)
        
        # Iniciar Barra de herramientas superior
        self.menubar = MenuBar(self.root, self)
            
        self.root.title('TSP-Framework')
        #self.root.resizable(0,0)
        self.root.geometry('670x400')
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
                        
        file = filedialog.askopenfilename(title='Abrir archivo de instancia con problema TSP', 
                                                    initialdir='instances/',
                                                    filetypes=(('Archivo de instancia con problema TSP', '*.tsp'),))
        if file:
            self.options.instance = file
    
        if var:
            var.set(self.options.instance)
                
        
            
    def saveFile(self, extension: str, ar: StringVar) -> None:
        """ Abrir archivo de instancia TSP """
        sol = ''
        tra = ''
        if extension == '.txt':
            sol = filedialog.asksaveasfilename(title='Guardar archivo de solución al problema TSP', 
                                                    initialdir=os.getcwd(),
                                                    filetypes=(('Archivo de solución', '*.txt'),))
        elif extension == '.csv':
            tra = filedialog.asksaveasfilename(title='Guardar archivo de trayectoria a la solución al problema TSP', 
                                                    initialdir=os.getcwd(),
                                                    filetypes=(('Archivo de trayectoria a la solución', '*.csv'),))    
        
        if sol:
            check = os.path.splitext(sol)  # separa la ruta de la extension en lista
            if not check[1]:
                sol += '.txt'
            self.options.solution = sol
            ar.set(sol)
        if tra:
            check = os.path.splitext(tra)
            if not check[1]:
                tra += '.csv'
            self.options.trajectory = tra
            ar.set(tra)
    
    
    """ 
    
    
    S E L E C C I O N   D E   M E T O D O   D E   B U S Q U E D A 
    
    
    """
        
    def mainScreen(self) -> None:
        
        self.frameL.destroy()
        self.root.geometry('960x540')
        self.frame.destroy()
        self.frame = LabelFrame(
                    self.root,
                    text='Método de Búsqueda',
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
        
        b = Button(self.frame, text='Algoritmo Genético', command=self.geneticAlgorithm)
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
        """ Configura las opciones de simulated annealing """
        
        self.options.metaheuristic = MHType.SA
        self.frameL.destroy()
        self.frame.destroy()
        self.optionsFrame()
        
        
        frameSA = LabelFrame(
                    self.frameOptions,
                    text='Simulated Annealing',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameSA.pack(anchor='n', side='right', padx=25, pady=15)
        frameSA.grid(row=0, column=3, padx=15, pady=10)
        
        # movimiento
        lm = Label(frameSA, text='Movimiento:', font=menuLabelFont)
        lm.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        comboM = Combobox(frameSA, 
                               state='readonly', 
                               values=[ move.value for move in TSPMove ])
        comboM.set(self.options.move.value)
        comboM.grid(row=0, column=1, padx=5, pady=5)
        comboM.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboM, TSPMove, 'move'))
        
        # Enfriamiento
        le = Label(frameSA, text='Enfriamiento:', font=menuLabelFont)
        le.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        comboE = Combobox(frameSA, 
                               state='readonly', 
                               values=[ cool.value for cool in CoolingType ])
        comboE.set(self.options.cooling.value)
        comboE.grid(row=1, column=1, padx=5, pady=5)
        comboE.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboE, CoolingType))
        
        # alpha
        la = Label(frameSA, text='Alpha:', font=menuLabelFont)
        la.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        sva = StringVar(frameSA, value=self.options.alpha)
        ea = Entry(frameSA, textvariable=sva, validate="focusout", validatecommand=lambda: self.validateNumberSA(sva, 'alpha'))
        ea.grid(row=2, column=1, padx=5, pady=5)
        
        # temperatura inicial
        lti = Label(frameSA, text='Temperatura Inicial:', font=menuLabelFont)
        lti.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        svti = StringVar(frameSA, value=self.options.t0)
        eti = Entry(frameSA, textvariable=svti, validate="focusout", validatecommand=lambda: self.validateNumberSA(svti, 't0'))
        eti.grid(row=3, column=1, padx=5, pady=5)
        
        # temperatura minima
        ltm = Label(frameSA, text='Temperatura Mínima:', font=menuLabelFont)
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
                print('Alpha debe ser número')
            return self.options.alpha
        elif atribute == 't0':
            try:
                self.options.t0 = float(value.get())
            except:
                print('Temperatura inicial debe ser número')  
            return self.options.t0
        elif atribute == 'tmin':
            try:
                self.options.tmin = float(value.get())
            except:
                print('Temperatura mínima debe ser número')
            return self.options.tmin
        return 0
    
    
    """ A L G O R I T M O   G E N E T I C O """
    
    def geneticAlgorithm(self) -> None:
        """ Configura las opciones de algoritmo genético """
        
        self.options.metaheuristic = MHType.GA
        self.frameL.destroy()
        self.frame.destroy()
        self.optionsFrame()
        
        frameGA = LabelFrame(
                    self.frameOptions,
                    text='Algoritmo Genético',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameGA.pack(anchor='n', side='right', padx=25, pady=15)
        frameGA.grid(row=0, column=3, padx=10, pady=10)
        
        # cantidad de población
        lps = Label(frameGA, text='Cant. de individuos de la población: ', font=menuLabelFont)
        lps.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        svps = StringVar(frameGA, value=self.options.pop_size)
        eps = Entry(frameGA, textvariable=svps, validate="focusout", validatecommand=lambda: self.validateNumberGA(svps, 'pop_size'))
        eps.grid(row=0, column=1, padx=5, pady=5)
        
        # cantidad de hijos
        los = Label(frameGA, text='Cant. de hijos de la población: ', font=menuLabelFont)
        los.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        svos = StringVar(frameGA, value=self.options.offspring_size)
        eos = Entry(frameGA, textvariable=svos, validate="focusout", validatecommand=lambda: self.validateNumberGA(svos, 'offspring_size'))
        eos.grid(row=1, column=1, padx=5, pady=5)
        
        # Selección de padres
        lps = Label(frameGA, text='Selección de padres: ', font=menuLabelFont)
        lps.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        comboPs = Combobox(frameGA, 
                               state='readonly', 
                               values=[ sel.value for sel in SelectionType ])
        comboPs.set(self.options.pselection_type.value)
        comboPs.grid(row=2, column=1, padx=5, pady=5)
        comboPs.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboPs, SelectionType, 'ps'))
        
        # Tipo de cruzamiento
        lcr = Label(frameGA, text='Cruzamiento: ', font=menuLabelFont)
        lcr.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        comboCr = Combobox(frameGA, 
                               state='readonly', 
                               values=[ cro.value for cro in CrossoverType ])
        comboCr.set(self.options.crossover_type.value)
        comboCr.grid(row=3, column=1, padx=5, pady=5)
        comboCr.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboCr, CrossoverType))
        
        # Tipo de mutacion
        lmt = Label(frameGA, text='Mutación: ', font=menuLabelFont)
        lmt.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        comboMt = Combobox(frameGA, 
                               state='readonly', 
                               values=[ mu.value for mu in TSPMove ])
        comboMt.set(self.options.mutation_type.value)
        comboMt.grid(row=4, column=1, padx=5, pady=5)
        comboMt.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboMt, TSPMove, 'mu'))
        
        # probabilidad de mutacion
        lmp = Label(frameGA, text='Probabilidad de mutación: ', font=menuLabelFont)
        lmp.grid(row=5, column=0, padx=5, pady=5, sticky='e')
        svmp = StringVar(frameGA, value=self.options.mutation_prob)
        emp = Entry(frameGA, textvariable=svmp, validate="focusout", validatecommand=lambda: self.validateNumberGA(svmp, 'mutation_prob'))
        emp.grid(row=5, column=1, padx=5, pady=5)
        
        # Estrategia nueva población
        lss = Label(frameGA, text='Estrategia nueva población: ', font=menuLabelFont)
        lss.grid(row=6, column=0, padx=5, pady=5, sticky='e')
        comboSs = Combobox(frameGA, 
                               state='readonly', 
                               values=[ sel.value for sel in SelectionStrategy ])
        comboSs.set(self.options.selection_strategy.value)
        comboSs.grid(row=6, column=1, padx=5, pady=5)
        comboSs.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboSs, SelectionStrategy))
        
        # Tipo selección nueva población
        lgs = Label(frameGA, text='Selección nueva población: ', font=menuLabelFont)
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
                print('La cantidad de población debe ser un número entero')
            return self.options.pop_size
        elif atribute == 'offspring_size':
            try:
                self.options.offspring_size = int(value.get())
            except:
                print('La cantidad de hijos de la población debe ser un número entero')  
            return self.options.offspring_size
        elif atribute == 'mutation_prob':
            try:
                self.options.mutation_prob = float(value.get())
            except:
                print('Probabilidad de mutacion debe ser número')
            return self.options.tmin
        return 0
    
    """ L O C A L   S E A R C H """    
        
    def localSearch(self) -> None:
        """ Configura la opciones de Local Search """

        self.options.metaheuristic = MHType.LS
        self.frameL.destroy()
        self.frame.destroy()
        self.optionsFrame()
        
        
        frameLS = LabelFrame(
                    self.frameOptions,
                    text='Local Search',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        #frameLS.pack(anchor='n', side='right', padx=25, pady=15)
        frameLS.grid(row=0, column=3, padx=10, pady=10)
        
        # tipo de búsqueda
        lm = Label(frameLS, text='Tipo de búsqueda:', font=menuLabelFont)
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
        
        # Verbose
        ve = StringVar(frameLS)
        cve = Checkbutton(frameLS, text='Full Feedback', variable=ve, onvalue=1, offvalue=0, command=lambda : self.setBool(ve, 'verbose'))
        cve.deselect()
        cve.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        
        
    """ I T E R A T E D   L O C A L   S E A R C H """
        
    def iteratedLocalSearch(self) -> None:
        """ Configura las opciones de Iterated Local Search """
        
        self.options.metaheuristic = MHType.ILS
        self.frameL.destroy()
        self.frame.destroy()
        self.optionsFrame()
        
        
        frameILS = LabelFrame(
                    self.frameOptions,
                    text='Iterated Local Search',
                    bg='#f0f0f0',
                    font=("consolas", 20)
                )
        
        #frameLS.pack(anchor='n', side='right', padx=25, pady=15)
        frameILS.grid(row=0, column=3, padx=10, pady=10)
        
        # tipo de búsqueda
        lm = Label(frameILS, text='Tipo de búsqueda:', font=menuLabelFont)
        lm.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        comboM = Combobox(frameILS, 
                               state='readonly', 
                               values=[ move.value for move in TSPMove ])
        comboM.set(self.options.move.value)
        comboM.grid(row=0, column=1, padx=5, pady=5)
        comboM.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboM, TSPMove, 'move'))
        
        # Tipo de perturbación
        lp = Label(frameILS, text='Perturbación:', font=menuLabelFont)
        lp.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        comboP = Combobox(frameILS, 
                               state='readonly', 
                               values=[ per.value for per in PerturbationType ])
        comboP.set(self.options.perturbation.value)
        comboP.grid(row=1, column=1, padx=5, pady=5)
        comboP.bind("<<ComboboxSelected>>", lambda a: self.setCombobox(comboP, PerturbationType))
        
        # cantidad de perturbaciones
        lnp = Label(frameILS, text='Cant. de perturbaciones:', font=menuLabelFont)
        lnp.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        svnp = StringVar(frameILS, value=self.options.nPerturbations)
        enp = Entry(frameILS, textvariable=svnp, validate="focusout", validatecommand=lambda: self.validateNumberG(svnp, 'nPerturbations'))
        enp.grid(row=2, column=1, padx=5, pady=5)
    
        # Best Improvement
        bi = StringVar(frameILS)
        cbi = Checkbutton(frameILS, text='Best Improvement', variable=bi, onvalue=1, offvalue=0, command=lambda : self.setBool(bi, 'bestImprovement'))
        cbi.deselect()
        cbi.grid(row=3, column=1, padx=5, pady=5, sticky='e')
      
    
    
    
    """ 
    
    
    P A N T A L L A   D E   O P C I O N E S
    
    
    """



    def optionsFrame(self) -> None:
        """ Configura frame de opciones """
        
        # Maximizar ventana para windows y linux
        if os.name == 'nt':
            self.root.state('zoomed')
        else:
            self.root.attributes('-zoomed', True)

        
        # Configurar seccion de opciones
        if self.options.replit:
            self.frameOptions = Frame(self.root)
        else:
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
            
            scrollBar = Scrollbar(self.frameFeedback, orient='vertical')
            scrollBar.pack(side='right', fill='y')
            
            self.textFeed = Text(self.frameFeedback, bg='#fff', fg='#000', yscrollcommand=scrollBar.set)
            self.textFeed.config(state='disable', padx=10, pady=10, width=500, height=700, font=feedbackFont)
            self.textFeed.pack(fill="y", padx=5, pady=5)
            
            # Redireccionar todos los print desde el stdout a el texto de feedback
            sys.stdout = TextRedirector(self.textFeed, "stdout")
            
            
            scrollBar.config(command=self.textFeed.yview)

        
        # configurar seccion de opciones generales
        frameGeneral = LabelFrame(
                    self.frameOptions,
                    text='Generales',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        frameGeneral.grid(row=0, column=0, padx=15, pady=10)
        
        # Opciones Generales
        # archivo de intancia
        lins = Label(frameGeneral, text='Archivo de instancia:', font=menuLabelFont)
        lins.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        ins = StringVar(frameGeneral, value=self.options.instance)
        eins = Entry(frameGeneral, textvariable=ins, state='disabled')
        eins.grid(row=1, column=1, padx=5, pady=5)
        bins = Button(frameGeneral, text='Cambiar', command=lambda: self.openFile(ins), font=('arial', 8, 'bold'))
        bins.grid(row=1, column=2, padx=5, pady=5)
        
        # archivo de solución
        l = Label(frameGeneral, text='Archivo para solución:', font=menuLabelFont)
        l.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        sol = StringVar(frameGeneral, value=self.options.solution)
        e = Entry(frameGeneral, textvariable=sol, state='disabled')
        e.grid(row=2, column=1, padx=5, pady=5)
        b = Button(frameGeneral, text='Cambiar', command=lambda: self.saveFile('.txt', sol), font=('arial', 8, 'bold'))
        b.grid(row=2, column=2, padx=5, pady=5)
        
        # archivo de trayectoria
        l = Label(frameGeneral, text='Archivo para trayectoria:', font=menuLabelFont)
        l.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        tra = StringVar(frameGeneral, value=self.options.trajectory)
        e = Entry(frameGeneral, textvariable=tra, state='disabled')
        e.grid(row=3, column=1, padx=5, pady=5)
        b = Button(frameGeneral, text='Cambiar', command=lambda: self.saveFile('.csv', tra), font=('arial', 8, 'bold'))
        b.grid(row=3, column=2, padx=5, pady=5)
        
        # seed
        ls = Label(frameGeneral, text='Seed: ', font=menuLabelFont)
        ls.grid(row=4, column=0, padx=5, pady=5, sticky='e')
        svs = StringVar(frameGeneral, value=self.options.seed)
        es = Entry(frameGeneral, textvariable=svs, validate="focusout", validatecommand=lambda: self.validateNumberG(svs, 'seed'))
        es.grid(row=4, column=1, padx=5, pady=5)
        
        # solución inicial
        ls = Label(frameGeneral, text='Solución inicial:', font=menuLabelFont)
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
        self.watchButton = Button(frameGeneral, text=' Ver ', command=self.watchTrajec, state='disabled', font=('arial', 8, 'bold'))
        self.watchButton.grid(row=6, column=2, padx=1, pady=1)

        
        # Opciones Condición de término
        frameTermino = LabelFrame(
                    self.frameOptions,
                    text='Condición de término',                   
                    bg='#f0f0f0',
                    font=("consolas", 20)
        )
        frameTermino.grid(row=7, column=0, padx=10, pady=10)
        
        # Iteraciones máximas
        li = Label(frameTermino, text='Iteraciones máx.:', font=menuLabelFont)
        li.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        svi = StringVar(frameTermino, value=self.options.max_iterations)
        ei = Entry(frameTermino, textvariable=svi, validate="focusout", validatecommand=lambda: self.validateNumberG(svi, 'iterations'))
        
        if self.options.metaheuristic == MHType.LS:
            ei.config(state='disabled')
            
        ei.grid(row=0, column=1, padx=5, pady=5)
        
        # Evaluaciones máximas
        le = Label(frameTermino, text='Evaluaciones máx.:', font=menuLabelFont)
        le.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        sve = StringVar(frameTermino, value=self.options.max_evaluations)
        ee = Entry(frameTermino, textvariable=sve, validate="focusout", validatecommand=lambda: self.validateNumberG(sve, 'evaluations'))
        
        if self.options.metaheuristic == MHType.LS:
            ee.config(state='disabled')
            
        ee.grid(row=1, column=1, padx=5, pady=5)
        
        # Tiempo maximo
        lt = Label(frameTermino, text='Tiempo máx. de ejecución (seg): ', font=menuLabelFont)
        lt.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        svt = StringVar(frameTermino, value=self.options.max_time)
        et = Entry(frameTermino, textvariable=svt, validate="focusout", validatecommand=lambda: self.validateNumberG(svt, 'time'))
        
        if self.options.metaheuristic == MHType.LS:
            et.config(state='disabled')
            
        et.grid(row=2, column=1, padx=5, pady=5)
        
        
        # Boton ejecutar
        frameEj = LabelFrame(
                    self.frameOptions,
                    text='',
                    bg='#f0f0f0',
                    font=("consolas", 22)
                )
        
        frameEj.grid(row=7, column=3, padx=25, pady=5)

        bej = Button(frameEj, text='EJECUTAR', command=self.search)
        bej.config(fg='#f00', font=('consolas', 22, 'bold'))
        bej.grid(row=0, column=0, padx=20, pady=20)
        
        
    def watchTrajec(self) -> None:
        """ Ver nuevamente la trayectoria """
        if not self.solver:
            return
        self.solver.visualize()

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
        if var == 'verbose':
            if chk.get() == '1':
                self.options.verbose = True
            else:
                self.options.verbose = False
        
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
        
        # Algoritmo Genético    
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
                print('Seed debe ser número entero')
            return self.options.seed
        elif atribute == 'iterations':
            try:
                self.options.max_iterations = int(value.get())
            except:
                print('Las iteraciones máximas deben ser número entero')
            return self.options.max_iterations
        elif atribute == 'evaluations':
            try:
                self.options.max_evaluations = int(value.get())
            except:
                print('Las evaluaciones máximas deben ser número entero')
            return self.options.max_iterations
        elif atribute == 'time':
            try:
                self.options.max_time = float(value.get())
            except:
                print('Las evaluaciones máximas deben ser número')
            return self.options.max_time
        
        elif atribute == 'nPerturbations':
            try:
                self.options.nPerturbations = int(value.get())
            except:
                print('El número de perturbaciones debe ser número')   
            return self.options.nPerturbations
        
        return 0
    
    
    
    """ P A N TA L L A   D E   I N I C I O """

    def welcomeScreen(self) -> None:
        """ Pantalla de inicio y lectura de archivo de instancia """
        
        #self.frame = Frame(self.root)
        self.frame = LabelFrame(
                    self.root,
                    text='Selecciona una instancia TSP',
                    bg='#f0f0f0',
                    font=("consolas", 13)
                )
        
        self.frame.pack(anchor='center', pady=10)
        
        f = Frame(self.frame)
        f.grid(row=0, column=0)
        
        l = Label(f, text='Instancia TSP:', font=menuLabelFont)
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
        
        self.frameL = LabelFrame(
                    self.root,
                    text='Utilizar solución anterior',
                    bg='#f0f0f0',
                    font=("consolas", 13)
                )
        
        self.frameL.pack(anchor='s', pady=10)
        
        b3 = Button(self.frameL, text='Cargar archivo', command=self.menubar.loadConfig)
        b3.config(fg='#f00', font=('consolas',12, 'bold'))
        b3.pack(anchor='center', padx=10, pady=10)
        #b2.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        
    
    """ E J E C U C I O N """   
     
    def search(self) -> None:
        """ Realiza la búsqueda a traves metodo de búsqueda y opciones seleccionadas """
        
        if self.watchButton != None:
            self.watchButton.config(state='normal')
            self.menubar.fileMenu.entryconfig('Guardar Configuración...', state='normal')
            
        if not self.options.replit:
            self.textFeed.config(state='normal')
            self.textFeed.delete('1.0', END)
            self.textFeed.config(state='disabled')
            
        
        start = timer() # tiempo inicial de ejecución
        # leer e inicializar las opciones 
        options = self.options
        if not options.replit:
            bcolors.disable(bcolors)
            
        # validar optiones
        if options.errors():
            messagebox.showerror(title='Error', message='Se detectaron errores de configuración')
            return
        
        # Mostrar Opciones 
        options.printOptions()
        # asignar modo gui a la lectura de instancias para gestionar los errores
        TSPlibReader.gui = self.options.gui
        # leer e interpretar el problema TSP leido desde la instancia definida
        problem = Tsp(filename=options.instance)
        
        # si hubo algun error al leer la instancia e interpretarla
        if problem.error:
            messagebox.showerror(title="Error", message=f'{problem.error}')
            return

        # Ejecutar Simulated Annealing
        if (options.metaheuristic == MHType.SA):
                
            # Solución inicial
            first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
            # Crear solver
            self.solver = SimulatedAnnealing(options=options, problem=problem)
            # Ejecutar la búsqueda
            self.solver.search(first_solution)

        # Ejecutar Algoritmo Genético
        elif (options.metaheuristic == MHType.GA):
            # Crear solver
            self.solver = GeneticAlgorithm(options=options, problem=problem)
            # Ejecutar la búsqueda
            self.solver.search()
        
        # Ejecutar Local Search    
        elif (options.metaheuristic == MHType.LS):
            # Solución inicial
            first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
            # Crear solver
            self.solver = LocalSearch(options=options, problem=problem)
            # Ejecutar la búsqueda
            self.solver.search(first_solution)
        
        # Ejecutar Iterated Local Search  
        elif (options.metaheuristic == MHType.ILS):
            # Solución inicial
            first_solution = Tour(type_initial_sol=options.initial_solution, problem=problem)
            # Crear solver
            self.solver = IteratedLocalSearch(options=options, problem=problem)
            # Ejecutar la búsqueda
            self.solver.search(first_solution)

        else: 
            # Crear solver
            self.solver = GeneticAlgorithm(options=options, problem=problem)
            # Ejecutar la búsqueda
            self.solver.search()

        # Guardar la solución y trayectoria en archivo
        self.solver.printSolFile(options.solution)
        self.solver.printTraFile(options.trajectory)
        # Escribir la solución por consola
        self.solver.print_best_solution()
        
        end = timer() # tiempo final de ejecución
        print(f"{bcolors.BOLD}Tiempo total de ejecución: {bcolors.ENDC}{bcolors.OKBLUE} {end-start:.3f} segundos{bcolors.ENDC}")
        print(f'\n------------------------------------------------------------------------------------------------------------------\n')
        
        if options.visualize:
            self.solver.visualize()

        if not self.options.replit:
            self.textFeed.insert(END, "spam\n")
            self.textFeed.see(END)
   

def main(options: AlgorithmsOptions) -> None:
    """Funcion principal que crea las instancias para utilizar la interfaz

    Args:
        options (AlgorithmsOptions): instancia con las opciones para los algoritmos
    """
    
    root = Tk()
       
    gui = Gui(root=root, options=options)
    
    
    root.protocol("WM_DELETE_WINDOW", gui.onQuit)
    root.mainloop()
    
class MenuBar:
    """ Clase que representa el menu de herramientas superior """
    def __init__(self, window: Tk, gui: Gui) -> None:
        """Clase que representa la barra de herramientas superior

        Args:
            window (Tk): base de la barra de herramientas
            gui (Gui): instancia de la intefaz
        """
        
        self.menuBar = Menu(window)
        self.gui = gui
        
        # Archivo
        self.fileMenu = Menu(self.menuBar, tearoff = False)
        self.fileMenu.add_command(label="Guardar Configuración...", command=self.saveConfig, state='disabled')
        self.fileMenu.add_command(label="Cargar Configuración...", command=self.loadConfig)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Salir", command=gui.onQuit)
        self.menuBar.add_cascade(menu=self.fileMenu, label = "Archivo")
          
        # cambiar metodo
        self.editMenu = Menu(self.menuBar, tearoff = False)
        self.editMenu.add_command(label="Simulated Annealing", command=lambda: self.changeSearch(MHType.SA))
        self.editMenu.add_command(label="Algoritmo Genético", command=lambda: self.changeSearch(MHType.GA))
        self.editMenu.add_command(label="Local Search", command=lambda: self.changeSearch(MHType.LS))
        self.editMenu.add_command(label="Iterated Local Search", command=lambda: self.changeSearch(MHType.ILS))

        self.menuBar.add_cascade(menu=self.editMenu, label="Cambiar de Algoritmo")
  
        # Menu ayuda
        self.helpMenu = Menu(self.menuBar, tearoff = False)
        self.helpMenu.add_command(label="Documentación", command=lambda: webbrowser.open_new(DOCUMENTATION))
        self.helpMenu.add_command(label="Manual", command=lambda: webbrowser.open('file://' + os.path.realpath(MANUAL_FILE)))
        self.helpMenu.add_command(label="GitHub", command=lambda: webbrowser.open_new(GIT_HUB))
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="Acerca de...", command=lambda: messagebox.showinfo(title="Acerca de", 
                                                                                            message=f'TSP-Framework \nJavier del Canto\nJorge Polanco\n\nContacto\njavier.delcanto.m@mail.pucv.cl\njorge.polanco.sanmartin@gmail.com'))
        self.menuBar.add_cascade(menu=self.helpMenu, label="Ayuda")
        window.config(menu=self.menuBar)
        
    def changeSearch(self, searchType: MHType) -> None:
        """ Cambia de metodo de búsqueda en la barra de herramientas """
        
        if self.gui.frameOptions != None:
            self.gui.frameOptions.destroy()
        if not self.gui.options.replit and self.gui.frameFeedback != None:
            self.gui.frameFeedback.destroy()
        
        if searchType == MHType.SA:
            self.gui.simulatedAnnealing()
        elif searchType == MHType.GA:
            self.gui.geneticAlgorithm()
        elif searchType == MHType.LS:
            self.gui.localSearch()
        elif searchType == MHType.ILS:
            self.gui.iteratedLocalSearch()
    
            
    def saveConfig(self) -> None:
        """ Guarda la configuración y el texto de feedback de una solución """
        if not self.gui.solver:
            return
        
        save = filedialog.asksaveasfilename(title='Guardar configuración actual en archivo TSP-Framework', 
                                                    initialdir=os.getcwd(),
                                                    filetypes=(('Archivo de guardado TSP-Framework', '*.tspf'),))
        if not save:
            return
        
        check = os.path.splitext(save)
        if not check[1]:
            save += '.tspf'
        
        try:
            file = open(save, 'wb')
            # obtener texto de feedback
            txt = self.gui.textFeed.get("1.0", END)
            # crear diccionario con la data para guardar en el archivo de guardado
            data = {'options': self.gui.options,
                    'solver': self.gui.solver,
                    'textFeed': txt,
                    'coords': plot.Graph.coords}
            # guardar
            pickle.dump(data, file)
            file.close()
            
        except IOError:
            messagebox.showerror(title="Error", message=f'No se pudo leer el archivo... {save} Error: {IOError}\nAsegurese de tener permisos de lectura en la ruta seleccionada')
        
        
    def loadConfig(self) -> None:
        """ Carga la configuración y texto de feedback a través de un archivo de guardado """
        
        load = filedialog.askopenfilename(title='Cargar configuración desde archivo TSP-Framework', 
                                                    initialdir=os.getcwd(),
                                                    filetypes=(('Archivo de guardado TSP-Framework', '*.tspf'),))
        if not load:
            return
        
        try:
            file = open(load, 'rb')
            
            try:
                data = pickle.load(file)
                
                self.gui.options = data['options']
                self.gui.solver = data['solver']
                text = data['textFeed']
                
                plot.Graph.coords = data['coords'] # cargar coodenadas de la solución anterior para generar visualización
                
                self.changeSearch(self.gui.options.metaheuristic) # Cargar la pantalla del archivo guardado
                
                self.gui.textFeed.config(state='normal')
                self.gui.textFeed.delete('1.0', END)
                self.gui.textFeed.insert('1.0', text)
                self.gui.textFeed.config(state='disabled')
                self.gui.textFeed.see(END)
                
                self.gui.watchButton.config(state='normal')
            except:
                messagebox.showerror(title="Error", message='No se puede cargar este archivo, puede que este dañado o no sea del formato correcto')
            
            file.close()
        except IOError:
            messagebox.showerror(title="Error", message=f'No se pudo leer el archivo... {load} Error: {IOError}\nAsegurese de tener permisos de lectura en la ruta seleccionada')