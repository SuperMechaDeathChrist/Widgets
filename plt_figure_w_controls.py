import PySimpleGUI as sg
import numpy as np
#------------------------------- This is to include a matplotlib figure in a Tkinter canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as Tk


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side=Tk.RIGHT, fill=Tk.BOTH, expand=1)

    def on_key_press(event):
        key_press_handler(event, canvas, toolbar)
        canvas.TKCanvas.mpl_connect("key_press_event", on_key_press)
    return


class Toolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom')]
                # t[0] in ('Home', 'Pan', 'Zoom','Save')]

    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)
#-------------------------------

#------------------------------- PySimpleGUI CODE

layout = [
    [sg.T('Graph: y=sin(x)')],
    [sg.B('Plot'), sg.B('Exit')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.T('Figure:')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 400)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],

]

window = sg.Window(title='Graph with controls', layout=layout)
window.Finalize()
window.Maximize()


while True:
    event, values = window.Read()
    print('#####')
    print(event)
    print('#####')
    print(values)
    if event in [None, 'Exit']:  # always,  always give a way out!
        window.Close()
        break
    elif event is 'Plot':
        #------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        #------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it¿s close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        #-------------------------------
        x = np.linspace(0, 2 * np.pi)
        y = np.sin(x)
        plt.plot(x, y)
        plt.title('y=sin(x)')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid()

        #------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window.FindElement(
            'fig_cv').TKCanvas, fig, window.FindElement('controls_cv').TKCanvas)
        #-------------------------------
