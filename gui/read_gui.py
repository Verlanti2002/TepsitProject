import itertools
import pickle

from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry


from gui.parent_window import ParentWindow


class Read(ParentWindow):

    def __init__(self, socket=None):

        self.socket = socket
        self.entry_id_zona = None
        self.entry_id_dipendente = None
        self.dipendenti_entry_list = None
        self.zone_lavoro_entry_list = None

        # self.id_dipendenti_list = []
        self.dipendenti_data = pickle.loads(self.socket.recv(1024))
        self.id_dipendenti_list = [f"{id_dip} - {nome} {cognome}" for id_dip, nome, cognome, _, _, _, _, _ in self.dipendenti_data]

        # self.id_zone_lavoro_list = []
        self.zone_lavoro_data = pickle.loads(self.socket.recv(1024))
        self.id_zone_lavoro_list = [f"{id_zona} - {nome}" for id_zona, nome, _ in self.zone_lavoro_data]

        super(Read, self).__init__(
            title="Read",
            width=600,
            height=400,
            id_dipendenti_list=self.id_dipendenti_list,
            id_zone_lavoro_list=self.id_zone_lavoro_list
        )

    def get_combo_table_selected(self, *args):
        if self.selezioneCombobox.get() == "Tabella dipendenti":
            self.clear_frame()
            self.show_table_dipendenti(frame=self.frame, id_dipendenti_list=self.id_dipendenti_list)
        elif self.selezioneCombobox.get() == "Tabella zone":
            self.clear_frame()
            self.show_table_zone(frame=self.frame, id_zone_list=self.id_zone_lavoro_list)

    def show_table_dipendenti(self, frame, id_zone_lavoro=None, id_dipendenti_list=None, first_column=2, second_column=4, pady=3, table_name="dipendenti"):
        ttk.Label(frame, text="Tabella Dipendenti", font='Helvetica 12 bold').grid(
            columnspan=6,
            row=0,
            pady=15,
            sticky=S
        )
        ttk.Label(frame, text="Seleziona ID:").grid(columnspan=6, row=1)

        self.entry_id_dipendente = ttk.Combobox(frame, values=id_dipendenti_list, width=19)
        self.entry_id_dipendente.grid(row=2, columnspan=10, pady=10)
        self.entry_id_dipendente.bind("<<ComboboxSelected>>", self.get_data_from_combo_dipendenti)

        self.dipendenti_entry_list = [
            {"id": "name", "text": "Nome :", "row": 3, "column": first_column},
            {"id": "last_name", "text": "Cognome :", "row": 3, "column": second_column},
            {"id": "pos_lav", "text": "Pos. Lavorativa :", "row": 4, "column": first_column},
            {"id": "date", "text": "Data Assunzione :", "row": 4, "column": second_column},
            {"id": "salary", "text": "Stipendio :", "row": 5, "column": first_column},
            {"id": "phone", "text": "Numero telefono :", "row": 5, "column": second_column},
            {"id": "id_zone_lavoro", "text": "ID Zona: ", "row": 6, "column": first_column},
        ]

        for entry in self.dipendenti_entry_list:

            if entry["id"] == "date":
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
                entry["entry"] = DateEntry(frame, width=18)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)
            elif entry["id"] == "id_zone_lavoro":
                ttk.Label(frame, text=entry["text"]).grid(column=0, row=entry["row"], pady=pady, columnspan=6)
                entry["entry"] = ttk.Entry(frame, width=18)
                entry["entry"].grid(column=0, row=entry["row"]+1, pady=pady, columnspan=6)
            else:
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
                entry["entry"] = ttk.Entry(frame)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)
            entry["entry"].config(state=DISABLED)

    def show_table_zone(self, frame, id_zone_list=None, first_column=2, second_column=4, pady=3, table_name="zone_lavoro"):
        ttk.Label(frame, text="Tabella Zone di lavoro", font='Helvetica 12 bold').grid(
            columnspan=6, row=0, pady=15, sticky=S
        )
        ttk.Label(self.frame, text="Seleziona ID zona:").grid(columnspan=6, row=1)

        self.entry_id_zona = ttk.Combobox(frame, values=id_zone_list, width=19)
        self.entry_id_zona.grid(row=2, columnspan=10, pady=10)
        self.entry_id_zona.bind("<<ComboboxSelected>>", self.get_data_from_combo_zone_lavoro)

        self.zone_lavoro_entry_list = [
            {"id": "name", "text": "Nome zona: ", "row": 3, "column": first_column},
            {"id": "num_clienti", "text": "Numero clienti: ", "row": 4, "column": first_column},
        ]

        for entry in self.zone_lavoro_entry_list:
            ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
            entry["entry"] = ttk.Entry(frame, state=DISABLED)
            entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)

    def get_data_from_combo_dipendenti(self, event):

        self.get_data_from_server(
            data=self.dipendenti_data,
            combobox=self.entry_id_dipendente,
            entry_list=self.dipendenti_entry_list,
            zone_list=self.id_zone_lavoro_list
        )

    def get_data_from_combo_zone_lavoro(self, event):

        self.get_data_from_server(
            data=self.zone_lavoro_data,
            combobox=self.entry_id_zona,
            entry_list=self.zone_lavoro_entry_list
        )

    @staticmethod
    def get_data_from_server(data, combobox, entry_list, zone_list=None):

        id_selected = combobox.get().split()[0].strip()
        data_list = [item for item in data if item[0] == int(id_selected)]
        data_list = list(itertools.chain(*data_list))[1:]
        for entry, value in zip(entry_list, data_list):
            if entry["id"] == "id_zone_lavoro":
                try:
                    value = [zona for zona in zone_list if str(value) in zona][0]
                except IndexError:
                    value = "null"
            entry["entry"].config(state=NORMAL)
            entry["entry"].delete(0, END)
            entry["entry"].insert(0, value)
            entry["entry"].config(state=DISABLED)

    def close_window(self):
        self.finestra.destroy()


if __name__ == '__main__':
    Read()
