from socket import *
serverPort = 30000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
	connectionSocket, addr = serverSocket.accept()
	print('new request received from')
	print(addr)
	print('connectionSocket is')
	print(connectionSocket)
	request = connectionSocket.recv(1024).decode()
	response = 	"HTTP/1.1 200 OK\n" +\
			"Content-Length: 44\n" +\
			"Content-Type: text/html\n" +\
			"\n" +\
			"<html>" +\
			"<body>" +\
			"<h1>Hello, World!</h1>" +\
			"</body>" +\
			"</html>"
	connectionSocket.send(response.encode())
	connectionSocket.close()
