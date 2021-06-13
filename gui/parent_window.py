
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk


class ParentWindow:

    def __init__(self, title="Parent", width=600, height=450, id_dipendenti_list=None, id_zone_lavoro_list=None):

        self.id_dipendenti_list = id_dipendenti_list
        self.id_zone_lavoro_list = id_zone_lavoro_list

        self.selezioneCombobox = None

        self.finestra, self.frame = self.create_window(title=title, width=width, height=height)

        self.finestra.protocol("WM_DELETE_WINDOW", self.close_window)

        self.finestra.mainloop()

    def create_window(self, title, width, height):

        finestra = tk.ThemedTk(theme="arc", background=True)
        finestra.get_themes()
        self.center(window=finestra, width=width, height=height)
        finestra.resizable(False, False)
        finestra.title(title)

        ttk.Label(finestra, text="Seleziona una tabella").pack(pady=10)
        self.selezioneCombobox = ttk.Combobox(finestra, values=["Tabella dipendenti", "Tabella zone"])
        self.selezioneCombobox.pack(pady=10)
        self.selezioneCombobox.bind("<<ComboboxSelected>>", self.get_combo_table_selected)
        self.selezioneCombobox.current(0)

        frame = ttk.Frame(finestra)
        self.show_table_dipendenti(frame=frame, id_zone_lavoro=self.id_zone_lavoro_list, id_dipendenti_list=self.id_dipendenti_list)
        frame.pack()

        return finestra, frame

    def show_table_dipendenti(self, frame, id_zone_lavoro, id_dipendenti_list=None, first_column=2, second_column=4, pady=3, table_name="dipendenti"):

        pass

    def show_table_zone(self, frame, id_zone_list=None, first_column=2, second_column=4, pady=3, table_name="zone_lavoro"):

        pass

    def get_combo_table_selected(self, *args):
        if self.selezioneCombobox.get() == "Tabella dipendenti":
            self.clear_frame()
            self.show_table_dipendenti(frame=self.frame, id_zone_lavoro=self.id_zone_lavoro_list, id_dipendenti_list=self.id_dipendenti_list)
        elif self.selezioneCombobox.get() == "Tabella zone":
            self.clear_frame()
            self.show_table_zone(frame=self.frame, id_zone_list=self.id_zone_lavoro_list)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def close_window(self):

        pass

    # Funzione per il bottone reset
    @staticmethod
    def clear_all(entry_list):  # elimino tutto ciò che è stato inserito nelle entry
        for entry in entry_list:
            entry["entry"].delete(0, END)

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