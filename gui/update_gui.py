import itertools
import pickle

from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

from gui.parent_window import ParentWindow


class Update(ParentWindow):

    def __init__(self, socket=None):

        self.socket = socket
        self.entry_id_zona = None
        self.entry_id_dipendente = None
        self.dipendenti_entry_list = None
        self.zone_lavoro_entry_list = None
        self.id_selected = None

        # self.id_dipendenti_list = []
        self.dipendenti_data = pickle.loads(self.socket.recv(1024))
        self.id_dipendenti_list = [
            f"{id_dip} - {nome} {cognome}"
            for id_dip, nome, cognome, _, _, _, _, _ in self.dipendenti_data
        ]

        # self.id_zone_lavoro_list = []
        self.zone_lavoro_data = pickle.loads(self.socket.recv(1024))
        self.id_zone_lavoro_list = [f"{id_zona} - {nome}" for id_zona, nome, _ in self.zone_lavoro_data]

        super(Update, self).__init__(
            title="Update",
            width=600,
            height=400,
            id_dipendenti_list=self.id_dipendenti_list,
            id_zone_lavoro_list=self.id_zone_lavoro_list
        )

    def get_combo_table_selected(self, *args):
        if self.selezioneCombobox.get() == "Tabella dipendenti":
            self.clear_frame()
            self.show_table_dipendenti(frame=self.frame, id_dipendenti_list=self.id_dipendenti_list, id_zone_lavoro=self.id_zone_lavoro_list)
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

        ttk.Label(frame, text="ID:").grid(row=1, columnspan=6, pady=pady)
        self.entry_id_dipendente = ttk.Combobox(frame, values=id_dipendenti_list, width=18)
        self.entry_id_dipendente.grid(row=2, columnspan=6, pady=pady)
        self.entry_id_dipendente.bind("<<ComboboxSelected>>", self.get_data_from_combo_dipendenti)

        dipendenti_data = {
            "name": None,
            "last_name": None,
            "pos_lav": None,
            "date": None,
            "salary": None,
            "phone": None,
            "id_zone_lavoro": None
        }

        self.dipendenti_entry_list = [
            {"id": "name", "text": "Nome :", "row": 3, "column": first_column},
            {"id": "last_name", "text": "Cognome :", "row": 3, "column": second_column},
            {"id": "pos_lav", "text": "Pos. Lavorativa :", "row": 4, "column": first_column},
            {"id": "date", "text": "Data Assunzione :", "row": 4, "column": second_column},
            {"id": "salary", "text": "Stipendio :", "row": 5, "column": first_column},
            {"id": "phone", "text": "Numero telefono :", "row": 5, "column": second_column},
            {"id": "id_zone_lavoro", "text": "ID Zona:", "row": 6, "column": 0},
        ]

        for idx, entry in enumerate(self.dipendenti_entry_list):

            if entry["id"] == "date":
                entry["entry"] = DateEntry(frame, width=18)
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)
            elif entry["id"] == "id_zone_lavoro":
                entry["entry"] = ttk.Combobox(frame, values=id_zone_lavoro, width=18)
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady, columnspan=6)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"]+1, pady=pady, columnspan=6)
            else:
                entry["entry"] = ttk.Entry(frame)
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)

        button_change = ttk.Button(frame, text="Change", command=lambda: self.update_row(
                table_name=table_name, data=dipendenti_data, entry_list=self.dipendenti_entry_list
        ))

        button_change.grid(column=3, row=15, pady=20, padx=1, sticky=E)

        button_close = ttk.Button(frame, text="Reset", command=lambda: self.clear_all(entry_list=self.dipendenti_entry_list))
        button_close.grid(column=4, row=15, pady=20, padx=1, sticky=E)

    def show_table_zone(self, frame, id_zone_list=None, first_column=2, second_column=4, pady=3, table_name="zone_lavoro"):
        ttk.Label(frame, text="Tabella Zone di lavoro", font='Helvetica 12 bold').grid(
            columnspan=6, row=0, pady=15, sticky=S
        )
        ttk.Label(self.frame, text="ID Zona:").grid(column=first_column, row=1, pady=pady)

        self.entry_id_zona = ttk.Combobox(frame, values=id_zone_list, width=18)
        self.entry_id_zona.grid(row=2, column=first_column+1, pady=pady)
        self.entry_id_zona.bind("<<ComboboxSelected>>", self.get_data_from_combo_zone_lavoro)

        zone_lavoro_data = {
            "name": None,
            "num_clienti": None
        }

        self.zone_lavoro_entry_list = [
            {"id": "name", "text": "Nome zona: ", "row": 3, "column": first_column},
            {"id": "num_clienti", "text": "Numero clienti: ", "row": 4, "column": first_column},
        ]

        for entry in self.zone_lavoro_entry_list:
            ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
            entry["entry"] = ttk.Entry(frame)
            entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)

        button_change = ttk.Button(
            frame, text="Change", command=lambda: self.update_row(
                table_name=table_name, data=zone_lavoro_data, entry_list=self.zone_lavoro_entry_list)
        )
        button_change.grid(column=2, row=7, pady=20, padx=0)

        button_close = ttk.Button(frame, text="Reset", command=lambda: self.clear_all(entry_list=self.zone_lavoro_entry_list))
        button_close.grid(column=3, row=7, pady=20, padx=0)

    def get_data_from_combo_dipendenti(self, event):

        self.get_data_from_server(
            data=self.dipendenti_data,
            combobox=self.entry_id_dipendente,
            entry_list=self.dipendenti_entry_list
        )

    def get_data_from_combo_zone_lavoro(self, event):

        self.get_data_from_server(
            data=self.zone_lavoro_data,
            combobox=self.entry_id_zona,
            entry_list=self.zone_lavoro_entry_list
        )

    def get_data_from_server(self, data, combobox, entry_list):

        self.id_selected = combobox.get().split()[0].strip()
        data_list = [item for item in data if item[0] == int(self.id_selected)]
        data_list = list(itertools.chain(*data_list))[1:]
        for entry, value in zip(entry_list, data_list):
            entry["entry"].config(state=NORMAL)
            entry["entry"].delete(0, END)
            entry["entry"].insert(0, value)

    def update_row(self, table_name, data, entry_list):
        for entry in entry_list:
            data[entry["id"]] = entry["entry"].get()
        data["id"] = self.id_selected

        self.socket.send(table_name.encode())
        self.socket.send(pickle.dumps(data))

        response = self.socket.recv(1024).decode()
        if "ERROR" in response:
            messagebox.showerror(title="ERROR", message=response)
        else:
            messagebox.showinfo(title="INFO", message=response)
        self.finestra.destroy()

    def close_window(self):
        self.socket.send("CLOSE".encode())
        self.finestra.destroy()


if __name__ == '__main__':
    Update()
