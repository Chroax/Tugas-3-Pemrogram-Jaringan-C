from datetime import datetime
from socket import *
import socket
import threading
import logging

class ProcessTheClient(threading.Thread):
	def __init__(self,connection,address,server):
		self.connection = connection
		self.address = address
		self.server = server
		threading.Thread.__init__(self)

	def run(self):
		while True:
			data = self.connection.recv(1024).decode('utf-8')
			if data.startswith('TIME') and data.endswith('\r\n'):
				current_time = datetime.now()
				request = current_time.strftime("%H:%M:%S")
				response = f"JAM {request}\r\n"
				self.connection.sendall(response.encode('utf-8'))
				self.server.update_client_count()
			else:
				break
		self.connection.close()

class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.response_count = 0
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0',45000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning(f"connection from {self.client_address}")
			clt = ProcessTheClient(self.connection, self.client_address, self)
			clt.start()
			self.the_clients.append(clt)
            
	def update_client_count(self):
		self.response_count += 1  # Menambahkan jumlah response yang dikirimkan
		logging.warning(f"Total pesan respons: {self.response_count}")
            
    
def main():
	server = Server()
	server.start()

if __name__=="__main__":
	main()