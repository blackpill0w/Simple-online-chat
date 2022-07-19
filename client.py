import socket
from utils import  ADDR, FORMAT, BUFFER_SIZE
from rich import print as rprint

# TCP
print('[*] Trying to connect...')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('Connected!')

# First we need to set a nick name
nick_name_req = client.recv(BUFFER_SIZE).decode(FORMAT)
print(nick_name_req)

run = True

while run:
    rprint('[bright_blue bold]-> [/bright_blue bold]', end='')
    msg = input()

    client.send(msg.encode(FORMAT))
    resp = client.recv(4096).decode(FORMAT)
    if resp == '/QUIT' or msg == '/QUIT':
        run = False
        print('Shut down.')
    elif resp == 'ACK' + 'Nick name already taken.':
        print('Nick name already taken.')
    elif resp != 'ACK':
        rprint(resp)

client.close()
