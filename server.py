import mariadb
import pickle  # Serve per serializzare gli oggetti e poterli inviare tramite socket
import socket
import threading

from database import Database
from logger import get_logger

logger = get_logger(create_file=True, filename="server.log")


# Il login parte immediatamente
# Classe Server
class Server:

    # Costruttore
    def __init__(self, host, port, max_connection_supported=2):

        # Massimo delle connessioni supportate dal server
        self.max_connection_supported = max_connection_supported

        # Creazione del socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(self.max_connection_supported)

        # Istanza classe database
        self.db = None

        self.active_clients_connections = 0

    # Fa partire il server
    def start(self):
        while True:
            conn, addr = self.socket.accept()  # Accetta la connessione
            self.active_clients_connections += 1
            logger.info(f"Connection of {addr[0]}:{addr[1]}")  # Indirizzo ip : Porta
            logger.info(f"Active connections: {self.active_clients_connections}")
            # Controlla se ha superato il limite di connessioni possibili
            # Se si connette fa partire un thread nella funzione start_app
            # Altrimenti fa partire il decline_connection che declina dolcemente la connessione
            if self.active_clients_connections <= self.max_connection_supported:
                t = threading.Thread(target=self.start_app, args=(conn,))
                t.start()
            else:
                self.active_clients_connections -= 1
                t = threading.Thread(target=self.decline_connection, args=(conn, "Connessione rifiutata, Server pieno!"))
                t.start()

    # Chiude la connessione col client
    @staticmethod
    def decline_connection(conn, message):
        logger.info(message)
        conn.send(message.encode())
        conn.send("Bye!".encode())
        conn.close()

    # Metodo che fa partire l'app (quindi il menù) se l'autenticazione è avvenuta correttamente,
    # altrimenti chiude la connessione (decline_connection)
    def start_app(self, conn):
        # In caso non vada nell'else una volta svolte le operazioni manderà al client il messaggio di uscita in corso
        message = "Uscita in corso..."
        # Funzione login che ritorna due valori:
        #   True --> se l'autenticazione è andata bene, mostra il menu
        #   False --> se l'autenticazione è andata male, chiude la connessione col client
        try:
            login_access = self.login(conn=conn)
        except (ConnectionAbortedError, ConnectionResetError) as error:
            self.active_clients_connections -= 1
            logger.error(error)
            return
        if login_access:
            try:
                self.menu(conn)
            except (ConnectionAbortedError, ConnectionResetError) as error:
                self.active_clients_connections -= 1
                logger.error(error)
                return
        else:
            message = "Autenticazione fallita!\n"
        self.decline_connection(conn, message)

    # Funzione che controlla il corretto accesso da parte del client
    @staticmethod
    def login(conn, max_attempts=3):
        attempts = 0    # Variabile che conta i tentativi

        conn.send(f"Benvenuto client".encode())
        while attempts < max_attempts:
            username = conn.recv(1024)
            password = conn.recv(1024)
            if not username.decode() or username.decode() != "admin" and password.decode() or password.decode() != "admin":
                conn.send("Credenziali errate!".encode())
                logger.error("Credenziali errate!")
                attempts += 1
            else:
                conn.send("Congratulazioni, sei entrato!".encode())
                logger.info("Client autenticato!")
                return True
        return False

    # Metodo menu per presentare il menù
    def menu(self, conn):
        try:
            self.db = Database('root', '', 'localhost', 'tepsit', 3306)
        except mariadb.Error as error:
            logger.error(error)
            #conn.send(b"")
            self.decline_connection(conn, "Database not connected")
            raise ConnectionAbortedError

        while True:
            data = conn.recv(1024)
            try:
                option = int(data.decode())
            except ValueError:
                option = -1

            if option == 1:
                self.create(conn, self.db)
            elif option == 2:
                self.read(conn, self.db)
            elif option == 3:
                self.update(conn, self.db)
            elif option == 4:
                self.delete(conn, self.db)
            else:
                conn.send("Opzione non valida!".encode())

    # Funzione per l'inserimento dei dati nel database
    @staticmethod
    def create(conn, db):
        # invio lista dipendenti
        zone_lavoro_data = db.get_zone_lavoro_list()
        data = pickle.dumps(zone_lavoro_data)  # Per inviare la lista del nome, cognome e id dei dipendenti (encode())
        conn.send(data)

        data = conn.recv(1024)
        if data.decode().lower() == "dipendenti":
            data = conn.recv(1024)
            if b"CLOSE" in data:
                return
            dipendenti_data = pickle.loads(data)  # Per ricevere il dizionario dei dipendenti (decode())
            try:
                db.insert_dipendenti(
                    nome=dipendenti_data["name"],
                    cognome=dipendenti_data["last_name"],
                    posizione_lavoro=dipendenti_data["pos_lav"],
                    data_assunzione=dipendenti_data["date"],
                    stipendio=dipendenti_data["salary"],
                    telefono=dipendenti_data["phone"],
                    id_zone_lavoro=dipendenti_data["id_zone_lavoro"]
                )
                conn.send("INFO: L'inserimento è andato a buon fine!".encode())
                logger.info("L'inserimento è andato a buon fine!")
            except Exception as error:
                # conn.send("L'inserimento non è andato a buon fine!".encode())
                logger.error(error)
                conn.send(f"ERROR: {error}".encode())
        elif data.decode().lower() == "zone_lavoro":
            data = conn.recv(1024)
            if b"CLOSE" in data:
                return
            zone_lavoro_data = pickle.loads(data)  # Per ricevere il dizionario dei dipendenti (decode())
            try:
                db.insert_zone_lavoro(
                    nome_zona=zone_lavoro_data["name"],
                    numero_clienti=zone_lavoro_data["num_clienti"]
                )
                conn.send("INFO: L'inserimento è andato a buon fine!".encode())
                logger.info("L'inserimento è andato a buon fine!")
            except Exception as error:
                conn.send(f"ERROR: {error}".encode())
                logger.error(error)

    # Funzione per la lettura dei dati dal database
    @staticmethod
    def read(conn, db):
        dipendenti_data = db.read_all_dipendenti()
        data = pickle.dumps(dipendenti_data)
        conn.send(data)

        zone_lavoro_data = db.read_all_zone_lavoro()
        data = pickle.dumps(zone_lavoro_data)
        conn.send(data)

    # Funzione per l'aggiornamento dei dati nel database
    @staticmethod
    def update(conn, db):
        dipendenti_data = db.read_all_dipendenti()
        data = pickle.dumps(dipendenti_data)
        conn.send(data)

        zone_lavoro_data = db.read_all_zone_lavoro()
        data = pickle.dumps(zone_lavoro_data)
        conn.send(data)

        data = conn.recv(1024)
        if data.decode().lower() == "dipendenti":
            data = conn.recv(1024)
            if b"CLOSE" in data:
                return
            data = pickle.loads(data)
            try:
                db.update_dipendenti(**data)
                conn.send("INFO: Aggiornamento avvenuto con successo!".encode())
                logger.info("Aggiornamento avvenuto con successo!")
            except Exception as error:
                conn.send("ERROR: Aggiornamento non avvenuto con successo!".encode())
                logger.error(error)
        elif data.decode().lower() == "zone_lavoro":
            data = conn.recv(1024)
            if b"CLOSE" in data:
                return
            data = pickle.loads(data)
            try:
                db.update_zone_lavoro(**data)
                conn.send("INFO: Aggiornamento avvenuto con successo!".encode())
            except Exception as error:
                conn.send(f"ERROR: Aggiornamento non avvenuto con successo - {error}!".encode())
                logger.error(error)

    # Funzione per l'eliminazione dei dati nel database
    @staticmethod
    def delete(conn, db):
        dipendenti_data = db.read_all_dipendenti()
        data = pickle.dumps(dipendenti_data)
        conn.send(data)

        zone_lavoro_data = db.read_all_zone_lavoro()
        data = pickle.dumps(zone_lavoro_data)
        conn.send(data)

        data = conn.recv(1024)
        if data.decode().lower() == "dipendenti":
            id_da_eliminare = conn.recv(1024).decode()
            if "CLOSE" in id_da_eliminare:
                return
            try:
                db.delete_dipendenti(id_da_eliminare=id_da_eliminare)
                conn.send("INFO: Eliminazione avvenuta con successo!".encode())
                logger.info("Eliminazione avvenuta con successo!")
            except Exception as error:
                conn.send(f"ERROR: Eliminazione non avvenuta con successo! - {error}".encode())
                logger.error(error)
        elif data.decode().lower() == "zone_lavoro":
            id_da_eliminare = conn.recv(1024).decode()
            if "CLOSE" in id_da_eliminare:
                return
            try:
                db.delete_zone_lavoro(id_da_elimianare=id_da_eliminare)
                conn.send("INFO: Eliminazione avvenuta con successo!".encode())
                logger.info("Eliminazione avvenuta con successo!")
            except Exception as error:
                conn.send(f"ERROR: Eliminazione non avvenuta con successo! - {error}".encode())
                logger.error(error)


if __name__ == '__main__':      # Main
    server = Server(host="localhost", port=5000)
    try:
        server.start()
    except Exception as error:
        logger.error(error)
