"""

Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

@Samuel_Dubos

"""

import requests as rq
import sys
import time


def get_id(date_, footprint_, start_=0, rows_=10, k_=0):

    req = rq.get(f'https://scihub.copernicus.eu/dhus'
                 f'/search?'
                 f'format=json'
                 f'&start={start_}&rows={rows_}'
                 f'&q=(footprint:%22Intersects({footprint_})%22)'
                 f'%20AND%20(beginPosition:[{date_}%20TO%20NOW])'
                 f'%20AND%20(platformname:Sentinel-2'
                 f'%20AND%20filename:S2A_*'
                 f'%20AND%20producttype:S2MSI2A)',
                 auth=(str(username), str(password)))

    if req.status_code == 200:
        json_data = req.json()
        for i, answer in enumerate(json_data['feed']['entry']):
            print(f"Id n°{(i+1)+rows_*k_}: {answer['id']}")
    else:
        json_data = rows_
        sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

    return rows_ - len(json_data['feed']['entry'])


def get_all_id(date_, footprint_, step_, iter_):

    for i in range(iter_):
        deb_ = time.time()
        print(f"\nIteration n°{i+1}")
        get_id(date_, footprint_, i * step_, step_, i)
        fin_ = time.time()
        print(f"Answer time: {fin_-deb_}.")

    return 0


def download_id(id_):

    req = rq.get(f"https://scihub.copernicus.eu/dhus"
                 f"/odata/v1/Products('{id_}')"
                 f"/$value",
                 auth=(str(username), str(password)))
    if req.status_code == 200:
        f = open(f'{id_}.zip', 'wb')
        f.write(req.content)
        f.close()
    else:
        sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

    return 0


if __name__ == "__main__":

    # Parameters definition
    date = '2022-05-15T12:30:00.000Z'
    footprint = 'POLYGON((' \
                '-69.87041507596486 51.67827946383208,' \
                '-57.21416507596486 51.67827946383208,' \
                '-57.21416507596486 47.52343468727058,' \
                '-69.87041507596486 47.52343468727058,' \
                '-69.87041507596486 51.67827946383208))'

    # Settings
    demo_get2_id = True
    demo_get10_id = False
    demo_get_all_id = False
    demo_download = False

    # Author
    print(f'\n\n### Identification ###')
    username = input("What is your username? ")
    password = input("What is your password? ")

    # Requests
    deb = time.time()

    if demo_get2_id:
        print(f'\n\n### Demonstration with two id ###')
        get_id(date, footprint, start_=0, rows_=2, k_=0)

    if demo_get10_id:
        print(f'\n\n### Demonstration with ten id: both ways ###')
        get_id(date, footprint, start_=0, rows_=5, k_=0)
        get_id(date, footprint, start_=5, rows_=5, k_=1)
        print('')
        get_id(date, footprint, start_=0, rows_=10, k_=0)

    if demo_get_all_id:
        print(f'\n\n### Demonstration with a lot of id ###')
        get_all_id(date, footprint, 15, 3)

    if demo_download:
        print(f'\n\n### Demonstration of a download ###')
        download_id('eac56cab-6272-4532-8e3c-4372c30a5144')

    fin = time.time()
    print(f"\nTotal time: {fin - deb}.")
