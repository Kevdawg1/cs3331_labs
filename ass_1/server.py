import time
import socket 
import thread
import threading
import pickle
import sys

UDP_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TCP_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bind_ip = "127.0.0.1"
port = 9999
UDP_server.bind((bind_ip,port))
TCP_server.bind((bind_ip,port))

def UDP_listen(server):
	# listen(1)
	data, addr = UDP_server.recvfrom(1024)
	print (data)

def TCP_listen(server):
	# listen(1)
	conn,addr = TCP_server.accept()
	data = conn.recv(1024)
	print (data)

while True:
	try:
		thread.start_new_thread(UDP_listen, (UDP_server,))
	#thread.start_new_thread(TCP_listen, (TCP_server,))
	except: 
		continue