import matplotlib.pyplot as plt
import os
from matplotlib.animation import FuncAnimation

coords = []
points = []
trajectory = []
x, y = [], []
annotations =[]

fig, ax = plt.subplots(figsize=(10, 8))
plt.style.use('ggplot')


def generateCoords() -> None:
    for p in coords:
        x.append(p.x)
        y.append(p.y)

    ax.scatter(x, y, color='red', s=200, edgecolors='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Mapa')

    for i in range(len(coords)):
        ax.annotate(i,
            xy=(x[i], y[i]), 
            xytext=(x[i]-0.05, y[i]+0.15))



def generateMap(i: int) -> None:
    
    try:
        points = trajectory[i].tour
        #ax.set_xlabel(f'Tour: {trajectory[i]}')
    except:
        return

    for an in annotations:
        an.remove()
    annotations[:] = []
   
    #ax.cla()
    #ax.scatter(x,y, color='blue')
    a = ax.annotate('Partida',
            xy=(x[points[0]], y[points[0]]), 
            xytext=(x[points[0]]-0.1, y[points[0]] - 0.25))

    annotations.append(a)

    for i in range(len(points)-1):
               
        #ax.plot([x[points[i]], x[points[i+1]]],
        #[y[points[i]], y[points[i+1]]], color='red')
        
        a = ax.annotate("",
                        xy=(x[points[i+1]], y[points[i+1]]), 
                        xytext=(x[points[i]], y[points[i]]), 
                        arrowprops=dict(arrowstyle="->",
                                        connectionstyle="arc3", color="blue"))
        annotations.append(a)

    
       

def show() -> None:

    global ani
    generateCoords()

    ani = FuncAnimation(fig, generateMap, interval=500, blit=False)

    plt.tight_layout()
    plt.grid(color='black', linestyle='-', linewidth=0.1)
    plt_set_fullscreen()

    plt.show()

def plt_set_fullscreen():

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