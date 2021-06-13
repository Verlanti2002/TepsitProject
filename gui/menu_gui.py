from tkinter import messagebox
import ttkthemes as tk
from tkinter import ttk
from gui import create_gui
from gui import read_gui
from gui import update_gui
from gui import delete_gui


# import deleteGUI


class StartMenu:    # Classe per la creazione del menù

    # Costruttore
    def __init__(self, socket=None):

        # Attributi
        self.socket = socket

        self.finestra = tk.ThemedTk(theme="arc", background=True)
        self.center(window=self.finestra, width=420, height=420)
        self.finestra.resizable(False, False)
        self.finestra.title("Menu")

        self.crud_frame = ttk.Frame(self.finestra)

        self.finestra.report_callback_exception = self.callback_error

        ttk.Label(self.crud_frame, text="MENU'", font='Helvetica 18 bold').grid(column=1, pady=30)
        ttk.Button(self.crud_frame, text="Create", command=self.create).grid(column=1, pady=10)
        ttk.Button(self.crud_frame, text="Read", command=self.read).grid(column=1, pady=10)
        ttk.Button(self.crud_frame, text="Update", command=self.update).grid(column=1, pady=10)
        ttk.Button(self.crud_frame, text="Delete", command=self.delete).grid(column=1, pady=10)

        # imposto un messaggio popup durante la creazione della gui che indica la possibilità
        # di utilizzare delle shortcut per usufruire delle funzioni di CRUD
        messagebox.showinfo(title="Shortcuts", message="Usa le macro CTRL + C/R/U/D per richiamare le funzioni")

        # imposto i KeyBindings
        self.finestra.bind('<Control-c>', self.create)
        self.finestra.bind('<Control-r>', self.read)
        self.finestra.bind('<Control-u>', self.update)
        self.finestra.bind('<Control-d>', self.delete)

        self.finestra.protocol("WM_DELETE_WINDOW", self.close_window)

        self.crud_frame.pack()
        self.finestra.mainloop()

    # Metodo per avviare la procedura scelta (create)
    def create(self, e=None):
        # Invio l'opzione selezionata al server
        self.socket.send("1".encode())
        create_gui.Create(socket=self.socket)

    # Metodo per avviare la procedura scelta (read)
    def read(self, e=None):
        self.socket.send("2".encode())
        read_gui.Read(socket=self.socket)

    # Metodo per avviare la procedura scelta (update)
    def update(self, e=None):
        self.socket.send("3".encode())
        update_gui.Update(socket=self.socket)

    # Metodo per avviare la procedura scelta (delete)
    def delete(self, e=None):
        self.socket.send("4".encode())
        delete_gui.Delete(socket=self.socket)

    def close_window(self):
        self.socket.close()
        self.finestra.destroy()

    def callback_error(self):
        self.close_window()

    @staticmethod
    def center(window, width=None, height=None):
        window.update_idletasks()
        width = window.winfo_width() if not width else width
        frm_width = window.winfo_rootx() - window.winfo_x()
        win_width = width + 2 * frm_width
        height = window.winfo_height() if not height else height
        titlebar_height = window.winfo_rooty() - window.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = window.winfo_screenwidth() // 2 - win_width // 2
        y = window.winfo_screenheight() // 2 - win_height // 2
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window.deiconify()


if __name__ == '__main__':
    StartMenu()
