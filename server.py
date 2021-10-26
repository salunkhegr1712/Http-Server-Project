import socket

class ServerSocket(object):
	def __init__(self, port = 30000):
		self.PORT = port
		self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.SOCKET.bind(('',self.PORT))
		self.SOCKET.listen(1)
		
class Error(object):
	def __init__(self):
		self.CONTINUE = [100, "Continue"]
		self.SWITCHING_PROTOCOLS = [101, "Switching protocols"]
		
		self.OK = [200, "Ok"]
		self.CREATED = [201, "Created"]
		self.ACCEPTED = [202, "Accepted"]
		self.NON_AUTHORITATIVE_INFORMATION = [203, "Non-authoritive information"]
		self.NO_CONTENT = [204, "No content"]
		self.RESET_CONTENT = [205, "Reset content"]
		self.PARTIAL_CONTENT = [206, "Partial content"]
		
		self.MULTIPLE_CHOICES = [300, "Multiple choice"]
		self.MOVED_PERMANENTLY = [301, "Moved permanent"]
		self.FOUND = [302, "Found"]
		self.SEE_OTHER = [303, "See other"]
		self.NOT_MODIFIED = [304, "Not modified"]
		self.USE_PROXY = [305, "Use proxy"]
		self.TEMPORARY_REDIRECT = [307, "Temporary redirect"]
		
		self.BAD_REQUEST = [400, "Bad request"]
		self.UNAUTHORIZED = [401, "Unathorized"]
		self.PAYMENT_REQUIRED = [402, "Payment required"]
		self.FORBIDDEN = [403, "Forbidden"]
		self.NOT_FOUND = [404, "Not found"]
		self.METHOD_NOT_ALLOWED = [405, "Method not allowed"]
		self.NOT_ACCEPTABLE = [406, "Not acceptable"]
		self.PROXY_AUTHENTICATION_REQUIRED = [407, "Proxy authentication required"]
		self.REQUEST_TIMEOUT = [408, "Request timeout"]
		self.CONFLICT = [409, "Conflict"]
		self.GONE = [410, "Gone"]
		self.LENGTH_REQUIRED = [411, "Length required"]
		self.PRECONDITION_FAILED = [412, "Precondition failed"]
		self.PAYLOAD_TOO_LARGE = [413, "Payload too large"]
		self.URI_TOO_LONG = [414, "URI too long"]
		self.UNSUPPORTED_MEDIA_TYPE = [415, "Unsupported media type"]
		self.RANGE_NOT_SATISFIABLE = [416, "Range not satisfiable"]
		self.EXPECTATION_FIALED = [417, "Expectation failed"]
		
		self.INTERNAL_SERVER_ERROR = [500, "Internal server error"]
		self.NOT_IMPLEMENTED = [501, "Not implemented"]
		self.BAD_GATEWAY = [502, "Bad gateway"]
		self.SERVICE_UNAVAILABLE = [503, "Service unavailable"]
		self.GATEWAY_TIME_OUT = [504, "Gateway timeout"]
		self.HTTP_VERSION_NOT_SUPPORTED = [505, "HTTP version not supported"]
		
	def errorPage(self, err):
		page = "<html>\n"
		page += "<head><title>" + str(err[0]) + " " + str(err[1]) + "</title></head>\n"
		page += "<body bgcolor=\"white\">\n"
		page += "<center><h1>" + str(err[0]) + " " + str(err[1]) + "</h1></center>\n"
		page += "</body>\n"
		page += "</html>"
		return page
		
class Request(object):
	def getHeader(self, request, header):
		header = header + ": "
		i = request.index(header)
		tmp = request[i:]
		j = tmp.index("\n")
		tmp = request[i + len(header):i+j]
		return tmp
		
class Server(ServerSocket, Request, Error):
	def __init__(self):
		ServerSocket.__init__(self)
		Request.__init__(self)
		Error.__init__(self)
		
	def start(self):
		while True:
			connectionSocket, addr = self.SOCKET.accept()
			request = connectionSocket.recv(1024).decode()
			print(self.getHeader(request, "Accept"))
			response = "HTTP/1.1 200 OK\n" +\
			"Content-Length:" + str(len(self.errorPage(self.OK))) + "\n" +\
			"Content-Type: text/html\n" +\
			"\n" + self.errorPage(self.OK)
			connectionSocket.send(response.encode())
			connectionSocket.close()	
		
if __name__ == "__main__":
	server = Server()
	server.start()