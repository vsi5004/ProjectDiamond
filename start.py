#start.py
#Author: Ivan Iakimenko

from node1 import node1
from node2 import node2
from node3 import node3
from node4 import node4
import threading
import time


exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, node):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.node = node
    def run(self):
        print "Starting " + self.name
        start_nodes(self.name, self.node)
        print "Exiting " + self.name

def start_nodes(threadName, node):
	node.listenForPayload()
        if exitFlag:
		threadName.exit()

Node1 = node1()
Node2 = node2()
Node3 = node3()
Node4 = node4()

# Create new threads
thread1 = myThread(1, "Thread-1", Node1)
thread2 = myThread(2, "Thread-2", Node2)
thread3 = myThread(3, "Thread-3", Node3)
thread4 = myThread(4, "Thread-4", Node4)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
thread4.start()

Node1.getPayload()
