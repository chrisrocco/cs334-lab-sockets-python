import socket
from random import randint
import time

port = 3310
localhost = "localhost"
robothost = "localhost"
blazer_id = "chris77"

# create a new socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((robothost, port))

# send blazer ID over socket
client_socket.send(blazer_id.encode())

# get new port in response
new_port = int(client_socket.recv(5))

# create new socket and listen for connections on that port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((localhost, new_port))
server_socket.listen(5)
robot_client_socket, addr = server_socket.accept()

# upon connection, get response in format: fffff,eeeee (12 byes)
fffff_eeeee = robot_client_socket.recv(100).decode()
fffff = int(fffff_eeeee.split(",")[0])
eeeee = int(fffff_eeeee.split(",")[1])
num = randint(5, 10)

# send random number over UDP to port fffff (from last step)
udp_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_out.sendto(str(num).encode(), (robothost, fffff))

# get secret response (will be sent from robot 5 times)
udp_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_in.bind((localhost, eeeee))
x = udp_in.recv(100).decode()

# send it back 5 times * 10
time.sleep(5)
for i in range(0, 5):
    udp_out.sendto(x.encode(), (robothost, fffff))
    time.sleep(1)