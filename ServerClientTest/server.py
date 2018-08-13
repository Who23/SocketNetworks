import socket

s = socket.socket()
host = ''
port = 32456
s.bind((host, port))
x = 0
s.listen(1)
c, addr = s.accept()
print("Connection from: {}".format(addr))
msg = ''
while msg != "quit":
    msg = input("Message: ")
    c.send(bytes(msg, 'utf-8'))
    recvMsg = c.recv(1024).decode('utf-8')
    if recvMsg != '':
        print("{}: {}".format(addr[1], recvMsg))

c.close()
print("Disconnected from client: {}".format(addr) )