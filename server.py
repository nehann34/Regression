import socket
import threading
import numpy as np
import math


#recieve whole size of message sent by client
def rec_whole_size(sock, size):
	r = 0
	array = bytes()
	while r < size:
		array = array + sock.recv(size - r)
		r = len(array)
	return array


def hypothesis_logistic(X,theta):
	z=np.dot(X,theta)
	return (1 / (1 + np.exp(-z)))




def create_matrix_from_dataset(filename,m,n):
	a=np.loadtxt(filename,delimiter=',',dtype=int)
	b=np.ones((m,1),dtype=int)
	matrix=np.hstack((b,a))
	X=np.delete(matrix,n,1)
	y=np.delete(matrix,np.s_[0:n],1)
	theta=np.ones((n,1),dtype=int)
	#print(X,y,theta)	
	return X,y,theta


def hypothesis_linear(X,theta):
	Y=np.dot(X,theta)
	#print(Y)	
	return Y


def cost_linear(Y,y,m):
	t_m= 2*m
	J=(1/t_m)*((np.square(np.subtract(Y,y))).sum())
	#print(J)	
	return J




def cost_regularized_linear(y,Y,m,theta,lambd):
	t_m=2*m
	a=(1/t_m*(np.square(np.subtract(Y,y)))).sum()	
	b=((float(lambd)/t_m)*(np.square(theta))).sum()
	J=a+b
	return J

def gradient_descent_linear(X,y,alpha,theta,m,n):
	p=float(alpha)/m
	for k in range(1,3):	
		Y=hypothesis_linear(X,theta)
		gr=np.matrix(p*(np.dot(np.transpose(Y-y) , X)))
		theta=theta-np.transpose(gr)
		#print(theta)
	return theta		
	
def gradient_descent_linear_regularization(X,y,alpha,lambd,theta,m,n):
	p=float(alpha)/m
	for k in range(1,3):	
		Y=hypothesis_linear(X,theta)	
		gr1=np.matrix(p*(np.dot(np.transpose(Y-y) , X)))
		gr2=float(lambd)*theta
		gr=np.add(np.transpose(gr1), gr2)
		theta=theta-p*gr
	return theta	

def cost_logistic(y,Y,m):
	t=-1/m
	l=np.log(Y)
	b=np.ones((m,1),dtype=int)
	p=np.subtract(b,y)
	q=np.subtract(b,l)
	J=t*((np.multiply(y,l) + np.multiply(p,q)).sum())
	return J

def cost_regularized_logistic(y,Y,m,theta,lambd):
	t=-1/m
	l=np.log(Y)
	b=np.ones((m,1),dtype=int)
	p=np.subtract(b,y)
	q=np.subtract(b,l)
	e=t*((np.multiply(y,l) + np.multiply(p,q)).sum())
	f=(float(lambd)/(2*m))*(np.square(theta).sum())
	J=np.add(e,f)
	return J



def gradient_descent_logistic(X,y,alpha,theta,m,n):
	for k in range(1,3):
		Y=hypothesis_logistic(X,theta)
		gr=np.matrix(float(alpha)*(np.dot(np.transpose(Y-y) , X)))
		theta=theta-np.transpose(gr)
		
	return theta

def gradient_descent_logistic_regularization(X,y,alpha,lambd,theta,m,n):
	#for k in range(1,3):
		Y=hypothesis_logistic(X,theta)
		gr1=np.matrix((1/m)*(np.dot(np.transpose(Y-y) , X)))
		gr2=(float(lambd)/m) * theta
		theta=theta-float(alpha)*(np.add(np.transpose(gr1) ,gr2))
		return theta


#recieve input sent by client
def rec_from_client(client_sock):
	#while True:
		message_size = rec_whole_size(client_sock, 7)
		int_message_size = int(message_size.decode('utf-8'))
		message = rec_whole_size(client_sock, int_message_size)
		msg=message.decode('utf-8')
		l=[]
#list of sent messages username + filedata +regression + alpha and lambda
		l=msg.split(' ')
		m=l[1]
		data=m.encode('utf-8')
		uname=l[0]
		alpha=l[3]
		lambd=l[4]
		type_r=l[2]
		fp = open(uname,'wb')
		fp.write(data)
		fp.close()

		with open(uname,"r") as f:
			m_value=sum(1 for _ in f)
		f=open(uname)
		lines=f.readlines()
		count=lines[0].split(',')
		n_value=len(count)
		print(m_value,n_value)
		print("file recieved")

		#if n_value <= 5 & type_r is 'linear':
		#X,y,theta=create_matrix_from_dataset(uname,m_value,n_value)
		#Y=hypothesis_linear(X,theta)
		#J=cost_linear(Y,y,m_value)
		#theta=gradient_descent_linear(X,y,alpha,theta,m_value,n_value)


		#if n_value <= 5 & type_r is 'logistic':
		#X,y,theta=create_matrix_from_dataset(uname,m_value,n_value)
		#Y=hypothesis_logistic(X,theta)
		#J=cost_logistic(y,Y,m_value)
		#theta=gradient_descent_logistic(X,y,alpha,theta,m_value,n_value)


		#if n_value > 5 & l[1]='linear':
		#X,y,theta=create_matrix_from_dataset(uname,m_value,n_value)
		#Y=hypothesis_linear(X,theta)
		#J=cost_regularized_linear(y,Y,m_value,theta,lambd)		
		#theta=gradient_descent_linear_regularization(X,y,alpha,lambd,theta,m_value,n_value)
                


		#if n_value > 5 & l[1]='logistic':	
		X,y,theta=create_matrix_from_dataset(uname,m_value,n_value)
		Y=hypothesis_logistic(X,theta)
		J=cost_regularized_logistic(y,Y,m_value,theta,lambd)
		theta=gradient_descent_logistic_regularization(X,y,alpha,lambd,theta,m_value,n_value)







print("Server socket")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.43.50', 8323))
print("socket for accepting the connection",serversocket)
serversocket.listen(10)
while True:
	sock, add = serversocket.accept()
	
	tr = threading.Thread(target = rec_from_client, name = "receiving thread", args = [sock], daemon = True)
	tr.start()
	
