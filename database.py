import mariadb
import threading


class Database:  # Classe Database

    # Costruttore
    def __init__(self, user, password, host, database, port=3306):

        # Connessione al database
        self.conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )
        self.cursor = self.conn.cursor()

        self.lock = threading.Lock()

    # Metodo per ottenere i campi identificativi di ogni singolo dipendente
    # def get_dipendenti_list(self):
    #     query = f"SELECT id, nome, cognome FROM dipendenti"
    #     self.cursor.execute(query)
    #     dati = self.cursor.fetchall()
    #     return dati

    def get_zone_lavoro_list(self):
        query = f"SELECT id, nome_zona FROM zone_lavoro"
        self.cursor.execute(query)
        dati = self.cursor.fetchall()
        return dati

    # Metodo per l'inserimento dei record nella tabella dipendenti
    def insert_dipendenti(self, nome, cognome, posizione_lavoro, data_assunzione, stipendio, telefono, id_zone_lavoro):
        with self.lock:
            control_query = f"SELECT id FROM zone_lavoro WHERE 'id' = '{id_zone_lavoro}'"
            self.cursor.execute(control_query)
            if not self.cursor:
                return

            query = (
                "INSERT INTO dipendenti (nome, cognome, posizione_lavoro, data_assunzione, stipendio, telefono, id_zone_lavoro)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            parametri = (nome, cognome, posizione_lavoro, data_assunzione, stipendio, telefono, id_zone_lavoro)
            self.cursor.execute(query, parametri)  # Prende in ingresso una tupla
            self.conn.commit()  # Salva le modifiche nel database

    # Metodo per l'inserimento dei record nella tabella zone_lavoro
    def insert_zone_lavoro(self, nome_zona, numero_clienti):
        with self.lock:
            try:
                numero_clienti = int(numero_clienti)
            except ValueError:
                raise Exception("Valore inserito non valido")

            query = (
                "INSERT INTO zone_lavoro (nome_zona, numero_clienti)"
                "VALUES (%s, %s)"
            )
            parametri = (nome_zona, numero_clienti)
            self.cursor.execute(query, parametri)
            self.conn.commit()

    # Metodo per la lettura dei record della tabella dipendenti
    # def read_dipendenti(self, id):
    #     query = f"SELECT * FROM dipendenti WHERE id = '{id}'"
    #     self.cursor.execute(query)
    #     dati = self.cursor.fetchall()
    #     return dati

    def read_all_dipendenti(self):
        query = f"SELECT * FROM dipendenti"
        self.cursor.execute(query)
        dati = self.cursor.fetchall()

        return dati

    # Metodo per la lettura dei record della tabella zone_lavoro
    # def read_zone_lavoro(self, id):
    #     query = f"SELECT * FROM zone_lavoro WHERE id = '{id}'"
    #     self.cursor.execute(query)
    #     dati = self.cursor.fetchall()
    #     return dati

    def read_all_zone_lavoro(self):
        query = f"SELECT * FROM zone_lavoro"
        self.cursor.execute(query)
        dati = self.cursor.fetchall()
        return dati

    # Metodo per l'aggiornamento dei record nella tabella dipendenti
    def update_dipendenti(self, name, last_name, pos_lav, date, salary, phone, id_zone_lavoro, id):
        with self.lock:
            query = f"UPDATE dipendenti SET nome=%s , cognome=%s,posizione_lavoro=%s,data_assunzione=%s," \
                    f"stipendio=%s,telefono=%s,id_zone_lavoro=%s WHERE id=%s"
            self.cursor.execute(query, (name, last_name, pos_lav, date, salary, phone, id_zone_lavoro, id))
            self.conn.commit()

    # Metodo per l'aggiornamento dei record nella tabella zone_lavoro
    def update_zone_lavoro(self, name, num_clienti , id):
        with self.lock:
            query = f"UPDATE zone_lavoro SET nome_zona=%s, numero_clienti=%s WHERE id=%s"
            self.cursor.execute(query, (name, num_clienti, id))
            self.conn.commit()

    # Metodo per l'eliminazione dei record dalla tabella dipendenti
    def delete_dipendenti(self, id_da_eliminare):
        with self.lock:
            query = f"DELETE FROM dipendenti WHERE id = '{id_da_eliminare}'"
            self.cursor.execute(query)
            self.conn.commit()

    # Metodo per l'eliminazione dei record dalla tabella zone_lavoro
    def delete_zone_lavoro(self, id_da_elimianare):
        with self.lock:
            query = f"DELETE FROM zone_lavoro WHERE id = '{id_da_elimianare}'"
            self.cursor.execute(query)
            self.conn.commit()
