import time
import socket 
import threading
import pickle

bind_ip = "127.0.0.1"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)
print('Listening...')

peer_list = {}

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
>>>>>>> 6337d4d0322f132ebc1b18cd476c943f21aca0b3
