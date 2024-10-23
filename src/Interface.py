import os

from UI_Tools import ctk
from PIL import Image

from LiveValuesPlotting import get_plot_frame, set_reader
from UI_Tools import center, fastgrid


class MainApp(ctk.CTk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title('LogHeat')
        self.geometry('1080x720')
        self.iconbitmap(os.path.join('ressources', 'icon.ico'))
        # self.configure(fg_color=colors['white'])
        # root = self
        self.mainFrame = MainFrame(self)
        center(self)
        # fastgrid(self.mainFrame, 0, 0, 0, 0, "nsew")
        self.mainFrame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        self.mainloop()


class MainFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.option_menu = ctk.CTkOptionMenu(self, values=['COM1', 'COM5'], command=self.update_com_port)
        self.start_stop_button = ctk.CTkButton(self, command=self.button_clicked, text='Start / Stop')
        # self.save_button = ctk.CTkButton(self, command=self.on_save, text='',
        #                                  image=ctk.CTkImage(Image.open(os.path.join('ressources', 'save.png')),
        #                                                     size=(30, 30)), width=40, height=40)
        self.plot_frame = None

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        fastgrid(self.option_menu, 0, 0, 20, 20, '', columnspan=2)
        # fastgrid(self.9save_button, 2, 0, 20, 20, 'e')
        fastgrid(self.start_stop_button, 2, 1, 20, 20, '')

    def get_com_port(self):
        return self.option_menu.get()

    def update_com_port(self, event=None):
        com_port = self.get_com_port()
        set_reader(com_port)
        self.plot_frame = get_plot_frame(self)
        fastgrid(self.plot_frame, 1, 0, 20, 20, '', columnspan=2)

    def button_clicked(self):
        pass

    def on_save(self):
        pass




app = MainApp()
