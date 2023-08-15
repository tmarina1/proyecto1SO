from multiprocessing import Process
from multiprocessing.connection import Listener

def handle_client(client_conn, client_id):
    print(f"Cliente {client_id} conectado.")
    
    while True:
        try:
            data = client_conn.recv()
            if data is None:
                break 
            print(f"Cliente{client_id}: {data}")
        except EOFError:
            print(f"Cliente {client_id} salió.")
            break

    client_conn.close()

def main():
    server_address = ('localhost', 6000)
    server = Listener(server_address)

    client_id = 0

    while True:
        print("Iniciado y esperando")
        client_conn = server.accept()
        print("Conexion de:", server.last_accepted)

        client_process = Process(target=handle_client, args=(client_conn, client_id))
        client_process.start()

        client_id += 1

if __name__ == "__main__":
    main()
