import time
import socket 
import thread
import threading
import pickle
import sys
import signal

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcp_client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcp_client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
print('Now hosting TCP server....')
print('Listening for peer response....')

class Connection:
	def __init__(self, origin_port):
		self._origin_port = origin_port
		self._message_type = ""
		self._filename = ""
		self._quit_first_successor = ""
		self._quit_second_successor = ""
	@property
	def origin_port(self):
		return self._origin_port
	@property
	def message_type(self):
		return self._message_type
	@property
	def filename(self):
		return self._filename
	@property
	def quit_first_successor(self):
		return self._quit_first_successor
	@property
	def quit_second_successor(self):
		return self._quit_second_successor
	def set_message_type(self, message_type):
		self._message_type = message_type
	def set_filename(self,filename):
		self._filename = filename
	def set_quit_first_successor(self,quit_first_successor):
		self._quit_first_successor = quit_first_successor
	def set_quit_second_successor(self,quit_second_successor):
		self._quit_second_successor = quit_second_successor	
peer_id = int(sys.argv[1])
peer_successor_first = int(sys.argv[2])
peer_successor_first_port = peer_successor_first + 50000
peer_successor_second = int(sys.argv[3]) 
peer_successor_second_port = peer_successor_second + 50000
# print (peer_id)
peer_port_num = 50000 + int(peer_id)
bind_ip = '127.0.0.1'
added_peers = [0, 0]

def signal_handler(signal, frame):
	conn_data = Connection(peer_port_num)
	conn_data.set_message_type("kill")
	conn_data.set_quit_first_successor(peer_successor_first)
	conn_data.set_quit_second_successor(peer_successor_second)
	peer_leave(conn_data)
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

udp_server.bind((bind_ip,peer_port_num))
tcp_server.bind((bind_ip,peer_port_num))
tcp_server.listen(5)
tcp_server.setblocking(0)
tcp_client1.setblocking(0)
tcp_client2.setblocking(0)
# connected_peers = 0
# while (connected_peers < 2 and (added_peers[0] == 0 or added_peers[1] == 0)):
# 		try:
# 			tcp_server.settimeout(int(peer_id))
# 			conn, addr = tcp_server.accept()
# 			data = conn.recv(1024)
# 			connected_peers += 1
# 			conn_data = pickle.loads(data)
# 			print("Connection made from %s " % conn_data.origin_port)
# 			message = pickle.dumps(conn_data)
# 			tcp_server.send(message)
# 			tcp_server.shutdown(0)
# 		except:
# 			conn_data = Connection(peer_port_num)
# 			conn_data.set_message_type("connection")
# 			message = pickle.dumps(conn_data)
# 			try:
# 				if (added_peers[0] == 0):
# 					tcp_client1.connect((bind_ip,peer_successor_first_port))
# 					print("sending connection to %d" % peer_successor_first)
# 					tcp_client1.send(message)
# 					# conn_data = tcp_client1.recv(1024)
# 					tcp_client1.shutdown(1)
# 					added_peers[0] = 1;
# 				elif (added_peers[1] == 0):
# 					print("connecting to %d" % peer_successor_second)
# 					tcp_client2.connect((bind_ip,peer_successor_second_port))
# 					print("sending connection to %d" % peer_successor_second)
# 					tcp_client2.send(message)
# 					# conn_data = tcp_client2.recv(1024)
# 					tcp_client2.shutdown(1)
# 					print("peer second added")
# 					added_peers[1] = 1;
# 			except:
# 				continue
# tcp_client1.close()
# tcp_client2.close()


# tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# tcp_server.bind((bind_ip,peer_port_num))
# tcp_server.listen(10)
# conn,addr = tcp_server.accept()
# data = conn.recv(1024)
# udp_server.listen(1)
# udp_server.sendto(peer_id, (bind_ip,peer_successor_first))
# def udp_listen():
# 	global pings
# 	data, addr = udp_server.recvfrom(1024)
# 	if (data != "approved"):
# 		print ("A ping request was received from Peer %s." % data)
# 		pings += 1
# 		port = int(data) + 50000
# 		udp_server.sendto("approved", (bind_ip,port))

# def ping_first_peer():
# 	global pings
# 	udp_server.sendto(peer_id,(bind_ip, peer_successor_first_port))
# 	data, addr = udp_server.recvfrom(1024)
# 	ping_count[0] = 1

# def ping_second_peer():
# 	global pings
# 	udp_server.sendto(peer_id,(bind_ip, peer_successor_second_port))
# 	data, addr = udp_server.recvfrom(1024)
# 	ping_count[1] = 1

# ping_count = [0, 0]
# pings = 0
# while (pings < 2):
# 	try:
# 		thread.start_new_thread(udp_listen, ())
# 		if (ping_count[0] == 0):
# 			thread.start_new_thread(ping_first_peer, ())
# 		if (ping_count[1] == 0):
# 			thread.start_new_thread(ping_second_peer, ())
# 	except:
# 		continue
print("Listening...")


def request_file(conn_data):
	filename = conn_data.filename
	hashed = int(filename) % 256							# filename is hashed to find peer id responsible

	origin_port = int(conn_data.origin_port)					# recovers the port first requested from
	#if (peer_port_num != origin_port):
	#	print("entered")
	#  response_sock.connect((bind_ip, origin_port))		# connects to peer from origin port
	if (origin_port == peer_port_num):
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		message = pickle.dumps(conn_data)
		response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		response_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		response_sock.connect((bind_ip, peer_successor_second_port))
		response_sock.send(message)
		return
	if (hashed == peer_id or (hashed > conn_data.quit_second_successor and hashed <= peer_id)):
		# it is stored in this peer
		print ('')
		response_message = "File %s is here." % filename
		print(response_message)
		response_message = "A response message, destined for peer %s, has been sent." % filename
		print(response_message)
		# response_message = filename + "," + peer_id
		print(origin_port)
		response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		response_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		response_sock.connect((bind_ip, origin_port))
		conn_data = Connection(peer_port_num)
		conn_data.set_filename(filename)
		message = pickle.dumps(conn_data)
		response_sock.send(message)
		conn_data = response_sock.recv(1024)
		response_sock.close()
	elif (hashed == peer_successor_first or (hashed < peer_successor_first and hashed > peer_id)):
		# it is stored in first successor
		print ('')
		response_message = "File %s is not stored here." % filename
		print(response_message)
		response_message = "File request message for %s has been forwarded to my successor %s." % (filename,peer_successor_first)
		print(response_message)
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		message = pickle.dumps(conn_data)
		tcp_client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_client1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		tcp_client1.connect((bind_ip,peer_successor_first_port))
		tcp_client1.send(message)
	elif (hashed == peer_successor_second or (hashed > peer_successor_first and hashed < peer_successor_second)):
		# it is stored in second successor
		print ('')
		response_message = "File %s is not stored here." % filename
		print(response_message)
		response_message = "File request message for %s has been forwarded to my successor %s." % (filename,peer_successor_second)
		print(response_message)
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		message = pickle.dumps(conn_data)
		response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		response_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		response_sock.connect((bind_ip, peer_successor_second_port))
		response_sock.send(message)
	else:
		if (hashed != peer_id):
			print ('')
			response_message = "File %s is not stored here." % filename
			print(response_message)
			response_message = "File request message for %s has been sent to my successor %s." % (filename,peer_successor_second)
			print(response_message)
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		message = pickle.dumps(conn_data)
		response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		response_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		response_sock.connect((bind_ip, peer_successor_second_port))
		response_sock.send(message)

def handle_request(conn_data):
	request_file(conn_data)
	print("Listening for response...")
	tcp_server.setblocking(1)
	conn,addr = tcp_server.accept()
	data = conn.recv(1024)
	conn_data = pickle.loads(data)
	# filename, peer = data.split(",")
	print ('')
	print("Received a response message from peer %s, which has the file %s." % (conn_data.origin_port,conn_data.filename))
	# tcp_server.setblocking(0)

def pinging(tcp_server,peer_port_num,bind_ip):
	# data, addr = udp_server.recvfrom(1024)
	# tcp_server.setdefaulttimeout(60)
	tcp_server.listen(10)
	try:
		conn, addr = tcp_server.accept()
	except:
		return
	data = conn.recv(1024)
	conn_data = pickle.loads(data)
	if (conn_data.message_type == "request"):
		request_file(conn_data)
	elif (conn_data.message_type == "connection"):
		respondConnection(conn_data)
	elif(conn_data.message_type == "quit" or conn_data.message_type == "kill"):
		peer_leave(conn_data)
	else: 
		conn_data = pickle.loads(data)
		print ("A ping request was received from Peer %s." % conn_data.origin_port)

def respondConnection(conn_data):
	resp_data = Connection(peer_port_num)
	resp_data.set_message_type("connection-ack")
	response_message = pickle.dumps(resp_data)
	# data = pickle.loads(conn_data)
	print("Connection Made with %d" % conn_data.origin_port)
	# tcp_server.send(conn_data)
	# response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# response_sock.connect((bind_ip, origin_port))
	# response_sock.send(response_message)

def peer_leave(conn_data):
	global peer_successor_first
	global peer_successor_first_port
	global peer_successor_second
	global peer_successor_second_port
	if (conn_data.origin_port == peer_port_num):
		quit_message = pickle.dumps(conn_data)
		tcp_client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_client1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		tcp_client1.connect((bind_ip,peer_successor_first_port))
		tcp_client1.send(quit_message)
	else:
		if (peer_successor_first_port == conn_data.origin_port):
			peer_successor_first = conn_data.quit_first_successor
			peer_successor_first_port = peer_successor_first + 50000
			peer_successor_second = conn_data.quit_second_successor
			peer_successor_second_port = peer_successor_second + 50000
			if (conn_data.message_type == "quit"):
				print ('')
				print("Peer " + str(conn_data.origin_port-50000) + " will depart from the network.")
			elif (conn_data.message_type == "kill"):
				print ('')
				print("Peer " + str(conn_data.origin_port-50000) + " is no longer alive.")
			print("My first successor is now peer " + str(peer_successor_first) + ".")
			print("My second successor is now peer " + str(peer_successor_second) + ".")
			return
		elif (peer_successor_second_port == conn_data.origin_port):
			peer_successor_second = conn_data.quit_second_successor
			peer_successor_second_port = conn_data.quit_second_successor + 50000
			print("My second successor is now peer " + str(peer_successor_second) + ".")
		quit_message = pickle.dumps(conn_data)
		tcp_client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcp_client1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		tcp_client1.connect((bind_ip,peer_successor_first_port))
		tcp_client1.send(quit_message)

def request_listen():
	i = raw_input("Enter your request:")
	if not i:
		return
	# i = ""
	input_message = i.split(" ")
	if (input_message[0] == "request"):
		conn_data = Connection(peer_port_num)
		conn_data.set_message_type(input_message[0])
		conn_data.set_filename(input_message[1])
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		handle_request(conn_data)
	elif (input_message[0] == "quit"):
		conn_data = Connection(peer_port_num)
		conn_data.set_message_type(input_message[0])
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		peer_leave(conn_data)
	else:
		print ('')
		print ("A ping request was received from Peer %s" % input_message)
	tcp_server.setblocking(0)

while True:
	try: 
		thread.start_new_thread(pinging, (tcp_server,peer_port_num,bind_ip,))
		request_thread = threading.Thread(target=request_listen, args=())
		request_thread.start()
		# thread.start_new_thread(request_listen,())
	except:
		continue
