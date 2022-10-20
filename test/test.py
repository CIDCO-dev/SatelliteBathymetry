"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""
import sys, os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(os.path.join(PROJECT_ROOT, "src/python/"))
from sentinel2_file_downloader import Sentinel2Downloader
from hashlib import md5
import requests
import pytest


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


# Unit tests concerning the Sentinel2Downloader class
class TestGeneral:
	
    def test_status_code(self, username, password):
    	date = 'NOW-1DAYS'
    	req = requests.get(f'https://scihub.copernicus.eu/dhus/search?'
    	f'q=(beginPosition:[{date}%20TO%20NOW])',
    	auth=(username, password))
    	assert req.status_code == 200


# Unit tests concerning the search() method
class TestSearchMethod:

    @pytest.mark.parametrize("begin_date, end_date", [('NOW-0DAYS', 'NOW')])
    def test_null_request_handled(self, begin_date, end_date, username, password):
        sat = Sentinel2Downloader(username, password)
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)

    @pytest.mark.parametrize("begin_date, end_date", [('2022-05-09T00:00:00.000Z', '2022-05-10T00:00:00.000Z')])
    def test_unit_request_handled(self, begin_date, end_date, username, password):
        sat = Sentinel2Downloader(username, password)
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)
        
    def test_is_list_of_strings(self, username, password):
        sat = Sentinel2Downloader(username, password)
        for el in sat.search(example_date, 'NOW', example_footprint):
            assert isinstance(el, str)
        
    def test_are_lengths_coherent(self, username, password):
        sat = Sentinel2Downloader(username, password)
        search_1 = sat.search(example_date_1, 'NOW', example_footprint)
        search_2 = sat.search(example_date_2, 'NOW', example_footprint)
        assert len(search_2) >= len(search_1)

    @pytest.mark.parametrize("begin_date, end_date", [('2022-05-15T00:00:00.000Z', '2022-05-17T00:00:00.000Z')])
    def test_answer_uncluded(self, begin_date, end_date, username, password):
        sat = Sentinel2Downloader(username, password)
        self.begin_date = begin_date
        self.end_date = end_date
        sat.search(self.begin_date, self.end_date, example_footprint)
        assert product in sat.search(self.begin_date, self.end_date, example_footprint)


# Unit tests concerning the download() method
class TestDownloadMethod:

    def test_can_create_zip(self, username, password):
        sat = Sentinel2Downloader(username, password)
        download = sat.download(product, os.path.expanduser("~"))
        assert (download)
        
    def test_file_exists(self, username, password):
        path = os.path.join(os.path.expanduser("~"), "{}.zip".format(product))
        assert os.path.exists(path)
    
    """
    not quite sure how useful it is to download twice the same product to verify its the same
    isnt it already tcp and https job ?
    def test_identical_binaries(self, username, password):
        sat = Sentinel2Downloader(username, password)
        download = sat.download(product)
        r = requests.get(f"https://scihub.copernicus.eu/dhus"
                         f"/odata/v1/Products('{product}')"
                         f"/$value",
                         auth=(username, password))   
        md5_test = md5()
        md5_test.update(r.content)
        
        md5_product = md5()
        with open(f'~/{product}.zip', 'rb') as f:
            data = f.read()
            md5_product.update(data)
        
        assert md5_product.hexdigest() == md5_test.hexdigest()
	"""
