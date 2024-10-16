import customtkinter as ctk
from InstanceManager import *


colors = {'black': '#1e1e1e', 'blue': '#14213d', 'red': '#b22b3b', 'yellow': '#fca311', 'white': '#e5e5e5'}


def center(widget: ctk.CTkBaseClass):
    widget.grid_rowconfigure(0, weight=1)
    widget.grid_columnconfigure(0, weight=1)


def fastgrid(widget: ctk.CTkBaseClass, x, y, xpad, ypad, sticky, columnspan=1, rowspan=1):
    widget.grid(row=x, column=y, padx=xpad, pady=ypad, sticky=sticky, columnspan=columnspan, rowspan=rowspan)
