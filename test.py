from Sentinel2 import Sentinel2
import requests
import pytest
import sys
import os
from hashlib import md5

# Create the satellite and chose a footprint
sat = Sentinel2('samueldubos', '5c6a7b54')
example_footprint = 'POLYGON((' \
                    '-69.87041507596486 51.67827946383208,' \
                    '-57.21416507596486 51.67827946383208,' \
                    '-57.21416507596486 47.52343468727058,' \
                    '-69.87041507596486 47.52343468727058,' \
                    '-69.87041507596486 51.67827946383208))'

# Set the required dates
set_example_date = '2022-05-15T00:00:00.000Z'
example_date = 'NOW-6DAYS'
example_date_1 = 'NOW-5DAYS'
example_date_2 = 'NOW-8DAYS'

# Make use of the search method
search = sat.search(example_date, example_footprint)
set_search = sat.search(set_example_date, example_footprint)
search_1 = sat.search(example_date_1, example_footprint)
search_2 = sat.search(example_date_2, example_footprint)

# Define a product
product = '311b58ad-9ca6-4137-a022-44c3f163d555'

# Download a product
sat.download(product)      


# Unit tests concerning the Sentinel2 class
class TestGeneral:

    def test_status_code(self):
        date = 'NOW-1DAYS'
        username = getattr(sat, 'username')
        password = getattr(sat, 'password')
        req = requests.get(f'https://scihub.copernicus.eu/dhus/search?'
                           f'q=(beginPosition:[{date}%20TO%20NOW])',
                           auth=(username, password))
        assert req.status_code == 200


# Unit tests concerning the search() method
class TestSearchMethod:

    def test_not_none(self):
        assert search is not None

    def test_is_list(self):
        assert isinstance(search, list)

    def test_is_list_of_strings(self):
        for el in search:
            assert isinstance(el, str)

    def test_compare_length(self):
        assert len(search_2) >= len(search_1)

    def test_values(self):
        assert product in set_search


# Unit tests concerning the download() method
class TestDownloadMethod:

    def test_file_exists(self):
        path = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
        assert os.path.exists(f"{path}/{product}.zip")

    def test_identical_binaries(self):
    
        username = getattr(sat, 'username')
        password = getattr(sat, 'password')
        r = requests.get(f"https://scihub.copernicus.eu/dhus"
                         f"/odata/v1/Products('{product}')"
                         f"/$value",
                         auth=(username, password))   
        md5_test = md5()
        md5_test.update(r.content)
        
        md5_product = md5()
        with open(f'{product}.zip', 'rb') as f:
            data = f.read()
            md5_product.update(data)
        

        assert md5_product.hexdigest() == md5_test.hexdigest()


