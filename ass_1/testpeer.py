import socket 
import threading
import pickle
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
peer_port_num = 50000 + 1
bind_ip = "127.0.0.1"

server.sendto("3", (bind_ip,peer_port_num))
