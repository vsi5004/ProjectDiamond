#node3.py
#Author: Ivan Iakimenko

import hashlib, Pyro4, os.path, time, zlib, sys, pysftp

class node3(object):
	
	run = True

	def __init__(self):
		pass

	def listenForPayload(self):
		print 'Node3 listening'
		cnopts = pysftp.CnOpts()
		cnopts.hostkeys = None
		cinfo = {'cnopts':cnopts, 'host':'oz-ist-linux.abington.psu.edu', 'username':'ftpuser', 'password':'test1234', 'port':109}
		while (self.run):
			try:
				with pysftp.Connection(**cinfo) as sftp:
					if sftp.isfile('/home/ftpuser/IvanIakimenko.json'):
						try:
							file = sftp.open('/home/ftpuser/IvanIakimenko.json','r',-1)
							print 'Node3 oppened sftp file'
							lines = file.readlines()
							payload = lines[0].rstrip('\n')
							if(self.checkChecksum(payload, lines[1])):
								self.sendPayload(payload)
							sftp.remove('/home/ftpuser/IvanIakimenko.json')
							self.run = False
						except:
							print 'Node3 file access error'
			except:
				print 'Node3 sftp connection error'

	def checkChecksum(self, payload, checksum):
		checksumGen = hashlib.md5(payload.encode()).hexdigest()
		if checksum == checksumGen:
			print 'Node3 passed checksum test'
			return True
		else:
			print 'Node3 failed checksum test'
			print checksum + '!=' + checksumGen
			return False

	def compress(self, payload):
		compPayload = zlib.compress(payload.encode('utf-8'),9)
		print'Node3 compressed payload'
		checksum = zlib.crc32(payload)
		compChecksum = zlib.crc32(compPayload)
		print'Node3 checksum:' + str(checksum) +' compressed:' + str(compChecksum)
		return compPayload

	def sendPayload(self, payload):
		#compPayload = self.compress(payload)
		#file = open('compressed_payload.json','wb')
		#file.write(compPayload)
		#file.close()
		remoteNode = Pyro4.Proxy("PYRONAME:node4")    # use name server object lookup uri shortcut
		remoteNode.recievePayload(payload)
		print 'Node3 sent payload to Node4'
