"""
Modulo Encargado de el manejo de la visualizacion o graficacion de las soluciones y su trayectoria
"""

import os
import tempfile
os.environ[ 'MPLCONFIGDIR' ] = tempfile.mkdtemp()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import mpl_toolkits.axes_grid1


coords = [] # lista de coordenadas
trajectory = [] # lista de con la trayectoria de la solucion
x, y = [], [] # lista de coordenadas x e y
annotations = [] # lista de anotaciones en el grafico que serian las numeraciones, flechas de union, etc.
iterations, cost, avg, worst = [], [], [], []

replit = False # bool si se ejecuta en replit o no
MAXLEN = 100 # numero maximo de puntos de coordenada para animar la trayectoria

fig, (ax, ax1) = plt.subplots(figsize=(16, 9), gridspec_kw={'height_ratios': [5, 1]}, dpi=90, nrows=2, ncols=1) # Crear figura y graficos

#fig, ax = plt.subplots(figsize=(16, 9), dpi=90) # Crear figura y grafico

#plt.style.use('ggplot')

def putCoords() -> None:
    """Obtiene, pone y numera en el grafico los puntos con las coordenadas a recorrer"""

    # Agregar titulo a la ventana
    fig = plt.gcf()
    fig.canvas.manager.set_window_title('Visualizador de trayectoria para soluciones TSP')

    for p in coords: # separar las coordenadas del eje x de los del eje y
        x.append(p.x)
        y.append(p.y)

    # Generar los puntos con las coordenadas
    ax.scatter(x, y, color='red', s=70, edgecolors='black', label='Punto Normal')
    
    ax.set_title('Visualizacion del Tour')
    #ax.set_xlabel('Eje X')
    #ax.set_ylabel('Eje Y')
    
    ax1.grid(color='black', linestyle='-', linewidth=0.1)
    ax1.set_title('Variacion por iteracion')
    ax1.set_ylabel('Costo')
    ax1.set_xlabel('Iteraciones\n\n')
    
    ax.grid(color='black', linestyle='-', linewidth=0.1)
    
    # Numerar puntos con las coordenadas 
    for i in range(len(coords)):
        ax.annotate(i,
            xy=(x[i], y[i]), 
            xytext=(x[i], y[i]+0.05))

    # expandir al tamaño de la ventana
    plt.tight_layout()

def generateMap(i: int) -> None:
    """Genera la visualizacion uniendo los puntos con las coordenadas en cada tour de la trayectoria"""
    
    if i >= len(trajectory):
        return
    
    # obtener tour de la trayectoria
    tour = trajectory[i].tour
    # limpiar todas las anotaciones de la graficacion anterior
    clearAnnotations()

    # generar texto con detalle de la graficacion
    textstr = '\n'.join((
    f'Tour: {trajectory[i].tour}',
    f'Costo: {trajectory[i].cost}',
    f'Iteraciones: {trajectory[i].iterations}',
    f'Evaluaciones: {trajectory[i].evaluations}'
    ))
    
    # si hay temperatura
    if trajectory[i].temperature >= 0:
        textstr += f'\nTemperatura: {trajectory[i].temperature:.2f}'

    # si hay promedio y desviacion estandar
    if trajectory[i].average > 0 and trajectory[i].deviation > 0:
        textstr += f'\nPromedio Poblacion: {trajectory[i].average:.2f}\nDesviacion Estandar Poblacion: {trajectory[i].deviation:.2f}'
    
    #ax.set_title(textstr)
    # generar cuadro de texto con los detalles de la graficacion
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.77)

    # poner el cuadro de texto en la esquina superior izquierda del grafico
    a = ax.text(0.01, 0.98, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)

    annotations.append(a) # guardar anotacion para ser borrada en la siguiente graficacion

   
    #ax.cla()
    #ax.scatter(x,y, color='blue')
    # marcar punto de inicio del tour
    a = ax.scatter(x[tour[0]], y[tour[0]], s=70, edgecolors='black', color='lime', label='Punto de Partida') 

    annotations.append(a) # guardar anotacion para ser borrada en la siguiente graficacion
    a = ax.legend(loc='upper right')
    annotations.append(a)
    # Poner la figura en el grafico
    drawFig(tour)
    
    drawStats(i)

def drawStats(i: int) -> None:
    """Grafica los cambios en la calidad de los tour a lo largo de la iteraciones"""
    
    # graficar completamente los cambios de calidad en las iteraciones
    if len(coords) > MAXLEN:
        ax1.plot([tra.iterations for tra in trajectory],
                [tra.cost for tra in trajectory],
                label="Mejor Actual", linestyle='-', marker='', color='green')
        return
    
    ax1.cla()
    
    ax1.grid(color='black', linestyle='-', linewidth=0.1)
    ax1.set_title('Variacion por iteracion')
    ax1.set_ylabel('Costo')
    ax1.set_xlabel('Iteraciones')
    #x_data = [tra.iterations for tra in trajectory]
    #y_data = [tra.cost for tra in trajectory]
    iterations.append(trajectory[i].iterations)
    cost.append(trajectory[i].cost)
    
    ax1.plot(iterations, cost, label="Mejor", linestyle='-', marker='', color='green')

    if trajectory[i].average > 0 and trajectory[i].worst > 0:
        avg.append(trajectory[i].average)
        worst.append(trajectory[i].worst)
        ax1.plot(iterations, avg, label="Promedio", linestyle='-', marker='', color= 'blue')
        ax1.plot(iterations, worst, label="Peor", linestyle='-', marker='', color='red')
        
    ax1.legend(loc='upper right')
    
    #ax1.plot(trajectory[i].iterations, trajectory[i].average, label="", linestyle='--')
    

def clearAnnotations() -> None:
    """Elimina todas las anotaciones de la figura"""
    for an in annotations:
        an.remove()
    annotations[:] = []

def drawFig(tour: list) -> None:
    """Grafica el tour en el grafico conectando los puntos a traves de flechas"""

    for i in range(len(tour)-1):
               
        #ax.plot([x[tour[i]], x[tour[i+1]]],
        #[y[tour[i]], y[tour[i+1]]], color='red')
        
        # conectar los puntos con flechas
        a = ax.annotate("",
                        xy=(x[tour[i+1]], y[tour[i+1]]), 
                        xytext=(x[tour[i]], y[tour[i]]), 
                        arrowprops=dict(arrowstyle="->",
                                        connectionstyle="arc3", 
                                        color="royalblue"))
        annotations.append(a) # guardar anotacion para ser borrada en la siguiente graficacion


def show() -> None:
    """Mostrar la figura y el grafico"""

    global ani # variable con la animacion de la graficacion de la trayectoria

    # poner los puntos de coordenadas
    putCoords()

    # generar la animacion de la graficacion de la trayectoria
    if replit:
        if len(coords) > MAXLEN:
            generateMap(len(trajectory)-1)
        else:
            ani = FuncAnimation(fig, generateMap, interval=500, blit=False)
    else:
        if len(coords) > MAXLEN:
            generateMap(len(trajectory)-1)
        else:
            ani = Player(fig, generateMap, maxi=len(trajectory)-1, interval=300, blit=False)
        
    # poner el grafico en pantalla maximizada para evitar conflictos con los distitos tipos de pantallas 
    plt_set_fullscreen()
    # mostrar el grafico y la figura
    plt.show()

def plt_set_fullscreen() -> None:
    """Poner el grafico en pantalla maximizada para evitar conflictos con los distitos tipos de pantallas """

    backend = str(plt.get_backend())
    mgr = plt.get_current_fig_manager()
    
    if backend == 'TkAgg':
        if os.name == 'nt':
            mgr.window.state('zoomed')
        else:
            mgr.resize(*mgr.window.maxsize())
    elif backend == 'wxAgg':
        mgr.frame.Maximize(True)
    elif backend == 'Qt4Agg':
        mgr.window.showMaximized()


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
