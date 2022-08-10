import sys, os, subprocess, threading
from collections import deque
sys.path.insert(0,"../src/python")
from sentinel2_imgs_downloader import Sentinel2Downloader


def download_products(products, SentinelDirDeck):
	for product in products:
		#print("product ID: ", product)
		productPath = os.path.join(workingDir, product)
		os.mkdir(productPath)
		#print("path : ", productPath)
		print("downloading product : ", productPath)
		sentinel2.download(product, productPath)
		zipFile = os.path.join(productPath, product)
		print("unzip file : ", zipFile)
		p = subprocess.Popen('unzip {} -d {}'.format(zipFile+".zip", productPath) , shell='True')
		p.wait() # ?? is that necessary
		
		p = subprocess.Popen('rm {}'.format(zipFile+".zip") , shell='True')
		p.wait()
		newDirName = os.path.join(productPath, product)
		p = subprocess.Popen('mv {}/* {}'.format(productPath, newDirName) , shell='True')
		p.wait()
		
		SentinelDirDeck.append(newDirName)
		#break;


#def georeference():

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

print("{} sentinel2 zip file to download".format(len(products)))

SentinelDirDeck = deque([])
pointFileDeck = deque([])

sentinel2DownloaderThread = threading.Thread(target=download_products, args=(products, SentinelDirDeck))

#georeferenceThread = threading.Thread(target=georeference, args=(pointFileDeck))

#processSentinelThread = threading.Thread(target=computeSatBathy, args=(SentinelDirDeck, pointFileDeck))


# starting thread 1
sentinel2DownloaderThread.start()

# wait until thread 1 is completely executed
sentinel2DownloaderThread.join()

# both threads completely executed
print("Done!")
