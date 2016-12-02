#node1.py
#Author: Ivan Iakimenko

import socket, ssl, pprint, urllib, urllib2, pika
from Crypto.Cipher import AES

class node1(object):

	def __init__(self):
		pass

	def sendPayload(self, payload):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssl_sock = ssl.wrap_socket(s, ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
		ssl_sock.connect(('localhost', 10028))
		ssl_sock.write(payload)
		print('Node1 sent payload to Node2')
	
	def getPayload(self):	
		title='Blade Runner'
		url = 'http://omdbapi.com/?'
		param = {'t':title,'y':'','plot':'short','r':'json'}
		value = urllib.urlencode(param)
		response = urllib2.urlopen(url+value)
		payload = response.read()

		print ('Node1 recieved payload from OMDB')
		self.sendPayload(payload)
	

	#This is where we listen for the return message from node 4
	def listenForPayload(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
		channel = connection.channel()

		channel.queue_declare(queue='node4Message')

		#The message is parsed and decrypted
		def callback(ch, method, properties, body):
			aesObj  = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
			message = aesObj.decrypt(body)
			print 'Node1 recieved payload from Node4'
			print("Node1 received %r" % message)

		channel.basic_consume(callback,queue='node4Message',no_ack=True)
		print 'Node1 listening'
		channel.start_consuming()
