#node2.py
#Author: Ivan Iakimenko

import socket, ssl, hashlib, pysftp, time
from dbLog import log

class node2(object):
	
	logger = log()
	run = True

	def __init__(self):
		pass

	def listenForPayload(self):
		bindsocket = socket.socket()
		bindsocket.bind(('', 10028))
		self.logger.addLog('Node2','Node2 listening')
		bindsocket.listen(5)

		run=True

		def do_something(connstream, data):
			self.logger.addLog('Node2','Node2 recieved payload from Node1')
			self.sendPayload(data)
			self.run=False
			return False

		def deal_with_client(connstream):
			data = connstream.read()
			while data:
				if not do_something(connstream, data):
					break
				data = connstream.read()

		while self.run:
			newsocket, fromaddr = bindsocket.accept()
			connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="server.crt", keyfile="server.key")
			try:
				deal_with_client(connstream)
			finally:
				connstream.shutdown(socket.SHUT_RDWR)
				connstream.close()

	def sendPayload(self, data):
		#creates new file with payload
		file = open('IvanIakimenko.json', 'w')
		data = self.calculateChecksum(data)
		file.write(data)
		file.close()
		self.logger.addLog('Node2','Node2 stored payload in file')
		self.sftpPut()

	def calculateChecksum(self, data):
		checksum = hashlib.md5(data.encode()).hexdigest()
		self.logger.addLog('Node2','Node2 calculated checksum')
		return data +'\n'+ checksum

	def sftpPut(self):
		time.sleep(0.2)
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None
		cinfo = {'cnopts':cnopts , 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109 }

		try:
			with pysftp.Connection(**cinfo) as sftp:
				try:
					with sftp.cd('/home/ftpuser'):
						sftp.put('/home/ftpuser/IvanIakimenko.json')
						self.logger.addLog('Node2','Node2 sftp file into Node3 directory')
				except:
					self.logger.addLog('Node2','file issue')
		except:
			self.logger.addLog('Node2','connection issue')
