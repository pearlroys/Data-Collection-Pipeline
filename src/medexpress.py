from curses.ascii import alt
from token import AWAIT
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

       
        # set storage location
        self.data_store = "./raw_data"

    
    def get_drug_class(self): 
    
        """
        This method gets the drug class to be scraped.

        """
        self.class_choice = input("Enter drug class: ")
        return self.class_choice

    def get_class_links(self):


        """ This methods returns the link of the desired class and 
        puts them in a dictionary corresponding to their classes

        Returns
        --------
        str
            a string with the url of the class of drugs
        """
        #get user choice
        self.get_drug_class()
        # get drug class container
        class_container = self.driver.find_element(By.XPATH, '//div[@class="row margintop20"]')
        class_a_tag = class_container.find_elements(By.TAG_NAME, 'a')
        most_pop_class_tags = class_a_tag[0:8]
        drug_classes = [item.get_attribute('href') for item in most_pop_class_tags]
        # print(drug_classes)
        
        class_dictionary = {0 :'erectile dysfunction', 1 : 'covid', 2 : 'migraine', 3 : 'period delay', 4 : 'asthma', 5 : 'herpes', 6 : 'acne', 7 : 'hair loss'}

        for key, value in class_dictionary.items():
            # if class is give
            if value == self.class_choice.lower():
                drug_class = drug_classes[key]
                return drug_class
    
    def get_drug_links(self):
        """
        This method gets the links of all drugs in each class and the names of the drugs in the list.

        Returns
        --------
        lists
            list containing the name of drugs in the class
            list containing hyperlinks to all drugs in the class
        """
        global drugs_list
        drug_class = self.get_class_links()
        # access class link
        self.driver.get(drug_class)
        time.sleep(2)
        # access drug list and links on class page 
        drug_links_container = self.driver.find_element(By.XPATH, '//div[@class="panel-treatment-row"]')
        link_tag = drug_links_container.find_elements(By.TAG_NAME, 'a')
        drugs_links = [item.get_attribute('href') for item in link_tag]
        print(drugs_links)
        drugs_list = [name.split('/')[-1] for name in drugs_links]
        dict_self = {i : point.split('/')[-1] for i, point in enumerate(drugs_links)}
        # print(dict_self)
        return (drugs_links)

    def get_metadata(self):
        """
        This method collects metadata from each drug page
        Returns
        --------
        Dictionary with meta data on each drug
        """
        global drug_name
        drug_dictionary = {}
        self.metadata_list = []
        # Goes to each drug link and scrapes relevant data from it
        drug_links = self.get_drug_links()
        for i in tqdm(drug_links):
            self.driver.get(i)
            time.sleep(2)
            drug_name = self.driver.find_element(By.XPATH, '//div[@class="col-sm-7 product-row-title"]/h1').text
            #create drug folder inside raw_data folder and begin appending key/value pairs to dictionary
            self._create_metadata_folders(f'raw_data/{self.class_choice}')
            drug_dictionary["DRUG NAME"] = drug_name
            drug_dictionary["ALTERNATIVES"] = drugs_list
            time.sleep(2)
            # try and except statemnets used to bypass heterogeneity in websites htmls
            try:
                doses = self.driver.find_element(By.XPATH, '//ul[@class="nav nav-tabs strengthMenuTab"]')
                doze = doses.find_elements(By.XPATH, '//span[@class="tab-dosage"]')
                dosages = [items.text for items in doze]
                dose = dosages[0:3]
            except:
                dose = 'only one dose available'
            drug_dictionary["DOSAGES AVAILABLE"] = dose
            time.sleep(2)
            #Scrape quantity for each drug
            quant = self.driver.find_element(By.XPATH, '//span[@class="select-container select-container-product"]')
            quanti = quant.find_elements(By.XPATH, '//select[@class="quantityMenu"]/option')
            quantity = [q.text for q in quanti]
            quanitities = [x for x in quantity if x != '']
            drug_dictionary["QUANTITY AVAILABLE"] = quanitities
            #apppend uuid and unique id of code which in this case is the website link as the drug page had no visible unique id
            product_id_num = str(uuid.uuid4())
            product_id_num = product_id_num[:8]
            drug_dictionary["UUID"] = product_id_num
            time.sleep(2)
            # get the price
            pri = self.driver.find_element(By.XPATH, '//div[@class="sitewide-sale-price-wrapper"]')
            price = pri.find_element(By.TAG_NAME, 'span')
            drug_dictionary["PRICE"] = price.text
            #get the reviews with a try and except block for drugs without reviews
            try:
                reviews = self.driver.find_element(By.XPATH, '//div[@class="feefo-rating-big"]/span').text
            except:
                reviews = 'No reviews available'
            
            drug_dictionary["REVIEWS"] = reviews
            time.sleep(2)
            # get the drug information
            drug_inf= self.driver.find_element(By.XPATH, '//amp-accordion[@class="i-amphtml-element i-amphtml-layout-container i-amphtml-built i-amphtml-layout"]')
            
            drug_info = drug_inf.find_element(By.XPATH, '//div[@class="tab-pane i-amphtml-accordion-content"]')
            try:
                drun = drug_info.find_elements(By.TAG_NAME, 'p')
            except:
                self.driver.implicitly_wait(10)
                drun = drug_info.find_elements(By.TAG_NAME, 'h2')
                drug_infoo = [drug.text for drug in drun]
            drug_infoo = [drug.text for drug in drun]
            drug_dictionary["INFORMATION"] = drug_infoo
            drug_dictionary["DRUG URL"] = i
            dictionary_copy = drug_dictionary.copy()
            self.metadata_list.append(dictionary_copy) 
        return (self.metadata_list)

    def save_data(self):

        drug_dictionary = self.get_metadata()
        print(drug_dictionary)
   
        # create the data.json from the above dictionary
        with open(f"raw_data/{self.class_choice}/data.json", "w") as f:

            # try:
                
            json_output = json.dump(drug_dictionary, f)
            #upload to S3
            s3_url = self.aws.upload_file_method(self.class_choice)
            return(s3_url)
            # except Exception as e:

            #     print(e)
            #     return None

            # finally:
                    
            #     if os.path.exists(f"raw_data/{self.class_choice}/data.json"):
                    
            #         os.remove(f"raw_data/{self.class_choice}/data.json")

           
    

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
       
    def get_image(self):
        """
        This Method created a folder called 'images' in the raw data folder
        scrapes images for each drug and stores them in the folder.

        Returns
        --------
        images stored as jpg files

        """
        drug_links = self.get_drug_links()
        for i in drug_links:
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


    # def data_dump(self,):
    #     """
    #     Parameters:
    #     ----------
    #     folder_name: str
    #         String value of the folder path for each player's data store
    #     Returns:
    #     -------
    #     None
    #     """
    #     try:
    #         pic_file = (f"raw_data/images/{self.alt}.jpg")
    #     except Exception:

    #         pic_file = ""

    #     self.upload_file_method((f"raw_data/{drug_name}/data.json"), drug_name, pic_file)
    #     # return AwsScraper.upload_file_method()
               

if __name__ == "__main__":
    bot = Scraper()
    # bot.get_metadata()
    # bot.get_image()
    bot.save_data()
    # bot.get_drug_links