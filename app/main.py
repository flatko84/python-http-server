import socket
from threading import Thread
from webapp.connection import Connection

class HttpServer:
    def main(self, *args):
        print("Server started.")
        server = socket.create_server(("localhost", 4221), reuse_port=True)
        connection = Connection()
        try:
            while True:
                socket_object, ret_address = server.accept()
                Thread(target=connection.connect, args=(socket_object, ret_address)).start()
        except KeyboardInterrupt:
            print("Server stopped.")


if __name__ == "__main__":
    srv = HttpServer()
    srv.main()
