import socket, threading
from rich import print as rprint

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9991
ADDR = HOST, PORT

FORMAT = 'utf-8'
HEADER_SIZE = 64

run = True
nick_names = []

# TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global nick_names
    global run

    conn.send(b'Choose a nick name: ')
    while True:
        nick_name = conn.recv(4096)
        conn.send(b'ACK')
        nick_name = nick_name.decode(FORMAT)
        if not nick_name in nick_names:
            nick_names.append(nick_name)
            break
        else:
            conn.send(b'Nick name already taken.')

    rprint(f"[*] New  connection from [cyan]{nick_name}[/cyan]")
    connected = True
    while run and connected:
        msg = conn.recv(4096).decode(FORMAT)
        if msg == '/QUIT':
            connected = False
            nick_names.remove(nick_name)
        else:
            rprint(f'[[green]{nick_name}[/green]] {msg}')
        conn.send(b'ACK')
    rprint(f'[*] [red]{nick_name}[/red] has left.')
    conn.close()

def start():
    global run

    print('Starting server... (Ctrl-C to shut down, and make sure all clients are disconnected)')
    server.listen(5)
    print("Waiting for connection...")
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[*] ACTIVE CONNECTIONS: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        run = False
        print() # Make terminal prompt start in a new line
        server.shutdown(socket.SHUT_RDWR)
        server.close()

start()
