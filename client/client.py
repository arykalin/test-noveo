import socket
import sys
import time

expression_file = 'expression.txt'

# Connect the socket to the port where the server is listening
server_address = ('server', 10000)

while True:
    #Read expression
    f = open(expression_file, 'r')
    expression = f.read()
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Send data
    print('connecting to %s port %s' % server_address)
    connected = False
    while not connected:
      try:
        sock.connect(server_address)
        connected = True
      except:
        print('waiting for connection')
        time.sleep(3)
        pass
    print('sending "%s"' % expression)
    sock.send(expression.encode('ascii', 'ignore'))
    data = sock.recv(32)
    print(data.decode('ascii'))
    # print('closing socket')
    sock.close()
    # print('closing file')
    f.close()
    # print('File is closed: {}'.format(f.closed))
    # print('waiting')
    time.sleep(1)