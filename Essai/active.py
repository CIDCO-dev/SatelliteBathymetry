from Sentinel2 import Sentinel2, get_xml, get_percentage
from sentinelsat import read_geojson, geojson_to_wkt
from geojson_algos import polygon_to_string
import time


# geojson_file = read_geojson('THISONE.geojson')
# multipolygon = geojson_file['features'][0]['geometry']['coordinates'][0]
# polygon = multipolygon[0]
# footprint = polygon_to_string(polygon)
# footprint = 'POLYGON((' \
#                       '-69.9 51.7,' \
#                       '-57.2 51.7,' \
#                       '-57.2 47.5,' \
#                       '-69.9 47.5,' \
#                       '-69.9 51.7))'

def handle_products(a, b):

    PoI = []
    print(">>> Acquisition of the products.\n>>>\n>>>\n>>>\n>>>")
    product_list = sat.search(date1, date2, '6polygons_bay.geojson')
    print(f">>> {len(product_list)} products acquired.\n>>>\n>>>\n>>>\n>>>")
    print(f">>> Downloading {b - a} products.\n>>>\n>>>\n>>>\n>>>")
    for i, product in enumerate(product_list[a:b]):
        deb = time.time()
        sat.download(product)
        xml = get_xml(product)
        fin = time.time()
        print(f">>>\n>>> Product n°{i+1}: {product} downloaded in {round(fin - deb, 2)} seconds.")
        percentage_product(product)
        if get_percentage(xml, 'nodata') <= 0.1 and get_percentage(xml, 'water') >= 0.5:
            PoI.append(product)
    print(">>>\n>>>\n>>>\n>>>\n>>> End.\n>>>\n>>>")
    
    return PoI


def percentage_product(id):

    xml = get_xml(id, handle=False)
    for attribute in ['cloud', 'nodata', 'dark', 'vegetation', 'water']:
        percentage = get_percentage(xml, attribute)
        print(f'>>> {round(percentage, 1)}% of the image contains {attribute}.')


if __name__ == '__main__':

    sat = Sentinel2('samueldubos', '5c6a7b54')
    date1 = 'NOW-3DAYS'
    date2 = 'NOW'

    product_list = sat.search(date1, date2, '6polygons_bay.geojson')
    k = 0
    for product in product_list:
        if product_list.count(product) > 1:
            print(f'DUPLICATES: {product_list.count(product)}')
            k += 1
        print(product)
    print(f'{len(product_list) - k} unique products.')

    # results = handle_products(0, 5)
    # for result in results:
    #     print(result)






