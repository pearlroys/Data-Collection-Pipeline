import unittest
import sys
import time
import json

# append the parent folder
sys.path.append('../')
from src.medexpress import Scraper
print(sys.path)

from unittest.mock import ANY, patch, MagicMock, call



class ScraperTestCase(unittest.TestCase):

    @classmethod
    def setUp(self) -> None:
        self.scraper = Scraper()
        
    @patch('src.medexpress')
    def test_get_drug_class(self, mock_input):
        mock_input.return_value = 'covid'
        result = self.scraper.get_drug_class()
        self.assertEqual(result, 'covid')

    def test_get_class_links(self):
        actual_links = self.scraper.get_class_links()
        self.assertEqual(type(actual_links), str)
        self.assertIn('clinics', actual_links, 'got class links')

    def test_get_metadata(self):
        actual_get_metadata = self.scraper.get_metadata()
        self.assertEqual(dict, type(actual_get_metadata))
        self.assertIn('DRUG NAME', actual_get_metadata)
        self.assertIn('ALTERNATIVES', actual_get_metadata)
        self.assertIn('QUANTITY AVAILABLE', actual_get_metadata)
        self.assertIn('UUID', actual_get_metadata)
        self.assertIn('PRICE', actual_get_metadata)
        self.assertIn('REVIEWS', actual_get_metadata)
        self.assertIn("DRUG URL", actual_get_metadata)
        self.assertIn("INFORMATION", actual_get_metadata)

       
        # test the first drug information
        drug_number = 4
        self.assertEqual(drug_number, len(actual_get_metadata['ALTERNATIVES']))
        self.assertEqual('COVID-19 Home Test Kit', actual_get_metadata['DRUG NAME'])
        self.assertIn("DRUG URL", actual_get_metadata)
        
        self.assertEqual(list, type(actual_get_metadata['ALTERNATIVES']))
        self.assertEqual(str, type(actual_get_metadata["DRUG URL"]))
        self.assertEqual(str, type(actual_get_metadata['UUID']))
        # # break

    
            

    @classmethod
    def tearDown(self) -> None:
        self.scraper.driver.close()
 
            
if __name__ == "__main__":

   unittest.main(argv = [''],verbosity = 2, exit=False)
    