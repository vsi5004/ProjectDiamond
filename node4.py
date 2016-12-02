#node4.py
#Author: Ivan Iakimenko

import pika, Pyro4, zlib, sys
from Crypto.Cipher import AES


class node4(object):

	def __init__(self):
		pass

	#receive message from node3 via pyro
	def listenForPayload(self):
		@Pyro4.expose
		class RemoteNode(object):
			@Pyro4.oneway
			def recievePayload(self, payload):
				print 'Node4 recieved message'
				#self.decompress(payload)
				self.sendPayload(payload)

			#send the encrypted message to node1 via rabbitmq
			def sendPayload(self, payload):
				connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
				channel = connection.channel()
				channel.queue_declare(queue='node4Message')
				print("Node4 sent message to Node1")
				payload = self.encryptAES(payload)
				channel.basic_publish(exchange='',routing_key='node4Message',body=payload)
				connection.close()

			def decompress(self, fileCRC):
				#fileCRC = open(location+'.json','rb')
				payload = zlib.decompress(fileCRC)
				print 'Node4 uncompressed message'
				self.sendPayload(payload)

			#encrypt payload with AES
			def encryptAES(self, payload):
				pad = b' '
				obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
				
				#plaintext = message.encode('utf-8')
				#print(plaintext)
				length = 16 - (len(payload)%16)
				#print(length)
				payload += length*pad

				ciphertext = obj.encrypt(payload)
				print 'Node4 encrypted with AES'
				return ciphertext
	

		daemon = Pyro4.Daemon()                # make a Pyro daemon
		ns = Pyro4.locateNS()
		uri = daemon.register(RemoteNode)   # register the greeting maker as a Pyro object
		ns.register("node4", uri)

		print 'Node4 listening'
		daemon.requestLoop()                   # start the event loop of the server to wait for calls

