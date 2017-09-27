import socket
import sys
import time

expression_file = 'expression.txt'
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

while True:
    try:
        #Read expression
        with open(expression_file) as f:
            expression = f.read()
        # Send data
        print('sending "%s"' % expression)
        sock.sendall(expression.encode('utf-8'))

        # Look for the response
        amount_received = 0
        amount_expected = len(expression)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received "%s"' % data)

    finally:
        print('closing socket')
        sock.close()
        time.sleep(1)