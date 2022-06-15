import requests as rq
import sys
import time
import matplotlib.pyplot as plt


def count_id(date_, footprint_):

    req = rq.get(f'{service_root_uri}/$count?&{data_origin}'
                 f'%20and%20{date_filter}%27{date_}%27',
                 auth=('samueldubos', '5c6a7b54'))

    if req.status_code == 200:
        json_data = req.json()
        return json_data
        # for i, answer in enumerate(json_data['d']['results']):
        #     print(f"Id n°{i+1}: {answer['Id']}")
    else:
        sys.stderr.write(f"Error while fetching file search results: {req.status_code}")


def get_id(date_, footprint_, skip_, top_, k_):

    top = f"$top={top_}"
    skip = '&$skip='+str(skip_)

    req = rq.get(f'{service_root_uri}?{top}&{answer_format}&{data_origin}{skip}'
                 f'&{date_filter}%27{date_}%27{footprint_filter}({footprint_})%22',
                 auth=('samueldubos', '5c6a7b54'))

    if req.status_code == 200:
        json_data = req.json()
        for i, answer in enumerate(json_data['d']['results']):
            print(f"Id n°{(i+1)+10*k_}: {answer['Id']}")
    else:
        sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

    return 0


def get_all_id(date_, footprint_, pas_, iter_):
    times_list = []
    for i in range(iter_):
        deb_ = time.time()
        print(f"\nIteration n°{i+1}")
        get_id(date_, footprint_, i*pas_, pas_, i)
        fin_ = time.time()
        print(f"Answer time: {fin_-deb_}.")
        times_list.append([fin_-deb_])
    # plt.figure(f"Answer time evolution of {pas_}-long steps")
    # plt.plot(times_list)
    # plt.xlabel("Iteration")
    # plt.ylabel("Answer time")
    return 0


if __name__ == "__main__":

    # Variables definitions
    service_root_uri = 'https://scihub.copernicus.eu/dhus/odata/v1/Products'
    answer_format = '$format=json'
    date_filter = 'IngestionDate%20gt%20datetime'
    footprint_filter = '&q=footprint:%22Intersects'
    data_origin = "$filter=startswith(Name,'S2A')"

    # Parameters definition
    date = '2022-05-13T18:40:00.000'
    footprint = 'POLYGON((' \
                '-69.87041507596486 51.67827946383208,' \
                '-57.21416507596486 51.67827946383208,' \
                '-57.21416507596486 47.52343468727058,' \
                '-69.87041507596486 47.52343468727058,' \
                '-69.87041507596486 51.67827946383208))'

    # Request
    step = 10
    deb = time.time()
    n = count_id(date, footprint)
    print(f"There is {n} results.")
    rest = n % step
    get_all_id(date, footprint, step, n//step + 1)
    fin = time.time()
    n_ = count_id(date, footprint)
    print(f"\nn = {n_}, t = {fin-deb}")
