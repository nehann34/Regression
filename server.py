import socket
import threading

def rec_whole_size(sock, size):
	r = 0
	array = bytes()

	while r < size:
		array = array + sock.recv(size - r)
		r = len(array)
	return array

def rec_from_client(client_sock):
	#while True:
		message_size = rec_whole_size(client_sock, 7)
		int_message_size = int(message_size.decode('utf-8'))
		message = rec_whole_size(client_sock, int_message_size)
		msg=message.decode('utf-8')
		l=[]
		l=msg.split(' ')
		m=l[1]
		m_d=m.encode('utf-8')
		uname=l[0]
		fp = open(uname,'wb')
		fp.write(m_d)
		fp.close()
		print("file recieved")

print("Server socket")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.43.50', 4061))
print("socket for accepting the connection",serversocket)
serversocket.listen(10)
while True:
	sock, add = serversocket.accept()
	
	tr = threading.Thread(target = rec_from_client, name = "receiving thread", args = [sock], daemon = True)
	tr.start()
	
