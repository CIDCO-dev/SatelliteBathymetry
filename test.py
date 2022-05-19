"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from Sentinel2 import Sentinel2
from hashlib import md5
import requests
import pytest
import sys
import os

# Create the satellite and select a footprint
sat = Sentinel2('samueldubos', '5c6a7b54')
example_footprint = 'POLYGON((' \
                    '-69.9 51.7,' \
                    '-57.2 51.7,' \
                    '-57.2 47.5,' \
                    '-69.9 47.5,' \
                    '-69.9 51.7))'

# Set the required dates
example_date = 'NOW-6DAYS'
example_date_1 = 'NOW-5DAYS'
example_date_2 = 'NOW-8DAYS'

# Make use of the search method
search = sat.search(example_date, 'NOW', example_footprint)
search_1 = sat.search(example_date_1, 'NOW', example_footprint)
search_2 = sat.search(example_date_2, 'NOW', example_footprint)

# Define a product
product = '72574aaf-85f0-42f3-814a-ef08a079490a'

# Download a product
sat.download(product)      


# Unit tests concerning the Sentinel2 class
class TestGeneral:

    def test_status_code(self):
        date = 'NOW-1DAYS'
        username = sat.username
        password = sat.password
        req = requests.get(f'https://scihub.copernicus.eu/dhus/search?'
                           f'q=(beginPosition:[{date}%20TO%20NOW])',
                           auth=(username, password))
        assert req.status_code == 200


# Unit tests concerning the search() method
class TestSearchMethod:

    @pytest.mark.parametrize("begin_date, end_date", [('2022-05-09T00:00:00.000Z', '2022-05-10T00:00:00.000Z')])
    def test_unit_request_handled(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)

    def test_is_list_of_strings(self):
        for el in search:
            assert isinstance(el, str)

    def test_are_lengths_coherent(self):
        assert len(search_2) >= len(search_1)

    @pytest.mark.parametrize("begin_date, end_date", [('2022-05-15T00:00:00.000Z', '2022-05-17T00:00:00.000Z')])
    def test_answer_uncluded(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date
        assert product in sat.search(self.begin_date, self.end_date, example_footprint)


# Unit tests concerning the download() method
class TestDownloadMethod:

    def test_file_exists(self):
        path = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
        assert os.path.exists(f"{path}/{product}.zip")

    def test_identical_binaries(self):
        username = sat.username
        password = sat.password
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
