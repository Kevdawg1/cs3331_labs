import time
import socket 
import thread
import threading
import pickle
import sys

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
peer_id = sys.argv[1]
peer_successor_first = int(sys.argv[2])
peer_successor_first_port = peer_successor_first + 50000
peer_successor_second = int(sys.argv[3]) 
peer_successor_second_port = peer_successor_second + 50000
# print (peer_id)
peer_port_num = 50000 + int(peer_id)
bind_ip = '127.0.0.1'

udp_server.bind((bind_ip,peer_port_num))
# tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# tcp_server.bind((bind_ip,peer_port_num))
# tcp_server.listen(10)
# conn,addr = tcp_server.accept()
# data = conn.recv(1024)
# udp_server.listen(1)
# udp_server.sendto(peer_id, (bind_ip,peer_successor_first))
print("Listening...")

def request_file(conn_data):
	filename = conn_data.filename
	hashed = int(filename) % 256							# filename is hashed to find peer id responsible

	origin_port = int(conn_data.origin_port)					# recovers the port first requested from
	#if (peer_port_num != origin_port):
	#	print("entered")
	#  response_sock.connect((bind_ip, origin_port))		# connects to peer from origin port
	if (hashed == peer_successor_second):
		# it is stored in second successor
		message = pickle.dumps(conn_data)
		udp_server.sendto(message,(bind_ip,peer_successor_second_port))
	if (hashed <= peer_successor_first or hashed <= peer_id):
		if (hashed <= peer_id and origin_port != peer_port_num):
			response_message = "File %s is here." % filename
			print(response_message)
			response_message = "A response message, destined for peer %s, has been sent" % filename
			print(response_message)
			response_message = filename + "," + peer_id
			print(origin_port)
			response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			response_sock.connect((bind_ip, origin_port))
			response_sock.send(response_message)
			conn_data = response_sock.recv(1024)
			response_sock.close()
			# it is stored in this peer
		elif (hashed == peer_successor_first):
			message = pickle.dumps(conn_data)
			udp_server.sendto(message,(bind_ip,peer_successor_first_port))
			# it is stored in the next peer
	
	else:
		response_message = "File %s is not stored here." % filename
		print(response_message)
		response_message = "File request message for %s has been sent to my successor." % filename
		print(response_message)
		message = pickle.dumps(conn_data)
		udp_server.sendto(message,(bind_ip,peer_successor_second_port))
		# it is not stored in any known id's yet

def handle_request(conn_data):
	tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	request_file(conn_data)
	print('Now hosting TCP server....')
	print('Listening for peer response....')
	tcp_server.bind((bind_ip,peer_port_num))
	tcp_server.listen(10)
	conn,addr = tcp_server.accept()
	data = conn.recv(1024)
	filename, peer = data.split(",")
	print("Received a response message from peer %s, which has the file %s." % (peer,filename))
	conn.close()

def pinging(udp_server):
	data, addr = udp_server.recvfrom(1024)
	conn_data = pickle.loads(data)
	if (conn_data.message_type == "request"):
		request_file(conn_data)
	elif (conn_data.message_type == "connection"):
		respondConnection(conn_data)
	elif(conn_data.message_type == "quit"):
		peer_leave(conn_data)
	else: 
		print ("A ping request was received from Peer %s" % data)

def respondConnection(conn_data):
	resp_data = Connection(peer_port_num)
	resp_data.set_message_type("connection-ack")
	response_message = pickle.dumps(resp_data)
	response_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	response_sock.connect((bind_ip, origin_port))
	response_sock.send(response_message)

def peer_leave(conn_data):
	global peer_successor_first
	global peer_successor_first_port
	global peer_successor_second
	global peer_successor_second_port
	if (conn_data.origin_port == peer_port_num):
		quit_message = pickle.dumps(conn_data)
		udp_server.sendto(quit_message,(bind_ip,peer_successor_first_port))
	else:
		if (peer_successor_first_port == conn_data.origin_port):
			peer_successor_first = conn_data.quit_first_successor
			peer_successor_first_port = peer_successor_first + 50000
			peer_successor_second = conn_data.quit_second_successor
			peer_successor_second_port = peer_successor_second + 50000
			# print("new first successor: ",peer_successor_first)
			# print("new second successor: ",peer_successor_second)
			return
		elif (peer_successor_second_port == conn_data.origin_port):
			peer_successor_second = conn_data.quit_second_successor
			peer_successor_second_port = conn_data.quit_second_successor + 50000
			# print("new second successor: ",peer_successor_second)
		quit_message = pickle.dumps(conn_data)
		udp_server.sendto(quit_message,(bind_ip,peer_successor_first_port))

def request_listen():
	i = raw_input("Enter your request:")
	if not i:
		return
	print (i)
	# i = ""
	input_message = i.split(" ")
	if (input_message[0] == "request"):
		conn_data = Connection(peer_port_num)
		conn_data.set_message_type(input_message[0])
		conn_data.set_filename(input_message[1])
		handle_request(conn_data)
	elif (input_message[0] == "quit"):
		conn_data = Connection(peer_port_num)
		conn_data.set_message_type(input_message[0])
		conn_data.set_quit_first_successor(peer_successor_first)
		conn_data.set_quit_second_successor(peer_successor_second)
		peer_leave(conn_data)
	else:
		print ("A ping request was received from Peer %s" % input_message)

while True:
	try: 
		thread.start_new_thread(pinging, (udp_server,))
		request_thread = threading.Thread(target=request_listen, args=())
		request_thread.start()
		# thread.start_new_thread(request_listen,())
	except:
		continue

'''
server.listen(5)
print('Listening...')

peer_list = []

def create_peer_list(dictionary_list, hostname, port):
	keys = ['Hostname', 'Port Number']

	entry = [hostname, str(port)]
	dictionary_list.insert(0, dict(zip(keys, entry)))
	return dictionary_list, keys

def create_rfc_list(dictionary_list, dict_list_of_rfcs, hostname):
	keys = ['RFC Number', 'RFC Title', 'Hostname']

	for rfc in dict_list_of_rfcs:
		rfc_number = rfc['RFC Number']
		rfc_title = rfc['RFC Title']
		entry = [str(rfc_number), rfc_title, hostname]
		dictionary_list.insert(0, dict(zip(keys, entry)))

	return dictionary_list, keys

def create_combined_list(dictionary_list, dict_list_of_rfcs, hostname, port):
	keys = ['RFC Number', 'RFC Title', 'Hostname', 'Port Number']
	for rfc in dict_list_of_rfcs:
		rfc_number = rfc['RFC Number']
		rfc_title = rfc['RFC Title']
		entry = [str(rfc_number), rfc_title, hostname, str(port)]
		dictionary_list.insert(0, dict(zip(keys, entry)))
	return dictionary_list, keys

def handle_client(client_socket,addr):
	client_socket.send(bytes('Thank you for connecting', 'utf-8'))
	print('Got connection from ', addr)
	data = pickle.loads(conn.recv(1024))  # receive the[upload_port_num, rfcs_num, rfcs_title]
	my_port = data[0]
	my_port = data[0]
	# Generate the peer list and RFC list
	peer_list, peer_keys = create_peer_list(peer_list, addr[0], data[0])  # change addr[1] to data[0]
	RFC_list, rfc_keys = create_rfc_list(RFC_list, data[1], addr[0])
	combined_list, combined_keys = create_combined_list(combined_list, data[1], addr[0], data[0])

	while True:
		data = pickle.loads(conn.recv(1024))  # receive the[upload_port_num, rfcs_num, rfcs_title]
		if data == "EXIT":
			break
		if type(data) == str:
			p2s_list_response(conn)
			new_data = pickle.dumps(return_dict())
			conn.send(new_data)
		else:
			if data[0][0] == "A":
				 p2s_add_response(conn, data[1], data[4], addr[0], data[3])  # Put server response message here
				 RFC_list = append_to_rfc_list(RFC_list, data[1], data[4], addr[0])
				 combined_list = append_to_combined_list(combined_list, data[1], data[4], addr[0], my_port)
				 print_dictionary(RFC_list, rfc_keys)
			if data[2] == "0":
				new_data = pickle.dumps(p2s_lookup_response(data[1]))
				conn.send(new_data)
			elif data[2] == "1":
				print(p2s_lookup_response2(data[1]))
				new_data = pickle.dumps(p2s_lookup_response2(data[1]))
				conn.send(new_data)
	# Remove the client's info from the dictionaries
	peer_list = delete_peers_dictionary(peer_list, addr[0])
	RFC_list = delete_rfcs_dictionary(RFC_list, addr[0])
	combined_list = delete_combined_dictionary(combined_list, addr[0])
	#print_dictionary(peer_list, peer_keys)
	#print_dictionary(RFC_list, rfc_keys)
	#print_dictionary(combined_list, combined_keys)
	conn.close()

while True:
	global users
	client, addr = server.accept()
	print ("[*] Accepted connection from %s:%d" % (addr[0],addr[1]))
	if (len(users) < 10):
		client_handler = threading.Thread(target=handle_client, args=(client,addr))
		client_handler.start()
'''
