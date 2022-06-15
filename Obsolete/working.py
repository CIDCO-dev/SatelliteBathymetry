import requests as rq
import sys
import time


def get_id(date_, footprint_, start_=0, rows_=10, k_=0):

    req = rq.get(f'{service_root_uri}'
                 f'/search?'
                 f'format=json'
                 f'&start={start_}&rows={rows_}'
                 f'&q=(footprint:%22Intersects({footprint_})%22)'
                 f'%20AND%20(beginPosition:[{date_}%20TO%20NOW])'
                 f'%20AND%20(platformname:Sentinel-2'
                 f'%20AND%20filename:S2A_*)',
                 auth=('samueldubos', '5c6a7b54'))

    if req.status_code == 200:
        json_data = req.json()
        # print(json_data['feed'])
        # print(json_data['feed']['entry'][0]['id'])
        for i, answer in enumerate(json_data['feed']['entry']):
            print(f"Id n°{(i+1)+rows_*k_}: {answer['id']}")
    else:
        sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

    return 0


def get_all_id(date_, footprint_, step_, iter_):
    # times_list = []
    for i in range(iter_):
        deb_ = time.time()
        print(f"\nIteration n°{i+1}")
        get_id(date_, footprint_, i * step_, step_, i)
        fin_ = time.time()
        print(f"Answer time: {fin_-deb_}.")
        # times_list.append([fin_-deb_])
    # plt.figure(f"Answer time evolution of {pas_}-long steps")
    # plt.plot(times_list)
    # plt.xlabel("Iteration")
    # plt.ylabel("Answer time")
    return 0


def download_id(id_):

    req = rq.get(f"{service_root_uri}"
                 f"/odata/v1/Products({id_})"
                 f"/$value",
                 auth=('samueldubos', '5c6a7b54'))
    if req.status_code == 200:
        return req
    else:
        sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

    return 0


if __name__ == "__main__":

    # Variables definitions
    service_root_uri = 'https://scihub.copernicus.eu/dhus'

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
    demo_get_all_id = True

    # Request
    deb = time.time()

    if demo_get2_id:
        print(f'\n\n### Demonstration with two id. ###')
        get_id(date, footprint, start_=0, rows_=2, k_=0)

    if demo_get10_id:
        print(f'\n\n### Demonstration with ten id: both ways. ###')
        get_id(date, footprint, start_=0, rows_=5, k_=0)
        get_id(date, footprint, start_=5, rows_=5, k_=1)
        print('')
        get_id(date, footprint, start_=0, rows_=10, k_=0)

    if demo_get_all_id:
        print(f'\n\n### Demonstration with a lot of id. ###')
        get_all_id(date, footprint, 15, 3)

    fin = time.time()
    print(f"\nTotal time:{fin - deb}.")

    # rq.get("https://scihub.copernicus.eu/dhus/odata/v1/Products('7bc9745c-a32a-4334-95a5-add664bba06e')/$value", auth=('samueldubos', '5c6a7b54'))
    # print('Finished.')
