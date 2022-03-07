"""
Módulo Encargado de el manejo de la visualización o graficacion de las soluciones y su trayectoria

"""

import os
import tempfile
from tkinter import Tk, Frame
os.environ[ 'MPLCONFIGDIR' ] = tempfile.mkdtemp()

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import mpl_toolkits.axes_grid1


MAXLEN = 100 # número máximo de puntos de coordenada para animar la trayectoria
TOOLBARLEN = 50  # número mínimo de puntos de coordenada para agregar barra de herramientas de matplotlib en el grafico
        
        
def show(onGui: bool = False) -> None:
    """ Muestra y anima el gráfico de la trayectoria a una solución a problema TSP """
        
    gui = Tk()
       
    Graph(gui)
    
    # Si se ejecuta la visualización desde la terminal
    if not onGui:
        
        gui.protocol("WM_DELETE_WINDOW", lambda: quit(gui))
        gui.mainloop()
        


class Graph(Frame):
    """ Clase que representa la graficacion de la trayectoria de una solucion a problema TSP """
    
    coords = [] # lista de coordenadas
    trajectory = [] # lista de con la trayectoria de la solucion
    replit = False # bool si se ejecuta en replit o no
  
    def __init__(self, master: Tk = None):
        Frame.__init__(self, master)
        
        self.fig, (self.ax, self.ax1) = plt.subplots(figsize=(16, 9), gridspec_kw={'height_ratios': [5, 1]}, dpi=90, nrows=2, ncols=1) # Crear figura y graficos

        self.master = master
        self.master.title('Visualizador de trayectoria para soluciones TSP')
        
        self.x, self.y = [], [] # lista de coordenadas x e y
        self.annotations = [] # lista de anotaciones en el grafico que serian las numeraciones, flechas de union, etc.
        self.iterations, self.cost, self.avg, self.worst = [], [], [], []
        self.initWindow()
        
        #plt.show()
     
     
    def initWindow(self):
        
        if self.replit:
            # Maximizar ventana para windows y linux
            if os.name == 'nt':
                self.master.state('zoomed')
            else:
                self.master.attributes('-zoomed', True)
            
        
        self.putCoords()
        self.pack()     


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw_idle()
        self.canvas.get_tk_widget().pack(fill='both', expand=1)
        
        
        # Agregar barra de herramientas y maximizar si el grafico tiene determinados nodos
        if len(self.coords) >= TOOLBARLEN:
            
            if os.name == 'nt':
                self.master.state('zoomed')
            else:
                self.master.attributes('-zoomed', True)
            
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master, pack_toolbar=True)
        self.toolbar.update()
        #self.canvas._tkcanvas.grid(column=0,row=0)

        # generar la animacion de la graficacion de la trayectoria
        if self.replit:
            if len(self.coords) > MAXLEN:
                self.generateMap(len(self.trajectory)-1)
            else:
                self.ani = FuncAnimation(self.fig, self.generateMap, interval=300, blit=False)
        else:
            if len(self.coords) > MAXLEN:
                self.generateMap(len(self.trajectory)-1)
            else:
                self.ani = Player(self.fig, self.generateMap, maxi=len(self.trajectory)-1, interval=300, blit=False)
        
        
    def putCoords(self) -> None:
        """ Obtiene, posiciona y numera en el grafico los puntos con las coordenadas a recorrer """

        # Agregar titulo a la ventana
        self.fig = plt.gcf()
        self.fig.canvas.manager.set_window_title('Visualizador de trayectoria para soluciones TSP')

        for p in self.coords: # separar las coordenadas del eje x de los del eje y
            self.x.append(p.x)
            self.y.append(p.y)

        # Generar los puntos con las coordenadas
        self.ax.scatter(self.x, self.y, color='red', s=70, edgecolors='black', label='Punto Normal')
        
        self.ax.set_title('Visualización del Tour')
        #ax.set_xlabel('Eje X')
        #ax.set_ylabel('Eje Y')
        
        self.ax1.grid(color='black', linestyle='-', linewidth=0.1)
        self.ax1.set_title('Variacion por iteración')
        self.ax1.set_ylabel('Costo')
        self.ax1.set_xlabel('Iteraciones\n\n')
        
        self.ax.grid(color='black', linestyle='-', linewidth=0.1)
        
        # Numerar puntos con las coordenadas 
        for i in range(len(self.coords)):
            self.ax.annotate(i,
                xy=(self.x[i], self.y[i]), 
                xytext=(self.x[i], self.y[i]+0.05))

        # expandir al tamaño de la ventana
        plt.tight_layout()

    def generateMap(self, i: int) -> None:
        """Genera la visualización uniendo los puntos con las coordenadas en cada tour de la trayectoria"""
        
        if i >= len(self.trajectory):
            return
        
        # obtener tour de la trayectoria
        tour = self.trajectory[i].tour
        # limpiar todas las anotaciones de la graficacion anterior
        self.clearAnnotations()

        # generar texto con detalle de la graficacion
        textstr = '\n'.join((
        f'Tour: {self.trajectory[i].tour}',
        f'Costo: {self.trajectory[i].cost}',
        f'Iteraciones: {self.trajectory[i].iterations}',
        f'Evaluaciones: {self.trajectory[i].evaluations}'
        ))
        
        # si hay temperatura
        if self.trajectory[i].temperature >= 0:
            textstr += f'\nTemperatura: {self.trajectory[i].temperature:.2f}'

        # si hay promedio y desviacion estandar
        if self.trajectory[i].average > 0 and self.trajectory[i].deviation > 0:
            textstr += f'\nPromedio Poblacion: {self.trajectory[i].average:.2f}\nDesviacion Estandar Poblacion: {self.trajectory[i].deviation:.2f}'
        
        #ax.set_title(textstr)
        # generar cuadro de texto con los detalles de la graficacion
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.77)

        # poner el cuadro de texto en la esquina superior izquierda del grafico
        a = self.ax.text(0.01, 0.98, textstr, transform=self.ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)

        self.annotations.append(a) # guardar anotacion para ser borrada en la siguiente graficacion

    
        #ax.cla()
        #ax.scatter(x,y, color='blue')
        # marcar punto de inicio del tour
        a = self.ax.scatter(self.x[tour[0]], self.y[tour[0]], s=70, edgecolors='black', color='lime', label='Punto de Partida') 

        self.annotations.append(a) # guardar anotacion para ser borrada en la siguiente graficacion
        a = self.ax.legend(loc='upper right')
        self.annotations.append(a)
        # Poner la figura en el grafico
        self.drawFig(tour)
        
        self.drawStats(i)

    def drawStats(self, i: int) -> None:
        """Grafica los cambios en la calidad de los tour a lo largo de la iteraciones"""
        
        # graficar completamente los cambios de calidad en las iteraciones
        if len(self.coords) > MAXLEN:
            self.ax1.plot([tra.iterations for tra in self.trajectory],
                    [tra.cost for tra in self.trajectory],
                    label="Mejor Actual", linestyle='-', marker='', color='green')
            return
        
        self.ax1.cla()
        
        self.ax1.grid(color='black', linestyle='-', linewidth=0.1)
        self.ax1.set_title('Variacion por iteración')
        self.ax1.set_ylabel('Costo')
        self.ax1.set_xlabel('Iteraciones')
        #x_data = [tra.iterations for tra in trajectory]
        #y_data = [tra.cost for tra in trajectory]
        self.iterations.append(self.trajectory[i].iterations)
        self.cost.append(self.trajectory[i].cost)
        
        self.ax1.plot(self.iterations, self.cost, label="Mejor", linestyle='-', marker='', color='green')

        if self.trajectory[i].average > 0 and self.trajectory[i].worst > 0:
            self.avg.append(self.trajectory[i].average)
            self.worst.append(self.trajectory[i].worst)
            self.ax1.plot(self.iterations, self.avg, label="Promedio", linestyle='-', marker='', color= 'blue')
            self.ax1.plot(self.iterations, self.worst, label="Peor", linestyle='-', marker='', color='red')
            
        self.ax1.legend(loc='upper right')
        
        #ax1.plot(trajectory[i].iterations, trajectory[i].average, label="", linestyle='--')
    

    def clearAnnotations(self) -> None:
        """Elimina todas las anotaciones de la figura"""
        for an in self.annotations:
            an.remove()
        self.annotations[:] = []

    def drawFig(self, tour: list) -> None:
        """Grafica el tour en el grafico conectando los puntos a traves de flechas"""

        for i in range(len(tour)-1):
                
            #ax.plot([x[tour[i]], x[tour[i+1]]],
            #[y[tour[i]], y[tour[i+1]]], color='red')
            
            # conectar los puntos con flechas
            a = self.ax.annotate("",
                            xy=(self.x[tour[i+1]], self.y[tour[i+1]]), 
                            xytext=(self.x[tour[i]], self.y[tour[i]]), 
                            arrowprops=dict(arrowstyle="->",
                                            connectionstyle="arc3", 
                                            color="royalblue"))
            self.annotations.append(a) # guardar anotacion para ser borrada en la siguiente graficacion
            
            
            
class Player(FuncAnimation):
    """Clase que sirve como reproductor para tener la posibilidad de navegar por los graficos de la trayectoria"""

    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, mini=0, maxi=100, pos=(0.403, 0.01), **kwargs) -> None:

        self.i = 0
        self.min=mini
        self.max=maxi
        self.runs = True
        self.forwards = True
        self.fig = fig
        self.func = func
        self.setup(pos)
        FuncAnimation.__init__(self,self.fig, self.func, frames=self.play(), 
                                           init_func=init_func, fargs=fargs,
                                           save_count=save_count, **kwargs )    

    def play(self) -> None:
        """Definir frames para el reproductor"""
        while self.runs:
            self.i = self.i+self.forwards-(not self.forwards)
            if self.i > self.min and self.i < self.max:
                yield self.i
            else:
                self.stop()
                yield self.i

    def start(self) -> None:
        """Iniciar"""
        self.runs=True
        self.event_source.start()

    def stop(self, event=None) -> None:
        """Parar"""
        self.runs = False
        self.event_source.stop()

    def oneforward(self, event=None) -> None:
        """Avanzar"""
        self.forwards = True
        self.onestep()

    def onebackward(self, event=None) -> None:
        """Retroceder"""
        self.forwards = False
        self.onestep()

    def onestep(self) -> None:
        """Mover un paso en la graficacion de la trayectoria"""
        if self.i > self.min and self.i < self.max:
            self.i = self.i+self.forwards-(not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i+=1
        elif self.i == self.max and not self.forwards:
            self.i-=1

        self.func(self.i)
        self.fig.canvas.draw_idle()

        self.stop()
        

    def setup(self, pos) -> None:
        """Configurar los botones y sus acciones"""
        # seccion de los botones
        playerax = self.fig.add_axes([pos[0],pos[1], 0.22, 0.04])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(playerax)
        sax = divider.append_axes("right", size="80%", pad=0.05)
        ofax = divider.append_axes("right", size="100%", pad=0.05)

        # crear botones
        self.button_oneback = Button(playerax, label=u'$\u25C0$')
        self.button_stop = Button(sax, label=u'$\u25A0$')
        self.button_oneforward = Button(ofax, label=u'$\u25B6$')

        # acciones de los botones
        self.button_oneback.on_clicked(self.onebackward)
        self.button_oneforward.on_clicked(self.oneforward)
        self.button_stop.on_clicked(self.stop)