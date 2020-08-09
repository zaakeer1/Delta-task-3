import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.2"
PORT = 1235

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

sockets_list = [server_socket]
clients = {}
clientsarmy = {}
clientsnavy = {}
clientsairforce = {}
clientstl = {}        


def recieve_message(client_socket):
	try:
		message_header = client_socket.recv(HEADER_LENGTH)
		
		if not len(message_header):
			return False
			
		message_length = int(message_header.decode("utf-8").strip())
		return {"header": message_header, "data": client_socket.recv(message_length)}
			
			
	except:
		return False
		
	
global chief_socket	
while True:
	read_sockets, _, exception_sockets = select.select(sockets_list, [],sockets_list)
	
	for notified_socket in read_sockets:
		if notified_socket == server_socket:
			client_socket, client_address = server_socket.accept()
			
			user = recieve_message(client_socket)
			u = user['data'].decode('utf-8')
			i = 1
			f = 0
			if u == 'Army General':
				f = 1
			if u == 'Navy Marshal':
				f = 1
			if u == 'Airforce Chief':
				f = 1
			if u == 'Chief Commander':
				f = 1
			while i <= 50:
				ID = "Army%d"
				ID = ID % i
				if u == ID:
					f = 1
				ID = "Navy%d"
				ID = ID % i
				if u == ID:
					f = 1
				ID = "Airforce%d"
				ID = ID % i
				if u == ID:
					f = 1
				if f == 1:
					break
				i = i+1
			if f == 0:
				print("Invalid user name")
				continue
			if user is False:
				continue
		
			sockets_list.append(client_socket)
			if "Army" in u:
				clientsarmy[client_socket] = user
				if "Army General" in u:
					clientstl[client_socket] = user
			if "Navy" in u:
				clientsnavy[client_socket] = user
				if "Navy Marshal" in u:
					clientstl[client_socket] = user
			if "Airforce" in u:
				clientsairforce[client_socket] = user
				if "Airforce Chief" in u:
					clientstl[client_socket] = user
			if "Chief Commander" in u:
					clientstl[client_socket] = user
					chief_socket = client_socket
			clients[client_socket] = user
			print(f"Accepted new connection from {client_address[1]} username:{user['data'].decode('utf-8')}")
		
		else:
			message = recieve_message(notified_socket)
			ut = clients[notified_socket]['data'].decode('utf-8')
			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				if "Army" in ut:
					del clientsarmy[notified_socket]
					if "Army General" in ut:
						del clientstl[notified_socket]
				if "Navy" in ut:
					del clientsnavy[notified_socket]
					if "Navy Marshal" in ut:
						del clientstl[notified_socket]
				if "Airforce" in ut:
					del clientsairforce[notified_socket]
					if "Airforce Chief" in ut:
						del clientstl[notified_socket]
				if "Chief Commander" in ut:
						del clientstl[notified_socket]
				continue
			user = clients[notified_socket]
			m = message['data'].decode('utf-8')
			em = 'end chat'
			if m == em:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				if "Army" in ut:
					del clientsarmy[notified_socket]
					if "Army General" in ut:
						del clientstl[notified_socket]
				if "Navy" in ut:
					del clientsnavy[notified_socket]
					if "Navy Marshal" in ut:
						del clientstl[notified_socket]
				if "Airforce" in ut:
					del clientsairforce[notified_socket]
					if "Airforce Chief" in ut:
						del clientstl[notified_socket]
				if "Chief Commander" in ut:
						del clientstl[notified_socket]
				continue
			#message distribution starts here
			
			print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
			
			if "Army General" in ut:
				for client_socket in clientstl:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				for client_socket in clientsarmy:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				continue
			if "Army" in ut:
				for client_socket in clientsarmy:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				chief_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				continue
			if "Navy Marshal" in ut:
				for client_socket in clientstl:		
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				for client_socket in clientsnavy:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				continue
			if "Navy" in ut:			
				for client_socket in clientsnavy:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				chief_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				continue
			if "Airforce Chief" in ut:
				for client_socket in clientstl:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				for client_socket in clientsairforce:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

				continue
			if "Airforce" in ut:				
				for client_socket in clientsairforce:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				chief_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				continue
			if "Chief Commander" in ut:
				for client_socket in clientstl:
				
					if client_socket != notified_socket:
						client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
				continue
			
	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]
		if "Army" in ut:
			del clientsarmy[notified_socket]
			if "Army General" in ut:
				del clientstl[notified_socket]
		if "Navy" in ut:
			del clientsnavy[notified_socket]
			if "Navy Marshal" in ut:
				del clientstl[notified_socket]
		if "Airforce" in ut:
			del clientsairforce[notified_socket]
			if "Airforce Chief" in ut:
				del clientstl[notified_socket]
		if "Chief Commander" in ut:
			del clientstl[notified_socket]
			




