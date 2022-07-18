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



class Scraper:
#to access website
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://www.medexpress.co.uk"
        self.driver.get(url)
        time.sleep(2)
        self.delay = 10
        # txt =  self.driver.find_element('xpath', '//li[@id="treatment-dropdown"]').click()
        # self.drug_panel = self.driver.find_element('xpath', '//div[@class="col-md-6 col-sm-12 column-menu"]')


    def get_drug_class(self): 
    
        """
        This method gets the drug class to be scraped.

        """
        self.class_choice = input("Enter drug class: ")
        return self.class_choice

    def get_class_links(self):


        """ This methods returns the link of the desired class.

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
            # if class is given
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

        drug_class = self.get_class_links()
        # access class link
        self.driver.get(drug_class)
        time.sleep(2)
        # access drug list and links on class page 
        drug_links_container = self.driver.find_element(By.XPATH, '//div[@class="panel-treatment-row"]')
        link_tag = drug_links_container.find_elements(By.TAG_NAME, 'a')
        drugs_links = [item.get_attribute('href') for item in link_tag]
        drugs_list = [name.split('/')[-1] for name in drugs_links]
        dict_self = {i : point.split('/')[-1] for i, point in enumerate(drugs_links)}
        print(dict_self)
        return (drugs_links)

    def get_metadata(self):
        drug_dictionary = []
      
        drug_links = self.get_drug_links()
        for i in drug_links:
            self.driver.get(i)
            time.sleep(2)
            drug_name = self.driver.find_element(By.XPATH, '//div[@class="col-sm-7 product-row-title"]/h1').text
            print(drug_name)
            time.sleep(2)
            try:

                doses = self.driver.find_element(By.XPATH, '//ul[@class="nav nav-tabs strengthMenuTab"]')
                doze = doses.find_elements(By.XPATH, '//span[@class="tab-dosage"]')
                dosages = [items.text for items in doze]
                print(dosages[0:3])
            except:
                print('only one dose available')


            time.sleep(2)
            quant = self.driver.find_element(By.XPATH, '//span[@class="select-container select-container-product"]')
            quanti = quant.find_elements(By.XPATH, '//select[@class="quantityMenu"]/option')
            quantity = [q.text for q in quanti]
            quanitities = [x for x in quantity if x != '']
            print(quanitities)
            product_id_num = str(uuid.uuid4())
            product_id_num = product_id_num[:8]
            print(product_id_num)
            time.sleep(2)
            pri = self.driver.find_element(By.XPATH, '//div[@class="sitewide-sale-price-wrapper"]')
            price = pri.find_element(By.TAG_NAME, 'span')
            print(price.text)
            try:
                reviews = self.driver.find_element(By.XPATH, '//div[@class="feefo-rating-big"]/span').text
            except:
                print('No reviews available')
            print(reviews)
            time.sleep(2)
            # self.driver.implicitly_wait(10)
            drug_inf= self.driver.find_element(By.XPATH, '//amp-accordion[@class="i-amphtml-element i-amphtml-layout-container i-amphtml-built i-amphtml-layout"]')
            # print(drug_inf)
            
            drug_info = drug_inf.find_element(By.XPATH, '//div[@class="tab-pane i-amphtml-accordion-content"]')
            try:

                drun = drug_info.find_elements(By.TAG_NAME, 'p')
            except:
                drun = drug_info.find_elements(By.TAG_NAME, 'h2')
                drug_infoo = [drug.text for drug in drun]
                print(drug_infoo, '\n')

            drug_infoo = [drug.text for drug in drun]
            print(drug_infoo, '\n')
if __name__ == "__main__":
    bot = Scraper()
    # bot.acid()
    # bot.acne()
    bot.get_metadata()