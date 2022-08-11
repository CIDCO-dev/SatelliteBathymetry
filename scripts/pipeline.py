import sys, os, subprocess, threading
from queue import Queue
sys.path.insert(0,"../src/python")
from sentinel2_imgs_downloader import Sentinel2Downloader

# Producer Thread Class
class Download_product(threading.Thread):
	def run(self):

		global mutex, empty, full, sentinelDirDeck, products
		
		index = 0
		
		while index < len(products)-1:
			empty.acquire()
			mutex.acquire()
			product = products[index]
			#print("product ID: ", product)
			productPath = os.path.join(workingDir, product)
			os.mkdir(productPath)
			#print("path : ", productPath)
			print("downloading product : ", productPath)
			"""
			sentinel2.download(product, productPath)
			zipFile = os.path.join(productPath, product)
			print("unzip file : ", zipFile)
			p = subprocess.Popen('unzip {} -d {}'.format(zipFile+".zip", productPath), shell='True', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
			p.wait() # ?? is that necessary
			p = subprocess.Popen('rm {}'.format(zipFile+".zip") , shell='True')
			p.wait()
			newDirName = os.path.join(productPath, product)
			p = subprocess.Popen('mv {}/* {}'.format(productPath, newDirName) , shell='True')
			p.wait()
			"""
			newDirName = productPath
			sentinelDirDeck.put(newDirName)
			print("Producer produced : ", newDirName)
			index+=1
			mutex.release()
			full.release()

 
# Consumer Thread Class
class georeferenceThread(threading.Thread):
	def run(self):

		global mutex, empty, full, sentinelDirDeck, nbProduct
		items_consumed = 0

		while items_consumed < nbProduct:
			full.acquire()
			mutex.acquire()

			item = sentinelDirDeck.get()
			print("georeferencing : ", item)

			mutex.release()
			empty.release()

			items_consumed += 1


#def georeference():
	# ici on va utiliser la class/fonction que Samuel a ecrit pour trouver les fichiers voulu et les parser avec MBES georeference
	# etape 1 trouver des surfaces avec une profondeur de 3 a 20m
	# etape 2 mettre tout les points (qui peuvent etre calculer dans un image X) dans un seul fichier


#def computeSatBathy:
	# ici on va processer les images via ./../build/depth workingDir/product/product/GRANULE/L2A.../IMG_DATA/


if len(sys.argv) != 4:
        sys.stderr.write("Usage: pyhon3 script.py username password workingDir  \n")
        sys.exit(1)
        
username = sys.argv[1]
password = sys.argv[2]
workingDir = sys.argv[3]

if not os.path.exists(workingDir):
	os.mkdir(workingDir)

sentinel2 = Sentinel2Downloader(username, password)

#TODO add set method for bounding box in sentinel2_imgs_downloader.py -> Sentinel2Downloader
Longitude1, Latitude1 = -70, 45
Longitude2, Latitude2 = -60, 52

#TODO make it a param
date1, date2 = '2022-07-25T18:30:00.000Z', '2022-07-26T18:30:00.000Z'

footprint = f'POLYGON(({Longitude1} {Latitude1},' \
                f' {Longitude2} {Latitude1},' \
                f' {Longitude2} {Latitude2},' \
                f' {Longitude1} {Latitude2},' \
                f' {Longitude1} {Latitude1}))'

products = sentinel2.search(date1, date2, footprint)
nbProduct = len(products)
print("{} sentinel2 zip file to download".format(nbProduct))

# Shared Memory variables
sentinelDirDeck =  Queue()
pointFileDeck = Queue()

# Declaring Semaphores
mutex = threading.Semaphore()
empty = threading.Semaphore(nbProduct)
full = threading.Semaphore(0)


# Creating Threads
producer = Download_product()
consumer = georeferenceThread()
 
# Starting Threads
consumer.start()
producer.start()
 
# Waiting for threads to complete
producer.join()
consumer.join()






"""
#sentinel2DownloaderThread = threading.Thread(target=download_products, args=(products, SentinelDirDeck))

#georeferenceThread = threading.Thread(target=georeference, args=(pointFileDeck))

#processSentinelThread = threading.Thread(target=computeSatBathy, args=(SentinelDirDeck, pointFileDeck))


# starting thread 1
sentinel2DownloaderThread.start()

# wait until thread 1 is completely executed
sentinel2DownloaderThread.join()

"""
