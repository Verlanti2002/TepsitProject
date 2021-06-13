import pickle  # Serve per serializzare gli oggetti e poterli inviare tramite socket
import sys
import socket

from gui.login_gui import Login
from gui.menu_gui import StartMenu
from logger import get_logger

logger = get_logger(create_file=True, filename="client.log")


class Client:   # Classe client

    # Costruttore
    def __init__(self, server_host, server_port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_host, server_port))

    # Metodo per la connesione al server
    def start(self):
        while True:
            try:
                data = self.socket.recv(1024)
                try:
                    data = data.decode()
                except UnicodeDecodeError:
                    data = pickle.loads(data)  # Per il decode delle query (liste, dizionari, tuple)
                if "Benvenuto client" in data:
                    login = Login(socket=self.socket)  # Login grafica
                    if login.result:
                        try:
                            StartMenu(socket=self.socket)  # Menù grafica
                        except ConnectionAbortedError as error:
                            logger.error(error)
                            raise Exception
                # elif "Q:" in data:  # Q = Question
                #     self.socket.send(input(data).encode()) # Se presente la Q di question allora il server si aspetta di ricevere una risposta (quindi un input da parte del client)
                elif data:
                    logger.info(f"Server: {data}")  # Stampa il messaggio ricevuto dal server
                else:
                    raise Exception
            except Exception as error:
                logger.error(error)
                sys.exit(0)


if __name__ == '__main__':
    try:
        client = Client(server_host="localhost", server_port=5000)
        client.start()
    except Exception as error:
        logger.error(error)
        sys.exit(0)