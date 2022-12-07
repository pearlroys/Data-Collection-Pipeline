# Data-Collection-Pipeline


As part of my training at AiCore I worked on a webscraping project <img width="1177" alt="Screenshot 2022-12-07 at 11 44 44" src="https://user-images.githubusercontent.com/103274172/206193205-ea30b283-43d2-49f4-ad31-648b7c506947.png">

## 🏅 Goals of the project 🏅

The requirements for this data collection pipeline are to:

- develop a module that scrapes data from various sources using Selenium and Requests;

- perform unit testing and integration testing on the application to ensure that the package published to Pypi works as expected;

- use Docker to containerise the application and deploy it to an EC2 instance;

- set up a CI/CD pipeline using GitHub Actions to push a new Docker image.

## Language and tools

<p align="left"> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.selenium.dev" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/detain/svg-logos/780f25886640cef088af994181646db2f6b1a3f8/svg/selenium-logo.svg" alt="selenium" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> </p>

## Milestones 1-2: Environment setup and choice of website to scrape
To perfect my webscraping skills with beautiful soup and selenium, I scraped two extra websites [https://www.imdb.com/] and [https://www.zoopla.co.uk/] before beginning the main project and can be seen on the firstpage of this repo.

The project was completed using [VS Code](https://code.visualstudio.com/) as a code editor, plus Git and GitHub for version control. The environment setup was done by creating a new environment, `web-scraping`, in conda. After every required package had been installed, a `requirements.txt` file was generated.

The choice of website to scrape was based on two main criteria: personal interest, and my background in healthcare as a Doctor and a care assitant. My choice fell rather naturally on a [Pharmaceutical company](https://www.medexpress.co.uk/). Scraping the website was challenging but offered plenty of opportunities to learn HTML tricks.

Given that the website included many classes of drugs to choose from, I decided to reduce the scope of my project to only include drugs that were commonly bought as shown on the image below.

<img width="1243" alt="Screenshot 2022-12-07 at 11 45 32" src="https://user-images.githubusercontent.com/103274172/206193470-bc531e0f-5feb-4b68-8d14-c28d12ecf86e.png">

## Milestone 3: Find links to the pages from which we wish to scrape data

The project is written in Python and utilises OOP concepts throughout.
1. Scraper class includes important initialisation & navigation methods, such as:
   + navigating to main webpage
   + a method that returns the link to the desired drug class which is accessed based on the input of the user
   + a method that returns links to all drugs class on the popular list and stores them in a dictionary
   + a method that returns the list and links of all drugs in the desired drug class
  

`if __name__ == '__main__':` assigns the scraper to the `bot` variable. The scraper then performs all actions from the methods in `scraper.py`, until all drugs in the web pages in consideration have been found.

The program utilises numerous `time.sleep(2)` methods to make sure the website does not recognise it as a bot and blocks our IP address.
## Milestone 4: Retreive data from details page

In this milestone, I created a method called `get_metadata(self, drugs_link, drug_list)` which loops through the `drug_links` list and creates dictionaries that map pre-determined keys (labels) to values extracted from a link. The dictionaries are then systematically appended to the end of the `self.drug_dictionary` list. The dictionaries structure was as follows:

```python
self.drug_dictionary = {"DRUG NAME": , "DOSAGES AVAILABLE": , "QUANTITY AVAILABLE": , "UUID": , "PRICE": , "REVIEWS": , "INFORMATION": }

```

Both the scraped images and the .json file are stored in a dedicated local directory called `raw_data`.

The most important takeaways of this milestone where the correct implementation of while loops and choice of relative xpaths to extract content from the page. I also learnt how to download images locally and to create a .json file from a list of dictionaries using the `json.dump()` method to store data locally.

## Milestone 5

The first part of milestone 5 was refactoring, i.e., a first scrutinisation of the scraper code. Accordingly:

- all unnecessary comments were removed;
- docstrings were added to all functions;
- method and variable names were changed when necessary to make them transparent;
- all code repetitions were discarded;
- longer methods were broken into smaller ones that only perform one task. Notably, the `get_metadata(self, drugs_link, drug_list)` method now only creates different folders for data storage and gets data from each drug page, without doing any scraping. The scraping part is now left to dedicated methods, nemely:

```python3
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
```
- imports and from statements are in consistent alphabetical order;
- there are no nested loops within the code.

In the second part of this milestone, I created unit tests for my scraper using `unittest`, i.e., one test for each of the public methods of my `Scraper()` class. These are in the file `test_scraper.py` and `test_images.py` within the `tests` file. They are run from `__main__.py`.


## Milestone 6

With the basic scraper code in `scraper.py` refactored and passing all tests, milestone 5 required to implement the lines of code needed to run the scraper in headless mode. This was done using `Options()` as follows:

```python3
 options = webdriver.ChromeOptions()
        options.add_argument("start-maximized") # open Browser in maximized mode
        options.add_argument("disable-infobars")# disabling infobars
        options.add_argument("--disable-extensions"); # disabling extensions
        options.add_argument("--no-sandbox") 
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-setuid-sandbox") 
        options.add_argument('--disable-gpu')      
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)  
```

The following task of this milestone was ithe creation of a `Dockerfile` to build a scraper image locally. This required instructions to:

- choose a base image (in my case, `python:latest`);
- put everything required by my scraper within the container;
- install all dependencies;
- run the main Python file.


```FROM python:latest

#download & install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
    apt-get -y update &&\
    apt-get install -y google-chrome-stable &&\
    #install chromedriver
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    apt-get install -yqq unzip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#set display port to avoid crash
ENV DISPLAY=:99
#copy local files
COPY . .
#install dependencies
RUN pip install -r ./requirements.txt
#
ENTRYPOINT ["python", "src/medexpress.py"]
```

Once built, the image was run to make sure it worked properly, and then pushed to the [DockerHub](https://hub.docker.com/).



## Milestone 7

This milestone required the creation of two github secrets, `DOCKER_HUB_USERNAME` and `DOCKER_HUB_ACCESS_TOKEN`. These contain, respectively, my personal id from DockerHub and a [Personal Access Token](https://docs.docker.com/docker-hub/access-tokens/#create-an-access-token) created on DockerHub.

Subsequently, I could set up a CI/CD (continuous integration and continuous deployment) pipeline using GitHub actions. My GitHub action is triggered on a push to the main branch of my repository, builds the Docker image and pushes it to your Dockerhub account. My workflow is now automatically updated on the Actions of my repo everytime new changes are pushed.

