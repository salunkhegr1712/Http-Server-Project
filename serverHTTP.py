import socket
import os
import mimetypes
import logging
import threading
import time
from datetime import datetime

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
		
		self.MULTIPLE_CHOICES = [300, "Multiple choices"]
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
		
class Request(Error):
	def __init__(self):
		Error.__init__(self)

	def getMethod(self, request):
		i = request.index(" ")
		return request[:i]

	def getHeader(self, request, header):
		header = header + ": "
		try:
			i = request.index(header)
		except:
			return ''
		tmp = request[i:]
		j = tmp.index("\n")
		tmp = request[i + len(header):i+j]
		return tmp

	def getFileName(self, request):
		i = request.index(" ")
		request = request[i + 1:]
		i = request.index(" ")
		return request[:i]

	def getFilePath(self, request):
		file = self.getFileName(request)
		if(file == '/'):
			file = '/index.html'
		path = os.getcwd() + "/file" + file
		return path

	def getFileContent(self, request):
		path = self.getFilePath(request)
		if(not self.check_if_modified_since()):
			return self.errorPage(self.NOT_MODIFIED)
		if(not self.check_if_unmodified_since()):
			return self.errorPage(self.PRECONDITION_FAILED)
		elif(not os.path.isfile(path)):
			return self.errorPage(self.NOT_FOUND)
		else:
			try:
				f = open(path, 'r')
				content = f.read()
			except:
				f = open(path, 'rb')
				content = f.read()
			if(len(content) == 0):
				return self.errorPage(self.NO_CONTENT)
			return content

	def getFileType(self, request):
		file = self.getFileName(request)
		if(file == '/'):
			file = '/index.html'
		return mimetypes.guess_type(file)

	def getMonthByNumber(self, number):
		return self.months[number - 1]

	def getNumberByMonth(self, month):
		return self.months.index(month) + 1

	def check_if_modified_since(self):
		if_modified_since = self.getHeader(self.request, 'If-Modified_Since')
		if(if_modified_since == ''):
			return True
		else:
			if_modified_since = if_modified_since.split(' ')
			if(if_modified_since[8] == ' '):
				if_modified_since[8] = '0'
			day = int(if_modified_since[1])
			month = self.getNumberByMonth(if_modified_since[2])
			year = int(if_modified_since[3])
			timestr = if_modified_since[4]
			timestr = time.split(':')
			hr = int(timestr[0])
			min = int(timestr[1])
			sec = int(timestr[2])
			timestr = datetime(year, month, day, hr, min, sec)
			sec_required = int(time.mktime(timestr.timetuple()))
			sec_file = int(os.path.getmtime(self.getFilePath(self.request)))
			if(sec_required <= sec_file):
				return True
			else:
				return False

	def check_if_unmodified_since(self):
		if_unmodified_since = self.getHeader(self.request, 'If-Unmodified_Since')
		if(if_unmodified_since == ''):
			return True
		else:
			if_unmodified_since = if_unmodified_since.split(' ')
			if(if_unmodified_since[8] == ' '):
				if_unmodified_since[8] = '0'
			day = int(if_unmodified_since[1])
			month = self.getNumberByMonth(if_unmodified_since[2])
			year = int(if_unmodified_since[3])
			timestr = if_unmodified_since[4]
			timestr = time.split(':')
			hr = int(timestr[0])
			min = int(timestr[1])
			sec = int(timestr[2])
			timestr = datetime(year, month, day, hr, min, sec)
			sec_required = int(time.mktime(timestr.timetuple()))
			sec_file = int(os.path.getmtime(self.getFilePath(self.request)))
			if(sec_required > sec_file):
				return True
			else:
				return False


class Response(Request, Error):
	def __init__(self, request):
		Request.__init__(self)
		Error.__init__(self)
		self.response = ''
		self.request = request
		self.method = self.getMethod(request)
		self.path = self.getFilePath(request)
		self.content = self.getFileContent(request)
		self.content_type = self.getFileType(self.request)[0]
		self.time = time.asctime(time.gmtime())
		if(self.time[8] == ' '):
			self.time[8] = '0'
		self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
					   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	def begin_response(self, error):
		self.response = f"HTTP/1.1 {error[0]} {error[1]}\n"

	def setContent_length(self):
		self.response += f"Content-Length:{str(len(self.content))}\n"

	def setContent_type(self):
		self.response += f"Content-Type:{self.content_type}\n"

	def setContent(self):
		self.response += f"\n{str(self.content)}"

	def setDate(self):
		time_array = self.time.split(' ')
		day = time_array[0]
		month = time_array[1]
		date = time_array[2]
		time = time_array[3]
		year = time_array[4]
		self.response += f"Date:{day}, {date} {month} {year} {time} GMT\n"

	def setLast_modified(self):
		time_array = time.asctime(time.gmtime(os.path.getmtime(self.path))).split()
		day = time_array[0]
		month = time_array[1]
		date = time_array[2]
		timestr = time_array[3]
		year = time_array[4]
		self.response += f"Last-Modified:{day}, {date} {month} {year} {timestr} GMT\n"

	def setE_tag(self):
		timestr = time.asctime(time.gmtime(os.path.getmtime(self.path)))
		etag = []
		for i in timestr:
			etag.append(chr(ord(i) % 26 + 65))
		etag = ''.join(etag)
		self.response += f"E-tag:{etag}\n"

	def setServer(self):
		self.response += f"Server: Apache/2.4.1 (Unix)\n"

	def getResponse(self):
		accept = self.getHeader(self.request, 'Accept')
		if(self.method in ['GET', 'HEAD'] and 
		   self.content_type in accept and accept != ''):
			self.begin_response(self.OK)
			self.setContent_length()
			self.setContent_type()
			self.setDate()
			self.setLast_modified()
			self.setE_tag()
			self.setServer()
			if(self.method == 'GET'):
				self.setContent()
		elif(self.method == 'POST'):
			data = self.request[self.request.rindex('\n') + 1:]
			data = data.split('&')
			for d in data:
				data[data.index(d)] = d.split('=')
			f = open(os.getcwd() + '/file/form_data.txt', 'w')
			string = ''
			for d in data:
				string += f'{data[data.index(d)][0]}\t\t{data[data.index(d)][1]}\n'		
			f.write(string)
			f.close()
			self.begin_response(self.OK)
			self.setContent_length()
			self.setContent_type()
			self.setDate()
			self.setLast_modified()
			self.setE_tag()
			self.setServer()
			self.setContent()
		elif(self.method == 'DELETE'):
			if(os.path.isfile(self.path)):
				os.remove(self.path)
				self.__init__('GET /deleted.html')
				self.begin_response(self.OK)
				self.setContent_length()
				self.setContent_type()
				self.setDate()
				self.setContent()
			else:
				content = self.errorPage(self.NOT_FOUND)
				self.response = f'HTTP/1.1 404 NOT FOUND\nContent-Length:{len(content)}\n' +\
					content
		elif(self.method == 'PUT'):
			f = open(self.path, 'w')
			content_length = self.getHeader(self.request, 'Content-Length')
			if(content_length == ''):
				content = self.errorPage(self.LENGTH_REQUIRED)
				self.response = f'HTTP/1.1 411 LENGTH REQUIRED\nContent-Length:{len(content)}' +\
					content
			else:
				content = self.request[len(self.request) - content_length:]
				f.write(content)
				f.close()
				content = self.errorPage(self.CREATED)
				self.response = f'HTTP/1.1 201 CREATED\nContent-Length:{len(content)}' +\
					content
		return self.response

		
class Server(ServerSocket, Request, Error):
	def __init__(self):
		ServerSocket.__init__(self)
		Request.__init__(self)
		Error.__init__(self)

	def sendResponse(self, request, connectionSocket):
		res = Response(request)
		response = res.getResponse()
		connectionSocket.send(response.encode())
		connection = self.getHeader(request, 'Connection')
		keep_alive = self.getHeader(request, 'Keep-Alive') 
		if(connection == 'close' or connection == ''):
			connectionSocket.close()
		elif(keep_alive != ''):
			time.sleep(int(keep_alive[keep_alive.index('timeout') + 8]))
			connectionSocket.close()
		
	def start(self):
		addrlist = {}
		while True:
			connectionSocket, addr = self.SOCKET.accept()
			if(addr[0] not in addrlist):
				addrlist[addr[0]] = 0
			else:
				addrlist[addr[0]] += 1
			f = open("cookie.txt", 'w')
			string = ''
			for a in addrlist:
				string += f'{a} : {addrlist[a]}'
			f.write(string)
			f.close()
			request = connectionSocket.recv(1024).decode()
			t = threading.Thread(target=self.sendResponse, args=(request, connectionSocket,))
			t.start()
		
if __name__ == "__main__":
	server = Server()
	server.start()