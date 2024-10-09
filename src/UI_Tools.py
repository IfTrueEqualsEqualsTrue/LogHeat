import customtkinter as ctk
from InstanceManager import *

colors = {'light_blue': '#02B0D5', 'gray': '#323030', 'dark_blue': '#3B536B', 'white': '#D9D9D9', 'pink': '#E33B74',
          'hlb': '#06D3FF', 'hdb': '#497198', 'hp': '#FE4181', 'disabled': '#D9D9D9', 'hgray': '#272525',
          'red': '#8F2828', 'green': '#1C8D12'}

colors2 = {'black': '#1e1e1e', 'blue': '#14213d', 'red': '#b22b3b', 'yellow': '#fca311', 'white': '#e5e5e5'}


def center(widget: ctk.CTkBaseClass):
    widget.grid_rowconfigure(0, weight=1)
    widget.grid_columnconfigure(0, weight=1)


def fastgrid(widget: ctk.CTkBaseClass, x, y, xpad, ypad, sticky, columnspan=1, rowspan=1):
    widget.grid(row=x, column=y, padx=xpad, pady=ypad, sticky=sticky, columnspan=columnspan, rowspan=rowspan)
