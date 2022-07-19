import socket, threading
from utils import ADDR, FORMAT, BUFFER_SIZE
from rich import print as rprint

run = True
nicknames = []
clients = []
messages_to_send = []

# TCP server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(1)
server.bind(ADDR)

def format_msg(nickname, msg):
    return f'[[green]{nickname}[/green]] {msg}'

def handle_client(conn):
    global nick_names
    global run
    global messages_to_send

    conn.send(b'Choose a nick name: ')
    while True:
        nickname = conn.recv(BUFFER_SIZE).decode(FORMAT)
        conn.send(b'ACK')
        if not nickname in nicknames:
            nicknames.append(nickname)
            break
        else:
            conn.send(b'Nick name already taken.')

    rprint(f"[*] New  connection from [cyan]{nickname}[/cyan]")
    connected = True
    while run and connected:
        msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
        if msg == '/QUIT':
            connected = False
            nicknames.remove(nickname)
        else:
            formatted_msg = format_msg(nickname, msg)
            rprint(formatted_msg)
            messages_to_send.append([conn, formatted_msg.encode(FORMAT)])
        conn.send(b'ACK')
    rprint(f'[*] [red]{nickname}[/red] has left.')
    conn.close()

def start():
    global run
    global clients
    global server

    print('Starting server... (Ctrl-C to shut down)')
    server.listen(5)
    print("Waiting for connection...")
    try:
        while True:
            if len(messages_to_send) > 0:
                c, m = messages_to_send.pop(0)
                for client in clients:
                    if client != c:
                        client.send(m)
            try:
                conn, _ = server.accept()
                clients.append(conn)
                thread = threading.Thread(target=handle_client, args=(conn,))
                thread.start()
            except TimeoutError:
                pass
            print(f"[*] ACTIVE CONNECTIONS: {threading.active_count() - 1}")

    except KeyboardInterrupt:
        run = False
        print() # Make terminal prompt start in a new line
        server.shutdown(socket.SHUT_RDWR)
        server.close()

start()
