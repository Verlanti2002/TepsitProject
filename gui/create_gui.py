from datetime import datetime

import pickle
from tkinter import messagebox, ttk
from tkcalendar import DateEntry


from gui.parent_window import ParentWindow


class Create(ParentWindow):

    def __init__(self, socket=None):
        # Attributi
        self.socket = socket

        # self.id_zone_lavoro_list = []
        self.id_zone_lavoro_list = pickle.loads(self.socket.recv(1024))
        self.id_zone_lavoro_list = [f"{id_zona} - {nome}" for id_zona, nome in self.id_zone_lavoro_list]

        super(Create, self).__init__(title="Create", id_zone_lavoro_list=self.id_zone_lavoro_list)

    def show_table_dipendenti(self, frame, id_zone_lavoro=None, id_dipendenti_list=None, first_column=2, second_column=4, pady=3, table_name="dipendenti"):
        dipendenti_data = {
            "name": None,
            "last_name": None,
            "pos_lav": None,
            "date": None,
            "salary": None,
            "phone": None,
            "id_zone_lavoro": None
        }
        dipendenti_entry_list = [
            {"id": "name", "text": "Nome :", "row": 3, "column": first_column},
            {"id": "last_name", "text": "Cognome :", "row": 3, "column": second_column},
            {"id": "pos_lav", "text": "Pos. Lavorativa :", "row": 4, "column": first_column},
            {"id": "date", "text": "Data Assunzione :", "row": 4, "column": second_column},
            {"id": "salary", "text": "Stipendio :", "row": 5, "column": first_column},
            {"id": "phone", "text": "Numero telefono :", "row": 5, "column": second_column},
            {"id": "id_zone_lavoro", "text": "ID Zona: ", "row": 6, "column": 0},
        ]

        ttk.Label(frame, text="Tabella Dipendenti", font='Helvetica 12 bold').grid(columnspan=6, row=0, pady=30)
        for entry in dipendenti_entry_list:
            if entry["id"] == "date":
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
                entry["entry"] = DateEntry(frame, width=18)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)
            elif entry["id"] == "id_zone_lavoro":
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], columnspan=6, pady=pady)
                entry["entry"] = ttk.Combobox(frame, values=id_zone_lavoro, width=18)
                entry["entry"].grid(column=entry["column"], row=entry["row"] + 1, columnspan=6, pady=pady)
            else:
                ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
                entry["entry"] = ttk.Entry(frame)
                entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)

        add_button = ttk.Button(frame, text="Aggiungi", command=lambda: self.add_row(
            table_name=table_name, data=dipendenti_data, entry_list=dipendenti_entry_list
        ))
        add_button.grid(columnspan=10, row=11, pady=10)

    def show_table_zone(self, frame, id_zone_list=None, first_column=2, second_column=4, pady=3, table_name="zone_lavoro"):
        zone_lavoro_data = {
            "name": None,
            "num_clienti": None
        }

        zone_lavoro_entry_list = [
            {"id": "name", "text": "Nome zona: ", "row": 3, "column": first_column},
            # {"id": "id_dipendente", "text": "ID Dipendente: ", "row": 3, "column": second_column},
            {"id": "num_clienti", "text": "Numero clienti: ", "row": 4, "column": first_column},
        ]

        ttk.Label(frame, text="Tabella Zone di lavoro", font='Helvetica 12 bold').grid(columnspan=6, row=0, pady=30)
        for entry in zone_lavoro_entry_list:
            ttk.Label(frame, text=entry["text"]).grid(column=entry["column"], row=entry["row"], pady=pady)
            entry["entry"] = ttk.Entry(frame)
            entry["entry"].grid(column=entry["column"] + 1, row=entry["row"], pady=pady)

        add_button = ttk.Button(frame, text="Aggiungi", command=lambda: self.add_row(
            table_name=table_name, data=zone_lavoro_data, entry_list=zone_lavoro_entry_list
        ))
        add_button.grid(columnspan=10, row=11, pady=10)

    def add_row(self, table_name, data, entry_list):
        for entry in entry_list:
            if table_name == "dipendenti" and entry["id"] == "date":
                data[entry["id"]] = datetime.strptime(entry["entry"].get(), "%m/%d/%y").strftime("%Y-%m-%d")
            else:
                data[entry["id"]] = entry["entry"].get()

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


if __name__ == '__main__':  # main
     Create()
