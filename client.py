import socket
import select
import errno
import sys

HEADER_LENGTH = 10
PORT = 1235
IP = "127.0.0.2"

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
	
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

i = 1
f = 0
if my_username == 'Army General':
	f = 1
if my_username == 'Navy Marshal':
	f = 1
if my_username == 'Airforce Chief':
	f = 1
if my_username == 'Chief Commander':
	f = 1
while i <= 50:
	ID = "Army%d"
	ID = ID % i
	if my_username == ID:
		f = 1
	ID = "Navy%d"
	ID = ID % i
	if my_username == ID:
		f = 1
	ID = "Airforce%d"
	ID = ID % i
	if my_username == ID:
		f = 1
	if f == 1:
		break
	i += 1
if f == 0:
	print("Invalid user name")
	sys.exit()
print("'end chat' to quit")

		

while True:
	message = input(f"{my_username} > ")
	
	if message: 
		message = message.encode("utf-8")
		message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
		client_socket.send(message_header + message)
		em = 'end chat'
		if message.decode("utf-8") == em:
			sys.exit()
	try:
		while True:
 			
			username_header = client_socket.recv(HEADER_LENGTH)
			if not len(username_header):
				print("connection closed by the server")
				sys.exit()

			username_length = int(username_header.decode("utf-8").strip())
			username = client_socket.recv(username_length).decode("utf-8")
			
			message_header = client_socket.recv(HEADER_LENGTH)
			message_length = int(message_header.decode("utf-8").strip())
			message = client_socket.recv(message_length).decode("utf-8")
			print(f"{username} > {message}")
	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error',	str(e))
			sys.exit()
		continue
	
	except Exception as e:
		print('General error', str(e))
		sys.exit()
