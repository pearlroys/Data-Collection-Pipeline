from curses.ascii import alt
from token import AWAIT
import datetime as datetime
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException
from tqdm import tqdm
import time
import uuid
import os
import json
import urllib.request
import sys
sys.path.append('../')
from src.aws import AwsScraper








class Scraper:
    """ This class contains all the navigation & data collection methods
    of a webscraper.
    
    Parameters
    ----------
    url : str 
        the url of the desired website  
    """
#to access website
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://www.medexpress.co.uk"
        self.driver.get(url)
        time.sleep(2)
        self.delay = 10
        self.aws = AwsScraper()
        self.drug_dictionary = {}
       
        
        # set storage location
        self.data_store = "./raw_data"

    
    def get_drug_class(self): 
    
        """
        This method gets the drug class to be scraped.

        """
        
        self.class_choice = input("Enter drug class: ")
        return self.class_choice

    def get_class_links(self, class_choice):


        """ This methods returns the link of the desired class and 
        puts them in a dictionary corresponding to their classes

        Returns
        --------
        str
            a string with the url of the class of drugs
        """
        
        # get drug class container
        class_container = self.driver.find_element(By.XPATH, '//div[@class="row margintop20"]')
        class_a_tag = class_container.find_elements(By.TAG_NAME, 'a')
        most_pop_class_tags = class_a_tag[0:8]
        drug_classes = [item.get_attribute('href') for item in most_pop_class_tags]
        # print(drug_classes)
        
        class_dictionary = {0 :'erectile dysfunction', 1 : 'covid', 2 : 'migraine', 3 : 'period delay', 4 : 'asthma', 5 : 'herpes', 6 : 'acne', 7 : 'hair loss'}

        for key, value in class_dictionary.items():
            # if class is give
            if value == class_choice.lower():
                self.drug_class = drug_classes[key]
                return self.drug_class
    
    def get_drug_links(self):
        """
        This method gets the links of all drugs in each class and the names of the drugs in the list.

        Returns
        --------
        lists
            list containing the name of drugs in the class
            list containing hyperlinks to all drugs in the class
        """
        
        
        # access class link
        self.driver.get(self.drug_class)
        time.sleep(2)
        # access drug list and links on class page 
        drug_links_container = self.driver.find_element(By.XPATH, '//div[@class="panel-treatment-row"]')
        link_tag = drug_links_container.find_elements(By.TAG_NAME, 'a')
        self.drugs_links = [item.get_attribute('href') for item in link_tag]
        return self.drugs_links

    def get_drugs_list(self):
        """
        This method gets the names of the drugs in the list.

        Returns
        --------
        lists
            list containing the name of drugs in the class
        """
        self.drugs_list = [name.split('/')[-1] for name in self.drugs_links]
        dict_self = {i : point.split('/')[-1] for i, point in enumerate(self.drugs_links)}
        return self.drugs_list
        

    def get_drug_name(self, webpage_driver):
        """
        This gets the name of the drug and updates the drug dictionary

        Args:
            webpage_driver: The webdriver for the current page,

        Returns:
            None
        """
        
        

        drug_name = webpage_driver.find_element(By.XPATH, '//div[@class="col-sm-7 product-row-title"]/h1').text
        self.drug_dictionary["DRUG NAME"] = drug_name


    def get_drug_dosage(self, webpage_driver) -> None:
        """ gets drug dosage 

        Args:
            webpage_driver (chrome_Webdriver): chrome_webdriver for that specific page
        """
        
        

        try:
            doses = webpage_driver.find_element(By.XPATH, '//ul[@class="nav nav-tabs strengthMenuTab"]')
            doze = doses.find_elements(By.XPATH, '//span[@class="tab-dosage"]')
            dosages = [items.text for items in doze]
            dose = dosages[0:3]
        except:
            dose = 'only one dose available'
        self.drug_dictionary["DOSAGES AVAILABLE"] = dose


    def get_drug_quantity(self, webpage_driver):
        """ gets the quantity of drugs needed

        Args:
            webpage_driver (chrome_Webdriver): chrome_webdriver for that specific page
        """
        

        quant = webpage_driver.find_element(By.XPATH, '//span[@class="select-container select-container-product"]')
        quanti = quant.find_elements(By.XPATH, '//select[@class="quantityMenu"]/option')
        quantity = [q.text for q in quanti]
        quanitities = [x for x in quantity if x != '']
        self.drug_dictionary["QUANTITY AVAILABLE"] = quanitities


    def get_unique_code(self):
        """ 
        generates a unique ID for each drug

        """
        product_id_num = str(uuid.uuid4())
        product_id_num = product_id_num[:8]
        self.drug_dictionary["UUID"] = product_id_num

    def get_price(self, webpage_driver):
        # self.driver.get(drug_link)
        # time.sleep(2)
        pri = webpage_driver.find_element(By.XPATH, '//div[@class="sitewide-sale-price-wrapper"]')
        price = pri.find_element(By.TAG_NAME, 'span')
        self.drug_dictionary["PRICE"] = price.text

    def get_drug_review(self, webpage_driver):
        # self.driver.get(drug_link)
        # time.sleep(2)
        try:
            reviews = webpage_driver.find_element(By.XPATH, '//div[@class="feefo-rating-big"]/span').text
        except:
            reviews = 'No reviews available'
            
        self.drug_dictionary["REVIEWS"] = reviews

    def get_drug_info(self, webpage_driver):
        # self.driver.get(drug_link)
        # time.sleep(2)
        drug_inf= webpage_driver.find_element(By.XPATH, '//amp-accordion[@class="i-amphtml-element i-amphtml-layout-container i-amphtml-built i-amphtml-layout"]')
            
        drug_info = drug_inf.find_element(By.XPATH, '//div[@class="tab-pane i-amphtml-accordion-content"]')
        try:
            drun = drug_info.find_elements(By.TAG_NAME, 'p')
            drug_infoo = [drug.text for drug in drun]
        except:
            webpage_driver.implicitly_wait(10)
            drun = drug_info.find_elements(By.TAG_NAME, 'h2')
            drug_infoo = [drug.text for drug in drun]
        
        self.drug_dictionary["INFORMATION"] = drug_infoo

    def get_metadata(self, drugs_link, drug_list):
        """ This method creates different folders for data storage and gets data from each drug page
        Args:
            drug_links: the links of 
            drug_list: the list of drugs in the class

        Returns:
            a dictionary with all the data from each drug in the class
        -----------
        directory_name : str
            a string representing the name of a new folder to be created and cd into
        """

        self._create_metadata_folders(f'raw_data/{self.class_choice}')

        self.metadata_list = []
        for i in tqdm(drugs_link):
            self.driver.get(i)
            webpage_driver = self.driver
            time.sleep(2)
            self.drug_dictionary["ALTERNATIVES"] = drug_list

            # get the drug name and update the drug dictionary
            self.get_drug_name(webpage_driver=webpage_driver)
            #get drug dosage
            self.get_drug_dosage(webpage_driver)
            # get drug quantity
            self.get_drug_quantity(webpage_driver)
            # get unique code
            self.get_unique_code()
            # get drug price
            self.get_price(webpage_driver)
            # get drug review
            self.get_drug_review(webpage_driver)
            # get drug info
            self.get_drug_info(webpage_driver)
            # get drug dictionary
            self.drug_dictionary["DRUG URL"] = i
            # make a copy of the dictionary
            dictionary_copy = self.drug_dictionary.copy()

            self.metadata_list.append(dictionary_copy)
        print(self.metadata_list) 
        return self.metadata_list

    

   
    def save_data(self):
   
        # create the data.json from the above dictionary
        with open(f"raw_data/{self.class_choice}/data.json", "w") as f:

            # try:
                
            json_output = json.dump(self.drug_dictionary, f)
            #upload to S3
            s3_url = self.aws.upload_file_method(self.class_choice)
            return(s3_url)
            
           
    

    @staticmethod  
    def _create_metadata_folders(folder_name: str):
        """This method creates different folders for data storage
        
        Parameters
        ----------
        directory_name : str
            a string representing the name of a new folder to be created and cd into
        """
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
       
    def get_image(self, drugs_link):
        """
        This Method created a folder called 'images' in the raw data folder
        scrapes images for each drug and stores them in the folder.

        Returns
        --------
        images stored as jpg files

        """
        
        for i in drugs_link:
            self.driver.get(i)
            time.sleep(2)
            # get image 
            self._create_metadata_folders(f'raw_data/images')
            image = self.driver.find_element(By.XPATH, '//div[@class="i-amphtml-carousel-scroll"]')
            image_img = image.find_elements(By.TAG_NAME, 'img')
            
            for i in image_img:
                try:
                    images_src = i.get_attribute('src') 
                    self.alt = i.get_attribute('alt')
                    urllib.request.urlretrieve(images_src, f"raw_data/images/{self.alt}.jpg")

                    s3_url = self.aws.upload_file_method(f"raw_data/images/{self.alt}.jpg", self.alt)
                    return(s3_url)
                except Exception as e:
                    print(e)
                    return None

                finally:
                    
                    if os.path.exists(f"raw_data/images/{self.alt}"):
                    
                        os.remove(f"raw_data/images/{self.alt}")


    def _quit_scraper(self):
        ''' 
        The quit_scraper function will close the scraper once the data is collected and saved.
        '''
        self.driver.quit()

    

        
        
    

if __name__ == "__main__":
    bot = Scraper()
    
    
    
   
    class_choice = bot.get_drug_class()
    bot.get_class_links(class_choice)
    drugs_link = bot.get_drug_links()
    drugs_list = bot.get_drugs_list()
    bot.get_metadata(drugs_link, drugs_list)
    bot.save_data()
    bot.get_image(drugs_link)
    bot._quit_scraper()


    
    