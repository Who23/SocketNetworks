import socket

s = socket.socket()
host = 'PUT HOST HERE'
port = 32456

s.connect((host, port))
msg = ''
while msg != "quit":
    msg = s.recv(1024).decode('utf-8')
    print("SERVER: {}".format(msg))
    if msg != '':
        s.send(b"Message Recieved")

s.close()
print("Disconnected from server")
