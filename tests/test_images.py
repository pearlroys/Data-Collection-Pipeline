from turtle import pd
import unittest
import sys
import time
import json

# append the parent folder
sys.path.append('../')
from src.medexpress import Scraper
print(sys.path)

from unittest.mock import ANY, patch, MagicMock, call

class ScraperTestCaseUnit(unittest.TestCase):

    @classmethod
    def setUp(self) -> None:
        self.scraper = Scraper()

    @patch('urllib.request.urlretrieve')
    def test_get_image(self,  mock_urlretrieve):
        mock_urlretrieve.return_value = MagicMock()
        self.scraper.get_image()
        mock_urlretrieve.assert_called_with('https://www.medexpress.co.uk/images/672x480/product-images/lateral-flow-test-5.webp', 'raw_data/images/flowflex qr cassette lateral flow diagnostic testing medication.jpg')
    
   
       