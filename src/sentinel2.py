import requests
import sys

username="glabmoris"
password="SuperSatellite42$"
platformName="Sentinel-2"

params = {
		'q':'platformname : {} AND beginposition : [NOW-1DAY TO NOW] AND footprint:Intersects()'.format(platformName)
	}

r = requests.get("https://apihub.copernicus.eu/apihub/search",params,auth=(username, password))

if r.status_code == 200:
	print("doing")
else:
	sys.stderr.write("Error while fetching Sentinel 2 data: code {}\n".format(r.status_code))
