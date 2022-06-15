from Sentinel2 import Sentinel2
import time

sat = Sentinel2('samueldubos', '5c6a7b54')
date1 = 'NOW-2DAYS'
date2 = 'NOW'
footprint = 'POLYGON((' \
                      '-69.9 51.7,' \
                      '-57.2 51.7,' \
                      '-57.2 47.5,' \
                      '-69.9 47.5,' \
                      '-69.9 51.7))'

print(">>> Acquisition of the products.\n>>>\n>>>\n>>>\n>>>")                    
product_list = sat.search(date1, date2, footprint)
print(f">>> {len(product_list)} products acquired.\n>>>\n>>>\n>>>\n>>>")
print(">>> Downloading the five first products.\n>>>\n>>>\n>>>\n>>>")   
for i, product in enumerate(product_list[10:15]):
    deb = time.time()
    sat.download(product)
    fin = time.time()
    print(f">>>\n>>> Product n°{i+1}: {product} downloaded in {fin - deb} seconds.")
print(">>>\n>>>\n>>>\n>>>\n>>> End.\n>>>\n>>>")

