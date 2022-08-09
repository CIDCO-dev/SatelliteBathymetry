import sys, os, subprocess
sys.path.insert(0,"../src/python")
from sentinel2_imgs_downloader import Sentinel2Downloader

if len(sys.argv) != 4:
        sys.stderr.write("Usage: pyhon3 script.py username password workingDir  \n")
        sys.exit(1)
        
username = sys.argv[1]
password = sys.argv[2]
workingDir = sys.argv[3]

if not os.path.exists(workingDir):
	os.mkdir(workingDir)

sentinel2 = Sentinel2Downloader(username, password)
Longitude1, Latitude1 = -70, 45
Longitude2, Latitude2 = -60, 52
date1, date2 = '2022-07-25T18:30:00.000Z', '2022-07-27T18:30:00.000Z'

footprint = f'POLYGON(({Longitude1} {Latitude1},' \
                f' {Longitude2} {Latitude1},' \
                f' {Longitude2} {Latitude2},' \
                f' {Longitude1} {Latitude2},' \
                f' {Longitude1} {Latitude1}))'

products = sentinel2.search(date1, date2, footprint)

print("{} files to download".format(len(products)))

for product in products:
	print("product ID: ", product)
	productPath = os.path.join(workingDir, product)
	os.mkdir(productPath)
	print("path : ", productPath)
	print("downloading product")
	sentinel2.download(product, productPath)
	zipFile = os.path.join(productPath, product)
	print("zip file path : ", zipFile)
	p = subprocess.Popen('unzip {} -d {}'.format(zipFile+".zip", productPath) , shell='True')
	p.wait() # ?? is that necessary
	break;
	


