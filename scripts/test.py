import threading
import time
from queue import Queue
 
# Shared Memory variables
q = Queue()
 
# Declaring Semaphores
mutex = threading.Semaphore()
empty = threading.Semaphore(20)
full = threading.Semaphore(0)
 
# Producer Thread Class
class Producer(threading.Thread):
	def run(self):

		global mutex, empty, full, q

		items_produced = 0
		counter = 0

		while items_produced < 20:
			empty.acquire()
			mutex.acquire()

			counter += 1
			q.put(counter)
			print("Producer produced : ", counter)

			mutex.release()
			full.release()

			time.sleep(1)

			items_produced += 1
 
# Consumer Thread Class
class Consumer(threading.Thread):
	def run(self):

		global mutex, empty, full, q
		items_consumed = 0

		while items_consumed < 20:
			full.acquire()
			mutex.acquire()

			item = q.get()
			print("Consumer consumed item : ", item)

			mutex.release()
			empty.release()      

			time.sleep(5)

			items_consumed += 1
 
# Creating Threads
producer = Producer()
consumer = Consumer()
 
# Starting Threads
consumer.start()
producer.start()
 
# Waiting for threads to complete
producer.join()
consumer.join()

