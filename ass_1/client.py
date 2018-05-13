import time
import socket 
import thread
import threading
import pickle
import sys

UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bind_ip = "127.0.0.1"
port = 9999
message = "YOUR MUM"
UDP_client.sendto(message,(bind_ip,peer_successor_first_port))
TCP_client.connect((bind_ip,port))
TCP_client.send(message)
UDP_client.close()
TCP_client.close()