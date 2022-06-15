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


# Set the right footprint
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

# Define a product
product = '72574aaf-85f0-42f3-814a-ef08a079490a'   


class Settings(Sentinel2):

    def create_sat(self, username, password):

        # Create the satellite and select a footprint
        sat = Sentinel2(username, password)

        # Make use of the search method
        search = sat.search(example_date, 'NOW', example_footprint)
        search_1 = sat.search(example_date_1, 'NOW', example_footprint)
        search_2 = sat.search(example_date_2, 'NOW', example_footprint)

        # Download a product
        download = sat.download(product)
        
        yield sat, search, search_1, search_2, download


# Unit tests concerning the Sentinel2 class
class TestGeneral:

    def test_status_code(self, username, password):
        date = 'NOW-1DAYS'
        req = requests.get(f'https://scihub.copernicus.eu/dhus/search?'
                           f'q=(beginPosition:[{date}%20TO%20NOW])',
                           auth=(username, password))
        assert req.status_code == 200

    def test_sat_recognized(self):
        print(sat.username)


# Unit tests concerning the search() method
class TestSearchMethod:

    @pytest.mark.skip
    @pytest.mark.parametrize("begin_date, end_date", [('NOW-0DAYS', 'NOW')])
    def test_null_request_handled(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)
    
    @pytest.mark.skip
    @pytest.mark.parametrize("begin_date, end_date", [('2022-05-09T00:00:00.000Z', '2022-05-10T00:00:00.000Z')])
    def test_unit_request_handled(self, begin_date, end_date, username, password):
        sat = Sentinel2(username, password)
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)
    
    @pytest.mark.skip        
    def test_is_list_of_strings(self, username, password):
        sat = Sentinel2(username, password)
        for el in sat.search(example_date, 'NOW', example_footprint):
            assert isinstance(el, str)
    
    @pytest.mark.skip        
    def test_are_lengths_coherent(self, username, password):
        sat = Sentinel2(username, password)
        search_1 = sat.search(example_date_1, 'NOW', example_footprint)
        search_2 = sat.search(example_date_2, 'NOW', example_footprint)
        assert len(search_2) >= len(search_1)
    
    @pytest.mark.skip
    @pytest.mark.parametrize("begin_date, end_date", [('2022-05-15T00:00:00.000Z', '2022-05-17T00:00:00.000Z')])
    def test_answer_uncluded(self, begin_date, end_date, username, password):
        sat = Sentinel2(username, password)
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)
        assert product in sat.search(self.begin_date, self.end_date, example_footprint)


# Unit tests concerning the download() method
class TestDownloadMethod:
    
    @pytest.mark.skip
    def test_can_create_zip(self, username, password):
        sat = Sentinel2(username, password)
        download = sat.download(product)
     
    @pytest.mark.skip       
    def test_file_exists(self, username, password):
        sat = Sentinel2(username, password)
        download = sat.download(product)
        path = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
        assert os.path.exists(f"{path}/{product}.zip")
    
    @pytest.mark.skip    
    def test_identical_binaries(self, username, password):
        sat = Sentinel2(username, password)
        download = sat.download(product)
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

