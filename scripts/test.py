import threading
import time
import collections


 
def handleClient1(waitTime, deck):
	for i in range(11):
		deck.append(i)
		time.sleep(waitTime)   

def handleClient2(waitTime, deck):
	if(len(deck) != 0):
		deck.popleft()
		time.sleep(waitTime) 
 
 
if __name__ =="__main__":

	deck = collections.deque([])

	# creating thread
	t1 = threading.Thread(target=handleClient1, args=(10, deck))
	t2 = threading.Thread(target=handleClient2, args=(2, deck))

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()

	# wait until thread 1 is completely executed
	t1.join()
	# wait until thread 2 is completely executed
	t2.join()

	# both threads completely executed
	print("Done!")


