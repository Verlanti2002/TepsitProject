from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import ttkthemes as tk


class Login:    # Classe per il login con la gui

    # Costruttore
    def __init__(self, socket=None):

        # Attributi
        self.username = None
        self.password = None
        self.socket = socket
        self.attempts = 1
        self.result = False

        self.finestra = tk.ThemedTk(theme="arc", background=True)
        self.center(window=self.finestra, width=300, height=250)
        self.finestra.resizable(False, False)
        self.finestra.title("LOGIN")
        self.finestra.bind("<Return>", self.get_credentials) # key binding, premendo invio si richiama la funzione tentativo login, rendendo quindi l'accesso più veloce

        self.login_frame = ttk.Frame(self.finestra)  # il frame occupa tutta la finestra

        self.finestra.report_callback_exception = self.callback_error

        # Puoi modificare il font a tuo piacimento
        ttk.Label(self.login_frame, text="Login", font='Helvetica 18 bold').grid(column=0, columnspan=2, row=0, pady=15)
        # ttk.Label(login_frame, text="").grid(row=1)

        ttk.Label(self.login_frame, text="Username: ", font='Helvetica 9 bold').grid(column=0, row=1, pady=3)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(column=1, row=1, pady=3)

        # aCapo2 = ttk.Label(login_frame, text="")
        # aCapo2.grid(row=3)

        ttk.Label(self.login_frame, text="Password: ", font='Helvetica 9 bold').grid(column=0, row=2, pady=3)
        self.password_entry = ttk.Entry(self.login_frame, show=u"\u2022")  # u"\u2022" indica il valore che voglio che venga sostituito alle lettere scritte dall'utente
        self.password_entry.grid(column=1, row=2, pady=3)

        # aCapo3 = ttk.Label(login_frame, text="           ")
        # aCapo3.grid(row=5)
        ttk.Button(self.login_frame, text="ACCEDI", command=self.get_credentials).grid(column=0, columnspan=2, row=3, pady=3, sticky=E)  # se cliccato il bottone richiama la funzione tentativo_di_accesso
        self.login_frame.pack()
        self.finestra.protocol("WM_DELETE_WINDOW", self.close_window)
        self.finestra.mainloop()

    # Metodo che controlla il corretto accesso da parte del client tramite gui
    def get_credentials(self, *args):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.socket.send(username.encode() if username else b"")
        self.socket.send(password.encode() if password else b"")
        data = self.socket.recv(1024)
        if "Credenziali errate!" in data.decode() and self.attempts != 3:
            self.errore("Credenziali errate, riprova!")
            self.attempts += 1
        elif "Congratulazioni, sei entrato!" in data.decode():
            self.finestra.destroy()
            self.result = True
        else:
            self.errore("Credenziali errate, hai esaurito i tentativi!")
            self.finestra.destroy()

    def close_window(self):
        self.socket.close()
        self.finestra.destroy()

    def callback_error(self):
        self.close_window()

    # Funzione per la visualizzazione del messaggio di errore
    @staticmethod
    def errore(messaggio):
        messagebox.showerror(title="ERRORE", message=messaggio)

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
    Login()
