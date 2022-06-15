from Guillaume import Sentinel2
import requests
import pytest
import sys
import os
import zipfile
import numpy as np
import time
import hashlib as hl

deb = time.time()

name = '311b58ad-9ca6-4137-a022-44c3f163d555'

def compfichiers(nfc1, nfc2, lgbuf=32*1024):
    f1 = f2 = None
    result = False
    try:
        if os.path.getsize(nfc1) == os.path.getsize(nfc2):
            f1 = open(nfc1, "rb")
            f2 = open(nfc2, "rb")
            while True:
                buf1 = f1.read(lgbuf)
                if len(buf1) == 0:
                    result = True
                    break
                buf2 = f2.read(lgbuf)
                if buf1 != buf2:
                    break
            f1.close()
            f2.close()
    except:
        if f1 != None: f1.close()
        if f2 != None: f2.close()
        raise IOError
    return result

#with zipfile.ZipFile(f"{name}.zip", 'r') as zip:
#    zip.printdir()

#print(f"\n\nSize: {os.path.getsize(f'{name}.zip')}")

username = 'samueldubos'
password = '5c6a7b54'
r = requests.get(f"https://scihub.copernicus.eu/dhus"
                f"/odata/v1/Products('{name}')"
               f"/$value",
              auth=(username, password))
m = hl.md5()
m.update(r.content)
print(m.hexdigest())
#f = open(f'{os.path.dirname(os.path.abspath(os.path.realpath(__file__)))}/copy.zip', 'wb')
#f.write(r.content)
#f.close()

#print(f"Same: {compfichiers('311b58ad-9ca6-4137-a022-44c3f163d555.zip', 'copy.zip')}.")


m = hl.md5()
with open(f'{name}.zip', 'rb') as f:
    data = f.read()
    m.update(data)
    print(m.hexdigest())


fin = time.time() 
print(f"Total time: {fin - deb} seconds.")

# hash md5 of the .zip: 499f24e890a64ae209b2c2400dadac09















