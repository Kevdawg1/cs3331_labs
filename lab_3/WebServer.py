import socket 
import threading
import codecs

bind_ip = "127.0.0.1"
bind_port = 9997

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print ("[*] Listening on %s:%d" %(bind_ip, bind_port))

def handle_client (client_socket):
	request = client_socket.recv(1024)
	print ("[*] Received: %s" % request)
	request_method = request.split(' ')[0]
	if (request_method == 'GET'):
		file_requested = request.split(' ')[1]
	if ((file_requested == '/') or (file_requested == '/index.html')):
		file_requested = 'index.html'
	# file_requested = 'www' + file_requested
	print ("[*] Serving web page: %s" % file_requested)
	try:
		file_handler = open(file_requested,'rb')
		if (request_method == 'GET'):
			response_content = file_handler.read()
		file_handler.close()
	except Exception as e:
		print("Warning file not found. Serving response code 404")
		if (request_method == 'GET'):
			response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
	server_response = request.encode()
	if (request_method == 'GET'):
		server_response += response_content
	client_socket.send(response_content)
	# f=codecs.open("index.html", 'r')
	# client_socket.sendall(f.read())
	client_socket.close()

while True:
	client, addr = server.accept()
	print ("[*] Accepted connection from %s:%d" % (addr[0],addr[1]))
	client_handler = threading.Thread(target=handle_client, args=(client,))
	client_handler.start()

server.shutdown(socket.SHUT_WR)
server.close()