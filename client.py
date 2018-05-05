import socket

def length_to_seven(size):
	size='0'*(7-len(size))+ size
	return size

print("Hi,I'm client")
username= input("Username:")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket created")
print("connecting to server.....")
s.connect(('192.168.43.50',4061))
print("Now you are connected to server,Start the communication.")

#while True:

msg1=input()
msg2=input()
file_to_send = open(msg1, 'rb')
l= file_to_send.read()
ap= username.encode('utf-8')+ ' '.encode('utf-8') + l + ' '.encode('utf-8') + msg2.encode("utf-8")
size = length_to_seven(str(len(ap))).encode('utf-8')
message=size+ap
s.sendall(message)
s.close()

