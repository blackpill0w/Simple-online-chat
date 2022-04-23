import socket
from rich import print as rprint

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9991
ADDR = HOST, PORT

FORMAT = 'utf-8'
HEADER_SIZE = 64

# TCP
print('[*] Trying to connect...')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('Connected!')

# First we need to set a nick name
nick_name_req = client.recv(4096).decode(FORMAT)
print(nick_name_req)

run = True

while run:
    rprint('[bright_blue bold]-> [/bright_blue bold]', end='')
    msg = input()

    client.send(msg.encode(FORMAT))
    resp = client.recv(4096).decode(FORMAT)
    if msg in ('/QUIT', ''):
        run = False
        print('Server shut down.')
    elif resp == 'ACK' + 'Nick name already taken.':
        print('Nick name already taken.')
    elif resp != 'ACK':
        print(f'Response: {resp}')

client.close()
