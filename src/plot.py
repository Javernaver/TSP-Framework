import os
import tempfile
os.environ[ 'MPLCONFIGDIR' ] = tempfile.mkdtemp()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
import mpl_toolkits.axes_grid1


coords = []
points = []
trajectory = []
x, y = [], []
annotations =[]

replit = False

fig, ax = plt.subplots(figsize=(16, 9), dpi=90)
#plt.style.use('ggplot')


def generateCoords() -> None:

    for p in coords:
        x.append(p.x)
        y.append(p.y)

    # Generar los puntos con las coordenadas
    ax.scatter(x, y, color='red', s=100, edgecolors='black')

    ax.set_xlabel('X\n\nControles\n')
    ax.set_ylabel('Y')
    ax.set_title('Mapa')

    

    plt.tight_layout()
    plt.grid(color='black', linestyle='-', linewidth=0.1)
    
    # Numerar puntos con las coordenadas 
    for i in range(len(coords)):
        ax.annotate(i,
            xy=(x[i], y[i]), 
            xytext=(x[i], y[i]+0.05))

def generateMap(i: int) -> None:

    try:
        points = trajectory[i].tour
        
        clearAnnotations()

        textstr = '\n'.join((
        f'Tour: {trajectory[i].tour}',
        f'Costo: {trajectory[i].cost}',
        f'Iteraciones para esta solucion: {trajectory[i].iterations}',
        f'Evaluaciones para esta solucion: {trajectory[i].evaluations}'
        ))
        
        if trajectory[i].temperature >= 0:
            textstr += f'\nTemperatura: {trajectory[i].temperature:.2f}'

        if trajectory[i].average > 0 and trajectory[i].deviation > 0:
            textstr += f'\nPromedio Poblacion: {trajectory[i].average:.2f}\nDesviacion Estandar Poblacion: {trajectory[i].deviation:.2f}'
        
        #ax.set_title(textstr)
        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.77)

        # place a text box in upper left in axes coords
        a = ax.text(0.01, 0.98, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)

        annotations.append(a)
        
    except:
        return
   
    #ax.cla()
    #ax.scatter(x,y, color='blue')

    a = ax.annotate('Partida',
            xy=(x[points[0]], y[points[0]]), 
            xytext=(x[points[0]] - 0.1, y[points[0]] - 0.15))

    annotations.append(a)

    drawFig(points)



def show() -> None:

    global ani
    generateCoords()

    if replit:
        ani = FuncAnimation(fig, generateMap, interval=500, blit=False)
    else:
        ani = Player(fig, generateMap, maxi=len(trajectory)-1, interval=500, blit=False)
        

    plt_set_fullscreen()

    plt.show()


def clearAnnotations() -> None:
    for an in annotations:
        an.remove()
    annotations[:] = []

def drawFig(points: list) -> None:

    for i in range(len(points)-1):
               
        #ax.plot([x[points[i]], x[points[i+1]]],
        #[y[points[i]], y[points[i+1]]], color='red')
        
        a = ax.annotate("",
                        xy=(x[points[i+1]], y[points[i+1]]), 
                        xytext=(x[points[i]], y[points[i]]), 
                        arrowprops=dict(arrowstyle="->",
                                        connectionstyle="arc3", 
                                        color="blue"))
        annotations.append(a)


def plt_set_fullscreen() -> None:

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

    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, mini=0, maxi=100, pos=(0.403, 0.01), **kwargs):

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

    def play(self):
        while self.runs:
            self.i = self.i+self.forwards-(not self.forwards)
            if self.i > self.min and self.i < self.max:
                yield self.i
            else:
                self.stop()
                yield self.i

    def start(self):
        self.runs=True
        self.event_source.start()

    def stop(self, event=None):
        self.runs = False
        self.event_source.stop()

    def oneforward(self, event=None):
        self.forwards = True
        self.onestep()

    def onebackward(self, event=None):
        self.forwards = False
        self.onestep()

    def onestep(self):
        
        if self.i > self.min and self.i < self.max:
            self.i = self.i+self.forwards-(not self.forwards)
        elif self.i == self.min and self.forwards:
            self.i+=1
        elif self.i == self.max and not self.forwards:
            self.i-=1

        self.func(self.i)
        self.fig.canvas.draw_idle()

        self.stop()
        

    def setup(self, pos):
        playerax = self.fig.add_axes([pos[0],pos[1], 0.22, 0.04])
        divider = mpl_toolkits.axes_grid1.make_axes_locatable(playerax)

        sax = divider.append_axes("right", size="80%", pad=0.05)

        ofax = divider.append_axes("right", size="100%", pad=0.05)
        self.button_oneback = Button(playerax, label=u'$\u25C0$')

        self.button_stop = Button(sax, label=u'$\u25A0$')

        self.button_oneforward = Button(ofax, label=u'$\u25B6$')
        self.button_oneback.on_clicked(self.onebackward)
        self.button_oneforward.on_clicked(self.oneforward)
        self.button_stop.on_clicked(self.stop)
