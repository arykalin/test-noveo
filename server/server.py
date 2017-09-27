import math
import re
import socket
import sys
import time

integers_regex = re.compile(r'\b[\d\.]+\b')

def calc(expr):
   def safe_eval(expr, symbols={}):
       return eval(expr, dict(__builtins__=None), symbols)
   def whole_number_to_float(match):
       group = match.group()
       if group.find('.') == -1:
           return group + '.0'
       return group
   expr = expr.replace('^', '**')
   expr = integers_regex.sub(whole_number_to_float, expr)
   return safe_eval(expr)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('server', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        data = connection.recv(16)
        print('received "%s"' % data)
        if data:
            print('sending data back to the client')
            answer = str(calc(str(data.decode('ascii'))))
            print(answer)
            connection.send(answer.encode('ascii', 'ignore'))


    finally:
        # Clean up the connection
        time.sleep(1)